from binance.client import Client
import talib as ta
import numpy as np
import time

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
    filename = 'credentials.txt'
    connection = BinanceConnection(filename)

    symbol = 'AVAXUSDT'
    interval = '1m'
    limit = 500

    while True:
        # 10 saniye bekliyoruz. Sürekli srgu göndermeye gerek yok.
        time.sleep(2)

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

        print('anlık kapanış fiyatı', last_closing_price, ', bir önceki kapanış fiyatı', previous_closing_price)
        # https://kerteriz.net/python-diziler/
        # https://tr.csstricks.net/8226581-numpy-asarray-in-python-with-example   --Bir datayı diziye dönüştürür.
        # liste = ["ali","veli","de","fdsf"]
        # for i in range(len(liste)):
        #     print(liste[i])

        close_array = np.asarray(close)
        close_finished = close_array[:-1]
        high_array = np.asarray(high)
        high_finished = high_array[:-1]
        low_array = np.asarray(low)
        low_finished = low_array[:-1]

        # ******************    MACD
        macd, macdsignal, macdhist = ta.MACD(close_finished, fastperiod=12, slowperiod=26, signalperiod=9)
        last_macd = macd[-1]
        last_macd_signal = macdsignal[-1]
        previous_macd = macd[-2]
        previous_macd_signal = macdsignal[-2]
        macd_cross_up = last_macd > last_macd_signal and previous_macd < previous_macd_signal
        #print('Last Macd = ', last_macd, "last_macd_signal = ", last_macd_signal, "previous_macd = ", previous_macd,"previous_macd_signal = ", previous_macd_signal,"macd_cross_up =",macd_cross_up)

        # ******************    RSI
        rsi = ta.RSI(close_finished, timeperiod=14)
        rsi_last = rsi[-1]
        #print('rsi_last = ', rsi_last)

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
        #print('last_plus_di = ', last_plus_di, "last_minus_di = ", last_minus_di, "previous_plus_di = ", previous_plus_di, "previous_minus_di = ", previous_minus_di, "adx_cross_up =", adx_cross_up)

        # ******************    EMA
        ema5 = ta.EMA(close_finished, 5)
        ema20 = ta.EMA(close_finished, 20)
        last_ema5 = ema5[-1]
        last_ema20 = ema20[-1]
        previous_ema5 = ema5[-2]
        previous_ema20 = ema20[-2]
        ema_cross_up = previous_ema20 > previous_ema5 and last_ema5 > last_ema20
        #print('last_ema5 = ', last_ema5, "last_ema20 = ", last_ema20, "previous_ema5 = ",previous_ema5,"previous_ema20 = ", previous_ema20, "ema_cross_up =", ema_cross_up)

        print(' --------------------------------------------------------------------')
        #******************    Stoch RSI
        fastk, fastd = ta.STOCHRSI(close_finished, timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
        #slowk, slowd = ta.STOCH(high_finished, low_finished, close_finished, timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)

        last_fastk = fastk[-1]
        last_fastd = fastd[-1]
        previous_fastk = fastk[-2]
        previous_fastd = fastd[-2]
        stoch_cross_up = previous_fastd > previous_fastk and last_fastd < last_fastk
        #print('last_fastk = ', last_fastk, "last_fastd = ", last_fastd, "previous_fastk = ", previous_fastk,"previous_fastd = ", previous_fastd, "stoch_cross_up= ", stoch_cross_up)
        #************************************************
        print('ema_cross_up =',ema_cross_up, 'adx_cross_up= ',adx_cross_up);

        if ema_cross_up and adx_cross_up:
           print('EMA ve ADX kesti -- AL', flush=True)
           # alım yapabilirsiniz (0.1 miktarında market ya da limit alım emri girebiliriz):
           #buy_order = connection.client.order_market_buy(symbol=symbol, quantity=0.1)
        else:
            print('+ ALMA ', flush=True)
            #buy_order = connection.client.order_market_buy(symbol=symbol, quantity=0.1)

        # if stoch_cross_up:
        # print('+ stoch_cross_up yukarı kesti', flush=True)
        # ************************************************

        # mail atabilirsiniz, sms gönderebilirsiniz.

