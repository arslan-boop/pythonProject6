from binance.client import Client
import talib as ta
import numpy as np
import time
import DB_transactions
import Telebot_v1
from datetime import datetime
v_time_bef , v_time_befs, v_alim_var  = '2022-10-10 10:24',  '2022-10-10 10:24', 0

class BinanceConnection:
    def __init__(self, file):
        self.connect(file)
    """ Creates Binance client """
    def connect(self, file):
        lines , key , secret = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)
if __name__ == '__main__':
    filename = '../credentials.txt'
    connection = BinanceConnection(filename)
    symbol, interval, limit  = 'DYDXUSDT', '1m',  500
    while True:
        # 10 saniye bekliyoruz. Sürekli srgu göndermeye gerek yok.
        time.sleep(5)
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
        #----
        close_array = np.asarray(close)
        close_finished = close_array[:-1]
        high_array = np.asarray(high)
        high_finished = high_array[:-1]
        low_array = np.asarray(low)
        low_finished = low_array[:-1]
        print('anlık kapanış fiyatı', last_closing_price, ', bir önceki kapanış fiyatı', previous_closing_price,'closed_finished = ')

        # ******************    RSI
        rsi = ta.RSI(close_finished, timeperiod=14)
        rsi_last = rsi[-1]

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
        # print(' --------------------------------------------------------------------')
        # print('ema_cross_up =', ema_cross_up, 'last_plus_di= ', last_plus_di,'last_minus_di = ',last_minus_di);

        # ******************* Log tablosu oluştur  ***************************
        DB_transactions.Table_create()
        v_time = str(datetime.now())
        v_time = v_time[0:16]
        v_times = v_time

        if (ema_cross_up and  last_plus_di >= last_minus_di) and v_alim_var == 0: # İçerde 1 alım varken yeni alım yapmaması için kontrol
        #if 1 == 1:
            # ******************************TELEGRAM MESAJI ********************
            v_mess = ' Tuttum Seni =' + 'Coin = ' + symbol + ' Period = ' + str(interval) + ' Buy Price =' + str(last_closing_price) + ' Saat = ' + v_time

            if v_time_bef != v_time:  # Aynı period (dk ) içinde 2 defa mesaj atmasını engellemek için
                Telebot_v1.mainma(v_mess)
                v_time_bef = v_time
                # Trade_Logs tablosuna kayıt attı
                DB_transactions.Add_value(symbol,interval,last_closing_price,v_time,v_time,None,None,None,'İlk Alım ',None )
                v_alim_var = 1
                # ********************************************************************
        #elif ema_cross_down and  last_minus_di >=  last_plus_di: #  adx_cross_up:
        elif  v_alim_var == 1:
            # İçerde alım varsa bunu 2 türlü satarsın , ya karla ya da STOP (zararla)
            # Alış fiyatını çekme
            v_alis = DB_transactions.Select_Table(symbol)
            v_alis_k = v_alis * 1.003
            v_alis_z = v_alis * 0.99

            if last_closing_price > v_alis_k: # %0.3 kar gördünmü satacak
                v_mess_s = ' Karla Satti =' + 'Coin = ' + symbol + ' Period = ' + str(interval) + ' Alis Fiyat ='+ str(v_alis)+ ' Satis Fiyat ='+ str(last_closing_price)  + ' Saat = ' + v_times
                v_sell_price = last_closing_price
                #**********Telegram Mesajı
                Telebot_v1.mainma(v_mess_s)

                v_aciklama = 'Karla satti'
                v_result = 'Kar'
                v_kar_zarar_oran= last_closing_price / v_alis
                # DB ye kayıt
                DB_transactions.Update_Table(symbol, v_sell_price, v_result, v_kar_zarar_oran, v_times)
                # Yeni bir coin alabilmek için parametreyi boşaltıyoruz
                v_alim_var = 0
            elif last_closing_price < v_alis_z: # %1 zarar olunca STOP ol
                v_mess_s = ' STOP oldu =' + 'Coin = ' + symbol + ' Period = ' + str(interval) + ' Alis Fiyat =' + str(v_alis)+ ' Satis Fiyat ='+ str(last_closing_price)  + ' Saat = ' + v_times
                v_sell_price = last_closing_price
                #**********Telegram Mesajı
                Telebot_v1.mainma(v_mess_s)
                v_aciklama = 'STOP oldu'
                v_result = 'Zarar'
                v_kar_zarar_oran= v_alis / last_closing_price
                # DB kayit
                DB_transactions.Update_Table(symbol, v_sell_price, v_result, v_kar_zarar_oran, v_times)
                # Yeni bir coin alabilmek için parametreyi boşaltıyoruz
                v_alim_var = 0
            else:
                    print('ALım-Satım Fiyatı aynı ')
        else:
            v_time = str(datetime.now())
            v_time = v_time[0:16]
            print('İşleme Girmedi  = ', v_time)
            # DB_transactions.Add_value(symbol, interval, 12, v_time, v_time, 33, 'Kar', 1, 'İşleme Girmedi',None)
            # alım yapabilirsiniz (0.1 miktarında market ya da limit alım emri girebiliriz):
            # buy_order = connection.client.order_market_buy(symbol=symbol, quantity=0.1)
