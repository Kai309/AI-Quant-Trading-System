from flask import Flask, render_template, request, jsonify
import fetch_data
import model
import threading
import webbrowser
from backtest import backtest_strategy 
from forecast import forecast_lstm


app = Flask(__name__)

# Open browser when server starts
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5001/")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/get_stock_signals", methods=["POST"])
def get_stock_signals():
    try:
        data = request.json
        print("Received data from frontend:", data)

        risk = data.get("risk")
        investment = data.get("investment")
        expected_profit = data.get("expected_profit")

        if not all([risk, investment, expected_profit]):
            return jsonify({"error": "Missing input fields."})

        # Get best stock based on risk
        stocks = fetch_data.get_stocks_by_volatility(risk)
        if not stocks:
            return jsonify({"error": "No stocks found for this risk level."})
        
        selected_stock = stocks[0]
        print(f"✅ Selected stock for {risk} risk: {selected_stock}")

        # Compute signals
        signals = model.compute_quant_signals(
            selected_stock,
            investment_amount=investment,
            expected_profit=expected_profit
        )

        return jsonify(signals)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/get_stock_data", methods=["GET"])
def get_stock_data():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "No ticker specified."})

    stock_data = fetch_data.get_tiingo_stock_data(ticker, start_date="2023-01-01", end_date="2024-12-31")

    if stock_data is None or stock_data.empty:
        return jsonify({"error": f"No data found for {ticker}"})
    
    return jsonify(stock_data.to_dict(orient="records"))

@app.route("/backtest", methods=["POST"])
def backtest():
    try:
        data = request.json
        result = backtest_strategy(
            stock=data["stock"],
            buy_price=float(data["buy_price"]),
            sell_price=float(data["sell_price"]),
            stop_loss=float(data["stop_loss"])
        )

        # 🔍 Print to confirm what backend is sending
        print(f"[DEBUG] Final Return %: {result.get('return_percent')}")

        return jsonify({
            "result": result.get("result", "-"),
            "entry_price": result.get("entry_price", "-"),
            "exit_price": result.get("exit_price", "-"),
            "return_percent": result.get("return_percent", 0),
            "dates": result.get("dates", []),
            "prices": result.get("prices", []),
            "holding_days": result.get("holding_days", "-"),
            "sharpe_ratio": result.get("sharpe_ratio", 0.0),
            "max_drawdown": result.get("max_drawdown", 0.0),
            "cumulative_pnl": result.get("cumulative_pnl", [])
        })

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/forecast", methods=["GET"])
def forecast():
    stock = request.args.get("stock")
    if not stock:
        return jsonify({"error": "No stock provided"})

    result = forecast_lstm(stock, forecast_horizon=10)
    return jsonify(result)

if __name__ == "__main__":
    threading.Timer(1.25, open_browser).start()
    app.run(port=5001, debug=False)
