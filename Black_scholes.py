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

Future improvments, ensure better error & edge case handling, adapt project with streamlit.
"""

import numpy as np
import yfinance as yf
import math
from datetime import datetime


def cumulative_dist(d_):
    """ Cumulative dist function for a standard normal distribution, 
    the intergral doesn't have a simple algebraic solution, so use error function for a aproximation """
    return 0.5*(1+math.erf(d_/np.sqrt(2)))


def call_black_scholes(S,K,T,sigma,r):

    d1 = (np.log(S/K) + (r + (sigma**2/2))*T)/(sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    c = S * cumulative_dist(d1) - np.exp(-r*T) * K * cumulative_dist(d2)

    return c



def get_sigma(contract_symbol):
    # Come back to the function as still trust data too much
    ticker = contract_symbol.split('2')[0]
    expiry =f"20{contract_symbol[4:6]}-{contract_symbol[6:8]}-{contract_symbol[8:10]}"
    strike=float(contract_symbol[-8:]) / 1000
    cp = 'calls' if 'C' in contract_symbol else 'puts'

    chain = yf.Ticker(ticker).option_chain(expiry)
    df = chain.calls if cp == 'calls' else chain.puts

    matches = df[df['strike'] == strike]
    if len(matches) == 1:
        iv = matches['impliedVolatility'].iloc[0]
        if iv == 0.500005:
            raise ValueError("Invalid IV")
        return iv
    else:
        raise ValueError("Either not matchs found or multiple matchs found.")


def get_r():
    """ Getting the risk free interest rate, represented by long term government bonds. Closest real world example of a risk free interest rate. 
    Using ^IRX which is the ticker for a 13 week treasury bill, good in short term but change if start to trade options in different time period """
    bond_data =  yf.download('^IRX',period='1d',progress=False)
    # Remove the useless '^IRX' level
    if bond_data.columns.nlevels > 1:
        bond_data.columns = bond_data.columns.droplevel(1)

    # Not using period as bonds stable
    return bond_data['Close'].iloc[-1]/100



def get_s(contract_symbol):
    """ Getting the current stock price """
    given_stock = yf.Ticker(contract_symbol.split('2')[0])
    return given_stock.info['currentPrice']



def get_k(contract_symbol):
    """ Getting strike price for the given option, C or P displayed in the contract symbol, 
    denoting whether a call or put """
    if 'C' in contract_symbol:
        strike_string = contract_symbol.split('C')
        strike_string = strike_string[-1]
    elif 'P' in contract_symbol:
        strike_string = contract_symbol.split('P')
        strike_string = strike_string[-1]
    else:
        return "Invalid contract symbol given."
    try:
        # Padded with 00 on each side
        strike_price = float(strike_string)/1000
        return strike_price
    except ValueError:
        return "Could not convert contract symbol into interger."


def get_T(contract_symbol):
    expiry_str = contract_symbol[4:10]
    expiry = datetime(2000+int(expiry_str[:2]),int(expiry_str[2:4]),int(expiry_str[4:6]))
    today = datetime.today()
    T = (expiry - today).days / 365.25
    if T <=0:
        raise ValueError('Option expired')
    return T


contract_symbol = 'AAPL251121C00115000' # Ensure option valid.

c = call_black_scholes(S=get_s(contract_symbol), K=get_k(contract_symbol), T=get_T(contract_symbol), r=get_r(), sigma=get_sigma(contract_symbol))
print(round(c,4))

