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


from Black_scholes import call_black_scholes,cumulative_dist


# Constant ensuring portfolio is not over rebalanced
LEEWAY = 0.25
s = 100
k = 75
t = 5
sigma = 0.1
r = 0.2



def black_scholes_delta(s,k,t,sigma,r,option_type='call'):
    """ Getting delta with the black scholes """

    # Adjust for call or put
    if option_type=='call':
        return call_black_scholes(s,k,t,sigma,r)
    else:
        return call_black_scholes(s,k,t,sigma,r)-1
    


print(black_scholes_delta(s,k,t,sigma,r))
print(black_scholes_delta(s,k,t,sigma,r,option_type='put'))



def hedge_ratio(hedge_position,exposure):
    """ Important in showing how much protection you're getting """
    return hedge_position/exposure



def adjusting_hedge():
    """ Whenever delta moves from zero, executes buying or selling trade to reestablish delta neutrality """
    current_delta = black_scholes_delta(s,k,t,sigma,r)

    # Within threshold
    if abs(current_delta) <= LEEWAY:
        return

    # Delta too low ---> buy
    if current_delta < -LEEWAY:
        # delta negitive, buy trade executed to get back to delta-neutral 
        diference = (current_delta)-LEEWAY

    # Not too low & not in leeway --> too high --> sell
    else:
        # delta positive, sell trade executed to get back to delta-neutral
        diference = current_delta-LEEWAY