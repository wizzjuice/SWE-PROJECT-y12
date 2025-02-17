import pandas as pd
from binance.client import Client
import ta
import ta.momentum
import ta.trend
import ta.volatility
import dontshare as ds

API_KEY = ds.BINANCE_API_KEY
SECRET_KEY = ds.BINANCE_SECRET_API_KEY
client = Client(API_KEY, SECRET_KEY)

def crypto_data(symbol, interval):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=100)
    for kline in klines:
        del kline[6:]

    df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df.set_index("timestamp", inplace=True)
    df.to_csv("crypto_klines.csv")
    return df

df = crypto_data("BTCUSDT", "1m")

def sentiment_module():
    pass

def SMA_module():
    df["short_sma"] = ta.trend.sma_indicator(df.close, window=10)
    df["long_sma"] = ta.trend.sma_indicator(df.close, window=50)

    short_sma = df["short_sma"].iloc[-1]
    long_sma = df["long_sma"].iloc[-1]
    prev_short_sma = df["short_sma"].iloc[-2]
    prev_long_sma = df["long_sma"].iloc[-2]

    if prev_short_sma < prev_long_sma and short_sma > long_sma:
        return "BUY"
    elif prev_short_sma > prev_long_sma and short_sma < long_sma:
        return "SELL"

def RSI_module():
    df["rsi"] = ta.momentum.rsi(df.close, window=14)
    rsi = df["rsi"].iloc[-1]

    if rsi > 70:
        return "SELL"
    elif rsi < 30:
        return "BUY"

def BB_module():
    df["upper_band"] = ta.volatility.bollinger_hband(df.close, window=20, window_dev=2)
    df["middle_band"] = ta.volatility.bollinger_mavg(df.close, window=20)
    df["lower_band"] = ta.volatility.bollinger_lband(df.close, window=20, window_dev=2)

    price = df["close"].iloc[-1]
    upper = df["upper_band"].iloc[-1]
    lower = df["lower_band"].iloc[-1]

    if price < lower:
        return "BUY"
    elif price > upper:
        return "SELL"

def VWAP_module():
    df["vwap"] = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()

    price = df["close"].iloc[-1]
    vwap = df["vwap"].iloc[-1]
    prev_price = df["close"].iloc[-2]
    prev_vwap = df["vwap"].iloc[-2]

    if prev_price < prev_vwap and price > vwap:
        return "BUY"
    elif prev_price > prev_vwap and price < vwap:
        return "SELL"

def MACD_module():
    df["macd"] = ta.trend.macd(df["close"], window_slow=26, window_fast=12)
    df["macd_signal"] = ta.trend.macd_signal(df["close"], window_slow=26, window_fast=12, window_sign=9)
    df["macd_hist"] = ta.trend.macd_diff(df["close"], window_slow=26, window_fast=12, window_sign=9)

    macd = df["macd"].iloc[-1]
    signal = df["macd_signal"].iloc[-1]
    prev_macd = df["macd"].iloc[-2]
    prev_signal = df["macd_signal"].iloc[-2]

    if prev_macd < prev_signal and macd > signal:
        return "BUY"
    elif prev_macd > prev_signal and macd < signal:
        return "SELL"

# e.g. indicator_combiner(MACD_module, VWAP_module, BB_module)
def indicator_combiner(*indicators):
    pass