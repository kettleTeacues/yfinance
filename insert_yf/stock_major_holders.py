"""
Major holders data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import MajorHolders
from database.client import db_client


def insert_stock_major_holders(symbol: str) -> int:
    """
    指定された銘柄の主要株主情報データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    ticker = yf.Ticker(symbol)
    
    try:
        # 主要株主情報データを取得
        major_holders_data = ticker.major_holders
        
        if major_holders_data is None or major_holders_data.empty:
            print(f"No major holders data found for {symbol}")
            return 0
        
        # DataFrameを辞書に変換
        holders_dict = major_holders_data.to_dict('index')
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_major_holders_data(session, symbol, holders_dict)
            session.commit()
            print(f"Successfully processed {processed_count} major holders records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting major holders data for {symbol}: {e}")
        return 0


def _bulk_process_major_holders_data(session, symbol: str, data: dict) -> int:
    """
    主要株主情報データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with major holders data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_major_holders = session.query(MajorHolders).filter(
        MajorHolders.symbol == symbol
    ).first()
    
    if existing_major_holders:
        # 既存レコードの更新
        _update_major_holders_fields(existing_major_holders, data)
        setattr(existing_major_holders, 'updated_at', datetime.now().isoformat()[:24])
        print(f"Updated existing major holders record for {symbol}")
        return 1
    else:
        # 新規レコードの作成
        major_holders_record = _create_major_holders_record(symbol, data)
        if major_holders_record:
            session.add(major_holders_record)
            print(f"Created new major holders record for {symbol}")
            return 1
    
    return 0


def _create_major_holders_record(symbol: str, data: dict):
    """
    主要株主情報レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        data: 主要株主情報データ
        
    Returns:
        MajorHolders or None: 作成されたレコード
    """
    major_holders_record = MajorHolders(
        symbol=symbol,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_major_holders_fields(major_holders_record, data)
    
    return major_holders_record


def _update_major_holders_fields(record: MajorHolders, data: dict) -> None:
    """
    主要株主情報レコードのフィールドを更新する
    
    Args:
        record: MajorHoldersモデルのインスタンス
        data: 主要株主情報データ
    """
    # フィールドマッピング
    field_mappings = {
        'insiders_percent_held': ['insidersPercentHeld'],
        'institutions_percent_held': ['institutionsPercentHeld'],
        'institutions_float_percent_held': ['institutionsFloatPercentHeld'],
        'institutions_count': ['institutionsCount']
    }
    
    # 各フィールドの設定
    for db_field, json_keys in field_mappings.items():
        for json_key in json_keys:
            if json_key in data:
                item_data = data[json_key]
                value = data.get(json_key, None)
                if value is not None and not pd.isna(value):
                    try:
                        setattr(record, db_field, float(value))
                        break
                    except (ValueError, TypeError):
                        continue
