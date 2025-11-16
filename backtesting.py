import vectorbt as vbt
import yfinance as yf
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

start = '2024-11-16'
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
    print(f"Total return for statergy: {pf.total_return()}")  

    # Note for getting trades made
    trades = pf.trades.records_readable

    return pf.value()


def sandp_values():
    # Getting S&P500 (SPY) to compare to backtester
    price_spy = vbt.YFData.download('SPY',start=start,end=end,interval='1d').get('Close')

    pf_sandp = vbt.Portfolio.from_holding(
        price_spy,
        init_cash=10_000,
    )

    return pf_sandp.value()



ticker='AAPL'

# Plotting curves
plt.plot(pf_strategy_values(ticker))
plt.plot(sandp_values())
plt.title(f"Investment in SPY (orange) vs DMAC with {ticker} (blue)")
plt.ylabel('$$$$$')
plt.xlabel('Time')
plt.show()


