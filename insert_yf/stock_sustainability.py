"""
Stock sustainability data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd
import json

from models.models import Sustainability
from database.client import db_client


def insert_stock_sustainability(yf_client: yf.Ticker) -> int:
    """
    指定された銘柄のESG持続可能性データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # 持続可能性データを取得
        sustainability_data = yf_client.sustainability
        
        # データが存在しない場合の判定を修正
        if sustainability_data is None:
            print(f"No sustainability data found for {symbol}")
            return 0
        
        # データが既に辞書形式の場合はそのまま使用、DataFrameの場合は変換
        if isinstance(sustainability_data, pd.DataFrame):
            if sustainability_data.empty:
                print(f"Empty sustainability data found for {symbol}")
                return 0
            sustainability_dict = sustainability_data.to_dict()
        else:
            # 辞書形式の場合はそのまま使用
            sustainability_dict = sustainability_data
            if not sustainability_dict:
                print(f"Empty sustainability data found for {symbol}")
                return 0
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_sustainability_data(session, symbol, sustainability_dict)
            session.commit()
            return processed_count
            
    except Exception as e:
        print(f"Error inserting sustainability data for {symbol}: {e}")
        import traceback
        traceback.print_exc()
        return 0


def _bulk_process_sustainability_data(session, symbol: str, data: dict) -> int:
    """
    持続可能性データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: dict with sustainability data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの検索（シンボルで一意識別）
    existing_record = session.query(Sustainability).filter(
        Sustainability.symbol == symbol
    ).first()
    
    if existing_record:
        # 既存レコードの更新
        _update_sustainability_fields(existing_record, data)
        setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
        return 1
    else:
        # 新規レコードの作成
        new_record = _create_sustainability_record(symbol, data)
        if new_record:
            session.add(new_record)
            print(f"Created new sustainability record for {symbol}")
            return 1
    
    return 0


def _create_sustainability_record(symbol: str, data: dict):
    """
    持続可能性レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        data: 持続可能性データ
        
    Returns:
        Sustainability or None: 作成されたレコード
    """
    record = Sustainability(
        symbol=symbol,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_sustainability_fields(record, data)
    
    return record


def _update_sustainability_fields(record: Sustainability, data: dict) -> None:
    """
    持続可能性レコードのフィールドを更新する
    
    Args:
        record: Sustainabilityモデルのインスタンス
        data: 持続可能性データ
    """
    
    # ESGスコア関連のesgScoresキーから値を取得
    esg_scores_data = {}
    for key, value in data.items():
        if isinstance(value, dict) and 'esgScores' in value:
            esg_scores_data[key] = value['esgScores']
            print(f"Found esgScores data for {key}: {value['esgScores']}")
    
    # 基本情報の設定
    basic_fields = {
        'max_age': 'maxAge',
        'rating_year': 'ratingYear',
        'rating_month': 'ratingMonth',
        'total_esg': 'totalEsg',
        'environment_score': 'environmentScore',
        'social_score': 'socialScore',
        'governance_score': 'governanceScore',
        'highest_controversy': 'highestControversy',
        'esg_performance': 'esgPerformance',
        'peer_count': 'peerCount',
        'peer_group': 'peerGroup'
    }
    
    fields_set = 0
    for db_field, json_key in basic_fields.items():
        value = esg_scores_data.get(json_key, None)
        if value is not None and not pd.isna(value):
            try:
                if db_field in ['max_age', 'rating_year', 'rating_month', 'peer_count']:
                    setattr(record, db_field, int(value))
                elif db_field in ['total_esg', 'environment_score', 'social_score', 'governance_score', 'highest_controversy']:
                    setattr(record, db_field, float(value))
                else:
                    setattr(record, db_field, str(value))
                fields_set += 1
                print(f"Set {db_field} = {value}")
            except (ValueError, TypeError) as e:
                print(f"Error setting {db_field}: {e}")
                continue
    
    # ピアパフォーマンス情報の設定
    peer_performance_mappings = {
        'peerEsgScorePerformance': ['peer_esg_min', 'peer_esg_avg', 'peer_esg_max'],
        'peerGovernancePerformance': ['peer_governance_min', 'peer_governance_avg', 'peer_governance_max'],
        'peerSocialPerformance': ['peer_social_min', 'peer_social_avg', 'peer_social_max'],
        'peerEnvironmentPerformance': ['peer_environment_min', 'peer_environment_avg', 'peer_environment_max'],
        'peerHighestControversyPerformance': ['peer_controversy_min', 'peer_controversy_avg', 'peer_controversy_max']
    }
    
    for json_key, db_fields in peer_performance_mappings.items():
        peer_data = esg_scores_data.get(json_key, None)
        if peer_data and isinstance(peer_data, dict):
            for i, stat_key in enumerate(['min', 'avg', 'max']):
                value = peer_data.get(stat_key, None)
                if value is not None and not pd.isna(value):
                    try:
                        setattr(record, db_fields[i], float(value))
                    except (ValueError, TypeError):
                        continue
    
    # パーセンタイル情報の設定
    percentile_fields = {
        'percentile': 'percentile',
        'environment_percentile': 'environmentPercentile',
        'social_percentile': 'socialPercentile',
        'governance_percentile': 'governancePercentile'
    }
    
    for db_field, json_key in percentile_fields.items():
        value = esg_scores_data.get(json_key, None)
        if value is not None and not pd.isna(value):
            try:
                setattr(record, db_field, float(value))
            except (ValueError, TypeError):
                continue
    
    # 関連論争情報の設定（リスト形式の場合はJSON文字列として保存）
    related_controversy = esg_scores_data.get('relatedControversy', None)
    if related_controversy is not None:
        try:
            setattr(record, 'related_controversy', json.dumps(related_controversy))
        except (TypeError, ValueError):
            setattr(record, 'related_controversy', str(related_controversy))
    
    # 投資制限項目フラグの設定
    flag_fields = {
        'adult': 'adult',
        'alcoholic': 'alcoholic',
        'animal_testing': 'animalTesting',
        'catholic': 'catholic',
        'controversial_weapons': 'controversialWeapons',
        'small_arms': 'smallArms',
        'fur_leather': 'furLeather',
        'gambling': 'gambling',
        'gmo': 'gmo',
        'military_contract': 'militaryContract',
        'nuclear': 'nuclear',
        'pesticides': 'pesticides',
        'palm_oil': 'palmOil',
        'coal': 'coal',
        'tobacco': 'tobacco'
    }
    
    for db_field, json_key in flag_fields.items():
        value = esg_scores_data.get(json_key, None)
        if value is not None:
            try:
                setattr(record, db_field, str(value).lower())
            except (ValueError, TypeError):
                continue
