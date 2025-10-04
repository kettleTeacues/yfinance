"""
Cash flow data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime

from models.models import CashFlow
from database.client import db_client


def insert_stock_cashflow(symbol: str, period: str = "max") -> int:
    """
    指定された銘柄のキャッシュフローデータを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
        period: 取得期間 ("1y", "2y", "5y", "10y", "max")
    
    Returns:
        int: 処理された行数
    """
    ticker = yf.Ticker(symbol)
    
    try:
        # 年次および四半期のキャッシュフローデータを取得
        annual_cf = ticker.cashflow
        quarterly_cf = ticker.quarterly_cashflow
        
        if annual_cf.empty and quarterly_cf.empty:
            print(f"No cashflow data found for {symbol}")
            return 0
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            # 年次データの処理（バルク＋アップサート）
            if not annual_cf.empty:
                processed_count += _bulk_process_cashflow_data(
                    session, symbol, annual_cf, "annual", True
                )
            
            # 四半期データの処理（バルク＋アップサート）
            if not quarterly_cf.empty:
                processed_count += _bulk_process_cashflow_data(
                    session, symbol, quarterly_cf, "quarterly", True
                )
            
            session.commit()
            print(f"Successfully processed {processed_count} cashflow records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting cashflow data for {symbol}: {e}")
        return 0



def _bulk_process_cashflow_data(session, symbol: str, data, period_type: str, upsert: bool) -> int:
    """
    キャッシュフローデータを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: pandas DataFrame with cashflow data
        period_type: "annual" or "quarterly"
        upsert: アップサートフラグ（常にTrue）
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_cashflows = session.query(CashFlow).filter(
        CashFlow.symbol == symbol,
        CashFlow.period_type == period_type
    ).all()
    existing_records = {(str(record.date), record.period_type): record for record in existing_cashflows}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    for date_col in data.columns:
        # 日付の変換
        if hasattr(date_col, 'strftime'):
            date_str = date_col.strftime('%Y-%m-%d')
        else:
            date_str = str(date_col)[:10]
        
        record_key = (date_str, period_type)
        
        if record_key in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[record_key]
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            _map_cashflow_fields(existing_record, data, date_col)
            updated_count += 1
        else:
            # 新規レコードの作成
            cf_record = _create_cashflow_record(symbol, date_str, period_type, data, date_col)
            new_records.append(cf_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated cashflow records for {symbol} ({period_type})")
    return len(new_records) + updated_count


def _create_cashflow_record(symbol: str, date_str: str, period_type: str, data, date_col) -> CashFlow:
    """
    キャッシュフローレコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        date_str: 日付文字列
        period_type: 期間タイプ
        data: pandas DataFrame
        date_col: 日付カラム
        
    Returns:
        CashFlow: 作成されたレコード
    """
    cf_record = CashFlow(
        symbol=symbol,
        date=date_str,
        period_type=period_type,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドのマッピング
    _map_cashflow_fields(cf_record, data, date_col)
    
    return cf_record


def _map_cashflow_fields(record: CashFlow, data, date_col) -> None:
    """
    yfinanceのキャッシュフローデータをCashFlowモデルにマッピングする
    
    Args:
        record: CashFlowモデルのインスタンス
        data: pandas DataFrame
        date_col: 日付カラム
    """
    field_mappings = _get_cashflow_field_mappings()
    
    for yf_field, model_field in field_mappings.items():
        try:
            value = data.loc[yf_field, date_col] if yf_field in data.index else None
            if value is not None and not (hasattr(value, 'isna') and value.isna()):
                setattr(record, model_field, float(value))
        except (KeyError, ValueError, TypeError):
            continue


def _get_cashflow_field_mappings() -> dict:
    """
    yfinanceのキャッシュフローフィールド名とモデルのフィールド名のマッピングを返す
    
    Returns:
        dict: yfinanceフィールド -> モデルフィールドのマッピング
    """
    return {
        # 主要キャッシュフロー指標
        'Operating Cash Flow': 'operating_cash_flow',
        'Investing Cash Flow': 'investing_cash_flow',
        'Financing Cash Flow': 'financing_cash_flow',
        'Free Cash Flow': 'free_cash_flow',
        
        # キャッシュポジション
        'Beginning Cash Position': 'beginning_cash_position',
        'End Cash Position': 'end_cash_position',
        'Changes In Cash': 'changes_in_cash',
        
        # 営業キャッシュフロー詳細
        'Net Income From Continuing Operations': 'net_income_from_continuing_operations',
        'Depreciation And Amortization': 'depreciation_and_amortization',
        'Depreciation': 'depreciation',
        'Net Foreign Currency Exchange Gain Loss': 'net_foreign_currency_exchange_gain_loss',
        'Gain Loss On Investment Securities': 'gain_loss_on_investment_securities',
        'Other Non Cash Items': 'other_non_cash_items',
        
        # 運転資本の変動
        'Change In Working Capital': 'change_in_working_capital',
        'Change In Receivables': 'change_in_receivables',
        'Change In Inventory': 'change_in_inventory',
        'Change In Payable': 'change_in_payable',
        'Change In Other Current Assets': 'change_in_other_current_assets',
        'Change In Other Current Liabilities': 'change_in_other_current_liabilities',
        
        # 利息・税金
        'Interest Paid Cfo': 'interest_paid_cfo',
        'Interest Received Cfo': 'interest_received_cfo',
        'Taxes Refund Paid': 'taxes_refund_paid',
        
        # 投資キャッシュフロー詳細
        'Capital Expenditure': 'capital_expenditure',
        'Purchase Of Ppe': 'purchase_of_ppe',
        'Sale Of Ppe': 'sale_of_ppe',
        'Net Ppe Purchase And Sale': 'net_ppe_purchase_and_sale',
        'Capital Expenditure Reported': 'capital_expenditure_reported',
        
        # 投資活動
        'Purchase Of Investment': 'purchase_of_investment',
        'Sale Of Investment': 'sale_of_investment',
        'Net Investment Purchase And Sale': 'net_investment_purchase_and_sale',
        'Net Other Investing Changes': 'net_other_investing_changes',
        
        # 財務キャッシュフロー詳細
        'Cash Dividends Paid': 'cash_dividends_paid',
        'Common Stock Dividend Paid': 'common_stock_dividend_paid',
        'Net Common Stock Issuance': 'net_common_stock_issuance',
        'Common Stock Payments': 'common_stock_payments',
        'Repurchase Of Capital Stock': 'repurchase_of_capital_stock',
        'Net Other Financing Charges': 'net_other_financing_charges',
        
        # その他の調整
        'Effect Of Exchange Rate Changes': 'effect_of_exchange_rate_changes',
        'Other Cash Adjustment Outside Changein Cash': 'other_cash_adjustment_outside_change_in_cash',
    }


