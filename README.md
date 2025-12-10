Whis this code does:
This code runs a simulation for a portfolio of TQQQ (3x nasdaq 100) combined with otm options on TQQQ.
It runs on historical nasdaq 100 data, and is calculated as though there would have been a leveraged etf 3x of it; it uses the 2.9269, which the regression model showed. 
It runs from 1985 to 2025, which is the max availible data. 
_____functions and walk through of the code____
Here's what the code looks like and does:
Imports: yfinance, to get historical data; pandas, to make dataframes which the calculations run on; and numpy.
The first function, download_data, downloads the data and creates the leveraged monthly returns, by multiplying the daily returns and then runnig them together. It returns the monthly returns of the leveraged etf.
The second function, rolling_annual_returns, calculates the rolling annual returns of the TQQQ. It does this for the begining of every month, and multiplies it together to get the annual returns. The function returns all the annual returns.
The third function, calculate_hedged_returns, calculates the portfolio, given the annual returns.
The model of the options payoff was made as follows (copied from my substack post about this, sorry about the change of tone):
I took a real TQQQ option: strike at 20, TQQQ price 52, expiration January 16, 2027, which was 13.7 months from purchase. The ask price was $2.15.
I rounded it down to $2.00 (around a 7% cut) to compensate for the extra month and to keep the math clean. I also rounded TQQQ’s 52 down to 50. You can justify it by saying volatility is high now and that the spread was large. But I honestly did it just to make the math easier, as now the payoff is when the stock is down exactly 60% and the option cost 4% of the underlying.
In this setup, the options cost 4% of the underlying. So, for every percent that TQQQ falls past the strike price, the options gain .25 of their price.

