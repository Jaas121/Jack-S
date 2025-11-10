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
sigma = volatility of stock 
r = risk free intrest rate

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




price = call_black_scholes(S=100, K=105, T=1, r=0.05, sigma=0.2)
print(price)