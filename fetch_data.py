import requests
import pandas as pd
import numpy as np
import os

# Load API Key from environment variable
TIINGO_API_KEY = os.getenv("TIINGO_API_KEY", "")

def get_tiingo_stock_data(ticker, start_date="2023-01-01", end_date="2024-12-31"):
    """
    Fetches historical stock data from Tiingo API.
    """
    url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&endDate={end_date}&token={TIINGO_API_KEY}"

    try:
        response = requests.get(url)

        # Handle HTTP errors
        if response.status_code != 200:
            print(f"Error: Failed to fetch data for {ticker}. Status Code: {response.status_code}")
            return None

        data = response.json()
        if not data:
            print(f"Warning: No data received for {ticker}.")
            return None

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df = df[["date", "close"]].rename(columns={"close": "price"})

        return df

    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching {ticker}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching {ticker}: {e}")
        return None


def get_stocks_by_volatility(risk_level):
    """
    Selects stocks based on their volatility.
    """
    stocks = ["AAPL", "TSLA", "GOOGL", "MSFT", "NVDA", "AMZN", "META", "NFLX", "AMD", "BA", "PYPL", "KMT"]
    stock_volatility = {}

    for stock in stocks:
        stock_data = get_tiingo_stock_data(stock)
        
        if stock_data is None or len(stock_data) < 50:
            print(f"Skipping {stock}: Not enough data")
            continue

        stock_volatility[stock] = stock_data["price"].pct_change().std()

    if not stock_volatility:
        print("Warning: No stocks with sufficient data available.")
        return []

    # Sort stocks by volatility
    sorted_stocks = sorted(stock_volatility.items(), key=lambda x: x[1])

    if risk_level == "low":
        return [s[0] for s in sorted_stocks[:3]]  # Least volatile
    elif risk_level == "medium":
        return [s[0] for s in sorted_stocks[3:6]]  # Medium volatility
    else:
        return [s[0] for s in sorted_stocks[6:]]  # Most volatile
