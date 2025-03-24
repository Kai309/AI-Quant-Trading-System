import pandas as pd
import numpy as np
import fetch_data
from metrics import calculate_sharpe_ratio, calculate_max_drawdown

def backtest_strategy(stock, buy_price, sell_price, stop_loss, start_date="2023-01-01", end_date="2024-12-31"):
    df = fetch_data.get_tiingo_stock_data(stock, start_date, end_date)

    if df is None or df.empty:
        return {"error": f"No data available for {stock}"}

    df = df.reset_index(drop=True)
    df["date"] = pd.to_datetime(df["date"])
    df["price"] = df["price"].astype(float)

    entry_index = None
    for i in range(len(df)):
        if df.loc[i, "price"] <= buy_price:
            entry_index = i
            break

    if entry_index is None:
        return {
            "result": "Buy Not Triggered",
            "entry_price": buy_price,
            "exit_price": df["price"].iloc[-1],
            "return_percent": 0.0,
            "dates": [],
            "prices": [],
            "holding_days": "-",
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
            "cumulative_pnl": []
        }

    entry_date = df.loc[entry_index, "date"]
    entry_price = df.loc[entry_index, "price"]

    for j in range(entry_index + 1, len(df)):
        price = df.loc[j, "price"]
        date = df.loc[j, "date"]

        sliced = df.loc[entry_index:j + 1]
        prices = sliced["price"].tolist()
        returns = pd.Series(prices).pct_change().dropna()
        sharpe = calculate_sharpe_ratio(returns)
        max_dd = calculate_max_drawdown(prices)
        cum_pnl = (1 + returns).cumprod().tolist()

        # 🎯 Target Hit
        if price >= sell_price:
            return {
                "result": "Target Hit",
                "entry_price": round(entry_price, 2),
                "exit_price": round(sell_price, 2),
                "return_percent": round((sell_price - entry_price) / entry_price * 100, 2),
                "dates": sliced["date"].dt.strftime("%Y-%m-%d").tolist(),
                "prices": prices,
                "holding_days": (date - entry_date).days,
                "sharpe_ratio": sharpe,
                "max_drawdown": max_dd,
                "cumulative_pnl": cum_pnl
            }

        # 🛑 Stop Loss Hit
        elif price <= stop_loss:
            return {
                "result": "Stop Loss Hit",
                "entry_price": round(entry_price, 2),
                "exit_price": round(price, 2),  # actual exit price at stop hit
                "return_percent": round((price - entry_price) / entry_price * 100, 2),
                "dates": sliced["date"].dt.strftime("%Y-%m-%d").tolist(),
                "prices": prices,
                "holding_days": (date - entry_date).days,
                "sharpe_ratio": sharpe,
                "max_drawdown": max_dd,
                "cumulative_pnl": cum_pnl
            }

    # 📅 End of Data Exit
    final_date = df["date"].iloc[-1]
    final_price = df["price"].iloc[-1]
    sliced = df.loc[entry_index:]
    prices = sliced["price"].tolist()
    returns = pd.Series(prices).pct_change().dropna()
    sharpe = calculate_sharpe_ratio(returns)
    max_dd = calculate_max_drawdown(prices)
    cum_pnl = (1 + returns).cumprod().tolist()

    return {
        "result": "End of Data Exit",
        "entry_price": round(entry_price, 2),
        "exit_price": round(final_price, 2),
        "return_percent": round((final_price - entry_price) / entry_price * 100, 2),
        "dates": sliced["date"].dt.strftime("%Y-%m-%d").tolist(),
        "prices": prices,
        "holding_days": (final_date - entry_date).days,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_dd,
        "cumulative_pnl": cum_pnl
    }
