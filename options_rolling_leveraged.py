import yfinance as yf
import pandas as pd
import numpy as np

weights=[(1.0, 0),(.95, .05), (0.9,0.1), 
         (.85,.15),(0.8,0.2),(0.75,0.25),
         (0.7,0.3)]   ###1.0 is just to make sure the numbers are right and the same as the unhedged script, which they are.

def download_data():
    ndx = yf.download('^NDX', start='1995-10-01', end='2002-10-01', auto_adjust=True)
    daily = ndx['Close'].pct_change().dropna()   
    lev_daily = daily * 2.9269
    monthly = lev_daily.resample('ME').apply(lambda x: (1+x).prod() - 1)
    return monthly.dropna()     ###this returns percentage numbers in decimal form, e.g., 0.05 for 5%, and for negative, -0.05 for -5%

def rolling_annual_returns(monthly):
    r = monthly.rolling(12).apply(lambda x: (1+x).prod() - 1)
    r = r.dropna()    
    if isinstance(r, pd.DataFrame):   ##just to fix a bug in the first run of the code, idk if it's necessary
        r = r.iloc[:,0]
    return r.squeeze()  
         
def calculate_hedged_returns(rolling,weights):   ###I explain the math and assumptions of tihs function in the read_me and my substack
    rolling = pd.to_numeric(rolling,errors='coerce').dropna()  ##this just makes sure there are no non-numeric values
    hedged = {}
    for ws,wo in weights:
        out=[]
        for ret in rolling:
            mult = 1 + ret
            if mult <.4:   ###which is a 60% loss
                extra = .4 - mult   #this is the amount that gets the payoff - anything past 60%
                payoff = 0.25*(extra*100)*wo    ###each percent past 60% loss pays 25% of the option price.  ##in the case of the stock falling to 80% down, this variable would return .5 for a weight of .1 option. this is the 25% of 20% (the extra past 60%) times 10% (the weight of the option). It could only be a postiive number in this variable.
            else:
                payoff = 0  ##cause it didn't hit the strike
            out.append((ws*mult + payoff)-1) 
        hedged[(ws,wo)] = out

    return pd.DataFrame(hedged)

monthly = download_data()
rolling = rolling_annual_returns(monthly)
df = calculate_hedged_returns(rolling,weights)
print(df.describe())
print(df.quantile([0.05,0.1,0.15,0.2,.21,.22,.23,.24,0.25,0.3,0.35,0.4,0.45,0.5,
                   0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]))


### Count positive vs negative for each hedge combo
### I made this becasue of a bug I thought I had, and this checked and proved there was no bug. details in the read_me

counts = {}
for col in df.columns:
    series = df[col]
    positives = (series > 0).sum()
    negatives = (series < 0).sum()
    zeros = (series == 0).sum()
    
    counts[col] = {
        "positive": positives,
        "negative": negatives,
        "zero": zeros
    }
for k, v in counts.items():
    print(f"{k}: {v}")
