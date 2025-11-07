import yfinance as yf
import pandas as pd


# aia= yf.Ticker("AIA.nz")
# print(aia)



## .history is good for finding information about 1 company, more spesifics
# aia_historical = aia.history(start="2025-10-10", end="2025-11-05", interval="1d")
# print(aia_historical)



#  .download used for multiple tickers, returns a pandas data frame

# download(tickers, start=None, end=None, period="1y", interval="1d", group_by='column')
# data = yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
# print(data)



# # To get a spesific bit of information from a stock 
# appl=yf.Ticker('APPl')
# print(appl.info['quoteType'])
# print(appl.info['beta'])
# print(appl.info.keys()) # shows you the aviable fields in appl can access safely 


# Now using pandas 
# tickers_list = ["aapl", "goog", "amzn"]
# tickers_data= {} # empty dictionary (we'll put the final informtaion in here)

# for ticker in tickers_list: # For all out tickers in list
#     ticker_object=yf.Ticker(ticker)

#     # Most of the time you can just use, pdDataFrame()
#     # Convert info into dataframe
#     temp= pd.DataFrame.from_dict(ticker_object.info,orient="index")
#     temp.reset_index(inplace=True)
#     temp.columns = ['Attribute','Recent']
#     tickers_data[ticker]=temp

# # We can combine this dictonary of dataframes into single data frame 
# combined_data = pd.concat(tickers_data)
# combined_data = combined_data.reset_index() # Important as without each stock would have its own indices. i.e. flattens the muliindex the concat ceates
# del combined_data['level_1'] # Deleting unnesseory 'level_1' column
# combined_data.columns= ['Ticker','Attribute','Recent'] # New column names

# print(combined_data)
