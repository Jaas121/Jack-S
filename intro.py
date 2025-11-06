import yfinance as yf



# aia= yf.Ticker("AIA.nz")
# print(aia)



## .history is good for finding information about 1 company, more spesifics
# aia_historical = aia.history(start="2025-10-10", end="2025-11-05", interval="1d")
# print(aia_historical)



#  .download used for multiple tickers, returns a pandas data frame

# download(tickers, start=None, end=None, period="1y", interval="1d", group_by='column')
# data = yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
# print(data)



# To get a spesific bit of information from a stock 
appl=yf.Ticker('APPl')
print(appl.info['quoteType'])
print(appl.info)


