"""
Institutional holders data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import InstitutionalHolders
from database.client import db_client


def insert_stock_institutional_holders(yf_client: yf.Ticker) -> int:
    """
    指定された銘柄の機関投資家保有データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # 機関投資家保有データを取得
        institutional_holders_data = yf_client.institutional_holders
        
        if institutional_holders_data is None or institutional_holders_data.empty:
            print(f"No institutional holders data found for {symbol}")
            return 0
        
        # DataFrameを辞書に変換
        holders_dict = institutional_holders_data.to_dict('index')
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_institutional_holders_data(session, symbol, holders_dict)
            session.commit()
            print(f"Successfully processed {processed_count} institutional holders records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting institutional holders data for {symbol}: {e}")
        return 0


def _bulk_process_institutional_holders_data(session, symbol: str, data: dict) -> int:
    """
    機関投資家保有データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with institutional holders data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_holders = session.query(InstitutionalHolders).filter(
        InstitutionalHolders.symbol == symbol
    ).all()
    existing_records = {f"{record.date}_{record.holder}": record for record in existing_holders}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    for index, holder_data in data.items():
        # 機関投資家名と報告日の取得
        holder_name = holder_data.get('Holder', None)
        date_reported = holder_data.get('Date Reported', None)
        
        if not holder_name or not date_reported:
            continue
        
        # 日付の変換
        if isinstance(date_reported, str):
            try:
                date_obj = pd.to_datetime(date_reported)
                date_str = date_obj.strftime('%Y-%m-%d')
            except:
                date_str = str(date_reported)[:10]
        else:
            date_str = str(date_reported)[:10]
        
        # 機関投資家名の正規化（余分な空白を除去）
        holder_name = holder_name.strip()
        
        record_key = f"{date_str}_{holder_name}"
        
        if record_key in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[record_key]
            _update_institutional_holders_fields(existing_record, holder_data, date_str, holder_name)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            holder_record = _create_institutional_holders_record(
                symbol, holder_data, date_str, holder_name
            )
            if holder_record:
                new_records.append(holder_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated institutional holders records for {symbol}")
    return len(new_records) + updated_count


def _create_institutional_holders_record(symbol: str, data: dict, date_str: str, holder_name: str):
    """
    機関投資家保有レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        data: 機関投資家保有データ
        date_str: 報告日
        holder_name: 機関投資家名
        
    Returns:
        InstitutionalHolders or None: 作成されたレコード
    """
    if not holder_name or not date_str:
        return None
    
    holder_record = InstitutionalHolders(
        symbol=symbol,
        date=date_str,
        holder=holder_name,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_institutional_holders_fields(holder_record, data, date_str, holder_name)
    
    return holder_record


def _update_institutional_holders_fields(record: InstitutionalHolders, data: dict, date_str: str, holder_name: str) -> None:
    """
    機関投資家保有レコードのフィールドを更新する
    
    Args:
        record: InstitutionalHoldersモデルのインスタンス
        data: 機関投資家保有データ
        date_str: 報告日
        holder_name: 機関投資家名
    """
    # 保有割合の設定
    pct_held_value = data.get('pctHeld', None)
    if pct_held_value is not None and not pd.isna(pct_held_value):
        try:
            setattr(record, 'pct_held', float(pct_held_value))
        except (ValueError, TypeError):
            pass
    
    # 保有株式数の設定
    shares_value = data.get('Shares', None)
    if shares_value is not None and not pd.isna(shares_value):
        try:
            setattr(record, 'shares', float(shares_value))
        except (ValueError, TypeError):
            pass
    
    # 保有株式価値の設定
    value_value = data.get('Value', None)
    if value_value is not None and not pd.isna(value_value):
        try:
            setattr(record, 'value', float(value_value))
        except (ValueError, TypeError):
            pass
    
    # 保有割合変動率の設定
    pct_change_value = data.get('pctChange', None)
    if pct_change_value is not None and not pd.isna(pct_change_value):
        try:
            setattr(record, 'pct_change', float(pct_change_value))
        except (ValueError, TypeError):
            pass
