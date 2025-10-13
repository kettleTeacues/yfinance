"""
EPS trend data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import EpsTrend
from database.client import db_client


def insert_stock_eps_trend(yf_client: yf.Ticker) -> int:
    """
    指定された銘柄のEPS予想トレンドデータを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # EPS予想トレンドデータを取得
        eps_trend_data = yf_client.eps_trend
        
        if eps_trend_data is None or eps_trend_data.empty:
            print(f"No EPS trend data found for {symbol}")
            return 0
        
        # DataFrameを辞書に変換
        trend_dict = eps_trend_data.to_dict('index')
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_eps_trend_data(session, symbol, trend_dict)
            session.commit()
            print(f"Successfully processed {processed_count} EPS trend records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting EPS trend data for {symbol}: {e}")
        return 0


def _bulk_process_eps_trend_data(session, symbol: str, data: dict) -> int:
    """
    EPS予想トレンドデータを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with EPS trend data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_trends = session.query(EpsTrend).filter(
        EpsTrend.symbol == symbol
    ).all()
    existing_records = {record.period_type: record for record in existing_trends}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    # 現在の年度を取得
    current_year = datetime.now().year
    
    for period_type, trend_data in data.items():
        if period_type in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[period_type]
            _update_eps_trend_fields(existing_record, trend_data, current_year, period_type)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            trend_record = _create_eps_trend_record(
                symbol, period_type, trend_data, current_year
            )
            new_records.append(trend_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated EPS trend records for {symbol}")
    return len(new_records) + updated_count


def _create_eps_trend_record(symbol: str, period_type: str, data: dict, current_year: int) -> EpsTrend:
    """
    EPS予想トレンドレコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        period_type: 期間タイプ（0q, +1q, 0y, +1yなど）
        data: EPS予想トレンドデータ
        current_year: 現在年
        
    Returns:
        EpsTrend: 作成されたレコード
    """
    trend_record = EpsTrend(
        symbol=symbol,
        period_type=period_type,
        year=current_year,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_eps_trend_fields(trend_record, data, current_year, period_type)
    
    return trend_record


def _update_eps_trend_fields(record: EpsTrend, data: dict, current_year: int, period_type: str) -> None:
    """
    EPS予想トレンドレコードのフィールドを更新する
    
    Args:
        record: EpsTrendモデルのインスタンス
        data: EPS予想トレンドデータ
        current_year: 現在年
        period_type: 期間タイプ
    """
    # フィールドマッピング
    field_mappings = {
        'current': ['current'],
        'days_ago_7': ['7daysAgo'],
        'days_ago_30': ['30daysAgo'],
        'days_ago_60': ['60daysAgo'],
        'days_ago_90': ['90daysAgo']
    }
    
    # 年度の設定
    setattr(record, 'year', current_year)
    
    # 各フィールドの設定
    for db_field, json_keys in field_mappings.items():
        for json_key in json_keys:
            value = data.get(json_key, None)
            if value is not None and not pd.isna(value):
                try:
                    setattr(record, db_field, float(value))
                    break
                except (ValueError, TypeError):
                    continue
