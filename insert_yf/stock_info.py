"""
Stock Info data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import StockInfo
from database.client import db_client
from .utils import safe_get, safe_timestamp_to_str


def insert_stock_info(yf_client: yf.Ticker) -> int:
    """
    指定された銘柄の基本情報データを取得し、データベースに挿入する
    upsert機能を使用して既存レコードの更新または新規挿入を行う
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL", "7974.T")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # 株式基本情報を取得
        info_data = yf_client.info
        
        if not info_data or len(info_data) == 0:
            print(f"No stock info found for {symbol}")
            return 0
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _process_stock_info_data(session, symbol, info_data)
            session.commit()
            print(f"Successfully processed {processed_count} stock info record for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting stock info for {symbol}: {e}")
        return 0


def _process_stock_info_data(session, symbol: str, data: dict) -> int:
    """
    株式基本情報データを処理してDBに挿入する（アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: yfinance info dict
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの確認
    existing_info = session.query(StockInfo).filter(
        StockInfo.symbol == symbol
    ).first()
    
    current_time = datetime.now().isoformat()[:24]
    
    # データマッピング関数
    def get_safe_value(key, default=None):
        return safe_get(data, key) if data else default
    
    def get_safe_timestamp_str(key):
        timestamp_value = safe_get(data, key)
        if timestamp_value:
            return safe_timestamp_to_str(timestamp_value)
        return None
    
    def get_safe_bool_str(key):
        bool_value = safe_get(data, key)
        if bool_value is not None:
            return str(bool_value).lower()
        return None
    
    if existing_info:
        # 既存レコードの更新
        _update_stock_info_fields(existing_info, data, get_safe_value, get_safe_timestamp_str, get_safe_bool_str)
        existing_info.updated_at = current_time
        return 1
    else:
        # 新規レコードの作成
        stock_info = StockInfo(
            symbol=symbol,
            created_at=current_time,
            updated_at=current_time
        )
        
        _update_stock_info_fields(stock_info, data, get_safe_value, get_safe_timestamp_str, get_safe_bool_str)
        
        session.add(stock_info)
        return 1


def _update_stock_info_fields(stock_info: StockInfo, data: dict, get_safe_value, get_safe_timestamp_str, get_safe_bool_str):
    """
    StockInfoオブジェクトのフィールドを更新する
    
    Args:
        stock_info: StockInfo model instance
        data: yfinance info dict
        get_safe_value: 安全な値取得関数
        get_safe_timestamp_str: タイムスタンプ変換関数
        get_safe_bool_str: bool値変換関数
    """
    # 企業基本情報
    stock_info.long_name = get_safe_value('longName')
    stock_info.short_name = get_safe_value('shortName')
    
    # 住所・連絡先情報
    stock_info.address1 = get_safe_value('address1')
    stock_info.address2 = get_safe_value('address2')
    stock_info.city = get_safe_value('city')
    stock_info.zip_code = get_safe_value('zip')
    stock_info.country = get_safe_value('country')
    stock_info.phone = get_safe_value('phone')
    stock_info.website = get_safe_value('website')
    stock_info.ir_website = get_safe_value('irWebsite')
    
    # 業界・セクター情報
    stock_info.industry = get_safe_value('industry')
    stock_info.industry_key = get_safe_value('industryKey')
    stock_info.industry_disp = get_safe_value('industryDisp')
    stock_info.sector = get_safe_value('sector')
    stock_info.sector_key = get_safe_value('sectorKey')
    stock_info.sector_disp = get_safe_value('sectorDisp')
    
    # 企業情報
    stock_info.long_business_summary = get_safe_value('longBusinessSummary')
    stock_info.full_time_employees = get_safe_value('fullTimeEmployees')
    
    # 株価情報
    stock_info.currency = get_safe_value('currency')
    stock_info.current_price = get_safe_value('currentPrice')
    stock_info.previous_close = get_safe_value('previousClose')
    stock_info.open_price = get_safe_value('open')
    stock_info.day_low = get_safe_value('dayLow')
    stock_info.day_high = get_safe_value('dayHigh')
    stock_info.regular_market_previous_close = get_safe_value('regularMarketPreviousClose')
    stock_info.regular_market_open = get_safe_value('regularMarketOpen')
    stock_info.regular_market_day_low = get_safe_value('regularMarketDayLow')
    stock_info.regular_market_day_high = get_safe_value('regularMarketDayHigh')
    stock_info.regular_market_price = get_safe_value('regularMarketPrice')
    stock_info.regular_market_change = get_safe_value('regularMarketChange')
    stock_info.regular_market_change_percent = get_safe_value('regularMarketChangePercent')
    
    # 52週・年間データ
    stock_info.fifty_two_week_low = get_safe_value('fiftyTwoWeekLow')
    stock_info.fifty_two_week_high = get_safe_value('fiftyTwoWeekHigh')
    stock_info.fifty_two_week_change = get_safe_value('52WeekChange')
    stock_info.fifty_two_week_change_percent = get_safe_value('fiftyTwoWeekChangePercent')
    stock_info.all_time_high = get_safe_value('allTimeHigh')
    stock_info.all_time_low = get_safe_value('allTimeLow')
    
    # 移動平均
    stock_info.fifty_day_average = get_safe_value('fiftyDayAverage')
    stock_info.fifty_day_average_change = get_safe_value('fiftyDayAverageChange')
    stock_info.fifty_day_average_change_percent = get_safe_value('fiftyDayAverageChangePercent')
    stock_info.two_hundred_day_average = get_safe_value('twoHundredDayAverage')
    stock_info.two_hundred_day_average_change = get_safe_value('twoHundredDayAverageChange')
    stock_info.two_hundred_day_average_change_percent = get_safe_value('twoHundredDayAverageChangePercent')
    
    # 出来高情報
    stock_info.volume = get_safe_value('volume')
    stock_info.regular_market_volume = get_safe_value('regularMarketVolume')
    stock_info.average_volume = get_safe_value('averageVolume')
    stock_info.average_volume_10days = get_safe_value('averageVolume10days')
    stock_info.average_daily_volume_10day = get_safe_value('averageDailyVolume10Day')
    stock_info.average_daily_volume_3month = get_safe_value('averageDailyVolume3Month')
    
    # 入札・オファー情報
    stock_info.bid = get_safe_value('bid')
    stock_info.ask = get_safe_value('ask')
    stock_info.bid_size = get_safe_value('bidSize')
    stock_info.ask_size = get_safe_value('askSize')
    
    # 配当関連
    stock_info.dividend_rate = get_safe_value('dividendRate')
    stock_info.dividend_yield = get_safe_value('dividendYield')
    stock_info.ex_dividend_date = get_safe_timestamp_str('exDividendDate')
    stock_info.payout_ratio = get_safe_value('payoutRatio')
    stock_info.five_year_avg_dividend_yield = get_safe_value('fiveYearAvgDividendYield')
    stock_info.trailing_annual_dividend_rate = get_safe_value('trailingAnnualDividendRate')
    stock_info.trailing_annual_dividend_yield = get_safe_value('trailingAnnualDividendYield')
    stock_info.last_dividend_value = get_safe_value('lastDividendValue')
    stock_info.last_dividend_date = get_safe_timestamp_str('lastDividendDate')
    
    # 株式分割情報
    stock_info.last_split_factor = get_safe_value('lastSplitFactor')
    stock_info.last_split_date = get_safe_timestamp_str('lastSplitDate')
    
    # 市場・企業価値指標
    stock_info.market_cap = get_safe_value('marketCap')
    stock_info.enterprise_value = get_safe_value('enterpriseValue')
    stock_info.shares_outstanding = get_safe_value('sharesOutstanding')
    stock_info.float_shares = get_safe_value('floatShares')
    stock_info.implied_shares_outstanding = get_safe_value('impliedSharesOutstanding')
    stock_info.held_percent_insiders = get_safe_value('heldPercentInsiders')
    stock_info.held_percent_institutions = get_safe_value('heldPercentInstitutions')
    
    # 財務比率
    stock_info.beta = get_safe_value('beta')
    stock_info.trailing_pe = get_safe_value('trailingPE')
    stock_info.forward_pe = get_safe_value('forwardPE')
    stock_info.price_to_book = get_safe_value('priceToBook')
    stock_info.price_to_sales_trailing_12months = get_safe_value('priceToSalesTrailing12Months')
    stock_info.enterprise_to_revenue = get_safe_value('enterpriseToRevenue')
    stock_info.enterprise_to_ebitda = get_safe_value('enterpriseToEbitda')
    stock_info.trailing_peg_ratio = get_safe_value('trailingPegRatio')
    
    # 財務データ
    stock_info.total_cash = get_safe_value('totalCash')
    stock_info.total_cash_per_share = get_safe_value('totalCashPerShare')
    stock_info.total_debt = get_safe_value('totalDebt')
    stock_info.total_revenue = get_safe_value('totalRevenue')
    stock_info.revenue_per_share = get_safe_value('revenuePerShare')
    stock_info.ebitda = get_safe_value('ebitda')
    stock_info.gross_profits = get_safe_value('grossProfits')
    stock_info.net_income_to_common = get_safe_value('netIncomeToCommon')
    stock_info.book_value = get_safe_value('bookValue')
    
    # 流動性比率
    stock_info.quick_ratio = get_safe_value('quickRatio')
    stock_info.current_ratio = get_safe_value('currentRatio')
    
    # 収益性指標
    stock_info.return_on_assets = get_safe_value('returnOnAssets')
    stock_info.return_on_equity = get_safe_value('returnOnEquity')
    stock_info.profit_margins = get_safe_value('profitMargins')
    stock_info.gross_margins = get_safe_value('grossMargins')
    stock_info.ebitda_margins = get_safe_value('ebitdaMargins')
    stock_info.operating_margins = get_safe_value('operatingMargins')
    
    # 成長率
    stock_info.earnings_growth = get_safe_value('earningsGrowth')
    stock_info.revenue_growth = get_safe_value('revenueGrowth')
    stock_info.earnings_quarterly_growth = get_safe_value('earningsQuarterlyGrowth')
    
    # EPS関連
    stock_info.trailing_eps = get_safe_value('trailingEps')
    stock_info.forward_eps = get_safe_value('forwardEps')
    stock_info.eps_trailing_twelve_months = get_safe_value('epsTrailingTwelveMonths')
    stock_info.eps_forward = get_safe_value('epsForward')
    
    # アナリスト予想
    stock_info.target_high_price = get_safe_value('targetHighPrice')
    stock_info.target_low_price = get_safe_value('targetLowPrice')
    stock_info.target_mean_price = get_safe_value('targetMeanPrice')
    stock_info.target_median_price = get_safe_value('targetMedianPrice')
    stock_info.recommendation_mean = get_safe_value('recommendationMean')
    stock_info.recommendation_key = get_safe_value('recommendationKey')
    stock_info.number_of_analyst_opinions = get_safe_value('numberOfAnalystOpinions')
    stock_info.average_analyst_rating = get_safe_value('averageAnalystRating')
    
    # 取引所・市場情報
    stock_info.exchange = get_safe_value('exchange')
    stock_info.full_exchange_name = get_safe_value('fullExchangeName')
    stock_info.market = get_safe_value('market')
    stock_info.market_state = get_safe_value('marketState')
    stock_info.quote_type = get_safe_value('quoteType')
    stock_info.tradeable = get_safe_bool_str('tradeable')
    
    # 時間・地域情報
    stock_info.exchange_timezone_name = get_safe_value('exchangeTimezoneName')
    stock_info.exchange_timezone_short_name = get_safe_value('exchangeTimezoneShortName')
    stock_info.gmt_off_set_milliseconds = get_safe_value('gmtOffSetMilliseconds')
    stock_info.regular_market_time = get_safe_timestamp_str('regularMarketTime')
    
    # リスク指標
    stock_info.audit_risk = get_safe_value('auditRisk')
    stock_info.board_risk = get_safe_value('boardRisk')
    stock_info.compensation_risk = get_safe_value('compensationRisk')
    stock_info.shareholder_rights_risk = get_safe_value('shareHolderRightsRisk')
    stock_info.overall_risk = get_safe_value('overallRisk')
    
    # 決算関連
    stock_info.last_fiscal_year_end = get_safe_timestamp_str('lastFiscalYearEnd')
    stock_info.next_fiscal_year_end = get_safe_timestamp_str('nextFiscalYearEnd')
    stock_info.most_recent_quarter = get_safe_timestamp_str('mostRecentQuarter')
    stock_info.earnings_timestamp = get_safe_timestamp_str('earningsTimestamp')
    stock_info.earnings_timestamp_start = get_safe_timestamp_str('earningsTimestampStart')
    stock_info.earnings_timestamp_end = get_safe_timestamp_str('earningsTimestampEnd')
    stock_info.is_earnings_date_estimate = get_safe_bool_str('isEarningsDateEstimate')
