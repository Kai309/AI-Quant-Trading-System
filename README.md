# 🧠 AI Quant Trading System

A full-stack AI-powered stock trading dashboard that combines deep learning, financial modeling, and backtesting — all inside an intuitive web interface. This project provides end-to-end automated trade recommendations, based on real-time data, user-defined risk levels, and advanced quantitative signals.

---

## 📌 Project Overview

The **AI Quant Trading System** is designed to help investors and finance enthusiasts explore algorithmic trading through:

- 📈 **LSTM-based price forecasting**
- 🔁 **Mean reversion and momentum indicators**
- 📉 **GARCH volatility modeling**
- 🧪 **Backtesting with performance metrics**
- 🎛️ **User-defined investment inputs**
- 💻 **Flask-powered interactive dashboard**

It serves as a foundational quant research tool and a portfolio-worthy full-stack machine learning application.

---

## 🚀 Features & Methodologies

### 1. 🔮 LSTM Forecasting
- Uses `TensorFlow/Keras` to train a Long Short-Term Memory (LSTM) neural network on historical prices.
- Predicts multi-step future stock prices (10 days).
- Visualizes predictions vs. actuals, and computes MSE, MAE, and R².

### 2. 📊 Quantitative Signal Engine
- **Momentum (% change)**: Measures recent price direction.
- **Mean Reversion (Z-Score)**: Flags overbought/oversold conditions.
- **Volatility (GARCH)**: Models time-varying volatility using the `arch` package.

### 3. 🛠️ Backtesting Engine
- Simulates buy/sell/stop-loss logic from the suggested strategy.
- Outputs: final return, Sharpe ratio, max drawdown, holding period.
- Fully visualized on a chart with PnL trend.

### 4. 📉 Risk-Based Stock Selection
- Users select risk preference: Low / Medium / High.
- System auto-chooses stock based on recent volatility (std. dev of returns).

---

## 🖼️ Screenshots

### 🎯 Dashboard Overview
![UI Screenshot 1](https://github.com/Kai309/AI-Quant-Trading-System/blob/main/ss1.jpg)

### 📈 Forecast Mode with LSTM
![Forecast Screenshot](https://github.com/Kai309/AI-Quant-Trading-System/blob/main/ss2.jpg)

### 🧪 Backtest Results with PnL & Metrics
![Backtest Screenshot](https://github.com/Kai309/AI-Quant-Trading-System/blob/main/ss3.jpg)

---


