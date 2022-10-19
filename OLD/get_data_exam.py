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
i = 1
while i < 2000:
    syl = prices24[i]['symbol']
    son = prices24[i]['priceChange']
    deg = prices24[i]['priceChangePercent']
    if syl.endswith('USDT'):
        print(syl)
    i = i + 1

    #if float(deg) > 1:
     #  print('symbol', syl, ' priceChange = ', str(son), 'priceChangePercent = ', str(deg))
       #print('loooooo')
       #Her bir coin için 4s, 1s, 15dk, 5dk, 3k, 1dk daki değişimlerini de bulmak lazım. Bunlarda > 1 ise al diyeceğiz
       #4s Değişim
       #interval = c("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"),
     # symbol, interval, limit = syl, '4h', 500
       # while i < 20:
       #     # 10 saniye bekliyoruz. Sürekli srgu göndermeye gerek yok.
       #     #time.sleep(5)
       #     try:
       #         #filename = 'credentials.txt'
               #connection = client.  #BinanceConnection(filename)
       # klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
       # open = [float(entry[1]) for entry in klines]
       # high = [float(entry[2]) for entry in klines]
       # low = [float(entry[3]) for entry in klines]
       # close = [float(entry[4]) for entry in klines]
       # last_closing_price = close[-1]
       # previous_closing_price = close[-2]
       # # ----
       # close_array = np.asarray(close)
       # close_finished = close_array[:-1]
       # high_array = np.asarray(high)
       # high_finished = high_array[:-1]
       # low_array = np.asarray(low)
       # low_finished = low_array[:-1]
       # print('Sembol= ', symbol, ' anlık kapanış fiyatı', last_closing_price, ', bir önceki kapanış fiyatı', previous_closing_price,'closed_finished = ')
       #
#     else:
#        print('has no transactions')
#        i = i + 1
#
#
#      #time.sleep(0.1)
#
# #print('Se', syl, 'PCahge', son, 'değişim', deg)
#
#
#
# #Get Orderbook Tickers
# #Get first bid and ask entry in the order book for all markets.
# # prices_order = client.get_orderbook_tickers()
# #
# # # Get Market Depth
# depth = client.get_order_book(symbol='BNBBTC')
#
# # Get Recent Trades
# tradesr = client.get_recent_trades(symbol='BNBBTC')
#
# # Get Historical Trades
# # tradesh = client.get_historical_trades(symbol='BNBBTC')  HATA VERDI
#
# # #Get Kline/Candlesticks
# candles = client.get_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)

#Get Historical Kline/Candlesticks
#Fetch klines for any date range and interval
# fetch 1 minute klines for the last day up until now
#klines1 = client.get_historical_klines("AVAXUSDT", Client.KLINE_INTERVAL_1MINUTE, "3 minute ago UTC+3")

# fetch 30 minute klines for the last month of 2017
#klines30 = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Jan, 2022", "1 May, 2022")

# for price in klines1:
#     print(price)

#
# # fetch weekly klines since it listed
# klines_w = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")
#
# time_res = client.get_server_time()
#
# #print(str(time_res))

#Get Historical Kline/Candlesticks using a generator
#Fetch klines using a generator
#
#for kline in client.get_historical_klines_generator("AVAXUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC+3"):
#    print(kline)
#     # do something with the kline

#print(klines1)
# for price in klines_w:
#     print(price)
