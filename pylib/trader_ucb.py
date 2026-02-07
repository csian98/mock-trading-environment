import os, sys

sys.path.append("pylib/")


from stock_market import StockMarket
import numpy as np


class Trader:
    def __init__(self, cash: float):
        # Most of the code here are the same as trader.py
        self.window_size = 30  # I set this larger to capture more history
        self.symbols = [
            "NVDA",
            "AAPL",
            "GOOG",
            "MSFT",
            "AMZN",
            "META",
            "TSLA",
            "AVGO",
            "ORCL",
            "NFLX",
        ]
        self.cash = cash
        self.charge = 0.0001
        self.last_symbol = None
        self.ucb_index = {symbol: np.inf for symbol in self.symbols}
        self.num_arm_pulls = {symbol: 0 for symbol in self.symbols}
        self.rewards = {symbol: [] for symbol in self.symbols}

        self.market = StockMarket(self.symbols)
        # self.models = ...

        self.T = 100  # time horizon for UCB

        history = self.market.history(period="2y", days=self.T + 1)
        self.prev_prices = {symbol: history[symbol][-1] for symbol in self.symbols}
        self.prices = self.market.next()
        self.counts = {symbol: 0 for symbol in self.symbols}

        A = set([])

        for symbol in self.symbols:
            prices = history[symbol]
            returns = prices[1:] / prices[:-1] - 1
            returns = returns[~np.isnan(returns)]
            returns = np.abs(returns)
            A.update(returns.tolist())

        p = 0.95
        self.c = np.quantile(list(A), p)

    def _calculate_reward(self, percent_return):
        clipped_return = np.clip(percent_return, -self.c, self.c)
        reward = (clipped_return + self.c) / (2 * self.c)
        return reward

    def update_ucb_index(self, symbol, day):
        percent_return = (
            self.prices[symbol] - self.prev_prices[symbol]
        ) / self.prev_prices[symbol]
        reward = self._calculate_reward(percent_return)
        self.rewards[symbol].append(reward)
        self.num_arm_pulls[symbol] += 1
        n = self.num_arm_pulls[symbol]
        self.ucb_index[symbol] = np.mean(self.rewards[symbol]) + np.sqrt(
            2 * np.log(day) / n
        )

    def _sell_all(self, symbol):
        count = self.counts[symbol]
        if count > 0:
            value = self.prices[symbol] * count
            self.cash += value * (1 - self.charge)
            self.counts[symbol] = 0

    def _buy_fraction(self, symbol, fraction):
        price = float(self.prices[symbol])
        effective_price = price * (1 + self.charge)

        cash_to_spend = self.cash * float(fraction)
        shares = int(cash_to_spend / effective_price)

        if shares < 1:
            shares = int(self.cash // effective_price)

        if shares > 0:
            cost = shares * effective_price
            self.cash -= cost
            self.counts[symbol] += shares

    def trade(self, day):
        if self.last_symbol is not None:
            self.update_ucb_index(self.last_symbol, day)

        # find stock with highest UCB index
        highest_index_symbol = self.symbols[0]
        for symbol in self.symbols:
            if self.ucb_index[symbol] > self.ucb_index[highest_index_symbol]:
                highest_index_symbol = symbol

        # sell previous day's holdings unless they are the same as the current highest index stock
        for symbol in self.symbols:
            if self.counts[symbol] > 0:
                if symbol == highest_index_symbol:
                    pass  # hold
                else:
                    self._sell_all(symbol)

        if self.counts[highest_index_symbol] == 0:
            self._buy_fraction(
                highest_index_symbol, fraction=0.5
            )  # Buy with 50% of available cash

        self.last_symbol = highest_index_symbol

    def next(self):
        self.prev_prices = self.prices.copy()
        self.prices = self.market.next()

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
                print(
                    f"{symbol}: ${self.prices[symbol]:.2f} X {count} = ${self.prices[symbol] * count:.2f}"
                )

        print(f"Net Asset: {self.balance():.2f}")
        print(f"====================", end="\n\n")
