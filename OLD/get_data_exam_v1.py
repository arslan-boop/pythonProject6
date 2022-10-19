import API_Config
import talib as ta
import numpy as np
import time
import DB_transactions
import Telebot_v1
from datetime import datetime
v_time_bef , v_time_befs, v_alim_var  = '2022-10-10 10:24',  '2022-10-10 10:24', 0
from binance.client import Client

def islem():
    client = Client(API_Config.API_KEY, API_Config.API_SECRET)
    v_client = client
    #Get 24hr Ticker
    prices24 = client.get_ticker()
    i = 1
    while i < 2000:
        v_symbol = prices24[i]['symbol']
        v_priceChangePercent = prices24[i]['priceChangePercent']
        v_priceChange = prices24[i]['priceChange']
         # Her bir coin için 4s, 1s, 15dk, 5dk, 3k, 1dk daki değişimlerini de bulmak lazım. Bunlarda > 1 ise al diyeceğiz
        # 4s Değişim
        # interval = c("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"),
        #print('Saat = ', datetime.now())
        #print('Değer = ', v_symbol+'-'+str(v_priceChangePercent)+'-'+str(v_priceChange) )
        #v_symbol = 'AVAXUSDT'
        # ******************SADECE USDT DEĞERLERİ İÇİN BAKSIN***************************
        #v_usdt = v_symbol[4:]
        if v_symbol.endswith('USDT'):
        #if  v_usdt =='USDT':
            v_change_4h = kar_orani(v_symbol,'4h',500,v_priceChangePercent,v_priceChange,v_client)
            v_change_1h = kar_orani(v_symbol, '1h', 500, v_priceChangePercent, v_priceChange, v_client)
            v_change_15m = kar_orani(v_symbol, '15m', 500, v_priceChangePercent, v_priceChange, v_client)
            v_change_5m = kar_orani(v_symbol, '5m', 500, v_priceChangePercent, v_priceChange, v_client)
            v_change_1m = kar_orani(v_symbol, '1m', 500, v_priceChangePercent, v_priceChange, v_client)

            v_param = 1.003
            if v_change_4h>= v_param and  v_change_1h>=v_param and  v_change_15m>= v_param and  v_change_5m>=v_param and  v_change_1m>=v_param:

                print('Sembol (AL) = ',v_symbol, 'Değişim Oranları =', str(v_change_4h) + '-' + str(v_change_1h) + '-' + str(v_change_15m) + '-' + str(v_change_5m) + '-' + str(v_change_1m))
        #else:
        #    print('Alınmayacak = ', v_symbol + '-' + str(v_priceChangePercent) + '-' + str(v_priceChange))
        i = i +1

def kar_orani(v_symbol, v_interval, v_limit, v_priceChangePercent,v_priceChange,v_client): #, v_period, v_buy_price, v_buy_time, v_date, v_sell_price, v_result, v_percent, v_desc,v_sell_time):
    #if float(v_priceChangePercent) > 1:
    #print('symbol', v_symbol, ' priceChange = ', str(v_priceChangePercent), 'priceChangePercent = ', str(v_priceChange))
    klines = v_client.get_klines(symbol=v_symbol, interval=v_interval, limit=v_limit)
    #print('geçtiiiii')
    open = [float(entry[1]) for entry in klines]
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]
    last_closing_price = close[-1]
    previous_closing_price = close[-2]
    v_oran = (last_closing_price / previous_closing_price)
    v_f_oran = float(v_oran)
   # print('Interval =' , v_interval, ' Sembol= ', v_symbol, ' anlık kapanış fiyatı', float(last_closing_price), ', bir önceki kapanış fiyatı', previous_closing_price, 'Değişim Oranı= ',str(v_oran))
    # else:
    #     last_closing_price = 0
    #     v_symbol = v_symbol
    #     #print('has no transactions')
    return v_f_oran

if __name__ == '__main__':
   islem()