#!/usr/bin/env python3
""" main.py
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

from trader import Trader

# Main function define #

def main(*args, **kwargs):
    cash = 100000	# 100 k
    day = 0
    
    trader = Trader(cash)

    while not trader.empty():
        day += 1
        balance = trader.balance()
        trader.report(day)
        trader.trade()
        trader.next()
        

# EP
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
