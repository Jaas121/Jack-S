""" 
Author:
Date:

Important to note that all greeks can be found with the finite difference calcuation (I like thinking of this as manually finding gradient),
change in option price will always be ontop (denoted partial V)

"""


# Starting with the firt order greeks
def delta(opt_p_before,opt_p_after,asset_p_before,asset_p_after):
    """ Delta messures the change in option price to the change in the underlying asset price.
    Position with positive delta increases in price when underlying asset price increases
    
    Delta netural position, where portfolio delta 0, processes required to maintain this position dynamic hedging,
    this position hedges against risk, protecting portfolio from market volatility, which can focus on other factors effecting options value (e.g. theta, vega & etc)

    """
    opt_change = opt_p_after-opt_p_before
    asset_change = asset_p_after-asset_p_before
    return opt_change/asset_change

def vega(opt_p_before,opt_p_after,vol_before,vol_after):
    """ Vega messures the sensitivity to volatility """
    opt_change = opt_p_after - opt_p_before
    vol_change = vol_after - vol_before
    return opt_change/vol_change

def theta(opt_p_before,opt_p_after,time_before,time_after):
    """ Theta messure the sensitivity of value to change in time (time decay) """
    opt_change = opt_p_after - opt_p_before
    time_change = time_after - time_before
    return opt_change/time_change

def rho(opt_p_before,opt_p_after,rate_before,rate_after):
    """ Rho is the sensitivity to intreset rates """
    opt_change = opt_p_after - opt_p_before
    rate_change = rate_after - rate_before
    return opt_change/rate_change

def lam(opt_p_before,opt_p_after,asset_p_before,asset_p_after,v_final):
    """ i.e. omega or elasticity, delta but expressed in percentage terms rather than abs terms"""
    lam = delta(opt_p_before,opt_p_after,asset_p_before,asset_p_after) * v_final/asset_p_after
    return lam

def epsion(opt_p_before,opt_p_after,dividend_before,dividend_after):
    opt_change = opt_p_after - opt_p_before
    div_change = dividend_after - dividend_before
    return opt_change/div_change

# Higher order greeks are the sensitivity of the first order greeks to those same parameters