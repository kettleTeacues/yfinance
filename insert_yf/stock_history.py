"""
Stock History data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd
from typing import Optional

from models.models import History
from database.client import db_client


def insert_stock_history(symbol: str, period: str = "1y") -> int:
    """
    指定された銘柄の株価履歴データを取得し、データベースに挿入する
    upsert機能を使用して既存レコードの更新または新規挿入を行う
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL", "7974.T")
        period: 取得期間 ("1y", "2y", "5y", "10y", "ytd", "max"など)
    
    Returns:
        int: 処理された行数
    """
    ticker = yf.Ticker(symbol)
    
    try:
        # 株価履歴データを取得
        hist_data = ticker.history(period=period)
        
        if hist_data.empty:
            print(f"No stock history found for {symbol}")
            return 0
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _process_stock_history_data(session, symbol, hist_data)
            session.commit()
            print(f"Successfully processed {processed_count} stock history records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting stock history for {symbol}: {e}")
        return 0


def _process_stock_history_data(session, symbol: str, hist_data: pd.DataFrame) -> int:
    """
    株価履歴データを処理してDBに挿入する（bulk upsert）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        hist_data: yfinance history DataFrame
        
    Returns:
        int: 処理された行数
    """
    current_time = datetime.now().isoformat()[:24]
    processed_count = 0
    
    # 既存の日付を取得してセットに変換（高速検索用）
    existing_dates = set(
        row[0] for row in session.query(History.date).filter(
            History.symbol == symbol
        ).all()
    )
    
    # bulk処理用のリスト
    new_records = []
    update_records = []
    
    for date_index, row in hist_data.iterrows():
        try:
            # 日付をISO形式の文字列に変換
            date_str = _format_date(date_index)
            
            # 数値データを安全に取得
            record_data = {
                'symbol': symbol,
                'date': date_str,
                'open': _get_safe_float(row, 'Open'),
                'high': _get_safe_float(row, 'High'),
                'low': _get_safe_float(row, 'Low'),
                'close': _get_safe_float(row, 'Close'),
                'volume': _get_safe_float(row, 'Volume'),
                'created_at': current_time,
                'updated_at': current_time
            }
            
            if date_str in existing_dates:
                # 既存レコードを更新対象に追加
                update_records.append(record_data)
            else:
                # 新規レコードを挿入対象に追加
                new_records.append(record_data)
            
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing history record for {symbol} on {date_index}: {e}")
            continue
    
    # bulk insert実行
    if new_records:
        session.bulk_insert_mappings(History, new_records)
        print(f"Bulk inserted {len(new_records)} new history records")
    
    # bulk update実行
    if update_records:
        for record in update_records:
            session.query(History).filter(
                History.symbol == record['symbol'],
                History.date == record['date']
            ).update({
                'open': record['open'],
                'high': record['high'],
                'low': record['low'],
                'close': record['close'],
                'volume': record['volume'],
                'updated_at': record['updated_at']
            }, synchronize_session=False)
        
        print(f"Bulk updated {len(update_records)} existing history records")
    
    return processed_count


def _format_date(date_index) -> str:
    """
    pandasの日付インデックスをISO形式の文字列に変換
    
    Args:
        date_index: pandas DatetimeIndex
        
    Returns:
        str: ISO形式の日付文字列
    """
    try:
        # pandas Timestamp や datetime オブジェクトの場合
        return date_index.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:24]
    except (AttributeError, TypeError):
        # 文字列や他の型の場合
        return str(date_index)[:24]


def _get_safe_float(row: pd.Series, column_name: str) -> Optional[float]:
    """
    pandas Seriesから数値を安全に取得
    
    Args:
        row: pandas Series
        column_name: 列名
        
    Returns:
        float: 数値またはNone
    """
    try:
        if column_name not in row.index:
            return None
            
        value = row[column_name]
        
        # pandas NaN チェック
        if pd.isna(value):
            return None
            
        # 数値型チェック
        if isinstance(value, (int, float)):
            return float(value)
            
        # 文字列から数値変換を試行
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return None
                
        return None
        
    except Exception as e:
        print(f"Error getting numeric value for {column_name}: {e}")
        return None
