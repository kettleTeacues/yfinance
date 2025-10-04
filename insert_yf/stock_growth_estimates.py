"""
Growth estimates data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import GrowthEstimate
from database.client import db_client


def insert_stock_growth_estimates(symbol: str) -> int:
    """
    指定された銘柄の成長予想データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    ticker = yf.Ticker(symbol)
    
    try:
        # 成長予想データを取得
        growth_estimates_data = ticker.growth_estimates
        
        if growth_estimates_data is None or growth_estimates_data.empty:
            print(f"No growth estimates data found for {symbol}")
            return 0
        
        # DataFrameを辞書に変換
        estimates_dict = growth_estimates_data.to_dict('index')
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_growth_estimates_data(session, symbol, estimates_dict)
            session.commit()
            print(f"Successfully processed {processed_count} growth estimates records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting growth estimates data for {symbol}: {e}")
        return 0


def _bulk_process_growth_estimates_data(session, symbol: str, data: dict) -> int:
    """
    成長予想データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with growth estimates data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_estimates = session.query(GrowthEstimate).filter(
        GrowthEstimate.symbol == symbol
    ).all()
    existing_records = {record.period_type: record for record in existing_estimates}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    # 現在の年度を取得
    current_year = datetime.now().year
    
    for period_type, estimates_data in data.items():
        if period_type in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[period_type]
            _update_growth_estimates_fields(existing_record, estimates_data, current_year, period_type)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            estimates_record = _create_growth_estimates_record(
                symbol, period_type, estimates_data, current_year
            )
            new_records.append(estimates_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated growth estimates records for {symbol}")
    return len(new_records) + updated_count


def _create_growth_estimates_record(symbol: str, period_type: str, data: dict, current_year: int) -> GrowthEstimate:
    """
    成長予想レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        period_type: 期間タイプ（0q, +1q, 0y, +1y, LTGなど）
        data: 成長予想データ
        current_year: 現在年
        
    Returns:
        GrowthEstimate: 作成されたレコード
    """
    estimates_record = GrowthEstimate(
        symbol=symbol,
        period_type=period_type,
        year=current_year,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_growth_estimates_fields(estimates_record, data, current_year, period_type)
    
    return estimates_record


def _update_growth_estimates_fields(record: GrowthEstimate, data: dict, current_year: int, period_type: str) -> None:
    """
    成長予想レコードのフィールドを更新する
    
    Args:
        record: GrowthEstimateモデルのインスタンス
        data: 成長予想データ
        current_year: 現在年
        period_type: 期間タイプ
    """
    # フィールドマッピング
    field_mappings = {
        'stock_trend': ['stockTrend'],
        'index_trend': ['indexTrend']
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
