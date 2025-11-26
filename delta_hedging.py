"""
Author: Jack Slaughter
Date: 25/11/25

Delta hedging is ensuring portfolio is delta-neutral, (Delta is sensitivity of an options price to the underlying asset price),
it's important as it hedges portfolio against changes in the underlying asset price.

Considerations:
    Ensuring portfolio is not over rebalanced, due transaction.
    Complexity of portfolio.
    External market conditions.
"""

import math
import numpy as np

# Ensure portfolio is not over rebalanced
LEEWAY = 0.25

s = 100
k = 75
t = 0.5
sigma = 0.1
r = 0.2

# How many option contracts held, & how many stocks make up an option 
contracts = 10 
shares_per_contract = 100 
position_type = 'short call'  


def cumulative_dist(d):
    """ Cumulative dist function for a standard normal distribution, 
    the intergral doesn't have a simple algebraic solution, so use error function for an aproximation """
    return 0.5*(1+math.erf(d/np.sqrt(2)))

def bs_call_delta(S,K,T,sigma,r):
    d1 = (np.log(S/K) + (r + (sigma**2/2))*T)/(sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    c = S * cumulative_dist(d1) - np.exp(-r*T) * K * cumulative_dist(d2)
    return c

def bs_put_delta(S,K,T,sigma,r):
    return bs_call_delta(S,K,T,sigma,r)-1


def option_delta(s,k,t,sigma,r,position_type):
    """ Getting delta with the black scholes """
    # Adjust for call or put
    if 'call' in position_type:
        delta_per_share = bs_call_delta(s,k,t,sigma,r)
    elif 'put' in position_type:
        delta_per_share =  bs_put_delta(s,k,t,sigma,r)
    else:
        return ValueError("Option_type must be either call or put")
    sign = -1 if 'short' in position_type else 1
    return sign * delta_per_share




def get_portfolio_delta():
    """ w """
    delta_per_contract = option_delta(s,k,t,sigma,r,position_type)
    total_delta_contracts = delta_per_contract*contracts
    total_delta_shares = total_delta_contracts*shares_per_contract
    return ({
    'per_contract':delta_per_contract,
    'total_contracts':total_delta_contracts,
    'total_shares':total_delta_shares})


def adjusting_hedge():
    """ Whenever delta moves from zero, executes buying or selling trade to re-establish delta neutrality 
    note: inlude option type
    """
    portfolio_delta = get_portfolio_delta()
    total_shares_delta = portfolio_delta['total_shares']
    tolerance_shares = LEEWAY * shares_per_contract


    if abs(total_shares_delta) <= tolerance_shares:
        print(f"Within threshold ({tolerance_shares}) no trade needed")
        return

    # Go in the opposite direction 
    shares_to_cancel = -total_shares_delta

    action = 'Buy' if shares_to_cancel<0 else 'Sell'
    print(f"{action} {abs(round(shares_to_cancel))} to be delta neutral")
    


adjusting_hedge()