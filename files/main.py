import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    data = yf.download("AAPL","2025-11-01","2025-12-31")
    print("data:")
    print(data)
    price = data.dropna()
    print("Signals:")
    price["Short Avg"] = price["Close"].rolling(5).mean()
    price["Long Avg"] = price["Close"].rolling(10).mean()
    price["Signal"] = (price["Short Avg"] > price["Long Avg"]).astype(int) * price["Close"]["AAPL"]
    print(price)

    plt.figure(figsize=(12,6))

    plt.scatter(price.index,price["Signal"])
    plt.plot(price.index,price["Close"])
    plt.plot(price.index,price["Short Avg"])
    plt.plot(price.index,price["Long Avg"])
    
    plt.xlabel("Date")
    plt.ylabel("close and signal")
    plt.title("signals from close price")
    plt.legend()
    plt.grid(True)
    
    plt.savefig("plot.png", dpi=300, bbox_inches="tight")
    plt.close()



if __name__ == "__main__":
    main()
