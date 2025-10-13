"""
Income statement data insertion module for yfinance
"""
import yfinance as yf
from datetime import datetime
import pandas as pd

from models.models import IncomeStatement
from database.client import db_client


def insert_stock_income_stmt(yf_client: yf.Ticker) -> int:
    """
    指定された銘柄の損益計算書データを取得し、データベースに挿入する
    upsert機能とbulk機能を常に使用する
    
    Args:
        symbol: 銘柄シンボル (例: "AAPL")
    
    Returns:
        int: 処理された行数
    """
    symbol = yf_client.ticker or ''
    
    try:
        # 損益計算書データを取得
        income_stmt_data = yf_client.income_stmt
        
        if income_stmt_data is None or income_stmt_data.empty:
            print(f"No income statement data found for {symbol}")
            return 0
        
        processed_count = 0
        
        with db_client.session_scope() as session:
            processed_count = _bulk_process_income_stmt_data(session, symbol, income_stmt_data)
            session.commit()
            print(f"Successfully processed {processed_count} income statement records for {symbol}")
            return processed_count
            
    except Exception as e:
        print(f"Error inserting income statement data for {symbol}: {e}")
        return 0


def _bulk_process_income_stmt_data(session, symbol: str, data) -> int:
    """
    損益計算書データを処理してDBに挿入する（バルク処理＋アップサート）
    
    Args:
        session: SQLAlchemy session
        symbol: 銘柄シンボル
        data: DataFrame with income statement data
        
    Returns:
        int: 処理された行数
    """
    # 既存レコードの取得
    existing_income_stmts = session.query(IncomeStatement).filter(
        IncomeStatement.symbol == symbol
    ).all()
    existing_records = {record.date: record for record in existing_income_stmts}
    
    # 新規レコードリストの準備
    new_records = []
    updated_count = 0
    
    # データの構造解析
    # yfinanceのincome_stmtは行（項目名）×列（日付）の形式
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
        
        if date_str in existing_records:
            # 既存レコードの更新
            existing_record = existing_records[date_str]
            _update_income_stmt_fields(existing_record, data, column_date)
            setattr(existing_record, 'updated_at', datetime.now().isoformat()[:24])
            updated_count += 1
        else:
            # 新規レコードの作成
            income_stmt_record = _create_income_stmt_record(
                symbol, date_str, data, column_date
            )
            new_records.append(income_stmt_record)
    
    # バルクインサート
    if new_records:
        session.bulk_save_objects(new_records)
    
    print(f"Bulk processed {len(new_records)} new and {updated_count} updated income statement records for {symbol}")
    return len(new_records) + updated_count


def _create_income_stmt_record(symbol: str, date_str: str, data, column_date) -> IncomeStatement:
    """
    損益計算書レコードを作成する
    
    Args:
        symbol: 銘柄シンボル
        date_str: 日付文字列
        data: 損益計算書DataFrame
        column_date: 対象列の日付
        
    Returns:
        IncomeStatement: 作成されたレコード
    """
    income_stmt_record = IncomeStatement(
        symbol=symbol,
        date=date_str,
        created_at=datetime.now().isoformat()[:24],
        updated_at=datetime.now().isoformat()[:24]
    )
    
    # フィールドの設定
    _update_income_stmt_fields(income_stmt_record, data, column_date)
    
    return income_stmt_record


def _update_income_stmt_fields(record: IncomeStatement, data, column_date) -> None:
    """
    損益計算書レコードのフィールドを更新する
    
    Args:
        record: IncomeStatementモデルのインスタンス
        data: 損益計算書DataFrame
        column_date: 対象列の日付
    """
    # フィールドマッピング
    field_mappings = {
        # 売上・収益項目
        'total_revenue': ['Total Revenue', 'Operating Revenue'],
        'operating_revenue': ['Operating Revenue', 'Total Revenue'],
        'cost_of_revenue': ['Cost Of Revenue'],
        'reconciled_cost_of_revenue': ['Reconciled Cost Of Revenue'],
        'gross_profit': ['Gross Profit'],
        
        # 営業関連項目
        'operating_expense': ['Operating Expense'],
        'operating_income': ['Operating Income'],
        'total_operating_income_as_reported': ['Total Operating Income As Reported'],
        'total_expenses': ['Total Expenses'],
        
        # 利益指標
        'ebit': ['EBIT'],
        'ebitda': ['EBITDA'],
        'normalized_ebitda': ['Normalized EBITDA'],
        
        # 金利・金融項目
        'interest_income': ['Interest Income'],
        'interest_expense': ['Interest Expense'],
        'net_interest_income': ['Net Interest Income'],
        'interest_income_non_operating': ['Interest Income Non Operating'],
        'interest_expense_non_operating': ['Interest Expense Non Operating'],
        'net_non_operating_interest_income_expense': ['Net Non Operating Interest Income Expense'],
        
        # その他収益・費用
        'other_non_operating_income_expenses': ['Other Non Operating Income Expenses'],
        'special_income_charges': ['Special Income Charges'],
        'other_special_charges': ['Other Special Charges'],
        
        # 税引前・税引後利益
        'pretax_income': ['Pretax Income'],
        'tax_provision': ['Tax Provision'],
        
        # 純利益関連
        'net_income': ['Net Income'],
        'net_income_common_stockholders': ['Net Income Common Stockholders'],
        'net_income_continuous_operations': ['Net Income Continuous Operations'],
        'net_income_from_continuing_operation_net_minority_interest': ['Net Income From Continuing Operation Net Minority Interest'],
        'net_income_from_continuing_and_discontinued_operation': ['Net Income From Continuing And Discontinued Operation'],
        'net_income_including_noncontrolling_interests': ['Net Income Including Noncontrolling Interests'],
        'normalized_income': ['Normalized Income'],
        
        # 特別項目・調整
        'total_unusual_items': ['Total Unusual Items'],
        'total_unusual_items_excluding_goodwill': ['Total Unusual Items Excluding Goodwill'],
        'tax_effect_of_unusual_items': ['Tax Effect Of Unusual Items'],
        'tax_rate_for_calcs': ['Tax Rate For Calcs'],
        'reconciled_depreciation': ['Reconciled Depreciation'],
        
        # 株式・EPS関連
        'basic_average_shares': ['Basic Average Shares'],
        'diluted_average_shares': ['Diluted Average Shares'],
        'basic_eps': ['Basic EPS'],
        'diluted_eps': ['Diluted EPS'],
        'diluted_ni_availto_com_stockholders': ['Diluted NI Availto Com Stockholders'],
        
        # 少数株主・その他
        'minority_interests': ['Minority Interests'],
        'otherunder_preferred_stock_dividend': ['Otherunder Preferred Stock Dividend']
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
