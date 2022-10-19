import requests        # for making http requests to binance
import json            # for parsing what binance sends back to us
import pandas as pd    # for storing and manipulating the data we get back
import numpy as np     # numerical python, i usually need this somewhere
                       # and so i import by habit nowadays
symbol = "DOTUSDT"
interval =’15m’

Client.KLINE_INTERVAL_15MINUTE
klines = client.get_historical_klines(symbol, interval, "1 Jan,2021")
data = pd.DataFrame(klines)
# create colums name
data.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades',
                'taker_base_vol', taker_quote_vol', 'ignore']

                # change the timestamp
                data.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in data.close_time]
data.to_csv(symbol + '.csv', index=None, header=True)
# convert data to float and plot
df = df.astype(float)
df["close"].plot(title='DOTUSDT', legend='close')