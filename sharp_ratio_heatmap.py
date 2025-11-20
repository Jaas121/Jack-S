"""
Date: 18/11/25
Author: Jack Slaughter

Program will show the sharpe ratio as a heatmap comparing proportans of 2 stocks making up a portfolio 

We're using proportans of 2 stocks making up a portfolio, so will use proportan as x axes and y the lookback period (incrementing by 30 days)
It's important to note what having the lookback period on the y axes tells us.......

sharpe ratio = (expected return - risk free rate) / volitlity of portfolio

"""

import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from datetime import datetime,timedelta
import pandas as pd



ticker1 = 'AAPL'
ticker2 = 'MSFT'


def get_daily_returns(ticker,lookback):
    """ Returns daily returns, called for expected_retur function and for finding correlation (rho) """
    end = datetime.today()
    start = end - timedelta(lookback)
    # Progress = False, gets rid of the progress bar which is automaticly printed
    price_data = yf.download(ticker,start=start,end=end,progress=False).dropna()

    return price_data['Close'].pct_change().dropna()


def expected_return(ticker,lookback):
    """ Yfinance does not have an expected return function, so we will find the mean of past returns, over the last 2 years """
    daily_returns = get_daily_returns(ticker,lookback)
    ave_annual_returns = daily_returns.mean()*252

    return ave_annual_returns



def risk_free_rate():
    """ Using NZ bond for the risk free rate """
    bond_data =  yf.download('NGB.NZ',period='5d',progress=False)
    # Not using period as bonds stable
    return bond_data['Close'].iloc[-1]/100



def std_deviation(ticker,lookback):
    """ Getting std deviation which represents the volitilty of the portfolio"""
    end = datetime.today()
    start = end - timedelta(lookback)
    price_data = yf.download(ticker,start=start,end=end,progress=False)
    price_data['Daily_Return'] = price_data['Close'].pct_change()
    daily_std_dev = price_data['Daily_Return'].std()

    # Sigma(annual) = Sigma(daily) * sqrt(252)
    return daily_std_dev * np.sqrt(252)




def get_sharp_matrix():
    """ Function gets the matrix data for the sharp ratio heatmap, matrix represented by arrays in an array """
    matrix = np.zeros((10,10))

    LOOKBACK_STEP = 30
    WEIGHT_STEPS = 10

    # rf constant
    rf = risk_free_rate()

    for lb in range(1,11):
        lookback = lb * LOOKBACK_STEP
        # Getting information or either stock
        exp1 = expected_return(ticker1,lookback).iloc[0]
        std1 = std_deviation(ticker1,lookback)
        exp2 = expected_return(ticker2,lookback).iloc[0]
        std2 = std_deviation(ticker2,lookback)

        # Fill out rows, so need to factor in proporton
        for w in range(1,11):
            weight1 = w / WEIGHT_STEPS
            weight2 = 1 - weight1

            portfolio_return = exp1*weight1 + exp2*weight2
            # Now taking into account the correlation of the 2 assets

            # daily_returns_ticker1 = get_daily_returns(ticker1,lookback)
            # print(f"daily_returns_ticker1: {daily_returns_ticker1}")
            # daily_returns_ticker2 = get_daily_returns(ticker2,lookback)
            # print(f"daily_returns_ticker2: {daily_returns_ticker2}")
            # correlation = daily_returns_ticker1.corr(daily_returns_ticker2)

            # portfolio_std = np.sqrt(std1**2*weight1**2 + std2**2*weight2**2 + 2*weight1*weight2*std1*std2*correlation)

            portfolio_std = std1*weight1 + std2*weight2



            sharp = (portfolio_return - rf) / portfolio_std

            matrix[lb-1,w-1] = sharp
    return matrix


def main():
    data = get_sharp_matrix()

    # imshow displays the greyscale image
    plt.imshow(data,cmap='jet',origin='lower',aspect='auto')
    plt.colorbar(label='Sharpe Ratio')
    plt.title(f'Sharpe Ratio Heatmap - {ticker1} vs {ticker2}')

    plt.xlabel(f"Weight of {ticker1} in portfolio")
    plt.xticks(ticks=range(10),labels=['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])

    plt.ylabel("Lookback period")
    plt.yticks(ticks=range(10),labels=['30 days','60 days','90 days','120 days','150 days','180 days','210 days','240 days','270 days','300 days'])

    plt.show()


main()
