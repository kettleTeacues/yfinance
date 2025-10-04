"""
Earnings dates data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import EarningsDates
from database.client import db_client


def insert_stock_earnings_dates(symbol: str) -> int:
    """
    指定された銘柄の決算発表日データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    ticker = yf.Ticker(symbol)
    
    try:
        # 決算発表日データを取得
        earnings_dates_data = ticker.earnings_dates
        
        if earnings_dates_data.empty:
            print(f"No earnings dates data found for {symbol}")
            return 0
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_earnings_dates_data(session, symbol, earnings_dates_data)
            session.commit()
            print(f"Successfully processed {processed_count} earnings dates records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting earnings dates data for {symbol}: {e}")
        return 0


def _bulk_process_earnings_dates_data(session, symbol: str, data) -> int:
    """
    決算発表日データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: pandas DataFrame with earnings dates data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_earnings = session.query(EarningsDates).filter(
        EarningsDates.symbol == symbol
    ).all()
    existing_records = {str(record.date): record for record in existing_earnings}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    for date_index, row in data.iterrows():
        # 日付の変換
        if hasattr(date_index, 'strftime'):
            date_str = date_index.strftime('%Y-%m-%d')
        else:
            date_str = str(date_index)[:10]  # ISO形式の日付部分のみ取得
        
        # EPS関連データの取得
        eps_estimate = row.get('EPS Estimate') if hasattr(row, 'get') else (row['EPS Estimate'] if 'EPS Estimate' in row else None)
        reported_eps = row.get('Reported EPS') if hasattr(row, 'get') else (row['Reported EPS'] if 'Reported EPS' in row else None)
        surprise_percent = row.get('Surprise(%)') if hasattr(row, 'get') else (row['Surprise(%)'] if 'Surprise(%)' in row else None)
        
        if date_str in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[date_str]
            _update_earnings_fields(existing_record, eps_estimate, reported_eps, surprise_percent)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            earnings_record = _create_earnings_record(
                symbol, date_str, eps_estimate, reported_eps, surprise_percent
            )
            new_records.append(earnings_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated earnings dates records for {symbol}")
    return len(new_records) + updated_count


def _create_earnings_record(symbol: str, date_str: str, eps_estimate, reported_eps, surprise_percent) -> EarningsDates:
    """
    決算発表日レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        date_str: 日付文字列
        eps_estimate: 予想EPS
        reported_eps: 実績EPS
        surprise_percent: サプライズ率
        
    Returns:
        EarningsDates: 作成されたレコード
    """
    earnings_record = EarningsDates(
        symbol=symbol,
        date=date_str,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_earnings_fields(earnings_record, eps_estimate, reported_eps, surprise_percent)
    
    return earnings_record


def _update_earnings_fields(record: EarningsDates, eps_estimate, reported_eps, surprise_percent) -> None:
    """
    決算発表日レコードのフィールドを更新する
    
    Args:
        record: EarningsDatesモデルのインスタンス
        eps_estimate: 予想EPS
        reported_eps: 実績EPS
        surprise_percent: サプライズ率
    """
    # EPS予想の設定
    if eps_estimate is not None and not pd.isna(eps_estimate):
        try:
            setattr(record, 'eps_estimate', float(eps_estimate))
        except (ValueError, TypeError):
            pass
    
    # 実績EPSの設定
    if reported_eps is not None and not pd.isna(reported_eps):
        try:
            setattr(record, 'reported_eps', float(reported_eps))
        except (ValueError, TypeError):
            pass
    
    # サプライズ率の設定
    if surprise_percent is not None and not pd.isna(surprise_percent):
        try:
            setattr(record, 'surprise_percent', float(surprise_percent))
        except (ValueError, TypeError):
            pass


