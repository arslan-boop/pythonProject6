import binance.client
import API_Config
import talib as ta
import numpy as np
import time
import DB_transactions
import Telebot_v1
from datetime import datetime
from binance.client import Client

def Coin_Bul():
    with open('SembolTemp.txt', 'r') as dosya:
        for line in dosya.read().splitlines():
            #print(line)
            v_symbol = line
            v_change_4h, v_son_fiyat, v_adx_cross_up4h, v_adx_cross_down4h, v_ema_cross_up4h, v_ema_cross_down4h, v_adx_arti4h, v_ema_arti4h = kar_orani_y(v_symbol, '4h', 500, v_client)
            v_change_1h, v_son_fiyat1h, v_adx_cross_up1h, v_adx_cross_down1h, v_ema_cross_up1h, v_ema_cross_down1h, v_adx_arti1h, v_ema_arti1h = kar_orani_y(v_symbol, '1d', 500, v_client)
            # v_change_15m, v_son_fiyat15, v_adx_cross_up15,v_adx_cross_down15, v_ema_cross_up15, v_ema_cross_down15, v_adx_arti15, v_ema_arti15 = kar_orani_y(v_symbol, '15m', 500, v_client)
            # v_change_5m, v_son_fiyat5, v_adx_cross_up5, v_adx_cross_down5, v_ema_cross_up5, v_ema_cross_down5,v_adx_arti5, v_ema_arti5 = kar_orani_y(v_symbol, '5m', 500, v_client)
            # v_change_3m, v_son_fiyat3, v_adx_cross_up3, v_adx_cross_down3, v_ema_cross_up3, v_ema_cross_down3,v_adx_arti3, v_ema_arti3 = kar_orani_y(v_symbol, '3m', 500, v_client)
            # v_change_1m, v_son_fiyat, v_adx_cross_up1, v_adx_cross_down1, v_ema_cross_up1 ,v_ema_cross_down1,v_adx_arti1, v_ema_arti1 = kar_orani_y(v_symbol, '1m', 500, v_client)
            v_param = 1
            #if 1 == 1:
            if  v_change_4h>0.5 :
                #if  v_ema_cross_up1 == True  and v_adx_arti1 ==1 and v_change_5m>1  and v_change_15m>1   and v_change_1h>1 :
            #if v_ema_cross_up1 == True and v_adx_cross_up1 == True and v_change_5m > 1 and v_change_15m > 1:
                print('Sembol (ALIM ) = ', v_symbol,'Son Fiyat = ',v_son_fiyat,'Değişim', str(v_change_4h),'Zaman=',datetime.now())
                #dosya.close()
                v_return_coin = v_symbol
                v_interval = '1m'
                break
            else:
                v_return_coin = 'XXX'
                v_interval = '1m'
                print('Bu coin uygun değil = ', v_symbol, 'Zaman', datetime.now())
    return  v_return_coin, v_son_fiyat, v_interval
#*********************************************************************
def kar_orani_y(v_symbol, v_interval, v_limit,v_client): #, v_period, v_buy_price, v_buy_time, v_date, v_sell_price, v_result, v_percent, v_desc,v_sell_time):
    #print('symbol', v_symbol, ' priceChange = ', str(v_priceChangePercent), 'priceChangePercent = ', str(v_priceChange))
    klines = v_client.get_klines(symbol=v_symbol, interval=v_interval, limit=v_limit)
    open = [float(entry[1]) for entry in klines]
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]

    v_uz = len(close)
    print( 'dizu = ' , v_uz)
    if v_uz < 2:
       return 0,0, False,False, False, False, 0, 0
    last_closing_price = close[-1]
    previous_closing_price = close[-2]
    # ----
    close_array = np.asarray(close)
    close_finished = close_array[:-1]
    high_array = np.asarray(high)
    high_finished = high_array[:-1]
    low_array = np.asarray(low)
    low_finished = low_array[:-1]
    #print('anlık kapanış fiyatı', last_closing_price, ', bir önceki kapanış fiyatı',          previous_closing_price, 'closed_finished = ')

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

    if last_plus_di >= last_minus_di:
       adx_arti = 1
    else:
       adx_arti = 0

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

    if last_ema20 >= last_ema5:
        ema_arti = 0
    else:
        ema_arti = 1
    # print('last_ema5 = ', last_ema5, "last_ema20 = ", last_ema20, "previous_ema5 = ",previous_ema5,"previous_ema20 = ", previous_ema20, "ema_cross_up =", ema_cross_up)
    # print(' --------------------------------------------------------------------')
    # print('ema_cross_up =', ema_cross_up, 'last_plus_di= ', last_plus_di,'last_minus_di = ',last_minus_di);
    v_oran = ((last_closing_price - previous_closing_price)*100)/previous_closing_price
    v_f_oran = float(v_oran)

    return v_f_oran,last_closing_price, adx_cross_up,adx_cross_down, ema_cross_up, ema_cross_down, adx_arti, ema_arti

# *****************************************************************************************
if __name__ == '__main__':
    print('Başlangıç =', datetime.now())
    client = Client(API_Config.API_KEY, API_Config.API_SECRET)
    global v_client
    v_client = client
    global v_return_coin
    v_return_coin = 'XXX'
    global v_bulunan
    global v_last_price
    global v_inter
    global v_alim_var
    v_alim_var = 0
    global v_time_bef, v_time_befs
    v_time_bef, v_time_befs  = '2022-10-10 10:24', '2022-10-10 10:24'
    global v_satim
    v_satim = 0

    while True:
        # 10 saniye bekliyoruz. Sürekli srgu göndermeye gerek yok.
        #time.sleep(2)
        try:
            #İçerde alım yoksa yeni coin bul
            if v_alim_var == 0:
                # Uygun coini bul
                v_bulunan, v_last_price, v_inter = Coin_Bul()
                #---------------------------------------------
                if v_bulunan !='XXX':
                    print('Bitiş =', datetime.now(), 'Bulunan = ', v_bulunan, 'Last Price = ', v_last_price)
                    # Alım Yapılıyor
                    Coin_Al(v_bulunan,v_last_price,v_inter)
                    # ---------------------------------------------
                    v_alim_var = 1
                else:
                    print('Dosyada uygun coin yok',datetime.now())
                    v_alim_var = 0
        except Exception as exp:
             print('Hataa!! = ',v_bulunan, 'Hata Kodu = ', exp)
            # print(exp.status_code, flush=True)
            # print(exp.message, flush=True)
