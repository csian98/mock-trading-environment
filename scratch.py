import os, sys
sys.path.append("pylib/")

from stock_market import StockMarket
from lstm_model import LSTMModel
from utility import window_indexing, update_window

symbols = ["AAPL", "META", "MSFT", "AMZN", "TSLA"]
window_size = 8

market = StockMarket(symbols)
models = {symbol:LSTMModel(window_size) for symbol in symbols}
windows = {}

history = market.history()

for symbol in symbols:
    X, y = window_indexing(history[symbol], window_size=window_size)
    windows[symbol] = X[-1]
    
    X = X.reshape(X.shape + (1,))
    models[symbol].fit(X, y)

