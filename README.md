# AI Quant Trading System

This project is a full-stack AI-driven trading platform that enables users to forecast stock prices, analyze quantitative signals, and backtest trading strategies using real historical data. It is built with a Flask backend and a dynamic, responsive frontend.

## Project Overview

The AI Quant Trading System integrates core quantitative finance concepts with machine learning models to assist in algorithmic trading decision-making. It offers a seamless interface for users to enter investment preferences and receive intelligent trade recommendations based on real-time market data.

## Key Features

### LSTM Forecasting
A Long Short-Term Memory (LSTM) neural network is trained on historical stock data to forecast future prices. The model is implemented using TensorFlow and generates multi-step predictions.

### Quantitative Signal Engine
- **Momentum**: Calculates the percentage change in stock price over a defined window.
- **Mean Reversion (Z-score)**: Identifies overbought or oversold conditions relative to historical averages.
- **GARCH Volatility Modeling**: Uses the ARCH package to estimate time-varying volatility in asset returns.

### Backtesting Framework
A custom strategy simulator that:
- Executes buy, sell, and stop-loss logic
- Calculates Sharpe ratio, maximum drawdown, and final return
- Simulates realistic trade scenarios based on historical prices

### Risk-Based Stock Selection
Users select a risk level (Low, Medium, High), and the system automatically selects a stock based on recent return volatility.

### Web Dashboard
Built using Flask and Chart.js:
- Accepts investment amount, expected profit, and risk level
- Displays buy/sell signals, technical indicators, and visualizations
- Allows toggling between historical prices, backtest results, and LSTM forecasts

## Screenshots

### Dashboard Overview
![Dashboard](https://github.com/Kai309/AI-Quant-Trading-System/blob/main/ss1.jpg)

### LSTM Forecast Mode
![Forecast](https://github.com/Kai309/AI-Quant-Trading-System/blob/main/ss2.jpg)

### Backtest Results with Performance Metrics
![Backtest](https://github.com/Kai309/AI-Quant-Trading-System/blob/main/ss3.jpg)

## Technologies Used

- Python (Flask, Pandas, NumPy, scikit-learn, TensorFlow, arch)
- Tiingo API (for stock price data)
- Chart.js (for frontend charting)
- HTML, CSS, JavaScript

## Live Application

A deployed version of this application is available and actively running. For access to the live demo, please contact the author or refer to the link included in the resume or LinkedIn project description.

## Author

**Kaushik Naidu**  
GitHub: [Kai309](https://github.com/Kai309)  
LinkedIn: [linkedin.com/in/your-profile](https://www.linkedin.com/in/kaushik-naidu/)

## License

This project is not intended for replication or reuse. All rights reserved by the author.
