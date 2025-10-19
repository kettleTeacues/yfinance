"""
Stock model for SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class StockInfo(Base):
    """
    株式の包括的な基本情報を格納するテーブル
    企業情報、株価指標、財務比率、アナリスト予想等を管理
    """
    __tablename__ = 'stock_info'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), unique=True, comment='銘柄シンボル')

    # 企業基本情報
    long_name = Column(String(255), comment='会社正式名称')
    short_name = Column(String(100), comment='会社略称')
    
    # 住所・連絡先情報
    address1 = Column(String(255), comment='住所1')
    address2 = Column(String(255), comment='住所2')
    city = Column(String(100), comment='市区町村')
    zip_code = Column(String(20), comment='郵便番号')
    country = Column(String(50), comment='国')
    phone = Column(String(50), comment='電話番号')
    website = Column(String(500), comment='ウェブサイト')
    ir_website = Column(String(500), comment='IR専用ウェブサイト')
    
    # 業界・セクター情報
    industry = Column(String(100), comment='業界')
    industry_key = Column(String(100), comment='業界キー')
    industry_disp = Column(String(100), comment='業界表示名')
    sector = Column(String(100), comment='セクター')
    sector_key = Column(String(100), comment='セクターキー')
    sector_disp = Column(String(100), comment='セクター表示名')
    
    # 企業情報
    long_business_summary = Column(Text, comment='事業概要')
    full_time_employees = Column(Integer, comment='正社員数')
    
    # 株価情報
    currency = Column(String(10), comment='通貨')
    current_price = Column(Float, comment='現在価格')
    previous_close = Column(Float, comment='前日終値')
    open_price = Column(Float, comment='始値')
    day_low = Column(Float, comment='日中安値')
    day_high = Column(Float, comment='日中高値')
    regular_market_previous_close = Column(Float, comment='通常市場前日終値')
    regular_market_open = Column(Float, comment='通常市場始値')
    regular_market_day_low = Column(Float, comment='通常市場日中安値')
    regular_market_day_high = Column(Float, comment='通常市場日中高値')
    regular_market_price = Column(Float, comment='通常市場価格')
    regular_market_change = Column(Float, comment='通常市場変動額')
    regular_market_change_percent = Column(Float, comment='通常市場変動率')
    
    # 52週・年間データ
    fifty_two_week_low = Column(Float, comment='52週安値')
    fifty_two_week_high = Column(Float, comment='52週高値')
    fifty_two_week_change = Column(Float, comment='52週変動率')
    fifty_two_week_change_percent = Column(Float, comment='52週変動率（%）')
    all_time_high = Column(Float, comment='史上最高値')
    all_time_low = Column(Float, comment='史上最安値')
    
    # 移動平均
    fifty_day_average = Column(Float, comment='50日移動平均')
    fifty_day_average_change = Column(Float, comment='50日移動平均からの変動額')
    fifty_day_average_change_percent = Column(Float, comment='50日移動平均からの変動率')
    two_hundred_day_average = Column(Float, comment='200日移動平均')
    two_hundred_day_average_change = Column(Float, comment='200日移動平均からの変動額')
    two_hundred_day_average_change_percent = Column(Float, comment='200日移動平均からの変動率')
    
    # 出来高情報
    volume = Column(Float, comment='出来高')
    regular_market_volume = Column(Float, comment='通常市場出来高')
    average_volume = Column(Float, comment='平均出来高')
    average_volume_10days = Column(Float, comment='10日平均出来高')
    average_daily_volume_10day = Column(Float, comment='10日平均日次出来高')
    average_daily_volume_3month = Column(Float, comment='3ヶ月平均日次出来高')
    
    # 入札・オファー情報
    bid = Column(Float, comment='買値')
    ask = Column(Float, comment='売値')
    bid_size = Column(Float, comment='買気配数量')
    ask_size = Column(Float, comment='売気配数量')
    
    # 配当関連
    dividend_rate = Column(Float, comment='配当レート')
    dividend_yield = Column(Float, comment='配当利回り')
    ex_dividend_date = Column(String(24), comment='配当落ち日')
    payout_ratio = Column(Float, comment='配当性向')
    five_year_avg_dividend_yield = Column(Float, comment='5年平均配当利回り')
    trailing_annual_dividend_rate = Column(Float, comment='過去12ヶ月配当レート')
    trailing_annual_dividend_yield = Column(Float, comment='過去12ヶ月配当利回り')
    last_dividend_value = Column(Float, comment='最新配当額')
    last_dividend_date = Column(String(24), comment='最新配当日')
    
    # 株式分割情報
    last_split_factor = Column(String(20), comment='最新株式分割比率')
    last_split_date = Column(String(24), comment='最新株式分割日')
    
    # 市場・企業価値指標
    market_cap = Column(Float, comment='時価総額')
    enterprise_value = Column(Float, comment='企業価値')
    shares_outstanding = Column(Float, comment='発行済株式数')
    float_shares = Column(Float, comment='流通株式数')
    implied_shares_outstanding = Column(Float, comment='推定発行済株式数')
    held_percent_insiders = Column(Float, comment='内部者保有率')
    held_percent_institutions = Column(Float, comment='機関投資家保有率')
    
    # 財務比率
    beta = Column(Float, comment='ベータ値')
    trailing_pe = Column(Float, comment='実績PER')
    forward_pe = Column(Float, comment='予想PER')
    price_to_book = Column(Float, comment='PBR（株価純資産倍率）')
    price_to_sales_trailing_12months = Column(Float, comment='PSR（株価売上倍率）')
    enterprise_to_revenue = Column(Float, comment='EV/売上倍率')
    enterprise_to_ebitda = Column(Float, comment='EV/EBITDA倍率')
    trailing_peg_ratio = Column(Float, comment='PEGレシオ')
    
    # 財務データ
    total_cash = Column(Float, comment='総現金')
    total_cash_per_share = Column(Float, comment='1株当たり現金')
    total_debt = Column(Float, comment='総負債')
    total_revenue = Column(Float, comment='総売上')
    revenue_per_share = Column(Float, comment='1株当たり売上')
    ebitda = Column(Float, comment='EBITDA')
    gross_profits = Column(Float, comment='売上総利益')
    net_income_to_common = Column(Float, comment='普通株主帰属純利益')
    book_value = Column(Float, comment='1株当たり純資産')
    
    # 流動性比率
    quick_ratio = Column(Float, comment='当座比率')
    current_ratio = Column(Float, comment='流動比率')
    
    # 収益性指標
    return_on_assets = Column(Float, comment='ROA（総資産利益率）')
    return_on_equity = Column(Float, comment='ROE（自己資本利益率）')
    profit_margins = Column(Float, comment='純利益率')
    gross_margins = Column(Float, comment='売上総利益率')
    ebitda_margins = Column(Float, comment='EBITDA利益率')
    operating_margins = Column(Float, comment='営業利益率')
    
    # 成長率
    earnings_growth = Column(Float, comment='利益成長率')
    revenue_growth = Column(Float, comment='売上成長率')
    earnings_quarterly_growth = Column(Float, comment='四半期利益成長率')
    
    # EPS関連
    trailing_eps = Column(Float, comment='実績EPS')
    forward_eps = Column(Float, comment='予想EPS')
    eps_trailing_twelve_months = Column(Float, comment='過去12ヶ月EPS')
    eps_forward = Column(Float, comment='フォワードEPS')
    
    # アナリスト予想
    target_high_price = Column(Float, comment='目標株価上限')
    target_low_price = Column(Float, comment='目標株価下限')
    target_mean_price = Column(Float, comment='目標株価平均')
    target_median_price = Column(Float, comment='目標株価中央値')
    recommendation_mean = Column(Float, comment='推奨平均')
    recommendation_key = Column(String(20), comment='推奨キー')
    number_of_analyst_opinions = Column(Integer, comment='アナリスト意見数')
    average_analyst_rating = Column(String(50), comment='アナリスト平均評価')
    
    # 取引所・市場情報
    exchange = Column(String(50), comment='取引所')
    full_exchange_name = Column(String(100), comment='取引所正式名称')
    market = Column(String(50), comment='市場')
    market_state = Column(String(20), comment='市場状態')
    quote_type = Column(String(20), comment='商品タイプ')
    tradeable = Column(String(10), comment='取引可能フラグ')
    
    # 時間・地域情報
    exchange_timezone_name = Column(String(50), comment='取引所タイムゾーン名')
    exchange_timezone_short_name = Column(String(10), comment='取引所タイムゾーン略称')
    gmt_off_set_milliseconds = Column(Float, comment='GMT オフセット（ミリ秒）')
    regular_market_time = Column(String(24), comment='通常市場時間')
    
    # リスク指標
    audit_risk = Column(Integer, comment='監査リスク')
    board_risk = Column(Integer, comment='取締役会リスク')
    compensation_risk = Column(Integer, comment='報酬リスク')
    shareholder_rights_risk = Column(Integer, comment='株主権リスク')
    overall_risk = Column(Integer, comment='総合リスク')
    
    # 決算関連
    last_fiscal_year_end = Column(String(24), comment='前会計年度末')
    next_fiscal_year_end = Column(String(24), comment='次会計年度末')
    most_recent_quarter = Column(String(24), comment='最新四半期')
    earnings_timestamp = Column(String(24), comment='決算発表タイムスタンプ')
    earnings_timestamp_start = Column(String(24), comment='決算発表開始時刻')
    earnings_timestamp_end = Column(String(24), comment='決算発表終了時刻')
    is_earnings_date_estimate = Column(String(10), comment='決算日推定フラグ')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    def __repr__(self):
        return f"<StockInfo(symbol='{self.symbol}', long_name='{self.long_name}')>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'long_name': self.long_name,
            'short_name': self.short_name,
            'address1': self.address1,
            'address2': self.address2,
            'city': self.city,
            'zip_code': self.zip_code,
            'country': self.country,
            'phone': self.phone,
            'website': self.website,
            'ir_website': self.ir_website,
            'industry': self.industry,
            'industry_key': self.industry_key,
            'industry_disp': self.industry_disp,
            'sector': self.sector,
            'sector_key': self.sector_key,
            'sector_disp': self.sector_disp,
            'long_business_summary': self.long_business_summary,
            'full_time_employees': self.full_time_employees,
            'currency': self.currency,
            'current_price': self.current_price,
            'previous_close': self.previous_close,
            'open_price': self.open_price,
            'day_low': self.day_low,
            'day_high': self.day_high,
            'regular_market_previous_close': self.regular_market_previous_close,
            'regular_market_open': self.regular_market_open,
            'regular_market_day_low': self.regular_market_day_low,
            'regular_market_day_high': self.regular_market_day_high,
            'regular_market_price': self.regular_market_price,
            'regular_market_change': self.regular_market_change,
            'regular_market_change_percent': self.regular_market_change_percent,
            'fifty_two_week_low': self.fifty_two_week_low,
            'fifty_two_week_high': self.fifty_two_week_high,
            'fifty_two_week_change': self.fifty_two_week_change,
            'fifty_two_week_change_percent': self.fifty_two_week_change_percent,
            'all_time_high': self.all_time_high,
            'all_time_low': self.all_time_low,
            'fifty_day_average': self.fifty_day_average,
            'fifty_day_average_change': self.fifty_day_average_change,
            'fifty_day_average_change_percent': self.fifty_day_average_change_percent,
            'two_hundred_day_average': self.two_hundred_day_average,
            'two_hundred_day_average_change': self.two_hundred_day_average_change,
            'two_hundred_day_average_change_percent': self.two_hundred_day_average_change_percent,
            'volume': self.volume,
            'regular_market_volume': self.regular_market_volume,
            'average_volume': self.average_volume,
            'average_volume_10days': self.average_volume_10days,
            'average_daily_volume_10day': self.average_daily_volume_10day,
            'average_daily_volume_3month': self.average_daily_volume_3month,
            'bid': self.bid,
            'ask': self.ask,
            'bid_size': self.bid_size,
            'ask_size': self.ask_size,
            'dividend_rate': self.dividend_rate,
            'dividend_yield': self.dividend_yield,
            'ex_dividend_date': self.ex_dividend_date.isoformat() if self.ex_dividend_date is not None else None,
            'payout_ratio': self.payout_ratio,
            'five_year_avg_dividend_yield': self.five_year_avg_dividend_yield,
            'trailing_annual_dividend_rate': self.trailing_annual_dividend_rate,
            'trailing_annual_dividend_yield': self.trailing_annual_dividend_yield,
            'last_dividend_value': self.last_dividend_value,
            'last_dividend_date': self.last_dividend_date.isoformat() if self.last_dividend_date is not None else None,
            'last_split_factor': self.last_split_factor,
            'last_split_date': self.last_split_date.isoformat() if self.last_split_date is not None else None,
            'market_cap': self.market_cap,
            'enterprise_value': self.enterprise_value,
            'shares_outstanding': self.shares_outstanding,
            'float_shares': self.float_shares,
            'implied_shares_outstanding': self.implied_shares_outstanding,
            'held_percent_insiders': self.held_percent_insiders,
            'held_percent_institutions': self.held_percent_institutions,
            'beta': self.beta,
            'trailing_pe': self.trailing_pe,
            'forward_pe': self.forward_pe,
            'price_to_book': self.price_to_book,
            'price_to_sales_trailing_12months': self.price_to_sales_trailing_12months,
            'enterprise_to_revenue': self.enterprise_to_revenue,
            'enterprise_to_ebitda': self.enterprise_to_ebitda,
            'trailing_peg_ratio': self.trailing_peg_ratio,
            'total_cash': self.total_cash,
            'total_cash_per_share': self.total_cash_per_share,
            'total_debt': self.total_debt,
            'total_revenue': self.total_revenue,
            'revenue_per_share': self.revenue_per_share,
            'ebitda': self.ebitda,
            'gross_profits': self.gross_profits,
            'net_income_to_common': self.net_income_to_common,
            'book_value': self.book_value,
            'quick_ratio': self.quick_ratio,
            'current_ratio': self.current_ratio,
            'return_on_assets': self.return_on_assets,
            'return_on_equity': self.return_on_equity,
            'profit_margins': self.profit_margins,
            'gross_margins': self.gross_margins,
            'ebitda_margins': self.ebitda_margins,
            'operating_margins': self.operating_margins,
            'earnings_growth': self.earnings_growth,
            'revenue_growth': self.revenue_growth,
            'earnings_quarterly_growth': self.earnings_quarterly_growth,
            'trailing_eps': self.trailing_eps,
            'forward_eps': self.forward_eps,
            'eps_trailing_twelve_months': self.eps_trailing_twelve_months,
            'eps_forward': self.eps_forward,
            'target_high_price': self.target_high_price,
            'target_low_price': self.target_low_price,
            'target_mean_price': self.target_mean_price,
            'target_median_price': self.target_median_price,
            'recommendation_mean': self.recommendation_mean,
            'recommendation_key': self.recommendation_key,
            'number_of_analyst_opinions': self.number_of_analyst_opinions,
            'average_analyst_rating': self.average_analyst_rating,
            'exchange': self.exchange,
            'full_exchange_name': self.full_exchange_name,
            'market': self.market,
            'market_state': self.market_state,
            'quote_type': self.quote_type,
            'tradeable': self.tradeable,
            'exchange_timezone_name': self.exchange_timezone_name,
            'exchange_timezone_short_name': self.exchange_timezone_short_name,
            'gmt_off_set_milliseconds': self.gmt_off_set_milliseconds,
            'regular_market_time': self.regular_market_time.isoformat() if self.regular_market_time is not None else None,
            'audit_risk': self.audit_risk,
            'board_risk': self.board_risk,
            'compensation_risk': self.compensation_risk,
            'shareholder_rights_risk': self.shareholder_rights_risk,
            'overall_risk': self.overall_risk,
            'last_fiscal_year_end': self.last_fiscal_year_end.isoformat() if self.last_fiscal_year_end is not None else None,
            'next_fiscal_year_end': self.next_fiscal_year_end.isoformat() if self.next_fiscal_year_end is not None else None,
            'most_recent_quarter': self.most_recent_quarter.isoformat() if self.most_recent_quarter is not None else None,
            'earnings_timestamp': self.earnings_timestamp.isoformat() if self.earnings_timestamp is not None else None,
            'earnings_timestamp_start': self.earnings_timestamp_start.isoformat() if self.earnings_timestamp_start is not None else None,
            'earnings_timestamp_end': self.earnings_timestamp_end.isoformat() if self.earnings_timestamp_end is not None else None,
            'is_earnings_date_estimate': self.is_earnings_date_estimate,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class Actions(Base):
    """
    株式の配当（Dividends）と株式分割（Stock Splits）の履歴を格納するテーブル
    """
    __tablename__ = 'actions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    date = Column(String(24), nullable=False, index=True)
    dividends = Column(Float, default=0.0, comment='配当額')
    stock_splits = Column(Float, default=0.0, comment='株式分割比率')
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="actions")
    
    def __repr__(self):
        return f"<Actions(date='{self.date}', dividends={self.dividends}, splits={self.stock_splits})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'dividends': self.dividends,
            'stock_splits': self.stock_splits,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class Balancesheet(Base):
    """
    企業の貸借対照表データを格納するテーブル
    """
    __tablename__ = 'balancesheets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    date = Column(String(24), nullable=False, index=True)
    period_type = Column(String(20), nullable=False, default='annual', comment='annual, quarterly')
    
    # 資産項目 (Assets)
    total_assets = Column(Float, comment='総資産')
    current_assets = Column(Float, comment='流動資産')
    non_current_assets = Column(Float, comment='固定資産')
    cash_and_cash_equivalents = Column(Float, comment='現金および現金同等物')
    other_short_term_investments = Column(Float, comment='その他短期投資')
    cash_cash_equivalents_and_short_term_investments = Column(Float, comment='現金・現金同等物・短期投資')
    accounts_receivable = Column(Float, comment='売掛金')
    gross_accounts_receivable = Column(Float, comment='売掛金総額')
    inventory = Column(Float, comment='棚卸資産')
    other_current_assets = Column(Float, comment='その他流動資産')
    net_ppe = Column(Float, comment='有形固定資産純額')
    gross_ppe = Column(Float, comment='有形固定資産総額')
    land_and_improvements = Column(Float, comment='土地および改良')
    buildings_and_improvements = Column(Float, comment='建物および改良')
    machinery_furniture_equipment = Column(Float, comment='機械・家具・設備')
    construction_in_progress = Column(Float, comment='建設仮勘定')
    properties = Column(Float, comment='不動産')
    goodwill_and_other_intangible_assets = Column(Float, comment='のれんおよびその他無形資産')
    other_intangible_assets = Column(Float, comment='その他無形資産')
    investment_in_financial_assets = Column(Float, comment='金融資産投資')
    available_for_sale_securities = Column(Float, comment='売却可能有価証券')
    non_current_deferred_taxes_assets = Column(Float, comment='固定繰延税金資産')
    defined_pension_benefit = Column(Float, comment='確定給付年金')
    other_non_current_assets = Column(Float, comment='その他固定資産')
    
    # 負債項目 (Liabilities)
    total_liabilities_net_minority_interest = Column(Float, comment='総負債（少数株主持分除く）')
    current_liabilities = Column(Float, comment='流動負債')
    total_non_current_liabilities_net_minority_interest = Column(Float, comment='固定負債合計（少数株主持分除く）')
    accounts_payable = Column(Float, comment='買掛金')
    total_tax_payable = Column(Float, comment='未払税金')
    payables = Column(Float, comment='債務')
    pension_and_other_post_retirement_benefit_plans_current = Column(Float, comment='年金・退職後給付制度（流動）')
    other_current_liabilities = Column(Float, comment='その他流動負債')
    long_term_provisions = Column(Float, comment='長期引当金')
    non_current_pension_and_other_postretirement_benefit_plans = Column(Float, comment='年金・退職後給付制度（固定）')
    other_non_current_liabilities = Column(Float, comment='その他固定負債')
    
    # 株主資本項目 (Equity)
    stockholders_equity = Column(Float, comment='株主資本')
    minority_interest = Column(Float, comment='少数株主持分')
    total_equity_gross_minority_interest = Column(Float, comment='総資本（少数株主持分含む）')
    total_capitalization = Column(Float, comment='総資本')
    common_stock_equity = Column(Float, comment='普通株主資本')
    net_tangible_assets = Column(Float, comment='純有形資産')
    working_capital = Column(Float, comment='運転資本')
    invested_capital = Column(Float, comment='投下資本')
    tangible_book_value = Column(Float, comment='有形簿価')
    
    # 株式関連項目
    share_issued = Column(Float, comment='発行済株式数')
    ordinary_shares_number = Column(Float, comment='普通株式数')
    treasury_shares_number = Column(Float, comment='自己株式数')
    common_stock = Column(Float, comment='普通株式')
    capital_stock = Column(Float, comment='資本金')
    additional_paid_in_capital = Column(Float, comment='資本剰余金')
    retained_earnings = Column(Float, comment='利益剰余金')
    treasury_stock = Column(Float, comment='自己株式')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="balancesheets")
    
    def __repr__(self):
        return f"<BalanceSheet(date='{self.date}', period='{self.period_type}', total_assets={self.total_assets})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'period_type': self.period_type,
            'total_assets': self.total_assets,
            'current_assets': self.current_assets,
            'non_current_assets': self.non_current_assets,
            'cash_and_cash_equivalents': self.cash_and_cash_equivalents,
            'other_short_term_investments': self.other_short_term_investments,
            'cash_cash_equivalents_and_short_term_investments': self.cash_cash_equivalents_and_short_term_investments,
            'accounts_receivable': self.accounts_receivable,
            'gross_accounts_receivable': self.gross_accounts_receivable,
            'inventory': self.inventory,
            'other_current_assets': self.other_current_assets,
            'net_ppe': self.net_ppe,
            'gross_ppe': self.gross_ppe,
            'land_and_improvements': self.land_and_improvements,
            'buildings_and_improvements': self.buildings_and_improvements,
            'machinery_furniture_equipment': self.machinery_furniture_equipment,
            'construction_in_progress': self.construction_in_progress,
            'properties': self.properties,
            'goodwill_and_other_intangible_assets': self.goodwill_and_other_intangible_assets,
            'other_intangible_assets': self.other_intangible_assets,
            'investment_in_financial_assets': self.investment_in_financial_assets,
            'available_for_sale_securities': self.available_for_sale_securities,
            'non_current_deferred_taxes_assets': self.non_current_deferred_taxes_assets,
            'defined_pension_benefit': self.defined_pension_benefit,
            'other_non_current_assets': self.other_non_current_assets,
            'total_liabilities_net_minority_interest': self.total_liabilities_net_minority_interest,
            'current_liabilities': self.current_liabilities,
            'total_non_current_liabilities_net_minority_interest': self.total_non_current_liabilities_net_minority_interest,
            'accounts_payable': self.accounts_payable,
            'total_tax_payable': self.total_tax_payable,
            'payables': self.payables,
            'pension_and_other_post_retirement_benefit_plans_current': self.pension_and_other_post_retirement_benefit_plans_current,
            'other_current_liabilities': self.other_current_liabilities,
            'long_term_provisions': self.long_term_provisions,
            'non_current_pension_and_other_postretirement_benefit_plans': self.non_current_pension_and_other_postretirement_benefit_plans,
            'other_non_current_liabilities': self.other_non_current_liabilities,
            'stockholders_equity': self.stockholders_equity,
            'minority_interest': self.minority_interest,
            'total_equity_gross_minority_interest': self.total_equity_gross_minority_interest,
            'total_capitalization': self.total_capitalization,
            'common_stock_equity': self.common_stock_equity,
            'net_tangible_assets': self.net_tangible_assets,
            'working_capital': self.working_capital,
            'invested_capital': self.invested_capital,
            'tangible_book_value': self.tangible_book_value,
            'share_issued': self.share_issued,
            'ordinary_shares_number': self.ordinary_shares_number,
            'treasury_shares_number': self.treasury_shares_number,
            'common_stock': self.common_stock,
            'capital_stock': self.capital_stock,
            'additional_paid_in_capital': self.additional_paid_in_capital,
            'retained_earnings': self.retained_earnings,
            'treasury_stock': self.treasury_stock,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class Calendar(Base):
    """
    株式の財務カレンダー情報を格納するテーブル
    配当落ち日、決算発表日、収益予測等の重要な日程と予測値を管理
    """
    __tablename__ = 'calendars'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    
    # 重要な日程
    ex_dividend_date = Column(String(24), comment='配当落ち日')
    earnings_date = Column(String(24), comment='決算発表日（主要日程）')
    
    # 収益予測（Earnings）
    earnings_high = Column(Float, comment='収益予測上限')
    earnings_low = Column(Float, comment='収益予測下限')
    earnings_average = Column(Float, comment='収益予測平均')
    
    # 売上予測（Revenue）
    revenue_high = Column(Float, comment='売上予測上限')
    revenue_low = Column(Float, comment='売上予測下限')
    revenue_average = Column(Float, comment='売上予測平均')
    
    # その他の重要な日程
    dividend_payment_date = Column(String(24), comment='配当支払日')
    annual_general_meeting_date = Column(String(24), comment='株主総会日')
    fiscal_year_end = Column(String(24), comment='会計年度末')
    
    # メタデータ
    data_source = Column(String(50), default='yfinance', comment='データソース')
    last_updated = Column(String(24), comment='データ最終更新日')
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="calendars")
    
    def __repr__(self):
        return f"<Calendar(ex_dividend='{self.ex_dividend_date}', earnings='{self.earnings_date}')>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'ex_dividend_date': self.ex_dividend_date.isoformat() if self.ex_dividend_date is not None else None,
            'earnings_date': self.earnings_date.isoformat() if self.earnings_date is not None else None,
            'earnings_high': self.earnings_high,
            'earnings_low': self.earnings_low,
            'earnings_average': self.earnings_average,
            'revenue_high': self.revenue_high,
            'revenue_low': self.revenue_low,
            'revenue_average': self.revenue_average,
            'dividend_payment_date': self.dividend_payment_date.isoformat() if self.dividend_payment_date is not None else None,
            'annual_general_meeting_date': self.annual_general_meeting_date.isoformat() if self.annual_general_meeting_date is not None else None,
            'fiscal_year_end': self.fiscal_year_end.isoformat() if self.fiscal_year_end is not None else None,
            'data_source': self.data_source,
            'last_updated': self.last_updated.isoformat() if self.last_updated is not None else None,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class CashFlow(Base):
    """
    企業のキャッシュフロー計算書データを格納するテーブル
    営業、投資、財務の3つの主要なキャッシュフロー活動を管理
    """
    __tablename__ = 'cash_flows'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    date = Column(String(24), nullable=False, index=True)
    period_type = Column(String(20), nullable=False, default='annual', comment='annual, quarterly, ttm')
    
    # 主要なキャッシュフロー指標
    operating_cash_flow = Column(Float, comment='営業キャッシュフロー')
    investing_cash_flow = Column(Float, comment='投資キャッシュフロー')
    financing_cash_flow = Column(Float, comment='財務キャッシュフロー')
    free_cash_flow = Column(Float, comment='フリーキャッシュフロー')
    
    # キャッシュポジション
    beginning_cash_position = Column(Float, comment='期首現金残高')
    end_cash_position = Column(Float, comment='期末現金残高')
    changes_in_cash = Column(Float, comment='現金の変動')
    
    # 営業キャッシュフロー詳細
    net_income_from_continuing_operations = Column(Float, comment='継続事業からの純利益')
    depreciation_and_amortization = Column(Float, comment='減価償却費')
    depreciation = Column(Float, comment='減価償却費（個別）')
    net_foreign_currency_exchange_gain_loss = Column(Float, comment='外国為替差損益（純額）')
    gain_loss_on_investment_securities = Column(Float, comment='投資有価証券損益')
    other_non_cash_items = Column(Float, comment='その他非現金項目')
    
    # 運転資本の変動
    change_in_working_capital = Column(Float, comment='運転資本の変動')
    change_in_receivables = Column(Float, comment='売掛金の変動')
    change_in_inventory = Column(Float, comment='棚卸資産の変動')
    change_in_payable = Column(Float, comment='買掛金の変動')
    change_in_other_current_assets = Column(Float, comment='その他流動資産の変動')
    change_in_other_current_liabilities = Column(Float, comment='その他流動負債の変動')
    
    # 利息・税金
    interest_paid_cfo = Column(Float, comment='支払利息（営業CF）')
    interest_received_cfo = Column(Float, comment='受取利息（営業CF）')
    taxes_refund_paid = Column(Float, comment='税金の支払・還付')
    
    # 投資キャッシュフロー詳細
    capital_expenditure = Column(Float, comment='設備投資')
    purchase_of_ppe = Column(Float, comment='有形固定資産の取得')
    sale_of_ppe = Column(Float, comment='有形固定資産の売却')
    net_ppe_purchase_and_sale = Column(Float, comment='有形固定資産の取得・売却（純額）')
    capital_expenditure_reported = Column(Float, comment='報告設備投資')
    
    # 投資活動
    purchase_of_investment = Column(Float, comment='投資の取得')
    sale_of_investment = Column(Float, comment='投資の売却')
    net_investment_purchase_and_sale = Column(Float, comment='投資の取得・売却（純額）')
    net_other_investing_changes = Column(Float, comment='その他投資活動の変動')
    
    # 財務キャッシュフロー詳細
    cash_dividends_paid = Column(Float, comment='配当金の支払')
    common_stock_dividend_paid = Column(Float, comment='普通株式配当金の支払')
    net_common_stock_issuance = Column(Float, comment='普通株式の発行（純額）')
    common_stock_payments = Column(Float, comment='普通株式の支払')
    repurchase_of_capital_stock = Column(Float, comment='自己株式の取得')
    net_other_financing_charges = Column(Float, comment='その他財務活動費用')
    
    # その他の調整
    effect_of_exchange_rate_changes = Column(Float, comment='為替レート変動の影響')
    other_cash_adjustment_outside_change_in_cash = Column(Float, comment='現金変動外のその他調整')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="cash_flows")
    
    def __repr__(self):
        return f"<CashFlow(date='{self.date}', period='{self.period_type}', operating_cf={self.operating_cash_flow})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'period_type': self.period_type,
            'operating_cash_flow': self.operating_cash_flow,
            'investing_cash_flow': self.investing_cash_flow,
            'financing_cash_flow': self.financing_cash_flow,
            'free_cash_flow': self.free_cash_flow,
            'beginning_cash_position': self.beginning_cash_position,
            'end_cash_position': self.end_cash_position,
            'changes_in_cash': self.changes_in_cash,
            'net_income_from_continuing_operations': self.net_income_from_continuing_operations,
            'depreciation_and_amortization': self.depreciation_and_amortization,
            'depreciation': self.depreciation,
            'net_foreign_currency_exchange_gain_loss': self.net_foreign_currency_exchange_gain_loss,
            'gain_loss_on_investment_securities': self.gain_loss_on_investment_securities,
            'other_non_cash_items': self.other_non_cash_items,
            'change_in_working_capital': self.change_in_working_capital,
            'change_in_receivables': self.change_in_receivables,
            'change_in_inventory': self.change_in_inventory,
            'change_in_payable': self.change_in_payable,
            'change_in_other_current_assets': self.change_in_other_current_assets,
            'change_in_other_current_liabilities': self.change_in_other_current_liabilities,
            'interest_paid_cfo': self.interest_paid_cfo,
            'interest_received_cfo': self.interest_received_cfo,
            'taxes_refund_paid': self.taxes_refund_paid,
            'capital_expenditure': self.capital_expenditure,
            'purchase_of_ppe': self.purchase_of_ppe,
            'sale_of_ppe': self.sale_of_ppe,
            'net_ppe_purchase_and_sale': self.net_ppe_purchase_and_sale,
            'capital_expenditure_reported': self.capital_expenditure_reported,
            'purchase_of_investment': self.purchase_of_investment,
            'sale_of_investment': self.sale_of_investment,
            'net_investment_purchase_and_sale': self.net_investment_purchase_and_sale,
            'net_other_investing_changes': self.net_other_investing_changes,
            'cash_dividends_paid': self.cash_dividends_paid,
            'common_stock_dividend_paid': self.common_stock_dividend_paid,
            'net_common_stock_issuance': self.net_common_stock_issuance,
            'common_stock_payments': self.common_stock_payments,
            'repurchase_of_capital_stock': self.repurchase_of_capital_stock,
            'net_other_financing_charges': self.net_other_financing_charges,
            'effect_of_exchange_rate_changes': self.effect_of_exchange_rate_changes,
            'other_cash_adjustment_outside_change_in_cash': self.other_cash_adjustment_outside_change_in_cash,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class Dividends(Base):
    """
    株式の配当履歴を格納するテーブル
    サンプルデータに合わせたシンプルな構造（日付と配当額のみ）
    """
    __tablename__ = 'dividends'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    date = Column(String(24), nullable=False, index=True, comment='配当日')
    dividends = Column(Float, nullable=False, comment='配当金額（1株あたり）')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="dividends")
    
    def __repr__(self):
        return f"<Dividends(date='{self.date}', dividends={self.dividends})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'dividends': self.dividends,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class EarningsDates(Base):
    """
    決算発表日と収益データを格納するテーブル
    決算発表日ごとの予想EPS、実績EPS、サプライズ率を管理
    """
    __tablename__ = 'earnings_dates'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    date = Column(String(24), nullable=False, index=True, comment='決算発表日')
    
    # EPS関連データ
    eps_estimate = Column(Float, comment='予想EPS（1株あたり利益予想）')
    reported_eps = Column(Float, comment='実績EPS（1株あたり利益実績）')
    surprise_percent = Column(Float, comment='サプライズ率（%）実績が予想をどの程度上回った/下回ったかの割合')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="earnings_dates")
    
    def __repr__(self):
        return f"<EarningsDates(date='{self.date}', estimate={self.eps_estimate}, reported={self.reported_eps})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'eps_estimate': self.eps_estimate,
            'reported_eps': self.reported_eps,
            'surprise_percent': self.surprise_percent,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class EarningsEstimate(Base):
    """
    収益予想データを格納するテーブル
    四半期および年次の収益予想情報を管理
    """
    __tablename__ = 'earnings_estimates'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    year = Column(Integer, comment='今期')
    period_type = Column(String(10), nullable=False, index=True, comment='期間タイプ（0q, +1q, 0y, +1yなど）')
    
    # 収益予想データ
    avg_estimate = Column(Float, comment='平均予想EPS')
    low_estimate = Column(Float, comment='最低予想EPS')
    high_estimate = Column(Float, comment='最高予想EPS')
    year_ago_eps = Column(Float, comment='前年同期EPS')
    number_of_analysts = Column(Integer, comment='アナリスト数')
    growth_rate = Column(Float, comment='成長率')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="earnings_estimates")
    
    def __repr__(self):
        return f"<EarningsEstimate(year={self.year}, period='{self.period_type}')>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'year': self.year,
            'period_type': self.period_type,
            'avg_estimate': self.avg_estimate,
            'low_estimate': self.low_estimate,
            'high_estimate': self.high_estimate,
            'year_ago_eps': self.year_ago_eps,
            'number_of_analysts': self.number_of_analysts,
            'growth_rate': self.growth_rate,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class EarningsHistory(Base):
    """
    過去の収益実績データを格納するテーブル
    実績EPS、予想EPS、差額、サプライズ率を管理
    """
    __tablename__ = 'earnings_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    date = Column(String(24), nullable=False, index=True, comment='四半期末日')
    
    # 収益実績データ
    eps_actual = Column(Float, comment='実績EPS')
    eps_estimate = Column(Float, comment='予想EPS')
    eps_difference = Column(Float, comment='EPS差額（実績-予想）')
    surprise_percent = Column(Float, comment='サプライズ率')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="earnings_history")
    
    def __repr__(self):
        return f"<EarningsHistory(date='{self.date}', actual={self.eps_actual})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'eps_actual': self.eps_actual,
            'eps_estimate': self.eps_estimate,
            'eps_difference': self.eps_difference,
            'surprise_percent': self.surprise_percent,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class EpsRevisions(Base):
    """
    EPS予想の修正履歴データを格納するテーブル
    期間別のアナリスト予想修正状況を管理
    """
    __tablename__ = 'eps_revisions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    year = Column(Integer, comment='今期')
    period_type = Column(String(10), nullable=False, index=True, comment='期間タイプ（0q, +1q, 0y, +1yなど）')
    
    # 修正履歴データ
    up_last_7days = Column(Integer, default=0, comment='過去7日間の上方修正数')
    up_last_30days = Column(Integer, default=0, comment='過去30日間の上方修正数')
    down_last_7days = Column(Integer, default=0, comment='過去7日間の下方修正数')
    down_last_30days = Column(Integer, default=0, comment='過去30日間の下方修正数')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="eps_revisions")
    
    def __repr__(self):
        return f"<EpsRevisions(year={self.year}, period='{self.period_type}')>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'year': self.year,
            'period_type': self.period_type,
            'up_last_7days': self.up_last_7days,
            'up_last_30days': self.up_last_30days,
            'down_last_7days': self.down_last_7days,
            'down_last_30days': self.down_last_30days,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class EpsTrend(Base):
    """
    EPS予想のトレンドデータを格納するテーブル
    期間別の予想EPSの時系列変化を管理
    """
    __tablename__ = 'eps_trends'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    year = Column(Integer, comment='今期')
    period_type = Column(String(10), nullable=False, index=True, comment='期間タイプ（0q, +1q, 0y, +1yなど）')
    
    # トレンドデータ
    current = Column(Float, comment='現在の予想EPS')
    days_ago_7 = Column(Float, comment='7日前の予想EPS')
    days_ago_30 = Column(Float, comment='30日前の予想EPS')
    days_ago_60 = Column(Float, comment='60日前の予想EPS')
    days_ago_90 = Column(Float, comment='90日前の予想EPS')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="eps_trends")
    
    def __repr__(self):
        return f"<EpsTrend(year={self.year}, period='{self.period_type}')>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'year': self.year,
            'period_type': self.period_type,
            'current': self.current,
            'days_ago_7': self.days_ago_7,
            'days_ago_30': self.days_ago_30,
            'days_ago_60': self.days_ago_60,
            'days_ago_90': self.days_ago_90,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class FastInfo(Base):
    """
    株式の高速取得可能な基本情報を格納するテーブル
    リアルタイムに近い価格、出来高、移動平均などの重要指標を管理
    """
    __tablename__ = 'fast_info'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    
    # 基本情報
    currency = Column(String(10), comment='通貨')
    exchange = Column(String(50), comment='取引所')
    quote_type = Column(String(50), comment='商品タイプ')
    timezone = Column(String(50), comment='タイムゾーン')
    
    # 価格情報
    last_price = Column(Float, comment='最新価格')
    open_price = Column(Float, comment='始値')
    previous_close = Column(Float, comment='前日終値')
    regular_market_previous_close = Column(Float, comment='通常市場前日終値')
    day_high = Column(Float, comment='日中高値')
    day_low = Column(Float, comment='日中安値')
    year_high = Column(Float, comment='52週高値')
    year_low = Column(Float, comment='52週安値')
    year_change = Column(Float, comment='年初来変動率')
    
    # 出来高・移動平均情報
    last_volume = Column(Float, comment='最新出来高')
    ten_day_average_volume = Column(Float, comment='10日平均出来高')
    three_month_average_volume = Column(Float, comment='3ヶ月平均出来高')
    fifty_day_average = Column(Float, comment='50日移動平均')
    two_hundred_day_average = Column(Float, comment='200日移動平均')
    
    # 企業規模情報
    market_cap = Column(Float, comment='時価総額')
    shares = Column(Float, comment='発行済株式数')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="fast_info")
    
    def __repr__(self):
        return f"<FastInfo(last_price={self.last_price}, currency='{self.currency}')>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'currency': self.currency,
            'exchange': self.exchange,
            'quote_type': self.quote_type,
            'timezone': self.timezone,
            'last_price': self.last_price,
            'open_price': self.open_price,
            'previous_close': self.previous_close,
            'regular_market_previous_close': self.regular_market_previous_close,
            'day_high': self.day_high,
            'day_low': self.day_low,
            'year_high': self.year_high,
            'year_low': self.year_low,
            'year_change': self.year_change,
            'last_volume': self.last_volume,
            'ten_day_average_volume': self.ten_day_average_volume,
            'three_month_average_volume': self.three_month_average_volume,
            'fifty_day_average': self.fifty_day_average,
            'two_hundred_day_average': self.two_hundred_day_average,
            'market_cap': self.market_cap,
            'shares': self.shares,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class Financials(Base):
    """
    企業の財務諸表データを格納するテーブル
    損益計算書の主要項目を管理
    """
    __tablename__ = 'financials'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    date = Column(String(24), nullable=False, index=True, comment='財務年度末日')
    period_type = Column(String(20), nullable=False, default='annual', comment='annual, quarterly, ttm')
    
    # 売上・費用項目
    total_revenue = Column(Float, comment='総売上高')
    operating_revenue = Column(Float, comment='営業売上高')
    cost_of_revenue = Column(Float, comment='売上原価')
    gross_profit = Column(Float, comment='売上総利益')
    operating_expense = Column(Float, comment='営業費用')
    operating_income = Column(Float, comment='営業利益')
    total_expenses = Column(Float, comment='総費用')
    
    # 利益・損失項目
    ebit = Column(Float, comment='EBIT（利息・税引前利益）')
    ebitda = Column(Float, comment='EBITDA（利息・税・償却前利益）')
    normalized_ebitda = Column(Float, comment='正規化EBITDA')
    pretax_income = Column(Float, comment='税引前当期利益')
    tax_provision = Column(Float, comment='税金費用')
    net_income = Column(Float, comment='純利益')
    net_income_common_stockholders = Column(Float, comment='普通株主に帰属する純利益')
    net_income_continuous_operations = Column(Float, comment='継続事業からの純利益')
    normalized_income = Column(Float, comment='正規化純利益')
    
    # 金利・金融項目
    interest_income = Column(Float, comment='受取利息')
    interest_expense = Column(Float, comment='支払利息')
    net_interest_income = Column(Float, comment='純金利収益')
    interest_income_non_operating = Column(Float, comment='営業外受取利息')
    interest_expense_non_operating = Column(Float, comment='営業外支払利息')
    net_non_operating_interest_income_expense = Column(Float, comment='営業外純金利損益')
    
    # 特別項目
    other_non_operating_income_expenses = Column(Float, comment='その他営業外損益')
    special_income_charges = Column(Float, comment='特別損益')
    other_special_charges = Column(Float, comment='その他特別費用')
    total_unusual_items = Column(Float, comment='異常項目合計')
    total_unusual_items_excluding_goodwill = Column(Float, comment='のれん除く異常項目合計')
    tax_effect_of_unusual_items = Column(Float, comment='異常項目の税効果')
    tax_rate_for_calcs = Column(Float, comment='計算用税率')
    
    # 株式・EPS関連
    basic_average_shares = Column(Float, comment='基本平均株式数')
    diluted_average_shares = Column(Float, comment='希薄化後平均株式数')
    basic_eps = Column(Float, comment='基本1株当たり利益')
    diluted_eps = Column(Float, comment='希薄化後1株当たり利益')
    diluted_ni_availto_com_stockholders = Column(Float, comment='希薄化後普通株主利用可能純利益')
    
    # 少数株主・その他
    minority_interests = Column(Float, comment='少数株主持分損益')
    net_income_including_noncontrolling_interests = Column(Float, comment='非支配持分含む純利益')
    otherunder_preferred_stock_dividend = Column(Float, comment='優先株配当等')
    
    # 償却・調整項目
    reconciled_depreciation = Column(Float, comment='調整後償却費')
    reconciled_cost_of_revenue = Column(Float, comment='調整後売上原価')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="financials")
    
    def __repr__(self):
        return f"<Financials(date='{self.date}', period='{self.period_type}', revenue={self.total_revenue})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'period_type': self.period_type,
            'total_revenue': self.total_revenue,
            'operating_revenue': self.operating_revenue,
            'cost_of_revenue': self.cost_of_revenue,
            'gross_profit': self.gross_profit,
            'operating_expense': self.operating_expense,
            'operating_income': self.operating_income,
            'total_expenses': self.total_expenses,
            'ebit': self.ebit,
            'ebitda': self.ebitda,
            'normalized_ebitda': self.normalized_ebitda,
            'pretax_income': self.pretax_income,
            'tax_provision': self.tax_provision,
            'net_income': self.net_income,
            'net_income_common_stockholders': self.net_income_common_stockholders,
            'net_income_continuous_operations': self.net_income_continuous_operations,
            'normalized_income': self.normalized_income,
            'interest_income': self.interest_income,
            'interest_expense': self.interest_expense,
            'net_interest_income': self.net_interest_income,
            'interest_income_non_operating': self.interest_income_non_operating,
            'interest_expense_non_operating': self.interest_expense_non_operating,
            'net_non_operating_interest_income_expense': self.net_non_operating_interest_income_expense,
            'other_non_operating_income_expenses': self.other_non_operating_income_expenses,
            'special_income_charges': self.special_income_charges,
            'other_special_charges': self.other_special_charges,
            'total_unusual_items': self.total_unusual_items,
            'total_unusual_items_excluding_goodwill': self.total_unusual_items_excluding_goodwill,
            'tax_effect_of_unusual_items': self.tax_effect_of_unusual_items,
            'tax_rate_for_calcs': self.tax_rate_for_calcs,
            'basic_average_shares': self.basic_average_shares,
            'diluted_average_shares': self.diluted_average_shares,
            'basic_eps': self.basic_eps,
            'diluted_eps': self.diluted_eps,
            'diluted_ni_availto_com_stockholders': self.diluted_ni_availto_com_stockholders,
            'minority_interests': self.minority_interests,
            'net_income_including_noncontrolling_interests': self.net_income_including_noncontrolling_interests,
            'otherunder_preferred_stock_dividend': self.otherunder_preferred_stock_dividend,
            'reconciled_depreciation': self.reconciled_depreciation,
            'reconciled_cost_of_revenue': self.reconciled_cost_of_revenue,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class GrowthEstimate(Base):
    """
    成長予想データを格納するテーブル
    企業と業界指数の成長予想トレンドを管理
    """
    __tablename__ = 'growth_estimates'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    year = Column(Integer, comment='今期')
    period_type = Column(String(10), nullable=False, index=True, comment='期間タイプ（0q, +1q, 0y, +1y, LTGなど）')
    
    # 成長予想データ
    stock_trend = Column(Float, comment='企業の成長トレンド')
    index_trend = Column(Float, comment='業界指数の成長トレンド')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="growth_estimates")
    
    def __repr__(self):
        return f"<GrowthEstimate(year={self.year}, period='{self.period_type}', stock_trend={self.stock_trend})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'year': self.year,
            'period_type': self.period_type,
            'stock_trend': self.stock_trend,
            'index_trend': self.index_trend,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class History(Base):
    """
    株価履歴データを格納するテーブル
    日次の価格、出来高、配当、株式分割情報を管理
    """
    __tablename__ = 'history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    date = Column(String(24), nullable=False, index=True, comment='取引日')
    
    # 価格情報（OHLC）
    open = Column(Float, comment='始値')
    high = Column(Float, comment='高値')
    low = Column(Float, comment='安値')
    close = Column(Float, comment='終値')
    volume = Column(Float, comment='出来高')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="history")
    
    def __repr__(self):
        return f"<History(date='{self.date}')>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class History_1min(Base):
    """
    株価履歴データを格納するテーブル
    1分足の価格、出来高、配当、株式分割情報を管理
    """
    __tablename__ = 'history_1min'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    date = Column(String(24), nullable=False, index=True, comment='取引日')
    
    # 価格情報（OHLC）
    open = Column(Float, comment='始値')
    high = Column(Float, comment='高値')
    low = Column(Float, comment='安値')
    close = Column(Float, comment='終値')
    volume = Column(Float, comment='出来高')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="history_1min")
    
    def __repr__(self):
        return f"<History_1min(date='{self.date}')>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class IncomeStatement(Base):
    """
    損益計算書データを格納するテーブル
    企業の収益性と経営成績を詳細に管理
    """
    __tablename__ = 'income_statements'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    date = Column(String(24), nullable=False, index=True, comment='財務期間末日')
    
    # 売上・収益項目
    total_revenue = Column(Float, comment='総売上高')
    operating_revenue = Column(Float, comment='営業売上高')
    cost_of_revenue = Column(Float, comment='売上原価')
    reconciled_cost_of_revenue = Column(Float, comment='調整後売上原価')
    gross_profit = Column(Float, comment='売上総利益')
    
    # 営業関連項目
    operating_expense = Column(Float, comment='営業費用')
    operating_income = Column(Float, comment='営業利益')
    total_operating_income_as_reported = Column(Float, comment='報告営業利益')
    total_expenses = Column(Float, comment='総費用')
    
    # 利益指標
    ebit = Column(Float, comment='EBIT（利息・税引前利益）')
    ebitda = Column(Float, comment='EBITDA（利息・税・償却前利益）')
    normalized_ebitda = Column(Float, comment='正規化EBITDA')
    
    # 金利・金融項目
    interest_income = Column(Float, comment='受取利息')
    interest_expense = Column(Float, comment='支払利息')
    net_interest_income = Column(Float, comment='純金利収益')
    interest_income_non_operating = Column(Float, comment='営業外受取利息')
    interest_expense_non_operating = Column(Float, comment='営業外支払利息')
    net_non_operating_interest_income_expense = Column(Float, comment='営業外純金利損益')
    
    # その他収益・費用
    other_non_operating_income_expenses = Column(Float, comment='その他営業外損益')
    special_income_charges = Column(Float, comment='特別損益')
    other_special_charges = Column(Float, comment='その他特別費用')
    
    # 税引前・税引後利益
    pretax_income = Column(Float, comment='税引前当期利益')
    tax_provision = Column(Float, comment='税金費用')
    
    # 純利益関連
    net_income = Column(Float, comment='純利益')
    net_income_common_stockholders = Column(Float, comment='普通株主に帰属する純利益')
    net_income_continuous_operations = Column(Float, comment='継続事業からの純利益')
    net_income_from_continuing_operation_net_minority_interest = Column(Float, comment='継続事業純利益（少数株主持分調整後）')
    net_income_from_continuing_and_discontinued_operation = Column(Float, comment='継続・非継続事業純利益')
    net_income_including_noncontrolling_interests = Column(Float, comment='非支配持分含む純利益')
    normalized_income = Column(Float, comment='正規化純利益')
    
    # 特別項目・調整
    total_unusual_items = Column(Float, comment='異常項目合計')
    total_unusual_items_excluding_goodwill = Column(Float, comment='のれん除く異常項目合計')
    tax_effect_of_unusual_items = Column(Float, comment='異常項目の税効果')
    tax_rate_for_calcs = Column(Float, comment='計算用税率')
    reconciled_depreciation = Column(Float, comment='調整後償却費')
    
    # 株式・EPS関連
    basic_average_shares = Column(Float, comment='基本平均株式数')
    diluted_average_shares = Column(Float, comment='希薄化後平均株式数')
    basic_eps = Column(Float, comment='基本1株当たり利益')
    diluted_eps = Column(Float, comment='希薄化後1株当たり利益')
    diluted_ni_availto_com_stockholders = Column(Float, comment='希薄化後普通株主利用可能純利益')
    
    # 少数株主・その他
    minority_interests = Column(Float, comment='少数株主持分損益')
    otherunder_preferred_stock_dividend = Column(Float, comment='優先株配当等')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="income_statements")
    
    def __repr__(self):
        return f"<IncomeStatement(date='{self.date}', revenue={self.total_revenue})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'total_revenue': self.total_revenue,
            'operating_revenue': self.operating_revenue,
            'cost_of_revenue': self.cost_of_revenue,
            'reconciled_cost_of_revenue': self.reconciled_cost_of_revenue,
            'gross_profit': self.gross_profit,
            'operating_expense': self.operating_expense,
            'operating_income': self.operating_income,
            'total_operating_income_as_reported': self.total_operating_income_as_reported,
            'total_expenses': self.total_expenses,
            'ebit': self.ebit,
            'ebitda': self.ebitda,
            'normalized_ebitda': self.normalized_ebitda,
            'interest_income': self.interest_income,
            'interest_expense': self.interest_expense,
            'net_interest_income': self.net_interest_income,
            'interest_income_non_operating': self.interest_income_non_operating,
            'interest_expense_non_operating': self.interest_expense_non_operating,
            'net_non_operating_interest_income_expense': self.net_non_operating_interest_income_expense,
            'other_non_operating_income_expenses': self.other_non_operating_income_expenses,
            'special_income_charges': self.special_income_charges,
            'other_special_charges': self.other_special_charges,
            'pretax_income': self.pretax_income,
            'tax_provision': self.tax_provision,
            'net_income': self.net_income,
            'net_income_common_stockholders': self.net_income_common_stockholders,
            'net_income_continuous_operations': self.net_income_continuous_operations,
            'net_income_from_continuing_operation_net_minority_interest': self.net_income_from_continuing_operation_net_minority_interest,
            'net_income_from_continuing_and_discontinued_operation': self.net_income_from_continuing_and_discontinued_operation,
            'net_income_including_noncontrolling_interests': self.net_income_including_noncontrolling_interests,
            'normalized_income': self.normalized_income,
            'total_unusual_items': self.total_unusual_items,
            'total_unusual_items_excluding_goodwill': self.total_unusual_items_excluding_goodwill,
            'tax_effect_of_unusual_items': self.tax_effect_of_unusual_items,
            'tax_rate_for_calcs': self.tax_rate_for_calcs,
            'reconciled_depreciation': self.reconciled_depreciation,
            'basic_average_shares': self.basic_average_shares,
            'diluted_average_shares': self.diluted_average_shares,
            'basic_eps': self.basic_eps,
            'diluted_eps': self.diluted_eps,
            'diluted_ni_availto_com_stockholders': self.diluted_ni_availto_com_stockholders,
            'minority_interests': self.minority_interests,
            'otherunder_preferred_stock_dividend': self.otherunder_preferred_stock_dividend,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class InsiderPurchases(Base):
    """
    インサイダー取引情報を格納するテーブル
    過去6ヶ月のインサイダー取引項目別データを管理
    """
    __tablename__ = 'insider_purchases'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    
    # サンプルデータの3カラム構造に対応
    insider_purchases_last_6m = Column(String(100), nullable=False, comment='インサイダー取引項目名')
    shares = Column(Float, comment='株式数')
    trans = Column(Integer, comment='取引回数')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="insider_purchases")
    
    def __repr__(self):
        return f"<InsiderPurchases(item='{self.insider_purchases_last_6m}', shares={self.shares})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'insider_purchases_last_6m': self.insider_purchases_last_6m,
            'shares': self.shares,
            'trans': self.trans,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class InstitutionalHolders(Base):
    """
    機関投資家保有情報を格納するテーブル
    機関投資家の保有株式数、保有割合、投資金額等を管理
    """
    __tablename__ = 'institutional_holders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    
    # 機関投資家保有データ
    date = Column(String(24), nullable=False, index=True, comment='報告日')
    holder = Column(String(500), nullable=False, comment='機関投資家名')
    pct_held = Column(Float, comment='保有割合（%）')
    shares = Column(Float, comment='保有株式数')
    value = Column(Float, comment='保有株式価値（金額）')
    pct_change = Column(Float, comment='保有割合変動率（%）')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="institutional_holders")
    
    def __repr__(self):
        return f"<InstitutionalHolders(holder='{self.holder}', shares={self.shares})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'holder': self.holder,
            'pct_held': self.pct_held,
            'shares': self.shares,
            'value': self.value,
            'pct_change': self.pct_change,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class MajorHolders(Base):
    """
    主要株主情報を格納するテーブル
    インサイダーと機関投資家の保有比率サマリーを管理
    """
    __tablename__ = 'major_holders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    
    # 主要株主保有比率データ
    insiders_percent_held = Column(Float, comment='インサイダー保有比率')
    institutions_percent_held = Column(Float, comment='機関投資家保有比率')
    institutions_float_percent_held = Column(Float, comment='機関投資家流通株式保有比率')
    institutions_count = Column(Float, comment='機関投資家数')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="major_holders")
    
    def __repr__(self):
        return f"<MajorHolders(insiders={self.insiders_percent_held}, institutions={self.institutions_percent_held})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'insiders_percent_held': self.insiders_percent_held,
            'institutions_percent_held': self.institutions_percent_held,
            'institutions_float_percent_held': self.institutions_float_percent_held,
            'institutions_count': self.institutions_count,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class MutualfundHolders(Base):
    """
    投資信託保有情報を格納するテーブル
    投資信託の保有株式数、保有割合、投資金額等を管理
    """
    __tablename__ = 'mutualfund_holders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    
    # 投資信託保有データ
    date = Column(String(24), nullable=False, index=True, comment='報告日')
    holder = Column(String(500), nullable=False, comment='投資信託名')
    pct_held = Column(Float, comment='保有割合（%）')
    shares = Column(Float, comment='保有株式数')
    value = Column(Float, comment='保有株式価値（金額）')
    pct_change = Column(Float, comment='保有割合変動率（%）')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="mutualfund_holders")
    
    def __repr__(self):
        return f"<MutualfundHolders(holder='{self.holder}', shares={self.shares})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date is not None else None,
            'holder': self.holder,
            'pct_held': self.pct_held,
            'shares': self.shares,
            'value': self.value,
            'pct_change': self.pct_change,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class News(Base):
    """
    株式関連のニュース記事を格納するテーブル
    yfinanceから取得したニュースデータの主要情報を管理
    """
    __tablename__ = 'news'
    
    id = Column(String(50), primary_key=True, index=True, comment='ニュース記事固有ID')
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    
    # ニュース識別情報
    content_type = Column(String(20), default='STORY', comment='コンテンツタイプ（STORY, VIDEO等）')
    
    # 記事基本情報
    title = Column(String(1000), nullable=False, comment='記事タイトル')
    description = Column(Text, comment='記事説明')
    summary = Column(Text, comment='記事要約')
    
    # 公開・表示日時
    pub_date = Column(String(24), nullable=False, index=True, comment='公開日時')
    display_time = Column(String(24), comment='表示日時')
    
    # プロバイダー情報
    provider_name = Column(String(200), comment='配信元名称')
    provider_url = Column(String(500), comment='配信元URL')
    
    # URL情報
    canonical_url = Column(String(1000), comment='正規URL')
    click_through_url = Column(String(1000), comment='クリックスルーURL')
    preview_url = Column(String(1000), comment='プレビューURL')
    
    # 記事属性
    is_hosted = Column(String(10), default='false', comment='ホスト記事フラグ')
    bypass_modal = Column(String(10), default='false', comment='モーダルバイパスフラグ')
    editors_pick = Column(String(10), default='false', comment='編集者おすすめフラグ')
    
    # プレミアム記事情報
    is_premium_news = Column(String(10), default='false', comment='プレミアムニュースフラグ')
    is_premium_free_news = Column(String(10), default='false', comment='プレミアム無料ニュースフラグ')
    
    # 地域・言語情報
    site = Column(String(50), comment='サイト')
    region = Column(String(10), comment='地域')
    lang = Column(String(10), comment='言語')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="news")
    
    def __repr__(self):
        return f"<News(title='{self.title}', pub_date='{self.pub_date}')>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'content_type': self.content_type,
            'title': self.title,
            'description': self.description,
            'summary': self.summary,
            'pub_date': self.pub_date.isoformat() if self.pub_date is not None else None,
            'display_time': self.display_time.isoformat() if self.display_time is not None else None,
            'provider_name': self.provider_name,
            'provider_url': self.provider_url,
            'canonical_url': self.canonical_url,
            'click_through_url': self.click_through_url,
            'preview_url': self.preview_url,
            'is_hosted': self.is_hosted,
            'bypass_modal': self.bypass_modal,
            'editors_pick': self.editors_pick,
            'is_premium_news': self.is_premium_news,
            'is_premium_free_news': self.is_premium_free_news,
            'site': self.site,
            'region': self.region,
            'lang': self.lang,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class Recommendations(Base):
    """
    アナリスト推奨情報を格納するテーブル
    期間別のアナリスト推奨分布（強買い、買い、ホールド、売り、強売り）を管理
    """
    __tablename__ = 'recommendations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    period = Column(String(10), nullable=False, index=True, comment='期間（0m, -1m, -2m, -3mなど）')
    
    # アナリスト推奨分布
    strong_buy = Column(Integer, default=0, comment='強買い推奨数')
    buy = Column(Integer, default=0, comment='買い推奨数')
    hold = Column(Integer, default=0, comment='ホールド推奨数')
    sell = Column(Integer, default=0, comment='売り推奨数')
    strong_sell = Column(Integer, default=0, comment='強売り推奨数')
    
    # 計算フィールド
    total_analysts = Column(Integer, comment='総アナリスト数')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="recommendations")
    
    def __repr__(self):
        return f"<Recommendations(period='{self.period}', strong_buy={self.strong_buy}, buy={self.buy})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'period': self.period,
            'strong_buy': self.strong_buy,
            'buy': self.buy,
            'hold': self.hold,
            'sell': self.sell,
            'strong_sell': self.strong_sell,
            'total_analysts': self.total_analysts,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class RevenueEstimate(Base):
    """
    売上予想データを格納するテーブル
    期間別のアナリスト売上予想（平均、最低、最高、成長率）を管理
    """
    __tablename__ = 'revenue_estimates'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    period_type = Column(String(10), nullable=False, index=True, comment='期間タイプ（0q, +1q, 0y, +1yなど）')
    
    # 売上予想データ
    avg = Column(Float, comment='平均予想売上')
    low = Column(Float, comment='最低予想売上')
    high = Column(Float, comment='最高予想売上')
    number_of_analysts = Column(Integer, comment='アナリスト数')
    
    # 成長データ
    year_ago_revenue = Column(Float, comment='前年同期売上')
    growth = Column(Float, comment='成長率')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="revenue_estimates")
    
    def __repr__(self):
        return f"<RevenueEstimate(period='{self.period_type}', avg={self.avg_estimate})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'period_type': self.period_type,
            'avg': self.avg,
            'low': self.low,
            'high': self.high,
            'number_of_analysts': self.number_of_analysts,
            'year_ago_revenue': self.year_ago_revenue,
            'growth': self.growth,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

class Sustainability(Base):
    """
    企業のESG（環境・社会・ガバナンス）持続可能性データを格納するテーブル
    ESGスコア、ピア比較、業界分類、投資制限項目等を管理
    """
    __tablename__ = 'sustainability'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), ForeignKey('stock_info.symbol'), nullable=False, index=True)
    
    # データ更新情報
    max_age = Column(Integer, comment='データ最大経過時間（秒）')
    rating_year = Column(Integer, comment='評価年')
    rating_month = Column(Integer, comment='評価月')
    
    # ESGスコア
    total_esg = Column(Float, comment='総合ESGスコア')
    environment_score = Column(Float, comment='環境スコア')
    social_score = Column(Float, comment='社会スコア')
    governance_score = Column(Float, comment='ガバナンススコア')
    
    # 論争・リスク情報
    highest_controversy = Column(Float, comment='最高論争レベル')
    esg_performance = Column(String(50), comment='ESGパフォーマンス（LAG_PERF等）')
    
    # ピア情報
    peer_count = Column(Integer, comment='ピア企業数')
    peer_group = Column(String(100), comment='ピアグループ名')
    
    # ピアパフォーマンス比較
    peer_esg_min = Column(Float, comment='ピアESG最低スコア')
    peer_esg_avg = Column(Float, comment='ピアESG平均スコア')
    peer_esg_max = Column(Float, comment='ピアESG最高スコア')
    
    peer_governance_min = Column(Float, comment='ピアガバナンス最低スコア')
    peer_governance_avg = Column(Float, comment='ピアガバナンス平均スコア')
    peer_governance_max = Column(Float, comment='ピアガバナンス最高スコア')
    
    peer_social_min = Column(Float, comment='ピア社会最低スコア')
    peer_social_avg = Column(Float, comment='ピア社会平均スコア')
    peer_social_max = Column(Float, comment='ピア社会最高スコア')
    
    peer_environment_min = Column(Float, comment='ピア環境最低スコア')
    peer_environment_avg = Column(Float, comment='ピア環境平均スコア')
    peer_environment_max = Column(Float, comment='ピア環境最高スコア')
    
    peer_controversy_min = Column(Float, comment='ピア論争最低レベル')
    peer_controversy_avg = Column(Float, comment='ピア論争平均レベル')
    peer_controversy_max = Column(Float, comment='ピア論争最高レベル')
    
    # パーセンタイル
    percentile = Column(Float, comment='総合パーセンタイル')
    environment_percentile = Column(Float, comment='環境パーセンタイル')
    social_percentile = Column(Float, comment='社会パーセンタイル')
    governance_percentile = Column(Float, comment='ガバナンスパーセンタイル')
    
    # 関連論争
    related_controversy = Column(Text, comment='関連論争内容（JSON形式）')
    
    # 投資制限項目フラグ
    adult = Column(String(10), comment='アダルト産業フラグ')
    alcoholic = Column(String(10), comment='アルコール産業フラグ')
    animal_testing = Column(String(10), comment='動物実験フラグ')
    catholic = Column(String(10), comment='カトリック投資制限フラグ')
    controversial_weapons = Column(String(10), comment='論争兵器フラグ')
    small_arms = Column(String(10), comment='小火器フラグ')
    fur_leather = Column(String(10), comment='毛皮・革製品フラグ')
    gambling = Column(String(10), comment='ギャンブル産業フラグ')
    gmo = Column(String(10), comment='遺伝子組み換え作物フラグ')
    military_contract = Column(String(10), comment='軍事契約フラグ')
    nuclear = Column(String(10), comment='原子力産業フラグ')
    pesticides = Column(String(10), comment='農薬フラグ')
    palm_oil = Column(String(10), comment='パーム油フラグ')
    coal = Column(String(10), comment='石炭産業フラグ')
    tobacco = Column(String(10), comment='タバコ産業フラグ')
    
    created_at = Column(String(24))
    updated_at = Column(String(24))
    
    # リレーションシップ
    stock = relationship("StockInfo", backref="sustainability")
    
    def __repr__(self):
        return f"<Sustainability(total_esg={self.total_esg}, peer_group='{self.peer_group}')>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'max_age': self.max_age,
            'rating_year': self.rating_year,
            'rating_month': self.rating_month,
            'total_esg': self.total_esg,
            'environment_score': self.environment_score,
            'social_score': self.social_score,
            'governance_score': self.governance_score,
            'highest_controversy': self.highest_controversy,
            'esg_performance': self.esg_performance,
            'peer_count': self.peer_count,
            'peer_group': self.peer_group,
            'peer_esg_min': self.peer_esg_min,
            'peer_esg_avg': self.peer_esg_avg,
            'peer_esg_max': self.peer_esg_max,
            'peer_governance_min': self.peer_governance_min,
            'peer_governance_avg': self.peer_governance_avg,
            'peer_governance_max': self.peer_governance_max,
            'peer_social_min': self.peer_social_min,
            'peer_social_avg': self.peer_social_avg,
            'peer_social_max': self.peer_social_max,
            'peer_environment_min': self.peer_environment_min,
            'peer_environment_avg': self.peer_environment_avg,
            'peer_environment_max': self.peer_environment_max,
            'peer_controversy_min': self.peer_controversy_min,
            'peer_controversy_avg': self.peer_controversy_avg,
            'peer_controversy_max': self.peer_controversy_max,
            'percentile': self.percentile,
            'environment_percentile': self.environment_percentile,
            'social_percentile': self.social_percentile,
            'governance_percentile': self.governance_percentile,
            'related_controversy': self.related_controversy,
            'adult': self.adult,
            'alcoholic': self.alcoholic,
            'animal_testing': self.animal_testing,
            'catholic': self.catholic,
            'controversial_weapons': self.controversial_weapons,
            'small_arms': self.small_arms,
            'fur_leather': self.fur_leather,
            'gambling': self.gambling,
            'gmo': self.gmo,
            'military_contract': self.military_contract,
            'nuclear': self.nuclear,
            'pesticides': self.pesticides,
            'palm_oil': self.palm_oil,
            'coal': self.coal,
            'tobacco': self.tobacco,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }
