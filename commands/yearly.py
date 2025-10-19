from dotenv import load_dotenv
load_dotenv()

import os
import time
import requests
import yfinance as yf

from utils.jquants import JQuantsClient
from insert_yf.stock_info import insert_stock_info

jq_client = JQuantsClient()
companies = jq_client.getCompanies()
symbols = [company.get('Code', '')[:4] for company in companies]
