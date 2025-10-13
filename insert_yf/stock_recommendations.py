"""
Stock recommendations data insertion module for yfinance
"""
import yfinance as yf
from sqlalchemy import and_
from datetime import datetime
import pandas as pd

from models.models import Recommendations
from database.client import db_client
from .utils import safe_get, safe_timestamp_to_str


def insert_stock_recommendations(yf_client: yf.Ticker) -> int:
    """
    指定された銘柄のアナリスト推奨情報データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # アナリスト推奨情報データを取得
        recommendations_data = yf_client.recommendations
        
        if recommendations_data is None or recommendations_data.empty:
            print(f"No recommendations data found for {symbol}")
            return 0
        
        # DataFrameを辞書に変換
        recommendations_dict = recommendations_data.to_dict('index')
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_recommendations_data(session, symbol, recommendations_dict)
            session.commit()
            print(f"Successfully processed {processed_count} recommendations records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting recommendations data for {symbol}: {e}")
        return 0


def _bulk_process_recommendations_data(session, symbol: str, data: dict) -> int:
    """
    アナリスト推奨情報データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with recommendations data
        
    Returns:
        int: 処理された行数
    """
    processed_count = 0
    
    for index, recommendation_data in data.items():
        # 期間の取得
        period = recommendation_data.get('period', None)
        
        if not period:
            continue
        
        # 既存レコードの検索（シンボルと期間の複合キー）
        existing_record = session.query(Recommendations).filter(
            and_(
                Recommendations.symbol == symbol,
                Recommendations.period == period
            )
        ).first()
        
        if existing_record:
            # 既存レコードの更新
            _update_recommendations_fields(existing_record, recommendation_data)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            processed_count += 1
        else:
            # 新規レコードの作成
            new_record = _create_recommendations_record(symbol, recommendation_data)
            if new_record:
                session.add(new_record)
                processed_count += 1
    
    return processed_count


def _create_recommendations_record(symbol: str, recommendation_data: dict):
    """
    アナリスト推奨情報レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        recommendation_data: アナリスト推奨情報データ
        
    Returns:
        Recommendations or None: 作成されたレコード
    """
    period = recommendation_data.get('period', None)
    
    if not period:
        return None
    
    record = Recommendations(
        symbol=symbol,
        period=period,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_recommendations_fields(record, recommendation_data)
    
    return record


def _update_recommendations_fields(record: Recommendations, recommendation_data: dict) -> None:
    """
    アナリスト推奨情報レコードのフィールドを更新する
    
    Args:
        record: Recommendationsモデルのインスタンス
        recommendation_data: アナリスト推奨情報データ
    """
    # フィールドマッピング
    field_mappings = {
        'strong_buy': ['strongBuy'],
        'buy': ['buy'],
        'hold': ['hold'],
        'sell': ['sell'],
        'strong_sell': ['strongSell']
    }
    
    # 各フィールドの設定
    for db_field, json_keys in field_mappings.items():
        for json_key in json_keys:
            value = recommendation_data.get(json_key, None)
            if value is not None and not pd.isna(value):
                try:
                    setattr(record, db_field, int(value))
                    break
                except (ValueError, TypeError):
                    continue
    
    # 総アナリスト数を計算
    strong_buy = getattr(record, 'strong_buy', 0) or 0
    buy = getattr(record, 'buy', 0) or 0
    hold = getattr(record, 'hold', 0) or 0
    sell = getattr(record, 'sell', 0) or 0
    strong_sell = getattr(record, 'strong_sell', 0) or 0
    
    total_analysts = strong_buy + buy + hold + sell + strong_sell
    if total_analysts > 0:
        setattr(record, 'total_analysts', total_analysts)
