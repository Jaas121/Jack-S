""" 
9/10/2025
Author: J Slaughter

Finding cost of equity for APPL, COE = Rf + B(Mr - Rf) 
"""
import yfinance as yf


def find_rm(start_date='2025-5-1',end_date='2025-11-7'):
    # Need the market rate so, will use S&P500 average historical returns for the last 6 months  
    sandp_data=yf.download('^GSPC',start=start_date,end=end_date,progress=False)
    # Calculating annual returns
    # First daily returns
    sandp_data['daily_return'] = sandp_data['Close'].pct_change()
    # return annual market return
    return sandp_data['daily_return'].mean() * 252 # 252 trading days in a year


def find_rf():
    # Risk free rate, typicaly based on government bonds, i.e. investments with 0 risk
    # using ^IRX, which is a 13 week treasury week bill, matchs up with the 6 month period
    bond_data =  yf.download('^IRX',period='1d',progress=False)
    # Remove the useless '^IRX' level
    if bond_data.columns.nlevels > 1:
        bond_data.columns = bond_data.columns.droplevel(1)
    # Not using period as bonds stable
    return bond_data['Close'].iloc[-1]/100

def find_beta(ticker_code):
    # Beta of ticker
    return yf.Ticker(ticker_code).info['beta']



def find_cost_of_equity(ticker):
    # Cost of equity 
    try:
        # Can have start and end date paremters in rm, yyyy/mm/dd
        rm = find_rm()
        rf = find_rf()
        beta = find_beta(ticker)

        cost_of_equity = rf + beta*(rm-rf)
        return f"Cost of equity for {ticker}: {round(cost_of_equity*100,4)}%"
    except:
        return f"***Error, check if inputed ticker has a valid beta***"


print(find_cost_of_equity("AAPL"))

