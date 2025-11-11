"""
10/11/25
Author: J Slaughter 


For a fair valuation of a option, equition is,

c = S N(d1) - Ke^(-rT) N(d2)

d1 = (ln(S/K) + (r + (sigma^2)/2)T)/sigma sqrt(T)

d2 = d1 - sigma sqrt(T)


S = current stock price
K = strike price
T = time to maturity 
sigma = volatility of a single assests price
r = risk free interest rate

Under the assumptions, no arbitrage, log normal prices etc
"""

import numpy as np
import yfinance as yf
import math

def cumulative_dist(d_):
    """ Cumulative dist function for a standard normal distribution, 
    the intergral doesn't have a simple algebraic solution, so use error function for a aproximation """
    return 0.5*(1+math.erf(d_/np.sqrt(2)))


def call_black_scholes(S,K,T,sigma,r):

    d1 = (np.log(S/K) + (r + (sigma**2/2))*T)/(sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    c = S * cumulative_dist(d1) - np.exp(-r*T) * K * cumulative_dist(d2)

    return c






# Getting sigma this way is incorrect, as sigma should represent the average future volitlity, so historical data can be used to estimate it 
def get_sigma_call(tickercode):
    aapl = yf.Ticker(tickercode)
    options_dates_list = aapl.options

    # Getting the most recent option date 
    recent_option_date = options_dates_list[0]
    opt_chain = aapl.option_chain(recent_option_date)

    # Options chain has call and put atrabutes which are both pandas dataframes
    calls_df = opt_chain.calls
    return calls_df['impliedVolatility'][0]



def get_sigma_put(tickercode):
    aapl = yf.Ticker(tickercode)
    options_dates_list = aapl.options

    # Getting the most recent option date 
    recent_option_date = options_dates_list[0]
    opt_chain = aapl.option_chain(recent_option_date)

    # Options chain has call and put atrabutes which are both pandas dataframes
    puts_df = opt_chain.puts
    return puts_df['impliedVolatility'][0]


def get_r():
    """ Getting the risk free interest rate, represented by long term government bonds. Closest real world example of a risk free interest rate. 
    Using ^IRX which is the ticker for a 13 week treasury bill, good in short term but change if start to trade options in different time period """
    bond_data =  yf.download('^IRX',period='1d',progress=False)
    # Remove the useless '^IRX' level
    if bond_data.columns.nlevels > 1:
        bond_data.columns = bond_data.columns.droplevel(1)

    # Not using period as bonds stable
    return bond_data['Close'].iloc[-1]/100


def get_s(ticker_code):
    """ Getting the current stock price """
    given_stock = yf.Ticker(ticker_code)
    return given_stock.info['currentPrice']



x = get_sigma_call("AAPL")
y = get_sigma_put("AAPL")
z = get_r()

print(f"Sigma for call: {x}")
print(f"Sigma for put: {y}")
print(f"Risk free rate, {z}")
print(f"Current price, {get_s('AAPL')}")
# price = call_black_scholes(S=100, K=105, T=1, r=0.05, sigma=0.2)
