# Import #
import os, sys

sys.path.append("pylib/")
import numpy as np
from trader_bollinger_rsi import Trader

# Main function define #


def main(*args, **kwargs):
    cash = 100000  # 100 k
    day = 0

    br_trader = Trader(cash)
    balances = []

    while not br_trader.empty():
        day += 1
        balances.append(br_trader.balance())
        br_trader.report(day)
        br_trader.trade()
        br_trader.next()

    print(f"Final Balance: ${br_trader.balance():.2f}")
    print(f"Total Return: {(br_trader.balance() - cash) / cash * 100:.2f}%")
    print(
        f"Sharpe Ratio: {(np.mean(np.diff(balances)) / np.std(np.diff(balances))):.2f}"
    )


# EP
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
