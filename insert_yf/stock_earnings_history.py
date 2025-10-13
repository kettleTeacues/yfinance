"""
Earnings history data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import EarningsHistory
from database.client import db_client


def insert_stock_earnings_history(yf_client: yf.Ticker) -> int:
    """
    指定された銘柄の収益実績データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # 収益実績データを取得
        earnings_history_data = yf_client.earnings_history
        
        if earnings_history_data is None or earnings_history_data.empty:
            print(f"No earnings history data found for {symbol}")
            return 0
        
        # DataFrameを辞書に変換
        history_dict = earnings_history_data.to_dict('index')
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_earnings_history_data(session, symbol, history_dict)
            session.commit()
            print(f"Successfully processed {processed_count} earnings history records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting earnings history data for {symbol}: {e}")
        return 0


def _bulk_process_earnings_history_data(session, symbol: str, data: dict) -> int:
    """
    収益実績データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with earnings history data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_history = session.query(EarningsHistory).filter(
        EarningsHistory.symbol == symbol
    ).all()
    existing_records = {record.date: record for record in existing_history}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    for date_key, history_data in data.items():
        # 日付の変換
        if isinstance(date_key, str):
            # ISO形式の日付から YYYY-MM-DD 形式に変換
            try:
                date_obj = pd.to_datetime(date_key)
                date_str = date_obj.strftime('%Y-%m-%d')
            except:
                date_str = str(date_key)[:10]  # フォールバック
        else:
            date_str = str(date_key)[:10]
        
        if date_str in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[date_str]
            _update_earnings_history_fields(existing_record, history_data)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            history_record = _create_earnings_history_record(
                symbol, date_str, history_data
            )
            new_records.append(history_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated earnings history records for {symbol}")
    return len(new_records) + updated_count


def _create_earnings_history_record(symbol: str, date_str: str, data: dict) -> EarningsHistory:
    """
    収益実績レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        date_str: 日付文字列
        data: 収益実績データ
        
    Returns:
        EarningsHistory: 作成されたレコード
    """
    history_record = EarningsHistory(
        symbol=symbol,
        date=date_str,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_earnings_history_fields(history_record, data)
    
    return history_record


def _update_earnings_history_fields(record: EarningsHistory, data: dict) -> None:
    """
    収益実績レコードのフィールドを更新する
    
    Args:
        record: EarningsHistoryモデルのインスタンス
        data: 収益実績データ
    """
    # フィールドマッピング
    field_mappings = {
        'eps_actual': ['epsActual'],
        'eps_estimate': ['epsEstimate'],
        'eps_difference': ['epsDifference'],
        'surprise_percent': ['surprisePercent']
    }
    
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
