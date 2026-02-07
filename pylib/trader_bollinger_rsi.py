import os, sys
sys.path.append("pylib/")


from stock_market import StockMarket
from bollinger_rsi_model import BollingerRSIModel
from utility import window_indexing, update_window

class Trader:
    def __init__(self, cash: float):
        # Most of the code here are the same as trader.py
        self.window_size = 30  # I set this larger to capture more history
        self.symbols = ["NVDA", "AAPL", "GOOG", "MSFT", "AMZN",
                        "META", "TSLA", "AVGO", "ORCL", "NFLX"]
        self.cash = cash
        self.charge = 0.0001
        
        self.market = StockMarket(self.symbols)
        self.models = {symbol: BollingerRSIModel(self.window_size)
                       for symbol in self.symbols}
        
        self.prices = {}
        self.windows = {}
        self.counts = {symbol: 0 for symbol in self.symbols}
        
        history = self.market.history(period="2y", days=60)
        
        for symbol in self.symbols:
            X, y = window_indexing(history[symbol],
                                   window_size=self.window_size)
            
            self.prices[symbol] = y[-1]
            self.windows[symbol] = X[-1]
            
            # Technical models don't need training, but still call fit for compatibility
            X = X.reshape(X.shape + (1, ))
    
    def trade(self):
        signals = {}
    
        for symbol in self.symbols:
            signal = self.models[symbol].get_signal_strength(self.windows[symbol])
            signals[symbol] = signal
        
        # Sell overbought positions
        for symbol, count in list(self.counts.items()):
            if count > 0 and signals[symbol] < -0.3:  # Strong sell signal
                value = self.prices[symbol] * count
                self.cash += value * (1 - self.charge)
                print(f"SELL {symbol}: {count} shares @ ${self.prices[symbol]:.2f}, Signal={signals[symbol]:.3f}")
                self.counts[symbol] = 0
        
        # find oversold candidates
        candidates = []
        signal_sum = 0.0
        for symbol, signal in signals.items():
            if signal > 0.7:  # Oversold threshold
                candidates.append((symbol, signal))
                signal_sum += signal
        
        if signal_sum == 0:
            return  # No buying opportunities
        
        # Calculate total portfolio value
        total_portfolio_value = self.cash
        for symbol in self.symbols:
            total_portfolio_value += self.counts[symbol] * self.prices[symbol]
        
        # Invest 
        investable = total_portfolio_value * 0.95  # Keep 5% cash buffer
        
        '''
        There is a problem here that if we have a strong buy signal but currently our portfolio
        is filled with weak signal stocks, we are not able to sell them to free up cash for the strong buy.
        '''
        for symbol, signal in candidates:
            # allocate capital for each symbol based on signal strength
            target_value = (signal / signal_sum) * investable
            current_value = self.counts[symbol] * self.prices[symbol]
            
            if target_value > current_value + self.prices[symbol]:  # Only buy if difference > 1 share
                # BUY more
                shares_needed = int((target_value - current_value) / self.prices[symbol])
                cost = shares_needed * self.prices[symbol]
                
                if self.cash >= cost:
                    self.cash -= cost
                    self.counts[symbol] += shares_needed
                    print(f"BUY {symbol}: {shares_needed} shares @ ${self.prices[symbol]:.2f}, Signal={signal:.3f}")
            
            elif current_value > target_value + self.prices[symbol]:  # Only sell if difference > 1 share
                # TRIM position
                shares_to_sell = int((current_value - target_value) / self.prices[symbol])
                
                if shares_to_sell > 0:
                    proceeds = shares_to_sell * self.prices[symbol] * (1 - self.charge)
                    self.cash += proceeds
                    self.counts[symbol] -= shares_to_sell
                    print(f"TRIM {symbol}: {shares_to_sell} shares @ ${self.prices[symbol]:.2f}, Signal={signal:.3f}")

    
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

    def report(self, day: int) -> None:
        print(f"\n====== Day {day} ======")
        print(f"Cash: {self.cash:.2f}")
        for symbol, count in self.counts.items():
            if count != 0:
                signal = self.models[symbol].get_signal_strength(self.windows[symbol])
                print(f"{symbol}: ${self.prices[symbol]:.2f} X {count} = ${self.prices[symbol] * count:.2f} (Signal: {signal:.3f})")

        print(f"Net Asset: {self.balance():.2f}")
        print(f"====================", end="\n\n")