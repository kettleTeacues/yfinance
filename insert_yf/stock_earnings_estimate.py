"""
Earnings estimate data insertion module for yfinance
"""
import yfinance as yf
from sqlalchemy import exists
from datetime import datetime
import pandas as pd

from models.models import EarningsEstimate
from database.client import db_client
from .utils import safe_get, safe_timestamp_to_str


def insert_stock_earnings_estimate(symbol: str) -> int:
    """
    指定された銘柄の収益予想データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    ticker = yf.Ticker(symbol)
    
    try:
        # 収益予想データを取得
        earnings_estimate_data = ticker.earnings_estimate
        
        if earnings_estimate_data is None or earnings_estimate_data.empty:
            print(f"No earnings estimate data found for {symbol}")
            return 0
        
        # DataFrameを辞書に変換
        estimate_dict = earnings_estimate_data.to_dict('index')
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_earnings_estimate_data(session, symbol, estimate_dict)
            session.commit()
            print(f"Successfully processed {processed_count} earnings estimate records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting earnings estimate data for {symbol}: {e}")
        return 0


def _bulk_process_earnings_estimate_data(session, symbol: str, data: dict) -> int:
    """
    収益予想データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with earnings estimate data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_estimates = session.query(EarningsEstimate).filter(
        EarningsEstimate.symbol == symbol
    ).all()
    existing_records = {record.period_type: record for record in existing_estimates}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    # 現在の年度を取得
    current_year = datetime.now().year
    
    for period_type, estimate_data in data.items():
        if period_type in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[period_type]
            _update_earnings_estimate_fields(existing_record, estimate_data, current_year, period_type)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            estimate_record = _create_earnings_estimate_record(
                symbol, period_type, estimate_data, current_year
            )
            new_records.append(estimate_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated earnings estimate records for {symbol}")
    return len(new_records) + updated_count


def _create_earnings_estimate_record(symbol: str, period_type: str, data: dict, current_year: int) -> EarningsEstimate:
    """
    収益予想レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        period_type: 期間タイプ（0q, +1q, 0y, +1yなど）
        data: 収益予想データ
        current_year: 現在年
        
    Returns:
        EarningsEstimate: 作成されたレコード
    """
    estimate_record = EarningsEstimate(
        symbol=symbol,
        period_type=period_type,
        year=current_year,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_earnings_estimate_fields(estimate_record, data, current_year, period_type)
    
    return estimate_record


def _update_earnings_estimate_fields(record: EarningsEstimate, data: dict, current_year: int, period_type: str) -> None:
    """
    収益予想レコードのフィールドを更新する
    
    Args:
        record: EarningsEstimateモデルのインスタンス
        data: 収益予想データ
        current_year: 現在年
        period_type: 期間タイプ
    """
    # フィールドマッピング
    field_mappings = {
        'avg_estimate': ['avg'],
        'low_estimate': ['low'],
        'high_estimate': ['high'],
        'year_ago_eps': ['yearAgoEps'],
        'number_of_analysts': ['numberOfAnalysts'],
        'growth_rate': ['growth']
    }
    
    # 年度の設定
    setattr(record, 'year', current_year)
    
    # 各フィールドの設定
    for db_field, json_keys in field_mappings.items():
        for json_key in json_keys:
            value = data.get(json_key, None)
            if value is not None and not pd.isna(value):
                try:
                    if db_field == 'number_of_analysts':
                        setattr(record, db_field, int(value))
                    else:
                        setattr(record, db_field, float(value))
                    break
                except (ValueError, TypeError):
                    continue
