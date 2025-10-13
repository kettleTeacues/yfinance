"""
Stock news data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime

from models.models import News
from database.client import db_client


def insert_stock_news(yf_client: yf.Ticker) -> int:
    """
    指定された銘柄の株式ニュース情報データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # 株式ニュース情報データを取得
        news_data = yf_client.news
        
        if not news_data or len(news_data) == 0:
            print(f"No news data found for {symbol}")
            return 0
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_news_data(session, symbol, news_data)
            session.commit()
            print(f"Successfully processed {processed_count} news records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting news data for {symbol}: {e}")
        return 0


def _bulk_process_news_data(session, symbol: str, news_list: list) -> int:
    """
    ニュース情報データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        news_list: list of news data
        
    Returns:
        int: 処理された行数
    """
    processed_count = 0
    
    for news_item in news_list:
        # ニュースIDの取得
        news_id = news_item.get('id', None)
        if not news_id:
            continue
        
        # 既存レコードの検索（ニュースIDで一意識別）
        existing_record = session.query(News).filter(
            News.id == news_id
        ).first()
        
        if existing_record:
            # 既存レコードの更新
            _update_news_fields(existing_record, news_item)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            processed_count += 1
        else:
            # 新規レコードの作成
            new_record = _create_news_record(symbol, news_item)
            if new_record:
                session.add(new_record)
                processed_count += 1
    
    return processed_count


def _create_news_record(symbol: str, news_item: dict):
    """
    ニュース情報レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        news_item: ニュース情報データ
        
    Returns:
        News or None: 作成されたレコード
    """
    news_id = news_item.get('id', None)
    
    if not news_id:
        return None
    
    record = News(
        id=news_id,
        symbol=symbol,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_news_fields(record, news_item)
    
    return record


def _update_news_fields(record: News, news_item: dict) -> None:
    """
    ニュース情報レコードのフィールドを更新する
    
    Args:
        record: Newsモデルのインスタンス
        news_item: ニュース情報データ
    """
    # content情報の取得
    content = news_item.get('content', None)
    if not content:
        content = {}
    
    # 基本情報の設定（null値チェック）
    content_type = content.get('contentType', None)
    if content_type is not None:
        setattr(record, 'content_type', content_type)
    
    title = content.get('title', None)
    if title is not None:
        setattr(record, 'title', title)
    
    description = content.get('description', None)
    if description is not None:
        setattr(record, 'description', description)
    
    summary = content.get('summary', None)
    if summary is not None:
        setattr(record, 'summary', summary)
    
    # 日時情報の設定（文字列の場合は直接使用、timestampの場合は変換）
    pub_date = content.get('pubDate', None)
    if pub_date is not None:
        if isinstance(pub_date, str):
            setattr(record, 'pub_date', pub_date[:24])
        else:
            pub_date_str = pub_date.isoformat()[:24]
            if pub_date_str:
                setattr(record, 'pub_date', pub_date_str)
    
    display_time = content.get('displayTime', None)
    if display_time is not None:
        if isinstance(display_time, str):
            setattr(record, 'display_time', display_time[:24])
        else:
            display_time_str = display_time.isoformat()[:24]
            if display_time_str:
                setattr(record, 'display_time', display_time_str)
    
    # プロバイダー情報の設定
    provider = content.get('provider', None)
    if provider:
        provider_name = provider.get('displayName', None)
        if provider_name is not None:
            setattr(record, 'provider_name', provider_name)
        
        provider_url = provider.get('url', None)
        if provider_url is not None:
            setattr(record, 'provider_url', provider_url)
    
    # URL情報の設定
    canonical_url_obj = content.get('canonicalUrl', None)
    if canonical_url_obj:
        canonical_url = canonical_url_obj.get('url', None)
        if canonical_url is not None:
            setattr(record, 'canonical_url', canonical_url)
        
        site = canonical_url_obj.get('site', None)
        if site is not None:
            setattr(record, 'site', site)
        
        region = canonical_url_obj.get('region', None)
        if region is not None:
            setattr(record, 'region', region)
        
        lang = canonical_url_obj.get('lang', None)
        if lang is not None:
            setattr(record, 'lang', lang)
    
    click_through_url_obj = content.get('clickThroughUrl', None)
    if click_through_url_obj:
        click_through_url = click_through_url_obj.get('url', None)
        if click_through_url is not None:
            setattr(record, 'click_through_url', click_through_url)
    
    preview_url = content.get('previewUrl', None)
    if preview_url is not None:
        setattr(record, 'preview_url', preview_url)
    
    # フラグ情報の設定
    is_hosted = content.get('isHosted', None)
    if is_hosted is not None:
        setattr(record, 'is_hosted', str(is_hosted).lower())
    
    bypass_modal = content.get('bypassModal', None)
    if bypass_modal is not None:
        setattr(record, 'bypass_modal', str(bypass_modal).lower())
    
    # メタデータ情報の設定
    metadata = content.get('metadata', None)
    if metadata:
        editors_pick = metadata.get('editorsPick', None)
        if editors_pick is not None:
            setattr(record, 'editors_pick', str(editors_pick).lower())
    
    # プレミアム情報の設定
    finance = content.get('finance', None)
    if finance:
        premium_finance = finance.get('premiumFinance', None)
        if premium_finance:
            is_premium_news = premium_finance.get('isPremiumNews', None)
            if is_premium_news is not None:
                setattr(record, 'is_premium_news', str(is_premium_news).lower())
            
            is_premium_free_news = premium_finance.get('isPremiumFreeNews', None)
            if is_premium_free_news is not None:
                setattr(record, 'is_premium_free_news', str(is_premium_free_news).lower())
