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
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

from model import Model

# Data Structures define - class #

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
tf.get_logger().setLevel("ERROR")

class LSTMModel(Model):
    def __init__(self, window_size: int):
        super().__init__("lstm")
        self.window_size = window_size

        self.scaler = MinMaxScaler()
        
        self.model = Sequential([
            LSTM(units=64, activation="relu", return_sequences=True),
            Dropout(0.3),
            LSTM(units=64, activation="relu", return_sequences=True),
            Dropout(0.3),
            LSTM(units=64, activation="relu", return_sequences=True),
            Dropout(0.3),
            LSTM(units=64, activation="relu", return_sequences=False),
            Dropout(0.3),
            Dense(1)
        ])
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-2),
                           loss="mean_squared_error")

    def fit(self, X, y, batch_size=64, epochs=10) -> None:
        ssz, wsz, fsz = X.shape
        X = X.reshape(ssz * wsz, fsz)
        X = self.scaler.fit_transform(X)
        X = X.reshape(ssz, wsz, fsz)

        y = y.reshape(ssz, fsz)
        y = self.scaler.transform(y)
        
        self.model.fit(X, y, batch_size=batch_size, epochs=epochs, verbose=0)

    def predict(self, X) -> float:
        X = X.reshape(self.window_size, 1)
        X = self.scaler.transform(X)
        X = X.reshape(1, self.window_size, 1)
        y = self.model.predict(X, verbose=0)
        return self.scaler.inverse_transform(y)

    def predict_multiple(self, X, count=3) -> List:
        output = []
        for i in range(count):
            value = self.predict(X)
            output.append(value[0][0])
            X = np.concatenate((X[1:], np.array(value[0])))

        return output

# Functions define #


# Closure & Decorator

