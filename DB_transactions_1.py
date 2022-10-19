import  sqlite3
con = sqlite3.connect("TRADE.db")
cursor = con.cursor()

def Table_create():
    cursor.execute("CREATE TABLE IF NOT EXISTS Trade_Logs_1 (Coin_name TEXT, Period TEXT , "
                   "Buy_Price REAL, Buy_Time TEXT, Date_System TEXT, Sell_Price REAL, Result TEXT , Percent REAL, Desc_coin TEXT, Sell_Time TEXT) ")
    con.commit()

def Table_create1():
    cursor.execute("CREATE TABLE IF NOT EXISTS Trade_Logs_Main_1 (Coin_name TEXT, Period TEXT , "
                   "Buy_Price REAL, Buy_Time TEXT, Date_System TEXT, Sell_Price REAL, Result TEXT , Percent REAL, Desc_coin TEXT, Sell_Time TEXT) ")
    con.commit()

def Add_value(v_name, v_period, v_buy_price, v_buy_time, v_date, v_sell_price, v_result, v_percent, v_desc, v_sell_time):
    my_data=(v_name, v_period, v_buy_price, v_buy_time, v_date, v_sell_price, v_result, v_percent, v_desc,v_sell_time)
    my_query="INSERT INTO Trade_Logs_1 values(?,?,?,?,?,?,?,?,?,?)"
    cursor.execute(my_query,my_data)
    con.commit()

def Add_Log(v_name):
    #my_query="INSERT INTO Trade_Logs_Main values(?,?,?,?,?,?,?,?,?,?)"
    my_query="INSERT INTO Trade_Logs_Main_1(Coin_name, Period, Buy_Price, Buy_Time, Date_System, Sell_Price, Result, Percent, Desc_coin,Sell_Time) SELECT Coin_name, Period, Buy_Price, Buy_Time, Date_System, Sell_Price, Result, Percent, Desc_coin, Sell_Time  FROM Trade_Logs  WHERE  Coin_name = ?"
    my_data = (v_name)
    cursor.execute(my_query,[my_data])
    con.commit()

#def Update_Table(v_name, v_period, v_buy_price, v_buy_time, v_date, v_sell_price, v_result, v_percent, v_desc,v_sell_time):
def Update_Table(v_name,v_sell_price, v_result, v_percent, v_sell_time,v_tip):
    my_query="UPDATE Trade_Logs_1 SET Sell_Price=? ,Sell_Time=?, Result=?, Percent=? WHERE Coin_name =? and Desc_coin=? "
    columnValues = (v_sell_price,v_sell_time,v_result, v_percent,v_name,v_tip)
    cursor.execute(my_query,columnValues)
    con.commit()

def Delete_Table(v_name,v_tip):
    my_query="DELETE FROM Trade_Logs_1 WHERE Coin_name =? and Desc_coin =?"
    mydata = (v_name,v_tip)
    #cursor.execute(my_query,[mydata])
    cursor.execute(my_query, (mydata))
    con.commit()

def Select_Table(v_name,v_tip): #, v_period, v_buy_price, v_buy_time, v_date, v_sell_price, v_result, v_percent, v_desc,v_sell_time):
    my_query="SELECT Buy_Price FROM Trade_Logs_1 WHERE Coin_name =? and Desc_coin = ?"
    cursor.execute(my_query,(v_name,v_tip))
    #print("Reading single row \n")
    record = cursor.fetchone()
    #print("Buyolan: ", record[0])
    v_buy = record[0]
    #print('Buuuu', str(v_buy))
    #cursor.close()
    return v_buy

if __name__ == '__main__':
    Table_create()
    Table_create1()
    #Delete_Table('CFXUSDT', 'TIP-1')
    # v_deg = Select_Table('CFXUSDT','TIP-1 ')
    # print('alışş ',v_deg)
    #Add_value('sym', '3m',0.8,'zaman','cdsfcsd',0, 'Kar', 1, 'Atutuutuuttuula')
    #Add_value()
    #Select_Table('AVAXUSDT')
    #Update_Table('AVAXUSDT', 17, 'Kar', 1,'202020')

    # v_alis = Select_Table('AVAXUSDT')
    # v_alis = str(v_alis)



