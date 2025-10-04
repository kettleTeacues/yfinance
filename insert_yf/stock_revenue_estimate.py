"""
Stock revenue estimate data insertion module for yfinance
"""
import yfinance as yf
from sqlalchemy import and_
from datetime import datetime
import pandas as pd

from models.models import RevenueEstimate
from database.client import db_client


def insert_stock_revenue_estimate(symbol: str) -> int:
    """
    指定された銘柄の売上予想データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    ticker = yf.Ticker(symbol)
    
    try:
        # 売上予想データを取得
        revenue_estimate_data = ticker.revenue_estimate
        
        if revenue_estimate_data is None or revenue_estimate_data.empty:
            print(f"No revenue estimate data found for {symbol}")
            return 0
        
        # DataFrameを辞書に変換
        estimate_dict = revenue_estimate_data.to_dict('index')
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_revenue_estimate_data(session, symbol, estimate_dict)
            session.commit()
            print(f"Successfully processed {processed_count} revenue estimate records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting revenue estimate data for {symbol}: {e}")
        return 0


def _bulk_process_revenue_estimate_data(session, symbol: str, data: dict) -> int:
    """
    売上予想データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with revenue estimate data
        
    Returns:
        int: 処理された行数
    """
    processed_count = 0
    
    for period_type, estimate_data in data.items():
        # 既存レコードの検索（シンボルと期間タイプの複合キー）
        existing_record = session.query(RevenueEstimate).filter(
            and_(
                RevenueEstimate.symbol == symbol,
                RevenueEstimate.period_type == period_type
            )
        ).first()
        
        if existing_record:
            # 既存レコードの更新
            _update_revenue_estimate_fields(existing_record, estimate_data)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            processed_count += 1
        else:
            # 新規レコードの作成
            new_record = _create_revenue_estimate_record(symbol, period_type, estimate_data)
            if new_record:
                session.add(new_record)
                processed_count += 1
    
    return processed_count


def _create_revenue_estimate_record(symbol: str, period_type: str, estimate_data: dict):
    """
    売上予想レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        period_type: 期間タイプ
        estimate_data: 売上予想データ
        
    Returns:
        RevenueEstimate or None: 作成されたレコード
    """
    if not period_type:
        return None
    
    record = RevenueEstimate(
        symbol=symbol,
        period_type=period_type,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_revenue_estimate_fields(record, estimate_data)
    
    return record


def _update_revenue_estimate_fields(record: RevenueEstimate, estimate_data: dict) -> None:
    """
    売上予想レコードのフィールドを更新する
    
    Args:
        record: RevenueEstimateモデルのインスタンス
        estimate_data: 売上予想データ
    """
    # フィールドマッピング
    field_mappings = {
        'avg': ['avg'],
        'low': ['low'],
        'high': ['high'],
        'number_of_analysts': ['numberOfAnalysts'],
        'year_ago_revenue': ['yearAgoRevenue'],
        'growth': ['growth']
    }
    
    # 各フィールドの設定
    for db_field, json_keys in field_mappings.items():
        for json_key in json_keys:
            value = estimate_data.get(json_key, None)
            if value is not None and not pd.isna(value):
                try:
                    if db_field == 'number_of_analysts':
                        setattr(record, db_field, int(value))
                    else:
                        setattr(record, db_field, float(value))
                    break
                except (ValueError, TypeError):
                    continue
