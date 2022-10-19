from binance.client import Client
import talib as ta
import numpy as np
import time

import DB_transactions
import Telebot_v1
from datetime import datetime

v_time_bef = '2022-10-10 10:24'
v_time_befs = '2022-10-10 10:24'
v_alim_var = 0


# *********************************************
class BinanceConnection:
    def __init__(self, file):
        self.connect(file)

    """ Creates Binance client """

    def connect(self, file):
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)


if __name__ == '__main__':
    filename = '../credentials.txt'
    connection = BinanceConnection(filename)

    # symbol = input(' Coini giriniz : ')
    # print("asembol", symbol)
    # interval = input(' Süreyi giriniz : ')
    # print("SÜRE", interval)
    # interval = enum(interval)

    symbol = 'AVAXUSDT'
    interval = '1m'
    limit = 500
    while True:
        # 10 saniye bekliyoruz. Sürekli srgu göndermeye gerek yok.
        time.sleep(3)
        try:
            klines = connection.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        except Exception as exp:
            print(exp.status_code, flush=True)
            print(exp.message, flush=True)

        open = [float(entry[1]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]
        close = [float(entry[4]) for entry in klines]
        last_closing_price = close[-1]
        previous_closing_price = close[-2]

        close_array = np.asarray(close)
        close_finished = close_array[:-1]
        high_array = np.asarray(high)
        high_finished = high_array[:-1]
        low_array = np.asarray(low)
        low_finished = low_array[:-1]

        print('anlık kapanış fiyatı', last_closing_price, ', bir önceki kapanış fiyatı', previous_closing_price,'closed_finished = ')

        # ******************    MACD
        macd, macdsignal, macdhist = ta.MACD(close_finished, fastperiod=12, slowperiod=26, signalperiod=9)
        last_macd = macd[-1]
        last_macd_signal = macdsignal[-1]
        previous_macd = macd[-2]
        previous_macd_signal = macdsignal[-2]
        macd_cross_up = last_macd > last_macd_signal and previous_macd < previous_macd_signal
        # print('Last Macd = ', last_macd, "last_macd_signal = ", last_macd_signal, "previous_macd = ", previous_macd,"previous_macd_signal = ", previous_macd_signal,"macd_cross_up =",macd_cross_up)

        # ******************    RSI
        rsi = ta.RSI(close_finished, timeperiod=14)
        rsi_last = rsi[-1]
        # print('rsi_last = ', rsi_last)

        # ******************    ADX
        # plus di ve minus di değerleri bir önceki çubuğun değerlerini alıyor.Güncellemeyi yeni 1 dk başladıktan sonra yapıyor !!!!!!!!!!!!!!!!!!!!!!!1

        adx = ta.ADX(high_finished, low_finished, close_finished, timeperiod=14)
        plus_di = ta.PLUS_DI(high_finished, low_finished, close_finished, timeperiod=14)
        minus_di = ta.MINUS_DI(high_finished, low_finished, close_finished, timeperiod=14)
        # last_adx = adx[-1]
        last_plus_di = plus_di[-1]
        last_minus_di = minus_di[-1]
        previous_plus_di = plus_di[-2]
        previous_minus_di = minus_di[-2]
        adx_cross_up = previous_plus_di < previous_minus_di and last_minus_di < last_plus_di
        adx_cross_down = previous_plus_di > previous_minus_di and last_minus_di > last_plus_di

        # print('last_plus_di = ', last_plus_di, "last_minus_di = ", last_minus_di, "previous_plus_di = ", previous_plus_di, "previous_minus_di = ", previous_minus_di, "adx_cross_up =", adx_cross_up)

        # ******************    EMA
        ema5 = ta.EMA(close_finished, 5)
        ema20 = ta.EMA(close_finished, 20)
        last_ema5 = ema5[-1]
        last_ema20 = ema20[-1]
        previous_ema5 = ema5[-2]
        previous_ema20 = ema20[-2]
        ema_cross_up = previous_ema20 > previous_ema5 and last_ema5 > last_ema20
        ema_cross_down = previous_ema20 < previous_ema5 and last_ema5 < last_ema20

        # print('last_ema5 = ', last_ema5, "last_ema20 = ", last_ema20, "previous_ema5 = ",previous_ema5,"previous_ema20 = ", previous_ema20, "ema_cross_up =", ema_cross_up)

        print(' --------------------------------------------------------------------')
        # ******************    Stoch RSI
        fastk, fastd = ta.STOCHRSI(close_finished, timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
        # slowk, slowd = ta.STOCH(high_finished, low_finished, close_finished, timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
        last_fastk = fastk[-1]
        last_fastd = fastd[-1]
        previous_fastk = fastk[-2]
        previous_fastd = fastd[-2]
        stoch_cross_up = previous_fastd > previous_fastk and last_fastd < last_fastk
        # print('last_fastk = ', last_fastk, "last_fastd = ", last_fastd, "previous_fastk = ", previous_fastk,"previous_fastd = ", previous_fastd, "stoch_cross_up= ", stoch_cross_up)
        # ************************************************
        print('ema_cross_up =', ema_cross_up, 'last_plus_di= ', last_plus_di,'last_minus_di = ',last_minus_di);

        # ******************* Log tablosu oluştur  ***************************
        DB_transactions.Table_create()
        v_alim_var = 1
        v_time = str(datetime.now())
        v_time = v_time[0:16]
        v_times = v_time

        if (ema_cross_up and  last_plus_di >= last_minus_di) and v_alim_var == 0:
        #if 1 == 1:
            # TELEGRAM MESAJI ***************************************************
            print('Alım = ', v_time)
            v_mess = ' BUY (Yukarı Kesti) =' + 'Coin = ' + symbol + 'Time = ' + str(interval) + 'Buy Price =' \
                     + str(last_closing_price) + str(adx_cross_up) + 'Saat = ' + v_time
            if v_time_bef != v_time:
                Telebot_v1.mainma(v_mess)
                v_time_bef = v_time
                # *******************Değerleri Tabloya Yazma ***************************
                v_sell = 0
                DB_transactions.Add_value(symbol,interval,last_closing_price,v_time,v_time,None,None,1,'İlk Alım Açıkla',None )
                v_alim_var = 1
                # ********************************************************************
        #elif ema_cross_down and  last_minus_di >=  last_plus_di: #  adx_cross_up:
        elif  v_alim_var == 1:
            print('Satım = ', v_times)
            v_mess_s = ' SELL (Aşağı Kesti) =' + 'Coin = ' + symbol + 'Time = ' + str(interval) + 'Buy Price ='\
                       + str(last_closing_price) + str(adx_cross_down) + 'Saat = ' + v_times
            if v_time_befs != v_times:
                print('Satım TELEBOT')
                Telebot_v1.mainma(v_mess_s)
                v_time_befs = v_times
                # *******************Değerleri Tabloya Yazma ***************************
                v_sell = 0
                # Alış fiyatını çekme
                v_alis = DB_transactions.Select_Table(symbol)
                v_alis_str = str(v_alis)
                print('Alış Fiyatı ',v_alis_str)
                v_sell_price = last_closing_price

                if v_sell_price > v_alis:
                   print('Karla satacak')
                   v_aciklama = 'Karla satacak'
                   v_result = 'Kar'
                   v_kar_zarar_oran= 1

                   #_Table(v_name, v_sell_price, v_result, v_percent, v_sell_time):
                   DB_transactions.Update_Table(symbol, v_sell_price, v_result, v_kar_zarar_oran, v_times)
                   #DB_transactions.Update_Table(symbol,v_sell_price, v_result, v_kar_zarar_oran, v_time)
                elif v_sell_price < v_alis:
                    print('Zararla satacak')
                    v_aciklama = 'Zararla satacak'
                    v_result = 'Zarar'
                    v_kar_zarar_oran = 2
                    #DB_transactions.Update_Table('AVAXUSDT', 18, 'Kar', 1, '202020')
                    DB_transactions.Update_Table(symbol, v_sell_price, v_result, v_kar_zarar_oran, v_times)
                    #DB_transactions.Update_Table(symbol, interval, last_closing_price, v_time, v_time,v_sell_price, v_result, v_kar_zarar_oran, v_aciklama, v_time)
                else:
                    print('ALım-Satım Fiyatı aynı ')
                    v_kar_zarar_oran = 3
                    #DB_transactions.Update_Table('AVAXUSDT', 19, 'Kar', 3, '202020')
                    DB_transactions.Update_Table(symbol, v_sell_price, v_result, v_kar_zarar_oran, v_time)

                    #DB_transactions.Update_Table(symbol, interval, last_closing_price, v_time, v_time,v_sell_price, v_result, v_kar_zarar_oran, v_aciklama, v_time)

                # ********************************************************************
        else:
            v_time = str(datetime.now())
            v_time = v_time[0:16]
            print('İşleme Girmedi  = ', v_time)
            v_sell = 0
            # DB_transactions.Add_value(symbol, interval, 12, v_time, v_time, 33, 'Kar', 1, 'İşleme Girmedi',None)

            # alım yapabilirsiniz (0.1 miktarında market ya da limit alım emri girebiliriz):
            # buy_order = connection.client.order_market_buy(symbol=symbol, quantity=0.1)

