import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def calc_returns(data,close):
    data["Returns"] = close.pct_change()
    data["Cumulative_Market"] = (data["Returns"]+1).cumprod()

def run_strategy_and_plot(strat,data,stock):

    close = data[("Close",stock)]
    opn = data[("Open",stock)]
    high = data[("High",stock)]
    low = data[("Low",stock)]
    volume = data[("Volume",stock)]

    name = strat(data,close,opn,high,low,volume)
    data["Strategy Returns"] = data["Signal"].shift(1)*data["Returns"]
    data["Cumulative_Strategy"] = (data["Strategy Returns"]+1).cumprod()


    data[["Cumulative_Market","Cumulative_Strategy"]].plot()
    plt.title(f"{name}__{stock}")

    os.makedirs("Graphs_By_Strategy",exist_ok=True)
    os.makedirs(f"Graphs_By_Strategy/{name}",exist_ok=True)
    plt.savefig(f"Graphs_By_Strategy/{name}/{name}__{stock}",format="png")
    os.makedirs("Graphs_By_Stock",exist_ok=True)
    os.makedirs(f"Graphs_By_Stock/{stock}",exist_ok=True)
    plt.savefig(f"Graphs_By_Stock/{stock}/{name}__{stock}",format="png")

    print(f"SAVED PLOT:{name}__{stock}.png\tRESULT:{data["Cumulative_Strategy"].iloc[-1]/data["Cumulative_Market"].iloc[-1]}")

#strategies

def moving_average(data,close,opn,high,low,volume):
    data["Signal"] = np.where(close.rolling(20).mean() > close.rolling(50).mean(),1,0)
    return "MOVING_AVERAGE_20-50"

def moving_average_shorting(data,close,opn,high,low,volume):
    data["Signal"] = np.where(close.rolling(20).mean() > close.rolling(50).mean(),1,-1)
    return "MOVING_AVERAGE_SHORT_20-50"

#extracting data
tickers = ("AAPL","NVDA","GOOGL","MSFT")
data = yf.download(tickers,"2023-01-01","2026-01-01")

if data is None or data.empty:
    print("Download failed.")
    exit()

strategies = [moving_average, moving_average_shorting]

for stock in tickers:
    calc_returns(data,(data[("Close",stock)]))
    for strat in strategies:
        run_strategy_and_plot(strat,data,stock)