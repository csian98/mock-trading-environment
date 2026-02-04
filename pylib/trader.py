#!/usr/bin/env python3
""" strategy.py
Description

Date
Feb 3, 2026
"""
__author__ = "Jeong Hoon (Sian) Choi"
__copyright__ = "Copyright 2024 Jeong Hoon Choi"
__license__ = "MIT"
__version__ = "1.0.0"

# Import #
import os, sys
sys.path.append("pylib/")
import math

from sklearn.preprocessing import MinMaxScaler
from stock_market import StockMarket
from lstm_model import LSTMModel
from utility import window_indexing, update_window

# Data Structures define - class #

class Trader:
    def __init__(self, cash: float):
        self.window_size = 8
        self.symbols = ["AAPL", "META"] #, "MSFT", "AMZN"]
        self.cash = cash
        self.charge = 0.01
        
        self.market = StockMarket(self.symbols)
        self.models = {symbol:LSTMModel(self.window_size)\
                       for symbol in self.symbols}

        self.prices = {}
        self.windows = {}
        self.counts = {symbol:0 for symbol in self.symbols}

        history = self.market.history()
        
        for symbol in self.symbols:
            X, y = window_indexing(history[symbol],
                                   window_size=self.window_size)

            self.prices[symbol] = y[-1]
            self.windows[symbol] = X[-1]
            
            X = X.reshape(X.shape + (1, ))
            self.models[symbol].fit(X, y)

    def trade(self):
        scores = {}
        
        for symbol in self.symbols:
            X = self.windows[symbol]
            pp = self.models[symbol].predict_multiple(
                self.windows[symbol], count=3)
            scores[symbol] = \
                (min(pp) - self.prices[symbol]) / self.prices[symbol]
        
        for symbol, count in self.counts.items():
            if count != 0 and scores[symbol] < 0:
                value = self.prices[symbol] * count
                self.cash += value * (1 - self.charge)
                self.counts[symbol] = 0
            elif count != 0:
                scores[symbol] *= 1.1	# conservation

        candidate = []
        score_sum = 0.0
        for symbol, score in scores.items():
            if score > 0:
                candidate.append((score, symbol))
                score_sum += score

        if abs(score_sum - 0.0) < 1e-5:
            return
                
        candidate = sorted(candidate, key=lambda x: x[0])
        balance = self.balance()

        for symbol, score in scores.items():
            target = score / score_sum * balance
            current = self.counts[symbol] * self.prices[symbol]
            if current < target:
                # BUY
                c = (target - current) // self.prices[symbol]
                self.cash -= c * self.prices[symbol]
                self.counts[symbol] += c
            else:
                # SELL
                c = math.ceil((current - target) / self.prices[symbol])
                self.cash += c * self.prices[symbol] * (1 - self.charge)
                self.counts[symbol] -= c

    def next(self):
        self.prices = self.market.next()
        for symbol in self.symbols:
            self.windows[symbol] = update_window(
                self.windows[symbol], self.prices[symbol]
            )

    def empty(self) -> bool:
        return self.market.empty()

    def balance(self) -> float:
        value = self.cash
        for symbol, count in self.counts.items():
            value += count * self.prices[symbol]
        
        return value


# Functions define #



# Closure & Decorator

