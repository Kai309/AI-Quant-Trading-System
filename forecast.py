import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import fetch_data
from metrics import calculate_forecast_metrics


def prepare_data(series, window_size=30):
    X, y = [], []
    for i in range(len(series) - window_size):
        X.append(series[i:i + window_size])
        y.append(series[i + window_size])
    return np.array(X), np.array(y)


def forecast_lstm(stock, forecast_horizon=10):
    # === 1. Fetch historical data (training set)
    train_df = fetch_data.get_tiingo_stock_data(stock, "2023-01-01", "2024-12-31")
    if train_df is None or len(train_df) < 100:
        return {"error": "Not enough data to forecast"}

    prices = train_df["price"].values.reshape(-1, 1)

    # === 2. Normalize and prepare data
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(prices)

    window_size = 30
    X_train, y_train = prepare_data(scaled, window_size)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

    # === 3. Build & train LSTM model
    model = Sequential()
    model.add(LSTM(64, activation='relu', input_shape=(window_size, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=20, verbose=0)

    # === 4. Forecast next N steps
    last_sequence = scaled[-window_size:].reshape(1, window_size, 1)
    predictions = []
    for _ in range(forecast_horizon):
        pred = model.predict(last_sequence, verbose=0)[0][0]
        predictions.append(pred)
        last_sequence = np.append(last_sequence[:, 1:, :], [[[pred]]], axis=1)

    forecast_prices = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

    # === 5. Fetch actual prices for the forecast horizon
    start_date = datetime.strptime("2025-01-01", "%Y-%m-%d")
    end_date = start_date + timedelta(days=forecast_horizon * 2)  # buffer for weekends

    actual_df = fetch_data.get_tiingo_stock_data(stock, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    if actual_df is None or actual_df.empty:
        actual_prices = []
        actual_dates = []
    else:
        actual_prices = actual_df["price"].tolist()[:forecast_horizon]
        actual_dates = actual_df["date"].dt.strftime("%Y-%m-%d").tolist()[:forecast_horizon]

    # === 6. Create forecast dates from last training date
    forecast_start = train_df["date"].iloc[-1] + timedelta(days=1)
    forecast_dates = []
    cur_date = forecast_start
    while len(forecast_dates) < forecast_horizon:
        if cur_date.weekday() < 5:
            forecast_dates.append(cur_date.strftime("%Y-%m-%d"))
        cur_date += timedelta(days=1)

    # === 7. Forecast evaluation metrics
    mse, mae, r2 = calculate_forecast_metrics(actual_prices, forecast_prices.tolist())

    return {
        "forecast_dates": forecast_dates,
        "forecast_prices": forecast_prices.tolist(),
        "actual_prices": actual_prices,
        "actual_dates": actual_dates,
        "mse": round(mse, 2),
        "mae": round(mae, 2),
        "r2": round(r2, 2)
    }


# Optional test
if __name__ == "__main__":
    output = forecast_lstm("AMZN", forecast_horizon=10)
    print(output)
