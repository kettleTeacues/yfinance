"""
Stock calendar data i        # カレンダーデータを取得
        calendar_data = ticker.calendar
        
        if not calendar_data or (isinstance(calendar_data, dict) and len(calendar_data) == 0):
            print(f"No calendar data found for {symbol}")
            return 0on module for yfinance
"""
import yfinance as yf
from datetime import datetime

from models.models import Calendar
from database.client import db_client
from .utils import safe_get


def insert_stock_calendar(symbol: str) -> int:
    """
    指定された銘柄のカレンダーデータを取得し、データベースに挿入する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 挿入された行数
    """
    ticker = yf.Ticker(symbol)
    
    try:
        # カレンダーデータを取得
        calendar_data = ticker.calendar
        
        if not calendar_data or (isinstance(calendar_data, dict) and len(calendar_data) == 0):
            print(f"No calendar data found for {symbol}")
            return 0
        
        with db_client.session_scope() as session:
            
            # カレンダーレコードの作成
            calendar_record = Calendar(
                symbol=symbol,
                data_source='yfinance',
                last_updated=datetime.now().isoformat()[:24],
                created_at=datetime.now().isoformat()[:24],
                updated_at=datetime.now().isoformat()[:24]
            )
            
            # データのマッピング
            _map_calendar_data(calendar_record, calendar_data)

            # 既存レコードの確認
            existing_record = session.query(Calendar).filter_by(
                symbol=symbol
            ).first()
            
            if existing_record:
                # 既存のレコードを更新
                calendar_record = existing_record
            else:
                # 新規レコードを作成
                session.add(calendar_record)
            
            session.commit()
            print(f"Inserted calendar record for {symbol}")
            return 1
            
    except Exception as e:
        print(f"Error inserting calendar data for {symbol}: {e}")
        return 0


def _map_calendar_data(record: Calendar, data) -> None:
    """
    yfinanceのカレンダーデータをCalendarモデルにマッピングする
    
    Args:
        record: Calendarモデルのインスタンス
        data: yfinanceから取得したカレンダーデータ
    """
    # データは辞書形式で取得される
    if isinstance(data, dict) and len(data) > 0:
        # 辞書データを直接使用
        row_data = data
        
        # Ex-Dividend Date
        ex_div_date = safe_get(row_data, 'Ex-Dividend Date')
        if ex_div_date:
            setattr(record, 'ex_dividend_date', ex_div_date)
        
        # Earnings Date (配列の場合は最初の要素を取得)
        earnings_date = safe_get(row_data, 'Earnings Date')
        if earnings_date:
            setattr(record, 'earnings_date', earnings_date[0])
        
        # Earnings予測値
        earnings_high = safe_get(row_data, 'Earnings High')
        if earnings_high is not None:
            try:
                setattr(record, 'earnings_high', float(earnings_high))
            except (ValueError, TypeError):
                pass
        
        earnings_low = safe_get(row_data, 'Earnings Low')
        if earnings_low is not None:
            try:
                setattr(record, 'earnings_low', float(earnings_low))
            except (ValueError, TypeError):
                pass
        
        earnings_avg = safe_get(row_data, 'Earnings Average')
        if earnings_avg is not None:
            try:
                setattr(record, 'earnings_average', float(earnings_avg))
            except (ValueError, TypeError):
                pass
        
        # Revenue予測値
        revenue_high = safe_get(row_data, 'Revenue High')
        if revenue_high is not None:
            try:
                setattr(record, 'revenue_high', float(revenue_high))
            except (ValueError, TypeError):
                pass
        
        revenue_low = safe_get(row_data, 'Revenue Low')
        if revenue_low is not None:
            try:
                setattr(record, 'revenue_low', float(revenue_low))
            except (ValueError, TypeError):
                pass
        
        revenue_avg = safe_get(row_data, 'Revenue Average')
        if revenue_avg is not None:
            try:
                setattr(record, 'revenue_average', float(revenue_avg))
            except (ValueError, TypeError):
                pass
