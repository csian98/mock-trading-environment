# Import #
import os, sys
sys.path.append("pylib/")

from trader_bollinger_rsi import Trader

# Main function define #

def main(*args, **kwargs):
    cash = 100000	# 100 k
    day = 0
    
    br_trader = Trader(cash)

    while not br_trader.empty():
        day += 1
        balance = br_trader.balance()
        br_trader.report(day)
        br_trader.trade()
        br_trader.next()
        

# EP
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))