import json
from datetime import datetime, date
from typing import Any
from pandas import DataFrame, Series
import yfinance as yf
from yfinance.scrapers.quote import FastInfo
from yfinance.scrapers.funds import FundsData

# date, datetimeの変換関数
def json_serial(obj):
    # 日付型の場合には、文字列に変換します
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    # 上記以外はサポート対象外.
    raise TypeError ("Type %s not serializable" % type(obj))

def output_sample_json(name: str, data):
    output: dict | list = {}
    if type(data) == dict:
        output = data
    elif type(data) == list:
        output = data
    elif type(data) == DataFrame:
        output = json.loads(data.to_json(orient='index', date_format='iso'))
    elif type(data) == Series:
        output = json.loads(data.to_json(orient='index', date_format='iso'))
    elif type(data) == FastInfo:
        output = json.loads(data.toJSON())
    else:
        print(f'{k} type: {type(data)}')
        print(data)

    if len(output):
        with open(f'./sample/{name}.json', 'w', encoding='utf8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4, default=json_serial)

#Tikerで一つの銘柄の情報を取得
symbol = "7974.T"
stock = yf.Ticker(symbol)

# 情報取得(.info)
stock_methods: dict[str, Any] = {
    'stock_info': stock.info,
    'stock_history': stock.history(),
    'stock_news': stock.news,
    'stock_major_holders': stock.major_holders,
    'stock_institutional_holders': stock.institutional_holders,
    'stock_mutualfund_holders': stock.mutualfund_holders,
    'stock_insider_purchases': stock.insider_purchases,
    'stock_insider_transactions': stock.insider_transactions,
    'stock_insider_roster_holders': stock.insider_roster_holders,
    'stock_dividends': stock.dividends,
    'stock_capital_gains': stock.capital_gains,
    'stock_splits': stock.splits,
    'stock_actions': stock.actions,
    # 'stock_shares': stock.shares,
    'stock_fast_info': stock.fast_info,
    'stock_calendar': stock.calendar,
    'stock_sec_filings': stock.sec_filings,
    'stock_recommendations': stock.recommendations,
    # 'stock_recommendations_summary': stock.recommendations_summary,
    'stock_upgrades_downgrades': stock.upgrades_downgrades,
    # 'stock_earnings': stock.earnings,
    # 'stock_quarterly_earnings': stock.quarterly_earnings,
    'stock_income_stmt': stock.income_stmt,
    # 'stock_quarterly_income_stmt': stock.quarterly_income_stmt,
    # 'stock_ttm_income_stmt': stock.ttm_income_stmt,
    'stock_incomestmt': stock.incomestmt,
    # 'stock_quarterly_incomestmt': stock.quarterly_incomestmt,
    # 'stock_ttm_incomestmt': stock.ttm_incomestmt,
    'stock_financials': stock.financials,
    # 'stock_quarterly_financials': stock.quarterly_financials,
    # 'stock_ttm_financials': stock.ttm_financials,
    # 'stock_balance_sheet': stock.balance_sheet,
    # 'stock_quarterly_balance_sheet': stock.quarterly_balance_sheet,
    'stock_balancesheet': stock.balancesheet,
    # 'stock_quarterly_balancesheet': stock.quarterly_balancesheet,
    # 'stock_cash_flow': stock.cash_flow,
    # 'stock_quarterly_cash_flow': stock.quarterly_cash_flow,
    'stock_cashflow': stock.cashflow,
    # 'stock_quarterly_cashflow': stock.quarterly_cashflow,
    # 'stock_ttm_cashflow': stock.ttm_cashflow,
    'stock_earnings_estimate': stock.earnings_estimate,
    'stock_revenue_estimate': stock.revenue_estimate,
    'stock_earnings_history': stock.earnings_history,
    'stock_eps_trend': stock.eps_trend,
    'stock_eps_revisions': stock.eps_revisions,
    'stock_growth_estimates': stock.growth_estimates,
    'stock_sustainability': stock.sustainability,
    'stock_earnings_dates': stock.earnings_dates,
    # 'stock_history_metadata': stock.history_metadata,
    'stock_funds_data': stock.funds_data,
}

for k, v in stock_methods.items():
    output_sample_json(k, v)

# 株価
## stock.history, yf.downloadは同一
# stock_history = stock.history(interval="1m", start='2025-09-01', end='2025-09-02')
# if stock_history is not None:
#     with open('./sample/stock_history.json', 'w', encoding='utf8') as f:
#         json.dump(json.loads(stock_history.to_json()), f, ensure_ascii=False, indent=4)
#     # with open('./sample/stock_history.csv', 'w', encoding='utf8') as f:
#     #     stock_history.to_csv(f)

# stock_download = yf.download(tickers=symbol, interval="1m", start='2025-09-01', end='2025-09-02')
# if stock_download is not None:
#     with open('./sample/stock_download.json', 'w', encoding='utf8') as f:
#         json.dump(json.loads(stock_download.to_json()), f, ensure_ascii=False, indent=4)
#     # with open('./sample/stock_download.csv', 'w', encoding='utf8') as f:
#     #     stock_download.to_csv(f)



pass
