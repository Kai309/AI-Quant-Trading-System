# 🧠 AI Quant Trading System

A full-stack, interactive AI-based stock trading dashboard that forecasts stock prices, analyzes quantitative signals, and performs strategy backtesting — built entirely in Python with Flask and modern web technologies.

> 📈 **Objective:** Empower users to make smarter trading decisions using AI-driven insights based on momentum, mean reversion, volatility, and LSTM-based forecasting.

---

## 🌟 Key Features

- **📉 Stock Forecasting using LSTM:**  
  Predicts future prices based on historical time series using deep learning.

- **📊 Quantitative Signal Engine:**  
  Calculates momentum, mean reversion (Z-score), and GARCH volatility for trading signal generation.

- **🛠️ Backtesting Framework:**  
  Simulates trading with buy/sell/stop logic and reports Sharpe Ratio, drawdown, and final return.

- **💡 Stock Filtering by Risk Level:**  
  Auto-selects stocks based on volatility for Low, Medium, or High risk preferences.

- **🖥️ Intuitive Frontend Dashboard:**  
  Interactive UI using Flask + Chart.js with historical, forecast, and backtest chart modes.

- **📊 Real-Time Metrics Displayed:**  
  Mean Squared Error, MAE, R² Score for forecast performance  
  Sharpe Ratio & Max Drawdown for strategy performance

---

## 🧠 Models & Techniques Used

| Category | Technique | Purpose |
|---------|-----------|---------|
| Forecasting | LSTM (Keras) | Multi-step time series prediction |
| Technical Signals | Momentum | Trend direction (price % change over window) |
| Mean Reversion | Z-score | Identifies deviation from average (entry signal) |
| Volatility Modeling | GARCH (ARCH Package) | Estimates risk & price variance |
| Backtesting | Price Simulation | Calculates return, Sharpe Ratio, drawdown |

---

## 📂 Project Structure

