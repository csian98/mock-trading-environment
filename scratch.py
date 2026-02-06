import os, sys
sys.path.append("pylib/")

import matplotlib.pyplot as plt
from stock_market import StockMarket
from lstm_model import LSTMModel
from utility import window_indexing, update_window

symbols = ["AAPL"]
symbol = symbols[0]

window_size = 8

market = StockMarket(symbols)
model = LSTMModel(window_size)

history = market.history(period="2y", days=45)

X, y = window_indexing(history[symbol], window_size=window_size)
windows = X[-1]

X = X.reshape(X.shape + (1, ))
model.fit(X, y, batch_size=64, epochs=100)

true_label = []
predict_label = []

while not market.empty():
    predict = model.predict(windows)[0][0]
    price = market.next()[symbol]
    windows = update_window(windows, price)
    
    true_label.append(price)
    predict_label.append(predict)

plt.plot(true_label, label="true")
plt.plot(predict_label, label="predict")
plt.legend()
plt.show()
