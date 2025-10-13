"""
Financials data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import Financials
from database.client import db_client


def insert_stock_financials(yf_client: yf.Ticker) -> int:
    """
    指定された銘柄の財務諸表データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # 財務諸表データを取得
        financials_data = yf_client.financials
        
        if financials_data is None or financials_data.empty:
            print(f"No financials data found for {symbol}")
            return 0
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_financials_data(session, symbol, financials_data)
            session.commit()
            print(f"Successfully processed {processed_count} financials records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting financials data for {symbol}: {e}")
        return 0


def _bulk_process_financials_data(session, symbol: str, data) -> int:
    """
    財務諸表データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: DataFrame with financials data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_financials = session.query(Financials).filter(
        Financials.symbol == symbol
    ).all()
    existing_records = {f"{record.date}_{record.period_type}": record for record in existing_financials}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    # データの構造解析
    # yfinanceのfinancialsは行（項目名）×列（日付）の形式
    for column_date in data.columns:
        # 日付の変換
        if hasattr(column_date, 'strftime'):
            date_str = column_date.strftime('%Y-%m-%d')
        else:
            try:
                date_obj = pd.to_datetime(column_date)
                date_str = date_obj.strftime('%Y-%m-%d')
            except:
                date_str = str(column_date)[:10]
        
        # 期間タイプの決定（年次データとして扱う）
        period_type = 'annual'
        record_key = f"{date_str}_{period_type}"
        
        if record_key in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[record_key]
            _update_financials_fields(existing_record, data, column_date)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            financials_record = _create_financials_record(
                symbol, date_str, period_type, data, column_date
            )
            new_records.append(financials_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated financials records for {symbol}")
    return len(new_records) + updated_count


def _create_financials_record(symbol: str, date_str: str, period_type: str, data, column_date) -> Financials:
    """
    財務諸表レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        date_str: 日付文字列
        period_type: 期間タイプ
        data: 財務諸表DataFrame
        column_date: 対象列の日付
        
    Returns:
        Financials: 作成されたレコード
    """
    financials_record = Financials(
        symbol=symbol,
        date=date_str,
        period_type=period_type,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_financials_fields(financials_record, data, column_date)
    
    return financials_record


def _update_financials_fields(record: Financials, data, column_date) -> None:
    """
    財務諸表レコードのフィールドを更新する
    
    Args:
        record: Financialsモデルのインスタンス
        data: 財務諸表DataFrame
        column_date: 対象列の日付
    """
    # フィールドマッピング
    field_mappings = {
        # 売上・費用項目
        'total_revenue': ['Total Revenue', 'Operating Revenue'],
        'operating_revenue': ['Operating Revenue', 'Total Revenue'],
        'cost_of_revenue': ['Cost Of Revenue', 'Reconciled Cost Of Revenue'],
        'gross_profit': ['Gross Profit'],
        'operating_expense': ['Operating Expense'],
        'operating_income': ['Operating Income', 'Total Operating Income As Reported'],
        'total_expenses': ['Total Expenses'],
        
        # 利益・損失項目
        'ebit': ['EBIT'],
        'ebitda': ['EBITDA'],
        'normalized_ebitda': ['Normalized EBITDA'],
        'pretax_income': ['Pretax Income'],
        'tax_provision': ['Tax Provision'],
        'net_income': ['Net Income'],
        'net_income_common_stockholders': ['Net Income Common Stockholders'],
        'net_income_continuous_operations': ['Net Income Continuous Operations'],
        'normalized_income': ['Normalized Income'],
        
        # 金利・金融項目
        'interest_income': ['Interest Income'],
        'interest_expense': ['Interest Expense'],
        'net_interest_income': ['Net Interest Income'],
        'interest_income_non_operating': ['Interest Income Non Operating'],
        'interest_expense_non_operating': ['Interest Expense Non Operating'],
        'net_non_operating_interest_income_expense': ['Net Non Operating Interest Income Expense'],
        
        # 特別項目
        'other_non_operating_income_expenses': ['Other Non Operating Income Expenses'],
        'special_income_charges': ['Special Income Charges'],
        'other_special_charges': ['Other Special Charges'],
        'total_unusual_items': ['Total Unusual Items'],
        'total_unusual_items_excluding_goodwill': ['Total Unusual Items Excluding Goodwill'],
        'tax_effect_of_unusual_items': ['Tax Effect Of Unusual Items'],
        'tax_rate_for_calcs': ['Tax Rate For Calcs'],
        
        # 株式・EPS関連
        'basic_average_shares': ['Basic Average Shares'],
        'diluted_average_shares': ['Diluted Average Shares'],
        'basic_eps': ['Basic EPS'],
        'diluted_eps': ['Diluted EPS'],
        'diluted_ni_availto_com_stockholders': ['Diluted NI Availto Com Stockholders'],
        
        # 少数株主・その他
        'minority_interests': ['Minority Interests'],
        'net_income_including_noncontrolling_interests': ['Net Income Including Noncontrolling Interests'],
        'otherunder_preferred_stock_dividend': ['Otherunder Preferred Stock Dividend'],
        
        # 償却・調整項目
        'reconciled_depreciation': ['Reconciled Depreciation'],
        'reconciled_cost_of_revenue': ['Reconciled Cost Of Revenue']
    }
    
    # 各フィールドの設定
    for db_field, json_keys in field_mappings.items():
        for json_key in json_keys:
            if json_key in data.index:
                try:
                    value = data.loc[json_key, column_date]
                    if value is not None and not pd.isna(value):
                        setattr(record, db_field, float(value))
                        break
                except (ValueError, TypeError, KeyError):
                    continue
