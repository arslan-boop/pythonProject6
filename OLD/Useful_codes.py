import API_Config
import talib as ta
import numpy as np
import time
import DB_transactions
import Telebot_v1
from datetime import datetime
v_time_bef , v_time_befs, v_alim_var  = '2022-10-10 10:24',  '2022-10-10 10:24', 0
from binance.client import Client

client = Client(API_Config.API_KEY, API_Config.API_SECRET)

# # get all symbol prices
# pricesall =  client.get_all_tickers()
# symbol =  pricesall[1]['symbol']
# sonuc= pricesall[1]['price']

#Get 24hr Ticker
prices24 = client.get_ticker()
cv = prices24.priceChangePercent
for price in prices24:
    print(cv)
# *************************************************


# Import libraries
import json
import requests

# defining key/request url
key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# requesting data from url
data = requests.get(key)
data = data.json()
print(f"{data['symbol']} price is {data['price']}")

#***************************************************
# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

# get timestamp of earliest date data is available
timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1d')
print(timestamp)


#https://api.binance.com/api/v1/klines?symbol=YFIUSDT&interval=1m

