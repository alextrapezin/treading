import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import talib

# data = yf.download(
#     "SPY AAPL",
#     start="2020-05-01",
#     end="2020-05-14",
#     interval="1d",
#     group_by='ticker',
#     auto_adjust=True,
#     prepost=True,
#     threads=True,
#     proxy=None
# )
#print(data)

aapl = yf.Ticker('FB')

aapl_history = aapl.history(start='2019-05-14', end='2020-05-14')
print(aapl_history)

# https://ta-lib.org/

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 8))

# ATR
tt = []
for k, v in talib.ATR(aapl_history['High'], aapl_history['Low'], aapl_history['Close']).items():
    tt.append(['ATR', k, v])


df = pd.DataFrame(tt, columns=['type', 'date', 'value'])
df.pivot(index='date', columns='type', values='value').plot(ax=axes[0][0])

# SME
tt = []
for k, v in aapl_history['Close'].items():
    tt.append(['close', k, v])
for k, v in talib.SMA(aapl_history['Close'], timeperiod=20).items():
    tt.append(['SMA_20', k, v])
for k, v in talib.SMA(aapl_history['Close'], timeperiod=50).items():
    tt.append(['SMA_50', k, v])

df = pd.DataFrame(tt, columns=['type', 'date', 'value'])
df.pivot(index='date', columns='type', values='value').plot(ax=axes[0][1])

# MACD
tt = []
macd, macdsignal, macdhist = talib.MACD(aapl_history['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
for k, v in macd.items():
    tt.append(['macd', k, v])
    tt.append(['zero', k, 0])
for k, v in macdsignal.items():
    tt.append(['macdsignal', k, v])

df = pd.DataFrame(tt, columns=['type', 'date', 'value'])
df.pivot(index='date', columns='type', values='value').plot(ax=axes[1][0])

# RSI
tt = []
for k, v in talib.RSI(aapl_history['Close'], timeperiod=12).items():
    tt.append(['rsi_12', k, v])
    tt.append(['rsi_h', k, 55])
    tt.append(['rsi_l', k, 45])

df = pd.DataFrame(tt, columns=['type', 'date', 'value'])
df.pivot(index='date', columns='type', values='value').plot(ax=axes[1][1])
plt.show()
