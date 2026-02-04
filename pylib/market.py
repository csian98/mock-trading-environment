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
from abc import ABC, abstractmethod

# Data Structures define - class #

class Market(ABC):
    def __init__(self, symbols: List):
        self._symbols = set(symbols)
        self._queue = {}

    @abstractmethod
    def history(self) -> dict:
        pass

    @abstractmethod
    def empty(self) -> bool:
        pass
            
    @abstractmethod
    def next(self) -> dict:
        pass

# Functions define #


# Closure & Decorator

