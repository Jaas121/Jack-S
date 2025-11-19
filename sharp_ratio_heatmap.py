"""
Date: 18/11/25
Author: Jack Slaughter

Program will show the sharp ratio as a heatmap comparing proportans of 2 stocks making up a portfolio 

We're using proportans of 2 stocks making up a portfolio, so will use proportan as x axes and y the lookback period (incrementing by 30 days)
It's important to note what having the lookback period on the y axes tells us.......

sharp ratio = (expected return - risk free rate) / volitlity of portfolio

"""

import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from datetime import datetime,timedelta

# 10 rows and 10 columns of random data
# data = np.random.rand(10,10)





def expected_return(ticker,lookback):
    """ Yfinance does not have an expected return function, so we will the mean of past returns, over the last 2 years """
    end = datetime.today()
    start = end - timedelta(lookback)
    # Progress = False, gets rid of the progress bar which is automaticly printed
    price_data = yf.download(ticker,start=start,end=end,progress=False).dropna()
    daily_returns = price_data['Close'].pct_change().dropna()
    ave_annual_returns = daily_returns.mean()*252

    return ave_annual_returns



def risk_free_rate():
    """ Using NZ bond for the risk free rate """
    bond_data =  yf.download('NGB.NZ',period='5d',progress=False)
    # Not using period as bonds stable
    return bond_data['Close'].iloc[-1]/100



def std_deviation(ticker,lookback):
    """ Getting std deviation which represents the volitilty of the portfolio, over last 2 years """
    end = datetime.today()
    start = end - timedelta(lookback)
    price_data = yf.download(ticker,start=start,end=end,progress=False)
    price_data['Daily_Return'] = price_data['Close'].pct_change()
    daily_std_dev = price_data['Daily_Return'].std()

    # Sigma(annual) = Sigma(daily) * sqrt(252)
    return daily_std_dev * np.sqrt(252)








# # How to put into 10x10 grid


ticker = 'AAPL'


# Lookback incremented by 30 days
array=np.array([])
LOOKBACK = 30

# rf constant
rf = risk_free_rate().iloc[0]
# 
for i in range(1,11):
    expected = expected_return(ticker,LOOKBACK*i).iloc[0]
    std_dev = std_deviation(ticker,LOOKBACK*i)
    sharp = (expected-rf)/std_dev

    array = np.append(array,sharp)

print(array)


# # imshow displays the greyscale image
# plt.imshow(data,cmap='hot',origin='lower',aspect='auto')
# plt.colorbar(label='Intensity')
# plt.show()
