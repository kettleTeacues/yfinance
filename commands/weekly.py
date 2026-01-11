from dotenv import load_dotenv
load_dotenv()

import time
import yfinance as yf

from utils.jquants import JQuantsClient
from insert_yf.stock_balancesheet import insert_stock_balancesheet

jq_client = JQuantsClient()
companies = jq_client.getCompanies()
symbols = [company.get('Code', '')[:4] for company in companies]

errors=[]
for symbol in symbols:
    yf_client = yf.Ticker(f'{symbol}.T')

    try:
        insert_stock_balancesheet(yf_client, period='quarterly')
    except Exception as e:
        errors.append(f"Error inserting stock history for {symbol}: {e}")

    time.sleep(0.1)
print(errors)
