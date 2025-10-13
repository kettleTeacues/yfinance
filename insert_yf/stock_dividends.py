"""
Dividends data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import Dividends
from database.client import db_client


def insert_stock_dividends(yf_client: yf.Ticker, period: str = "max") -> int:
    """
    指定された銘柄の配当履歴データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
        period: 取得期間 ("1y", "2y", "5y", "10y", "max")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # 配当履歴データを取得
        dividends_data = yf_client.dividends
        
        if dividends_data.empty:
            print(f"No dividends data found for {symbol}")
            return 0
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_dividends_data(session, symbol, dividends_data)
            session.commit()
            print(f"Successfully processed {processed_count} dividends records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting dividends data for {symbol}: {e}")
        return 0


def _bulk_process_dividends_data(session, symbol: str, data) -> int:
    """
    配当データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: pandas Series with dividends data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_dividends = session.query(Dividends).filter(
        Dividends.symbol == symbol
    ).all()
    existing_records = {str(record.date): record for record in existing_dividends}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    for date_index, dividend_amount in data.items():
        # 日付の変換
        if hasattr(date_index, 'strftime'):
            date_str = date_index.strftime('%Y-%m-%d')
        else:
            date_str = str(date_index)[:10]  # ISO形式の日付部分のみ取得
        
        # 配当額が0以下の場合はスキップ
        if pd.isna(dividend_amount) or dividend_amount <= 0:
            continue
        
        if date_str in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[date_str]
            setattr(existing_record, 'dividends', float(dividend_amount))
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            dividend_record = Dividends(
                symbol=symbol,
                date=date_str,
                dividends=float(dividend_amount),
                created_at=datetime.now().isoformat()[:24],
                updated_at=datetime.now().isoformat()[:24]
            )
            new_records.append(dividend_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated dividends records for {symbol}")
    return len(new_records) + updated_count
