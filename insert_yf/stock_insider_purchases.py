"""
Insider purchases data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import InsiderPurchases
from database.client import db_client


def insert_stock_insider_purchases(symbol: str) -> int:
    """
    指定された銘柄のインサイダー取引データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    ticker = yf.Ticker(symbol)
    
    try:
        # インサイダー取引データを取得
        insider_purchases_data = ticker.insider_purchases
        
        if insider_purchases_data is None or insider_purchases_data.empty:
            print(f"No insider purchases data found for {symbol}")
            return 0
        
        # DataFrameを辞書に変換
        purchases_dict = insider_purchases_data.to_dict('index')
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_insider_purchases_data(session, symbol, purchases_dict)
            session.commit()
            print(f"Successfully processed {processed_count} insider purchases records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting insider purchases data for {symbol}: {e}")
        return 0


def _bulk_process_insider_purchases_data(session, symbol: str, data: dict) -> int:
    """
    インサイダー取引データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with insider purchases data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_purchases = session.query(InsiderPurchases).filter(
        InsiderPurchases.symbol == symbol
    ).all()
    existing_records = {record.insider_purchases_last_6m: record for record in existing_purchases}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    for index, purchase_data in data.items():
        # 項目名の取得
        item_name = purchase_data.get('Insider Purchases Last 6m', None)
        
        if not item_name:
            continue
        
        if item_name in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[item_name]
            _update_insider_purchases_fields(existing_record, purchase_data)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            purchase_record = _create_insider_purchases_record(
                symbol, purchase_data
            )
            if purchase_record:
                new_records.append(purchase_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated insider purchases records for {symbol}")
    return len(new_records) + updated_count


def _create_insider_purchases_record(symbol: str, data: dict):
    """
    インサイダー取引レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        data: インサイダー取引データ
        
    Returns:
        InsiderPurchases or None: 作成されたレコード
    """
    # 項目名の取得
    item_name = data.get('Insider Purchases Last 6m', None)
    
    if not item_name:
        return None
    
    purchase_record = InsiderPurchases(
        symbol=symbol,
        insider_purchases_last_6m=item_name,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_insider_purchases_fields(purchase_record, data)
    
    return purchase_record


def _update_insider_purchases_fields(record: InsiderPurchases, data: dict) -> None:
    """
    インサイダー取引レコードのフィールドを更新する
    
    Args:
        record: InsiderPurchasesモデルのインスタンス
        data: インサイダー取引データ
    """
    # 株式数の設定
    shares_value = data.get('Shares', None)
    if shares_value is not None and not pd.isna(shares_value):
        try:
            setattr(record, 'shares', float(shares_value))
        except (ValueError, TypeError):
            pass
    
    # 取引回数の設定
    trans_value = data.get('Trans', None)
    if trans_value is not None and not pd.isna(trans_value):
        try:
            setattr(record, 'trans', int(trans_value))
        except (ValueError, TypeError):
            pass
