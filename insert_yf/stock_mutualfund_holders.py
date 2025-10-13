"""
Mutual fund holders data insertion module for yfinance
"""
import yfinance as yf
from sqlalchemy import and_
from datetime import datetime
import pandas as pd

from models.models import MutualfundHolders
from database.client import db_client


def insert_stock_mutualfund_holders(yf_client: yf.Ticker) -> int:
    """
    指定された銘柄の投資信託保有情報データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # 投資信託保有情報データを取得
        mutualfund_holders_data = yf_client.mutualfund_holders
        
        if mutualfund_holders_data is None or mutualfund_holders_data.empty:
            print(f"No mutual fund holders data found for {symbol}")
            return 0
        
        # DataFrameを辞書に変換
        holders_dict = mutualfund_holders_data.to_dict('index')
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_mutualfund_holders_data(session, symbol, holders_dict)
            session.commit()
            print(f"Successfully processed {processed_count} mutual fund holders records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting mutual fund holders data for {symbol}: {e}")
        return 0


def _bulk_process_mutualfund_holders_data(session, symbol: str, data: dict) -> int:
    """
    投資信託保有情報データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with mutual fund holders data
        
    Returns:
        int: 処理された行数
    """
    processed_count = 0
    
    for index, holder_data in data.items():
        # 日付とホルダー名の取得
        date_str = holder_data['Date Reported'].isoformat()[:24]
        holder_name = holder_data.get('Holder', None)
        
        if not date_str or not holder_name:
            continue
        
        # 既存レコードの検索（日付とホルダー名の複合キー）
        existing_record = session.query(MutualfundHolders).filter(
            and_(
                MutualfundHolders.symbol == symbol,
                MutualfundHolders.date == date_str,
                MutualfundHolders.holder == holder_name
            )
        ).first()
        
        if existing_record:
            # 既存レコードの更新
            _update_mutualfund_holders_fields(existing_record, holder_data)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            processed_count += 1
        else:
            # 新規レコードの作成
            new_record = _create_mutualfund_holders_record(symbol, date_str, holder_data)
            if new_record:
                session.add(new_record)
                processed_count += 1
    
    return processed_count


def _create_mutualfund_holders_record(symbol: str, date_str: str, holder_data: dict):
    """
    投資信託保有情報レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        date_str: 報告日
        holder_data: 投資信託保有情報データ
        
    Returns:
        MutualfundHolders or None: 作成されたレコード
    """
    holder_name = holder_data.get('Holder', None)
    
    if not holder_name:
        return None
    
    record = MutualfundHolders(
        symbol=symbol,
        date=date_str,
        holder=holder_name,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_mutualfund_holders_fields(record, holder_data)
    
    return record


def _update_mutualfund_holders_fields(record: MutualfundHolders, holder_data: dict) -> None:
    """
    投資信託保有情報レコードのフィールドを更新する
    
    Args:
        record: MutualfundHoldersモデルのインスタンス
        holder_data: 投資信託保有情報データ
    """
    # フィールドマッピング
    field_mappings = {
        'pct_held': ['pctHeld'],
        'shares': ['Shares'],
        'value': ['Value'],
        'pct_change': ['pctChange']
    }
    
    # 各フィールドの設定
    for db_field, json_keys in field_mappings.items():
        for json_key in json_keys:
            value = holder_data.get(json_key, None)
            if value is not None and not pd.isna(value):
                try:
                    setattr(record, db_field, float(value))
                    break
                except (ValueError, TypeError):
                    continue
