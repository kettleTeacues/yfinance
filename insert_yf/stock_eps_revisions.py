"""
EPS revisions data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import EpsRevisions
from database.client import db_client


def insert_stock_eps_revisions(yf_client: yf.Ticker) -> int:
    """
    指定された銘柄のEPS予想修正データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # EPS予想修正データを取得
        eps_revisions_data = yf_client.eps_revisions
        
        if eps_revisions_data is None or eps_revisions_data.empty:
            print(f"No EPS revisions data found for {symbol}")
            return 0
        
        # DataFrameを辞書に変換
        revisions_dict = eps_revisions_data.to_dict('index')
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_eps_revisions_data(session, symbol, revisions_dict)
            session.commit()
            print(f"Successfully processed {processed_count} EPS revisions records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting EPS revisions data for {symbol}: {e}")
        return 0


def _bulk_process_eps_revisions_data(session, symbol: str, data: dict) -> int:
    """
    EPS予想修正データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with EPS revisions data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_revisions = session.query(EpsRevisions).filter(
        EpsRevisions.symbol == symbol
    ).all()
    existing_records = {record.period_type: record for record in existing_revisions}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    # 現在の年度を取得
    current_year = datetime.now().year
    
    for period_type, revisions_data in data.items():
        if period_type in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[period_type]
            _update_eps_revisions_fields(existing_record, revisions_data, current_year, period_type)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            revisions_record = _create_eps_revisions_record(
                symbol, period_type, revisions_data, current_year
            )
            new_records.append(revisions_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated EPS revisions records for {symbol}")
    return len(new_records) + updated_count


def _create_eps_revisions_record(symbol: str, period_type: str, data: dict, current_year: int) -> EpsRevisions:
    """
    EPS予想修正レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        period_type: 期間タイプ（0q, +1q, 0y, +1yなど）
        data: EPS予想修正データ
        current_year: 現在年
        
    Returns:
        EpsRevisions: 作成されたレコード
    """
    revisions_record = EpsRevisions(
        symbol=symbol,
        period_type=period_type,
        year=current_year,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_eps_revisions_fields(revisions_record, data, current_year, period_type)
    
    return revisions_record


def _update_eps_revisions_fields(record: EpsRevisions, data: dict, current_year: int, period_type: str) -> None:
    """
    EPS予想修正レコードのフィールドを更新する
    
    Args:
        record: EpsRevisionsモデルのインスタンス
        data: EPS予想修正データ
        current_year: 現在年
        period_type: 期間タイプ
    """
    # フィールドマッピング
    field_mappings = {
        'up_last_7days': ['upLast7days'],
        'up_last_30days': ['upLast30days'],
        'down_last_7days': ['downLast7Days'],
        'down_last_30days': ['downLast30days']
    }
    
    # 年度の設定
    setattr(record, 'year', current_year)
    
    # 各フィールドの設定
    for db_field, json_keys in field_mappings.items():
        for json_key in json_keys:
            value = data.get(json_key, None)
            if value is not None and not pd.isna(value):
                try:
                    setattr(record, db_field, int(value))
                    break
                except (ValueError, TypeError):
                    continue
