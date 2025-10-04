"""
Stock Actions data insertion module for yfinance
配当と株式分割の履歴データを処理する
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import Actions
from database.client import db_client


def insert_stock_actions(symbol: str, period: str = "max") -> int:
    """
    指定された銘柄のアクション履歴データ（配当と株式分割）を取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL", "7974.T")
        period: 取得期間 ("1y", "2y", "5y", "10y", "max")
    
    Returns:
        int: 処理された行数
    """
    ticker = yf.Ticker(symbol)
    
    try:
        # アクション履歴データを取得
        actions_data = ticker.actions
        
        if actions_data.empty:
            print(f"No actions data found for {symbol}")
            return 0
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_actions_data(session, symbol, actions_data)
            session.commit()
            print(f"Successfully processed {processed_count} actions records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting actions data for {symbol}: {e}")
        return 0


def _bulk_process_actions_data(session, symbol: str, data) -> int:
    """
    アクションデータを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: pandas DataFrame with actions data (columns: Dividends, Stock Splits)
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_actions = session.query(Actions).filter(
        Actions.symbol == symbol
    ).all()
    existing_records = {str(record.date): record for record in existing_actions}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    for date_index, row in data.iterrows():
        # 日付の変換
        if hasattr(date_index, 'strftime'):
            date_str = date_index.strftime('%Y-%m-%d')
        else:
            date_str = str(date_index)[:10]  # ISO形式の日付部分のみ取得
        
        # 配当額と株式分割の取得
        dividends = row.get('Dividends', 0.0) if not pd.isna(row.get('Dividends', 0.0)) else 0.0
        stock_splits = row.get('Stock Splits', 0.0) if not pd.isna(row.get('Stock Splits', 0.0)) else 0.0
        
        # 配当も株式分割も0の場合はスキップ
        if dividends == 0.0 and stock_splits == 0.0:
            continue
        
        if date_str in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[date_str]
            setattr(existing_record, 'dividends', float(dividends))
            setattr(existing_record, 'stock_splits', float(stock_splits))
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            action_record = Actions(
                symbol=symbol,
                date=date_str,
                dividends=float(dividends),
                stock_splits=float(stock_splits),
                created_at=datetime.now().isoformat()[:24],
                updated_at=datetime.now().isoformat()[:24]
            )
            new_records.append(action_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated actions records for {symbol}")
    return len(new_records) + updated_count
