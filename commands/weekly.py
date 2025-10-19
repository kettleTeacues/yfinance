import time
import yfinance as yf

from utils.jquants import JQuantsClient
from insert_yf.stock_info import insert_stock_info

jq_client = JQuantsClient()
companies = jq_client.getCompanies()
symbols = [company.get('Code', '')[:4] for company in companies]

for symbol in symbols[:1]:
    yf_client = yf.Ticker(f'{symbol}.T')

    insert_stock_info(yf_client)
    time.sleep(0.1)
