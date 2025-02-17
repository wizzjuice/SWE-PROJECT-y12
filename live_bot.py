import websocket
import json
import pandas as pd
import os

def socket_data(symbol, interval):
    socket = f"wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}"
    return socket

socket = socket_data("btcusdt", "1m")

csv_filename = "ohlcv_data.csv"

def on_message(ws, message):
    data = json.loads(message)
    kline = data['k']

    ohlcv = {
        "timestamp": pd.to_datetime(data['E'], unit='ms'),
        "open": float(kline['o']),
        "high": float(kline['h']),
        "low": float(kline['l']),
        "close": float(kline['c']),
        "volume": float(kline['v'])
    }
    save_to_csv(ohlcv)

def save_to_csv(data):
    df = pd.DataFrame([data])

    if not os.path.isfile(csv_filename):
        df.to_csv(csv_filename, index=False)
    else:
        df.to_csv(csv_filename, mode='a', header=False, index=False)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")

def on_open(ws):
    print("Connected to Binance WebSocket!")

def load_data(filename="ohlcv_data.csv"):
    df = pd.read_csv(filename)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
ws.on_open = on_open
ws.run_forever()