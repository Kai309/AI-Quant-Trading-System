import numpy as np
import pandas as pd
import fetch_data
from arch import arch_model  # GARCH Model
from scipy.stats import zscore


# === 1. Momentum and Mean Reversion ===
def calculate_momentum(data, lookback=10):
    if len(data) < lookback:
        return None
    return round((data["price"].iloc[-1] / data["price"].iloc[-lookback] - 1) * 100, 2)

def mean_reversion_signal(data, window=20):
    if len(data) < window:
        return None
    try:
        rolling_mean = data["price"].rolling(window=window).mean()
        rolling_std = data["price"].rolling(window=window).std()
        z_score = (data["price"] - rolling_mean) / rolling_std
        return round(z_score.iloc[-1], 2) if not np.isnan(z_score.iloc[-1]) else None
    except Exception as e:
        print(f"Error computing mean reversion: {e}")
        return None

# === 2. GARCH Volatility ===
def garch_volatility(data):
    if len(data) < 50:
        return None
    try:
        returns = data["price"].pct_change().dropna() * 100
        model = arch_model(returns, vol="Garch", p=1, q=1)
        model_fit = model.fit(disp="off")
        forecast = model_fit.forecast(horizon=1)
        return round(np.sqrt(forecast.variance.iloc[-1, 0]) / 100, 4)
    except Exception as e:
        print(f"GARCH Model Error: {e}")
        return None


# === 3. Trading Signal Computation ===
def compute_quant_signals(stock, investment_amount, expected_profit):
    stock_data = fetch_data.get_tiingo_stock_data(stock, start_date="2023-01-01", end_date="2024-12-31")

    if stock_data is None or len(stock_data) < 60:
        return {"error": f"Not enough data for {stock}"}

    # Indicators
    momentum = calculate_momentum(stock_data)
    mean_rev = mean_reversion_signal(stock_data)
    volatility = garch_volatility(stock_data)

    # Buy/Sell Logic
    try:
        current_price = stock_data["price"].iloc[-1]
        buy_price = round(current_price, 2)
        sell_price = round(buy_price + float(expected_profit), 2)
        stop_loss = round(buy_price * 0.95, 2)
        quantity = int(float(investment_amount) / buy_price)
    except Exception as e:
        print(f"Strategy Calculation Error: {e}")
        buy_price = sell_price = stop_loss = quantity = "N/A"

    return {
        "stock": stock,
        "momentum": momentum if momentum is not None else "N/A",
        "mean_reversion": mean_rev if mean_rev is not None else "N/A",
        "volatility_garch": volatility if volatility is not None else "N/A",
        "strategy": {
            "buy_price": buy_price,
            "sell_price": sell_price,
            "stop_loss": stop_loss,
            "quantity": quantity,
            "holding_days": "-"  # Placeholder, will be set after backtest
        }
    }

# === 4. Test Model ===
if __name__ == "__main__":
    result = compute_quant_signals("AAPL", investment_amount=250, expected_profit=100)
    print("\nBacktest Output:\n", result)
