"""
Date: 16/11/25
Author: Jack Slaughter

Program compares portfolio statergy of holding or DMAC (Dual moving average crossover) with given stock(s).
DMAC is a good trend filter but slowing and more lagging than some of the other strategies.
"""

import vectorbt as vbt
import matplotlib.pyplot as plt

start = '2020-11-16'
end = '2025-11-16'

def pf_strategy_values(ticker):
    aapl_price = vbt.YFData.download(ticker,start=start,end=end,interval='1d').get('Close')

    # Moving averages, using dual moving average crossover (DMAC)
    fast_ma = vbt.MA.run(aapl_price,10,short_name='fast')
    slow_ma = vbt.MA.run(aapl_price,20,short_name='slow')

    # Creating moving averages
    # Generating entry signals, True = signal to enter (buy)
    # Occouring when the 10 day MA crosses above the 20 day MA -> bullish sign
    entries = fast_ma.ma_crossed_above(slow_ma)
    # Exit signal, when the 20 day MA crosses back above the 10 day MA -> bearish sign
    exits = slow_ma.ma_crossed_above(fast_ma)

    # Backtesting with portfolio
    pf = vbt.Portfolio.from_signals(
        aapl_price,
        entries,
        exits,
        init_cash=10_000,
        fees=0.001,
        slippage=0.0005,
        direction='longonly')
    print(f"Total return for DMAC statergy on {ticker}: {pf.total_return()}")  

    # Note for getting trades made
    trades = pf.trades.records_readable

    return pf.value()



def pf_holding_values(ticker):
    # Getting holing to compare to backtester
    price_hold = vbt.YFData.download(ticker,start=start,end=end,interval='1d').get('Close')

    pf_hold = vbt.Portfolio.from_holding(
        price_hold,
        init_cash=10_000,
    )

    print(f"Total return for holding {ticker}: {pf_hold.total_return()}")  
    return pf_hold.value()


def main():
    tickers_strategy=['AAPL']
    tickers_holding=['AAPL']

    # Plotting curves
    for ticker in tickers_strategy:
        plt.plot(pf_strategy_values(ticker),label=f'{ticker} strategy')

    for ticker in tickers_holding:
        plt.plot(pf_holding_values(ticker),label=f'{ticker} holding')

    plt.title(f"Backtesting investments over 5 year period")
    plt.legend()
    plt.ylabel('$$$$$')
    plt.xlabel('Year')
    plt.show()
    
main()

