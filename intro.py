import yfinance as yf
import pandas as pd

"""
Don't judge this file, note taking for the basics 
"""

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



def multi_tickers():
    # Now using pandas 
    tickers_list = ["aapl", "goog", "amzn"]
    tickers_data= {} # empty dictionary (we'll put the final informtaion in here)

    for ticker in tickers_list: # For all out tickers in list
        ticker_object=yf.Ticker(ticker)

        # Most of the time you can just use, pdDataFrame()
        # Convert info into dataframe
        temp= pd.DataFrame.from_dict(ticker_object.info,orient="index")
        temp.reset_index(inplace=True)
        temp.columns = ['Attribute','Recent']
        tickers_data[ticker]=temp

    # We can combine this dictonary of dataframes into single data frame 
    combined_data = pd.concat(tickers_data)
    combined_data = combined_data.reset_index() # Important as without each stock would have its own indices. i.e. flattens the muliindex the concat ceates
    del combined_data['level_1'] # Deleting unnesseory 'level_1' column
    combined_data.columns= ['Ticker','Attribute','Recent'] # New column names

    print(combined_data)


def getting_important_info():
    aapl=yf.Ticker("AAPL")

    # print(f"marketCap: {aapl.info["marketCap"]}")
    print(f"volume: {aapl.info['volume']}")
    print(f"averageVolume: {aapl.info['averageVolume']}")
    print(f"averageVolume within 10 days: {aapl.info['averageVolume10days']}")


    # print(aapl.history(period='max',interval='1wk'))
    # To get singuler columns
    print(aapl.history(period='max',interval='1wk'))




def options_basics():
    # Options give the trader the right but not the abolgation to buy an underlying asset 
    aaple=yf.Ticker('AAPL')
    for i in aaple.options:
        print(i)

    # Contains range of relevent information
    aaple.option_chain()


def getting_calls():
    aapl=yf.Ticker('AAPL')
    # Getting option calls for a spesific date, yyyy/mm/dd
    opt = aapl.option_chain(date='2025-11-14')
    print(opt.calls)


# Puts are pretty much the same
def getting_puts():
    aapl=yf.Ticker('AAPL')
    opt=aapl.option_chain()
    print(opt.puts)



getting_calls()