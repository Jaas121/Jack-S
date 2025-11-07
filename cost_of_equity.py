""" Finding cost of equity for APPL, COE = Rf + B(Mr - Rf) """
import yfinance as yf


# Will use download, which is a clean way to lay things out
# Need the market rate so, will use S&P500 average historical returns for the last 6 months  
start_date='2025-5-1'
end_date='2025-11-7'


sandp_data=yf.download('^GSPC',start=start_date,end=end_date,progress=False)
# Calculating annual returns
# First daily returns
sandp_data['daily_return'] = sandp_data['Close'].pct_change()
market_return_annual = sandp_data['daily_return'].mean() * 252 # 252 trading days in a year
# Estimated annual market return
market_rate = round(market_return_annual*100,2)



# Risk free rate, typicaly based on government bonds, i.e. investments with 0 risk
# using ^IRX, which is a 13 week treasury week bill, matchs up with the 6 month period
bond_data =  yf.download('^IRX',period='1d',progress=False)

# Remove the useless '^IRX' level
if bond_data.columns.nlevels > 1:
    bond_data.columns = bond_data.columns.droplevel(1)


# Not using period as bonds stable
risk_free_rate = bond_data['Close'].iloc[-1]/100
risk_free_rate_percent = round(risk_free_rate*100,2)


# Beta of APPLs
aapl=yf.Ticker('AAPL')
beta=aapl.info['beta']

# Cost of equity 
cost_of_equity = risk_free_rate + beta*(market_return_annual-risk_free_rate)
cost_of_equity_percent = round(cost_of_equity*100,2)




print("********************")
print(f"S&P 500 6-month return: {market_rate}%")
print(f"Risk-Free Rate (^IRX today): {risk_free_rate_percent}%")
print(f"AAPL Beta: {beta:.3f}")
print(f"Market Risk Premium: {round((market_return_annual - risk_free_rate)*100, 2)}%")
print(f"COST OF EQUITY FOR AAPL = {cost_of_equity_percent}%")
print("********************")