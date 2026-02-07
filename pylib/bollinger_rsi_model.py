import numpy as np
from typing import List

class BollingerRSIModel:
    def __init__(self, window_size: int):
        self.name = "bollinger_rsi"
        self.window_size = window_size
        self.bb_period = 20 # Bollinger Bands period
        self.bb_std = 2.0 
        self.rsi_period = 14
        
    def fit(self, X, y, batch_size=64, epochs=10) -> None:
        '''
        No need to fit in this model
        '''
        pass
    
    def _calculate_sma(self, prices: np.ndarray, period: int) -> float:
        if len(prices) < period:
            return np.mean(prices)
        return np.mean(prices[-period:])
    
    def _calculate_std(self, prices: np.ndarray, period: int) -> float:
        if len(prices) < period:
            return np.std(prices)
        return np.std(prices[-period:])
    
    def _calculate_rsi(self, prices: np.ndarray) -> float:
        if len(prices) < self.rsi_period + 1:
            return 50.0  # Neutral RSI
        
        deltas = np.diff(prices[-(self.rsi_period + 1):])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_bollinger_bands(self, prices: np.ndarray) -> tuple:
        '''
        Calculate Bollinger Bands (sma +- 2 * std, sma)
        '''
        sma = self._calculate_sma(prices, self.bb_period)
        std = self._calculate_std(prices, self.bb_period)
        
        upper_band = sma + (self.bb_std * std)
        lower_band = sma - (self.bb_std * std)
        
        return upper_band, sma, lower_band
    
    def predict(self, X) -> float:
        '''
        Returns the middle band (SMA) as the expected mean reversion target.
        '''
        prices = X.flatten()
        _, middle_band, _ = self._calculate_bollinger_bands(prices)
        return np.array([[middle_band]])
    
    def predict_multiple(self, X, count=3) -> List:
        '''
        Generate multiple predictions.
        For mean reversion, we return gradually converging values toward the mean.
        '''
        output = []
        current_prices = X.copy()
        
        for i in range(count):
            value = self.predict(current_prices)
            output.append(value[0][0])
            current_prices = np.concatenate((current_prices[1:], np.array([value[0][0]])))
        
        return output
    
    def get_signal_strength(self, X) -> float:
        '''
        Calculate signal strength based on Bollinger Bands position and RSI.
        Returns a score between -1 and 1:
        - Positive: Oversold condition (buy signal)
        - Negative: Overbought condition (sell signal)
        '''
        prices = X.flatten()
        current_price = prices[-1]
        
        upper_band, middle_band, lower_band = self._calculate_bollinger_bands(prices)
        rsi = self._calculate_rsi(prices)
        
        # Calculate Bollinger Band position (-1 to 1)
        band_range = upper_band - lower_band
        if band_range == 0:
            bb_position = 0
        else:
            bb_position = (current_price - middle_band) / (band_range / 2)
            bb_position = np.clip(bb_position, -1, 1)
        
        # Normalize RSI
        rsi_normalized = (rsi - 50) / 50
        
        # Combine signals, weight: 60% Bollinger, 40% RSI
        signal = -(0.6 * bb_position + 0.4 * rsi_normalized)
        
        return signal