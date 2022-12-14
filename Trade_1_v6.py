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
    with open('Sembol.txt', 'r') as dosya:
        for line in dosya.read().splitlines():
            # print(line)
            v_symbol = line

            v_4h_olusmadi = 0
            v_2h_olusmadi = 0
            v_1h_olusmadi = 0
            v_15m_olusmadi = 0
            v_5m_olusmadi = 0
            v_3m_olusmadi = 0
            v_1m_olusmadi = 0
            #----------------
            v_degis_oran = 0.4

            v_change_4h, v_son_fiyat4h, v_adx_cross_up4h, v_adx_cross_down4h, v_ema_cross_up4h, v_ema_cross_down4h, v_adx_arti4h, v_ema_arti4h = kar_orani_y(
                v_symbol, '4h', 500, v_client)
            if v_change_4h == 0 and v_son_fiyat4h == 0:
                v_4h_olusmadi = 1

            v_change_2h, v_son_fiyat2h, v_adx_cross_up2h, v_adx_cross_down2h, v_ema_cross_up2h, v_ema_cross_down2h, v_adx_arti2h, v_ema_arti2h = kar_orani_y(
                v_symbol, '2h', 500, v_client)
            if v_change_2h == 0 and v_son_fiyat2h == 0:
                v_2h_olusmadi = 1

            v_change_1h, v_son_fiyat1h, v_adx_cross_up1h, v_adx_cross_down1h, v_ema_cross_up1h, v_ema_cross_down1h, v_adx_arti1h, v_ema_arti1h = kar_orani_y(
                v_symbol, '1h', 500, v_client)
            if v_change_1h == 0 and v_son_fiyat1h == 0:
                v_1h_olusmadi = 1

            v_change_15m, v_son_fiyat15, v_adx_cross_up15, v_adx_cross_down15, v_ema_cross_up15, v_ema_cross_down15, v_adx_arti15, v_ema_arti15 = kar_orani_y(
                v_symbol, '15m', 500, v_client)
            if v_change_15m == 0 and v_son_fiyat15 == 0:
                v_15m_olusmadi = 1

            v_change_5m, v_son_fiyat5, v_adx_cross_up5, v_adx_cross_down5, v_ema_cross_up5, v_ema_cross_down5, v_adx_arti5, v_ema_arti5 = kar_orani_y(
                v_symbol, '5m', 500, v_client)
            if v_change_5m == 0 and v_son_fiyat5 == 0:
                v_5m_olusmadi = 1

            v_change_3m, v_son_fiyat3, v_adx_cross_up3, v_adx_cross_down3, v_ema_cross_up3, v_ema_cross_down3, v_adx_arti3, v_ema_arti3 = kar_orani_y(
                v_symbol, '3m', 500, v_client)
            if v_change_3m == 0 and v_son_fiyat3 == 0:
                v_3m_olusmadi = 1

            v_change_1m, v_son_fiyat, v_adx_cross_up1, v_adx_cross_down1, v_ema_cross_up1, v_ema_cross_down1, v_adx_arti1, v_ema_arti1 = kar_orani_y(
                v_symbol, '1m', 500, v_client)
            if v_change_1m == 0 and v_son_fiyat == 0:
                v_1m_olusmadi = 1

            v_param = 1
            # if 1 == 1:
            # if  v_ema_cross_up1 == True  and v_adx_arti1 ==1 and v_change_5m>1  and v_change_15m>1   and v_change_1h>1 :
            # if v_ema_cross_up1 == True and v_adx_cross_up1 == True and v_change_5m > 1 and v_change_15m > 1:

            if v_4h_olusmadi == 0:  # 4h olu??tuysa hepsi tamamd??r
                if v_change_1m >= v_degis_oran and v_change_3m >= v_degis_oran and v_change_5m > v_degis_oran and v_change_15m > v_degis_oran \
                    and v_change_1h > v_degis_oran and v_change_4h > v_degis_oran and v_ema_arti1 == 1 and v_adx_arti1 == 1:
                    print('Sembol (ALIM ) = ', v_symbol, 'Son Fiyat = ', v_son_fiyat, 'De??i??im', str(v_change_1m),
                          'Zaman=', datetime.now())
                    v_return_coin = v_symbol
                    v_interval = '1m'
                    break
                else:
                    print('Bu coin uygun de??il = ', v_symbol, 'Zaman', datetime.now())
                    v_return_coin = 'XXX'
                    v_interval = '1m'
            if v_4h_olusmadi == 1 and v_2h_olusmadi == 0:  # 4 saatlik olu??mam????t??r. Buna bakma
                if v_change_1m >= v_degis_oran and v_change_3m >= v_degis_oran and v_change_5m > v_degis_oran and v_change_15m > v_degis_oran \
                        and v_change_1h > v_degis_oran and v_change_2h > v_degis_oran and v_ema_arti1 == 1 and v_adx_arti1 == 1:
                    print('Sembol (ALIM ) = ', v_symbol, 'Son Fiyat = ', v_son_fiyat, 'De??i??im', str(v_change_1m),
                          'Zaman=', datetime.now())
                    v_return_coin = v_symbol
                    v_interval = '1m'
                    break
                else:
                    print('Bu coin uygun de??il = ', v_symbol, 'Zaman', datetime.now())
                    v_return_coin = 'XXX'
                    v_interval = '1m'

            if v_4h_olusmadi == 1 and v_2h_olusmadi == 1 and  v_1h_olusmadi == 0:  # 4h, 2h olu??mad??
                if v_change_1m >= v_degis_oran and v_change_3m >= v_degis_oran and v_change_5m > v_degis_oran and\
                        v_change_15m > v_degis_oran and v_change_1h > v_degis_oran\
                        and v_ema_arti1 == v_degis_oran and v_adx_arti1==1:
                    print('Sembol (ALIM ) = ', v_symbol, 'Son Fiyat = ', v_son_fiyat, 'De??i??im', str(v_change_1m),
                          'Zaman=', datetime.now())
                    v_return_coin = v_symbol
                    v_interval = '1m'
                    break
                else:
                    print('Bu coin uygun de??il = ', v_symbol, 'Zaman', datetime.now())
                    v_return_coin = 'XXX'
                    v_interval = '1m'

            if v_4h_olusmadi == 1 and v_2h_olusmadi == 1 and v_1h_olusmadi == 1 and v_15m_olusmadi == 0:  # 4-2-1 olu??mad??
                if v_change_1m >= v_degis_oran and v_change_3m >= v_degis_oran and v_change_5m > v_degis_oran \
                        and v_change_15m > v_degis_oran and v_ema_arti1 == 1 \
                        and v_adx_arti1==1:
                    print('Sembol (ALIM ) = ', v_symbol, 'Son Fiyat = ', v_son_fiyat, 'De??i??im', str(v_change_1m),
                          'Zaman=', datetime.now())
                    v_return_coin = v_symbol
                    v_interval = '1m'
                    break
                else:
                    print('Bu coin uygun de??il = ', v_symbol, 'Zaman', datetime.now())
                    v_return_coin = 'XXX'
                    v_interval = '1m'
            if v_4h_olusmadi == 1 and v_2h_olusmadi == 1  and v_1h_olusmadi == 1 and v_15m_olusmadi == 1 and v_5m_olusmadi == 0:
                if v_change_1m >= v_degis_oran and v_change_3m >= v_degis_oran and v_change_5m >= v_degis_oran and v_ema_arti1 == 1 and v_adx_arti1==1:
                    print('Sembol (ALIM ) = ', v_symbol, 'Son Fiyat = ', v_son_fiyat, 'De??i??im', str(v_change_1m),
                          'Zaman=', datetime.now())
                    v_return_coin = v_symbol
                    v_interval = '1m'
                    break
                else:
                    print('Bu coin uygun de??il = ', v_symbol, 'Zaman', datetime.now())
                    v_return_coin = 'XXX'
                    v_interval = '1m'

            if v_4h_olusmadi == 1 and v_2h_olusmadi == 1 and v_1h_olusmadi == 1 and v_15m_olusmadi == 1 and v_5m_olusmadi == 1 and v_3m_olusmadi == 0:
                if v_change_1m >= v_degis_oran and v_change_3m >= v_degis_oran and v_ema_arti1 == 1 and v_adx_arti1==1:
                    print('Sembol (ALIM ) = ', v_symbol, 'Son Fiyat = ', v_son_fiyat, 'De??i??im', str(v_change_1m),
                          'Zaman=', datetime.now())
                    v_return_coin = v_symbol
                    v_interval = '1m'
                    break
                else:
                    print('Bu coin uygun de??il = ', v_symbol, 'Zaman', datetime.now())
                    v_return_coin = 'XXX'
                    v_interval = '1m'
            if v_4h_olusmadi == 1 and v_2h_olusmadi == 1 and v_1h_olusmadi == 1 and v_15m_olusmadi == 1 \
                    and v_5m_olusmadi == 1 and v_3m_olusmadi == 1 and v_1m_olusmadi == 0:
                if v_change_1m >= v_degis_oran and v_ema_arti1 == 1 and v_adx_arti1==1:
                    print('Sembol (ALIM ) = ', v_symbol, 'Son Fiyat = ', v_son_fiyat, 'De??i??im', str(v_change_1m),
                          'Zaman=', datetime.now())
                    v_return_coin = v_symbol
                    v_interval = '1m'
                    break
                else:
                    print('Bu coin uygun de??il = ', v_symbol, 'Zaman', datetime.now())
                    v_return_coin = 'XXX'
                    v_interval = '1m'
    dosya.close()
    return v_return_coin, v_son_fiyat, v_interval

# ******************************************************************************
def Coin_Al(v_symboly, v_last_price, v_interval):
    # DB_transactions.Table_create()
    v_time = str(datetime.now())
    v_time = v_time[0:19]
    v_times = v_time
    # ******TELEGRAM MESAJI ********************
    v_mess = ' Tuttum Seni (1) =' + 'Coin = ' + v_symboly + ' Buy Price =' + str(v_last_price) + ' Saat = ' + v_time
    # if v_time_bef != v_time:  # Ayn?? period (dk ) i??inde 2 defa mesaj atmas??n?? engellemek i??in
    Telebot_v1.mainma(v_mess)
    # v_time_bef = v_time
    # Trade_Logs tablosuna kay??t att??
    DB_transactions.Add_value(v_symboly, v_interval, v_last_price, v_time, v_time, None, None, None, 'TIP-1', None)
#    v_alim_var = 1
#    return  v_alim_var
# **************************************************************************
def Coin_Sat(v_symboly, v_last_price, v_interval):
    # ????erde al??m varsa bunu 2 t??rl?? satars??n , ya karla ya da STOP (zararla)
    # Al???? fiyat??n?? ??ekme
    global v_time_bef, v_time_befs
    v_time_bef, v_time_befs = '2022-10-10 10:24', '2022-10-10 10:24'
    #global v_satim
    v_tip = 'TIP-1'
    v_alis = DB_transactions.Select_Table(v_symboly,v_tip)
    v_alis_k = v_alis * 1.004
    v_alis_z = v_alis * 0.98
    v_time = str(datetime.now())
    v_time = v_time[0:19]
    v_times = v_time

    # G??ncel fiyat?? ????renme
    # v_change_1m, v_son_fiyat ,v_adx_cross_up7, v_ema_cross_up7 = kar_orani_y(v_symboly, '1m', 500, v_client)
    v_change_3m, v_son_fiyat, v_adx_cross_up7, v_adx_cross_down7, v_ema_cross_up7, v_ema_cross_down7, v_adx_arti7, v_ema_arti7 = kar_orani_y(
        v_symboly, '1m', 500, v_client)

    # Karla Sat????
    # if v_son_fiyat > v_alis_k:  # %0.1 kar g??rd??nm?? satacak

    if (v_ema_cross_down7 == True) or (v_son_fiyat > v_alis_k)  or (v_son_fiyat < v_alis_z) : # 1 dk l??kta EMA5 - EMA20 ters kesince veya %1 kar g??r??nce sat
        if v_son_fiyat > v_alis:
            v_mess_s = ' Karla Satti =' + 'Coin = ' + v_symboly + ' Alis Fiyat =' + str(
                v_alis) + ' Satis Fiyat =' + str(v_son_fiyat) + ' Saat = ' + v_times
            v_aciklama = 'Karla satti'
            v_result = 'Kar'
            v_kar_zarar_oran = ((v_alis - v_son_fiyat) * 100) / v_son_fiyat
        elif v_son_fiyat < v_alis:
            v_mess_s = ' STOP oldu =' + 'Coin = ' + v_symboly + ' Alis Fiyat =' + str(v_alis) + ' Satis Fiyat =' + str(
                v_son_fiyat) + ' Saat = ' + v_times
            v_aciklama = 'STOP oldu'
            v_result = 'Zarar'
            v_kar_zarar_oran = ((v_son_fiyat - v_alis) * 100) / v_alis

        v_sell_price = v_son_fiyat
        # **********Telegram Mesaj??
        if v_time_bef != v_time:  # Ayn?? period (dk ) i??inde 2 defa mesaj atmas??n?? engellemek i??in
            Telebot_v1.mainma(v_mess_s)
            v_time_bef = v_time
        # Telebot_v1.mainma(v_mess_s)
        # DB ye kay??t
        DB_transactions.Update_Table(v_symboly, v_sell_price, v_result, v_kar_zarar_oran, v_times,v_tip)
        # Yeni bir coin alabilmek i??in parametreyi bo??alt??yoruz
        v_satim = 1
        # Trade_Logs tablosuna kay??t att??
        DB_transactions.Add_Log(v_symboly)
        # Ana i??lem yapt?????? Temp tabloyu sil ve Logu maine at..Trade_Logsu sil
        DB_transactions.Delete_Table(v_symboly,v_tip)
    else:
        v_satim = 0
        print('ALIM BEKLET??L??YOR !!! ', v_son_fiyat)
        # DB_transactions.Add_value(symbol, interval, 12, v_time, v_time, 33, 'Kar', 1, '????leme Girmedi',None)
        # al??m yapabilirsiniz (0.1 miktar??nda market ya da limit al??m emri girebiliriz):
        # buy_order = connection.client.order_market_buy(symbol=symbol, quantity=0.1)
    return v_satim
# *********************************************************************
def kar_orani_y(v_symbol, v_interval, v_limit,
                v_client):  # , v_period, v_buy_price, v_buy_time, v_date, v_sell_price, v_result, v_percent, v_desc,v_sell_time):
    # print('symbol', v_symbol, ' priceChange = ', str(v_priceChangePercent), 'priceChangePercent = ', str(v_priceChange))
    klines = v_client.get_klines(symbol=v_symbol, interval=v_interval, limit=v_limit)
    open = [float(entry[1]) for entry in klines]
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]
    # ----Yeni sat????a ????kan coinde 4h, 1h, 15dk vs de??erler olmad?????? i??in hata veriyordu.
    # O nedenle ??nce uzunlu??unu al??p olu??up olu??mad??????n?? kontrol ediyoruz. Olu??tuysa program ilerliyor
    v_uz = len(close)
    # print('dizu = ', v_uz)
    if v_uz < 2:
        return 0, 0, False, False, False, False, 0, 0
    # --------------------------------------------------
    last_closing_price = close[-1]
    previous_closing_price = close[-2]
    close_array = np.asarray(close)
    close_finished = close_array[:-1]
    high_array = np.asarray(high)
    high_finished = high_array[:-1]
    low_array = np.asarray(low)
    low_finished = low_array[:-1]
    # print('anl??k kapan???? fiyat??', last_closing_price, ', bir ??nceki kapan???? fiyat??',          previous_closing_price, 'closed_finished = ')

    # ******************    ADX
    # plus di ve minus di de??erleri bir ??nceki ??ubu??un de??erlerini al??yor.G??ncellemeyi yeni 1 dk ba??lad??ktan sonra yap??yor !!!!!!!!!!!!!!!!!!!!!!!1
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
    v_oran = ((last_closing_price - previous_closing_price) * 100) / previous_closing_price
    v_f_oran = float(v_oran)

    return v_f_oran, last_closing_price, adx_cross_up, adx_cross_down, ema_cross_up, ema_cross_down, adx_arti, ema_arti


# *****************************************************************************************
if __name__ == '__main__':
    print('Ba??lang???? =', datetime.now())
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
    global v_satim
    v_satim = 0
    global v_4h_olusmadi
    global v_2h_olusmadi
    global v_1h_olusmadi
    global v_15m_olusmadi
    global v_5m_olusmadi
    global v_3m_olusmadi
    global v_1m_olusmadi
    v_4h_olusmadi = 0
    v_2h_olusmadi = 0
    v_1h_olusmadi = 0
    v_15m_olusmadi = 0
    v_5m_olusmadi = 0
    v_3m_olusmadi = 0
    v_1m_olusmadi = 0

while True:
    # 10 saniye bekliyoruz. S??rekli srgu g??ndermeye gerek yok.
    # time.sleep(2)
    #v_alim_var =1 # Test i??in bazen 1 yap??yoruz
    try:
        # ????erde al??m yoksa yeni coin bul
        if v_alim_var == 0:
            print('????erde al??m yok !!!!  ', v_alim_var)
            # Uygun coini bul
            v_bulunan, v_last_price, v_inter = Coin_Bul()
            # ---------------------------------------------
            if v_bulunan != 'XXX':
                print('Uygun Coin Bulundu', datetime.now(), 'Bulunan = ', v_bulunan, 'Last Price = ', v_last_price)
                # Al??m Yap??l??yor
                Coin_Al(v_bulunan, v_last_price, v_inter)
                # ---------------------------------------------
                v_alim_var = 1
            else:
                print('Dosyada uygun coin yok', datetime.now())
                v_alim_var = 0
        if v_alim_var == 1:
            print('Al??m Yap??lm???? Sat?????? Bekleniyor = ', v_bulunan ,  str(v_alim_var))
            v_satim = Coin_Sat(v_bulunan, v_last_price, v_inter)
            # ---------------------------------------------
            if v_satim == 1:
                print(v_bulunan , ' Coin Sat??ld??. Yeniden coin bulunacak ', str(v_satim))
                v_alim_var = 0
    except Exception as exp:
        print('Hataa!! = ', v_bulunan, 'Hata Kodu = ', exp)
    # print(exp.status_code, flush=True)
    # print(exp.message, flush=True)
