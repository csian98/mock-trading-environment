#!/usr/bin/env python3
""" market.py
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

from typing import List
from collections import deque
from datetime import datetime, timedelta
import yfinance as yf
from market import Market

# Data Structures define - class #

class StockMarket(Market):
    def __init__(self, symbols: List):
        super().__init__(symbols)

    def history(self, period: str="3y", days: int=30) -> dict:
        output = {}
        for symbol in self._symbols:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)["Close"]
            idx = df.index < (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S%z")
            output[symbol] = df[idx].values
            self._queue[symbol] = deque(df[~idx])

        return output

    def empty(self) -> bool:
        for symbol in self._symbols:
            if len(self._queue[symbol]) == 0:
                return True

        return False
    
    def next(self) -> dict:
        output = {}
        for symbol in self._symbols:
            output[symbol] = self._queue[symbol].popleft()

        return output

# Functions define #


# Closure & Decorator

