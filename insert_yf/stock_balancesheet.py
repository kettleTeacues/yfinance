"""
Stock Balance Sheet data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd
from typing import Optional

from models.models import Balancesheet
from database.client import db_client


def insert_stock_balancesheet(yf_client: yf.Ticker, period: str = "annual") -> int:
    """
    指定された銘柄の貸借対照表データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL", "7974.T")
        period: 取得期間 ("annual", "quarterly")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''

    try:
        # 貸借対照表データを取得（年次と四半期）
        processed_count = 0
        
        # 年次データの処理
        if period in ["annual", "both"]:
            annual_data = yf_client.balance_sheet
            if not annual_data.empty:
                with db_client.session_scope() as session:
                    count = _bulk_process_balancesheet_data(session, symbol, annual_data, "annual")
                    session.commit()
                    processed_count += count
        
        # 四半期データの処理
        if period in ["quarterly", "both"]:
            quarterly_data = yf_client.quarterly_balance_sheet
            if not quarterly_data.empty:
                with db_client.session_scope() as session:
                    count = _bulk_process_balancesheet_data(session, symbol, quarterly_data, "quarterly")
                    session.commit()
                    processed_count += count
        
        if processed_count == 0:
            print(f"No balance sheet data found for {symbol}")
            return 0
        
        print(f"Successfully processed {processed_count} balance sheet records for {symbol}")
        return processed_count
            
    except Exception as e:
        print(f"Error inserting balance sheet data for {symbol}: {e}")
        return 0


def _bulk_process_balancesheet_data(session, symbol: str, data: pd.DataFrame, period_type: str) -> int:
    """
    貸借対照表データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: pandas DataFrame with balance sheet data
        period_type: "annual" or "quarterly"
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_records = session.query(Balancesheet).filter(
        Balancesheet.symbol == symbol,
        Balancesheet.period_type == period_type
    ).all()
    existing_dict = {f"{record.date}_{record.period_type}": record for record in existing_records}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    for date_col in data.columns:
        # 日付の変換
        try:
            if hasattr(date_col, 'strftime'):
                date_str = date_col.strftime('%Y-%m-%d')  # type: ignore
            else:
                date_str = str(date_col)[:10]  # ISO形式の日付部分のみ取得
        except (AttributeError, TypeError):
            date_str = str(date_col)[:10]
        
        record_key = f"{date_str}_{period_type}"
        current_time = datetime.now().isoformat()[:24]
        
        if record_key in existing_dict:
            # 既存レコードの更新
            existing_record = existing_dict[record_key]
            _update_balancesheet_fields(existing_record, data, date_col)
            setattr(existing_record, 'updated_at', current_time)
            updated_count += 1
        else:
            # 新規レコードの作成
            bs_record = Balancesheet(
                symbol=symbol,
                date=date_str,
                period_type=period_type,
                created_at=current_time,
                updated_at=current_time
            )
            _update_balancesheet_fields(bs_record, data, date_col)
            new_records.append(bs_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated balance sheet records for {symbol} ({period_type})")
    return len(new_records) + updated_count


def _update_balancesheet_fields(bs_record: Balancesheet, data: pd.DataFrame, date_col):
    """
    Balancesheetオブジェクトのフィールドを更新する
    
    Args:
        bs_record: Balancesheet model instance
        data: pandas DataFrame with balance sheet data
        date_col: 日付列
    """
    def safe_get_value(field_name: str) -> Optional[float]:
        """データフレームから安全に値を取得する"""
        try:
            if field_name in data.index:
                value = data.loc[field_name, date_col]
                # Series型の場合は最初の値を取得
                if isinstance(value, pd.Series) and len(value) > 0:
                    value = value.iloc[0]
                if pd.isna(value) or value is None:
                    return None
                # 数値型に変換可能かチェック
                if isinstance(value, (int, float)):
                    return float(value)
                # 文字列の場合は数値変換を試行
                if isinstance(value, str):
                    try:
                        return float(value)
                    except ValueError:
                        return None
                # その他の数値型（numpy等）の場合
                try:
                    # type: ignore でlint警告を無視
                    return float(value)  # type: ignore
                except (ValueError, TypeError):
                    return None
        except (KeyError, ValueError, TypeError, IndexError, AttributeError):
            pass
        return None
    
    # 資産項目 (Assets)
    setattr(bs_record, 'total_assets', safe_get_value('Total Assets'))
    setattr(bs_record, 'current_assets', safe_get_value('Current Assets'))
    setattr(bs_record, 'non_current_assets', safe_get_value('Total Non Current Assets'))
    setattr(bs_record, 'cash_and_cash_equivalents', safe_get_value('Cash And Cash Equivalents'))
    setattr(bs_record, 'other_short_term_investments', safe_get_value('Other Short Term Investments'))
    setattr(bs_record, 'cash_cash_equivalents_and_short_term_investments', safe_get_value('Cash Cash Equivalents And Short Term Investments'))
    setattr(bs_record, 'accounts_receivable', safe_get_value('Accounts Receivable'))
    setattr(bs_record, 'gross_accounts_receivable', safe_get_value('Gross Accounts Receivable'))
    setattr(bs_record, 'inventory', safe_get_value('Inventory'))
    setattr(bs_record, 'other_current_assets', safe_get_value('Other Current Assets'))
    setattr(bs_record, 'net_ppe', safe_get_value('Net PPE'))
    setattr(bs_record, 'gross_ppe', safe_get_value('Gross PPE'))
    setattr(bs_record, 'land_and_improvements', safe_get_value('Land And Improvements'))
    setattr(bs_record, 'buildings_and_improvements', safe_get_value('Buildings And Improvements'))
    setattr(bs_record, 'machinery_furniture_equipment', safe_get_value('Machinery Furniture Equipment'))
    setattr(bs_record, 'construction_in_progress', safe_get_value('Construction In Progress'))
    setattr(bs_record, 'properties', safe_get_value('Properties'))
    setattr(bs_record, 'goodwill_and_other_intangible_assets', safe_get_value('Goodwill And Other Intangible Assets'))
    setattr(bs_record, 'other_intangible_assets', safe_get_value('Other Intangible Assets'))
    setattr(bs_record, 'investment_in_financial_assets', safe_get_value('Investmentin Financial Assets'))
    setattr(bs_record, 'available_for_sale_securities', safe_get_value('Available For Sale Securities'))
    setattr(bs_record, 'non_current_deferred_taxes_assets', safe_get_value('Non Current Deferred Taxes Assets'))
    setattr(bs_record, 'defined_pension_benefit', safe_get_value('Defined Pension Benefit'))
    setattr(bs_record, 'other_non_current_assets', safe_get_value('Other Non Current Assets'))
    
    # 負債項目 (Liabilities)
    setattr(bs_record, 'total_liabilities_net_minority_interest', safe_get_value('Total Liabilities Net Minority Interest'))
    setattr(bs_record, 'current_liabilities', safe_get_value('Current Liabilities'))
    setattr(bs_record, 'total_non_current_liabilities_net_minority_interest', safe_get_value('Total Non Current Liabilities Net Minority Interest'))
    setattr(bs_record, 'accounts_payable', safe_get_value('Accounts Payable'))
    setattr(bs_record, 'total_tax_payable', safe_get_value('Total Tax Payable'))
    setattr(bs_record, 'payables', safe_get_value('Payables'))
    setattr(bs_record, 'pension_and_other_post_retirement_benefit_plans_current', safe_get_value('Pensionand Other Post Retirement Benefit Plans Current'))
    setattr(bs_record, 'other_current_liabilities', safe_get_value('Other Current Liabilities'))
    setattr(bs_record, 'long_term_provisions', safe_get_value('Long Term Provisions'))
    setattr(bs_record, 'non_current_pension_and_other_postretirement_benefit_plans', safe_get_value('Non Current Pension And Other Postretirement Benefit Plans'))
    setattr(bs_record, 'other_non_current_liabilities', safe_get_value('Other Non Current Liabilities'))
    
    # 株主資本項目 (Equity)
    setattr(bs_record, 'stockholders_equity', safe_get_value('Stockholders Equity'))
    setattr(bs_record, 'minority_interest', safe_get_value('Minority Interest'))
    setattr(bs_record, 'total_equity_gross_minority_interest', safe_get_value('Total Equity Gross Minority Interest'))
    setattr(bs_record, 'total_capitalization', safe_get_value('Total Capitalization'))
    setattr(bs_record, 'common_stock_equity', safe_get_value('Common Stock Equity'))
    setattr(bs_record, 'net_tangible_assets', safe_get_value('Net Tangible Assets'))
    setattr(bs_record, 'working_capital', safe_get_value('Working Capital'))
    setattr(bs_record, 'invested_capital', safe_get_value('Invested Capital'))
    setattr(bs_record, 'tangible_book_value', safe_get_value('Tangible Book Value'))
    
    # 株式関連項目
    setattr(bs_record, 'share_issued', safe_get_value('Share Issued'))
    setattr(bs_record, 'ordinary_shares_number', safe_get_value('Ordinary Shares Number'))
    setattr(bs_record, 'treasury_shares_number', safe_get_value('Treasury Shares Number'))
    setattr(bs_record, 'common_stock', safe_get_value('Common Stock'))
    setattr(bs_record, 'capital_stock', safe_get_value('Capital Stock'))
    setattr(bs_record, 'additional_paid_in_capital', safe_get_value('Additional Paid In Capital'))
    setattr(bs_record, 'retained_earnings', safe_get_value('Retained Earnings'))
    setattr(bs_record, 'treasury_stock', safe_get_value('Treasury Stock'))
