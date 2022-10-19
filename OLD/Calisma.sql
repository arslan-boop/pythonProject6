DELETE FROM Trade_Logs_Main

DELETE FROM Trade_Logs


COMMIT

INSERT into Trade_Logs_Main(Coin_name,Period, Buy_Price,Buy_Time,Date_System,Sell_Price,Result,Percent,Desc_coin,Sell_Time)
SELECT Coin_name,Period, Buy_Price,Buy_Time,Date_System,Sell_Price,Result,Percent,Desc_coin,Sell_Time
from  Trade_Logs
WHERE Coin_name = 'PHAUSDT'

NSERT INTO Trade_Logs_Main(Coin_name, Period, Buy_Price, Buy_Time, Date_System, Sell_Price, Result," \
             "Percent, Desc_coin,Sell_Time) " \
             "SELECT   Coin_name, Period, Buy_Price, Buy_Time, Date_System, Sell_Price, Result, " \
             "Percent, Desc_coin, Sell_Time " \
             "FROM Trade_Logs  WHERE  Coin_name = ?

SELECT * from Trade_Logs

SELECT * from Trade_Logs_Main


drop TABLE Trade_Logs_Main

INSERT INTO Trade_Logs_Main(Coin_name, Period, Buy_Price, Buy_Time, Date_System, Sell_Price, Result,
 Percent, Desc_coin,Sell_Time) SELECT Coin_name, Period, Buy_Price, Buy_Time, Date_System, Sell_Price, 
 Result, Percent, Desc_coin, Sell_Time  FROM Trade_Logs  WHERE  Coin_name = 'PHAUSDT'

