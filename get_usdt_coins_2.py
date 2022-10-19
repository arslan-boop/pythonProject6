import requests
import time
import json
import re
from pprint import pprint
from datetime import datetime
import sqlite3

con = sqlite3.connect("TRADE.db")
cursor = con.cursor()


def Sel_USDT(v_name):  # , v
    # Dosyaya açma
    v_semboldos = open("Sembol1.txt", "w")
    my_query = "SELECT name FROM USDT_COINS ORDER BY PRICE_CHANGE_PERCENT DESC "
    cursor.execute(my_query)
    i = 50
    record = cursor.fetchmany(i)  # .fetchall()
    for x in record:
        # print(x, 'kayıt= ', record[0])
        # Dosyaya Yazma ----------------------------
        y = str(x)
        y = y.replace("('", "")
        y = y.replace("',)", "")
        v_semboldos.write(y)
        v_semboldos.write("\n")
    # cursor.close()
    con.commit()


def File_write():
    Sel_USDT(1)


def Delete_USDT(v_name):
    my_query = "DELETE FROM USDT_COINS WHERE  1=? "
    mydata = (v_name)
    cursor.execute(my_query, [mydata])
    # cursor.execute(my_query,(mydata))
    con.commit()


def Add_USDT(v_name, v_last_price, v_price_change, v_price_change_percent, v_time):
    my_data = (v_name, v_last_price, v_price_change, v_price_change_percent, v_time)
    my_query = "INSERT INTO USDT_COINS values(?,?,?,?,?)"
    cursor.execute(my_query, my_data)
    con.commit()
# ---------------------------------------

def USDT_Tablo_Yaz():
    v_time = str(datetime.now())
    v_time = v_time[0:19]
    # Eski bilgileri sil
    Delete_USDT(1)
    # # Dosyaya açma
    # v_semboldos = open("Sembol.txt", "w")
    # #---------------------
    payload = {}
    headers = {
        'Content-Type': 'application/json'
    }

    url = "https://api.binance.com/api/v3/exchangeInfo"

    response = requests.request("GET", url, headers=headers, data=payload)
    markets = json.loads(response.text)
    active = {}
    for market in markets['symbols']:
        symbol = market['symbol']
        status = market['status']
        active[symbol] = status == 'TRADING'

    url = "https://api.binance.com/api/v3/ticker/24hr"

    response = requests.request("GET", url, headers=headers, data=payload)
    tickers = json.loads(response.text)
    i = 0
    prices = {}
    prices1 = {}
    prices2 = {}
    for ticker in tickers:
        symbol = ticker['symbol']
        if symbol == 'NBTUSDT':
            print('Eee')
        else:
            isUSDT = re.search("USDT$", symbol)
            if (isUSDT and active[symbol]):
                if ("UP" in symbol) or ("DOWN" in symbol):
                    print('kelime geçiyor')
                else:
                    i = i + 1
                    prices[symbol] = ticker['lastPrice']
                    prices1[symbol] = ticker['priceChange']
                    prices2[symbol] = ticker['priceChangePercent']
                    # Tabloya Yazma ----------------------------
                    Add_USDT(symbol, prices[symbol], prices1[symbol], prices2[symbol], v_time)
                    # # Dosyaya Yazma ----------------------------
                    # v_semboldos.write(symbol)
                    # v_semboldos.write("\n")
                    # #-----------------------------
                    print('Sembol =', symbol, 'lastPrice=', prices[symbol], 'priceChange', prices[symbol],
                          'priceChangePercent', prices2[symbol], str(i))
    # v_semboldos.close()

def Bekle():
    # run = raw_input("Start? > ")
    run = 1
    mins = 0
    # Only run if the user types in "start"
    if run == 1:
        # Loop until we reach 20 minutes running
        while mins != 2:
            print(">>>>>>>>>>>>>>>>>>>>>", mins)
            # Sleep for a minute
            time.sleep(5)
            # Increment the minute total
            mins += 1
        # Bring up the dialog box here
        print('2 dk geçti Başladı............')
    return mins


# *****************************************************
if __name__ == '__main__':
    print('Başladı............')
    while True:
        v_bekleme_dk = Bekle()
        if v_bekleme_dk == 2:
            v_time = str(datetime.now())
            v_time = v_time[0:19]
            print('Yenileyecek ............,=', v_time)
            v_semboldos = open("Sembol.txt", "w")

            USDT_Tablo_Yaz()
            File_write()

    #
    # while True:
    #     USDT_Tablo_Yaz()
    #     File_write()
    #     v_time = str(datetime.now())
    #     v_time = v_time[0:19]
    #     print('Tamamlandı............',v_time)
    #     time.sleep(10)
    #     v_time = str(datetime.now())
    #     v_time = v_time[0:19]
    #     print('Yenileyecek ............,=',v_time)
