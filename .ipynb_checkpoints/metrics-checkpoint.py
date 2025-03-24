import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def calculate_forecast_metrics(actual_prices, forecast_prices):
    if len(actual_prices) != len(forecast_prices) or len(actual_prices) < 2:
        return 0.0, 0.0, 0.0

    mse = mean_squared_error(actual_prices, forecast_prices)
    mae = mean_absolute_error(actual_prices, forecast_prices)
    r2 = r2_score(actual_prices, forecast_prices)

    return mse, mae, r2

def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
    returns = np.array(returns)
    if len(returns) < 2:
        return 0.0

    excess_returns = returns - risk_free_rate
    std_dev = np.std(excess_returns)
    if std_dev == 0 or np.isnan(std_dev):
        return 0.0

    sharpe_ratio = np.mean(excess_returns) / std_dev * np.sqrt(252)
    return round(sharpe_ratio, 2)

def calculate_max_drawdown(prices):
    if len(prices) < 2:
        return 0.0

    prices = np.array(prices)
    cum_returns = prices / prices[0]
    roll_max = np.maximum.accumulate(cum_returns)
    drawdowns = (cum_returns - roll_max) / roll_max
    max_drawdown = np.min(drawdowns)

    return round(max_drawdown * 100, 2)
