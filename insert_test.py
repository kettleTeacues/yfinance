import yfinance as yf
from time import sleep

from insert_yf.stock_actions import insert_stock_actions
from insert_yf.stock_balancesheet import insert_stock_balancesheet
from insert_yf.stock_calendar import insert_stock_calendar
from insert_yf.stock_cashflow import insert_stock_cashflow
from insert_yf.stock_dividends import insert_stock_dividends
from insert_yf.stock_earnings_dates import insert_stock_earnings_dates
from insert_yf.stock_earnings_estimate import insert_stock_earnings_estimate
from insert_yf.stock_earnings_history import insert_stock_earnings_history
from insert_yf.stock_eps_revisions import insert_stock_eps_revisions
from insert_yf.stock_eps_trend import insert_stock_eps_trend
from insert_yf.stock_financials import insert_stock_financials
from insert_yf.stock_growth_estimates import insert_stock_growth_estimates
from insert_yf.stock_history import insert_stock_history
from insert_yf.stock_income_stmt import insert_stock_income_stmt
from insert_yf.stock_info import insert_stock_info
from insert_yf.stock_insider_purchases import insert_stock_insider_purchases
from insert_yf.stock_institutional_holders import insert_stock_institutional_holders
from insert_yf.stock_major_holders import insert_stock_major_holders
from insert_yf.stock_mutualfund_holders import insert_stock_mutualfund_holders
from insert_yf.stock_news import insert_stock_news
from insert_yf.stock_recommendations import insert_stock_recommendations
from insert_yf.stock_revenue_estimate import insert_stock_revenue_estimate
from insert_yf.stock_sustainability import insert_stock_sustainability
from symbols import symbols

# テスト実行
if __name__ == "__main__":

    for symbol in symbols:
        yf_client = yf.Ticker(f'{symbol}.T')
        
        print(f"\nStarting stock info insertion for {symbol}")
        info_count = insert_stock_info(yf_client)
        print(f"Stock info insertion completed. {info_count} records processed")
        
        print(f"\nStarting stock calendar insertion for {symbol}")
        calendar_count = insert_stock_calendar(yf_client)
        print(f"Stock calendar insertion completed. {calendar_count} records processed")

        print(f"\nStarting stock cashflow insertion for {symbol}")
        cf_count = insert_stock_cashflow(yf_client)
        print(f"Stock cashflow insertion completed. {cf_count} records processed")

        print(f"\nStarting stock dividends insertion for {symbol}")
        dividends_count = insert_stock_dividends(yf_client)
        print(f"Stock dividends insertion completed. {dividends_count} records processed")

        print(f"\nStarting stock earnings dates insertion for {symbol}")
        earnings_count = insert_stock_earnings_dates(yf_client)
        print(f"Stock earnings dates insertion completed. {earnings_count} records processed")

        print(f"\nStarting stock earnings estimate insertion for {symbol}")
        estimate_count = insert_stock_earnings_estimate(yf_client)
        print(f"Stock earnings estimate insertion completed. {estimate_count} records processed")

        print(f"\nStarting stock earnings history insertion for {symbol}")
        history_count = insert_stock_earnings_history(yf_client)
        print(f"Stock earnings history insertion completed. {history_count} records processed")

        print(f"\nStarting stock EPS revisions insertion for {symbol}")
        revisions_count = insert_stock_eps_revisions(yf_client)
        print(f"Stock EPS revisions insertion completed. {revisions_count} records processed")

        print(f"\nStarting stock EPS trend insertion for {symbol}")
        trend_count = insert_stock_eps_trend(yf_client)
        print(f"Stock EPS trend insertion completed. {trend_count} records processed")

        print(f"\nStarting stock financials insertion for {symbol}")
        financials_count = insert_stock_financials(yf_client)
        print(f"Stock financials insertion completed. {financials_count} records processed")

        print(f"\nStarting stock growth estimates insertion for {symbol}")
        growth_count = insert_stock_growth_estimates(yf_client)
        print(f"Stock growth estimates insertion completed. {growth_count} records processed")

        print(f"\nStarting stock income statement insertion for {symbol}")
        income_stmt_count = insert_stock_income_stmt(yf_client)
        print(f"Stock income statement insertion completed. {income_stmt_count} records processed")

        print(f"\nStarting stock insider purchases insertion for {symbol}")
        insider_purchases_count = insert_stock_insider_purchases(yf_client)
        print(f"Stock insider purchases insertion completed. {insider_purchases_count} records processed")

        print(f"\nStarting stock institutional holders insertion for {symbol}")
        institutional_holders_count = insert_stock_institutional_holders(yf_client)
        print(f"Stock institutional holders insertion completed. {institutional_holders_count} records processed")
        
        print(f"\nStarting stock major holders insertion for {symbol}")
        major_holders_count = insert_stock_major_holders(yf_client)
        print(f"Stock major holders insertion completed. {major_holders_count} records processed")
        
        print(f"\nStarting stock mutual fund holders insertion for {symbol}")
        mutualfund_holders_count = insert_stock_mutualfund_holders(yf_client)
        print(f"Stock mutual fund holders insertion completed. {mutualfund_holders_count} records processed")
        
        print(f"\nStarting stock news insertion for {symbol}")
        news_count = insert_stock_news(yf_client)
        print(f"Stock news insertion completed. {news_count} records processed")
        
        print(f"\nStarting stock recommendations insertion for {symbol}")
        recommendations_count = insert_stock_recommendations(yf_client)
        print(f"Stock recommendations insertion completed. {recommendations_count} records processed")
        
        print(f"\nStarting stock revenue estimate insertion for {symbol}")
        revenue_estimate_count = insert_stock_revenue_estimate(yf_client)
        print(f"Stock revenue estimate insertion completed. {revenue_estimate_count} records processed")
        
        print(f"\nStarting stock sustainability insertion for {symbol}")
        sustainability_count = insert_stock_sustainability(yf_client)
        print(f"Stock sustainability insertion completed. {sustainability_count} records processed")

        print(f"\nStarting stock actions insertion for {symbol}")
        actions_count = insert_stock_actions(yf_client)
        print(f"Stock actions insertion completed. {actions_count} records processed")

        print(f"\nStarting stock balance sheet insertion for {symbol}")
        bs_count = insert_stock_balancesheet(yf_client)
        print(f"Stock balance sheet insertion completed. {bs_count} records processed")

        print(f"\nStarting stock history insertion for {symbol}")
        history_count = insert_stock_history(yf_client)
        print(f"Stock history insertion completed. {history_count} records processed")

        sleep(0.1)

    pass
