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

class Model(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def fit(self, X, y) -> None:
        pass

    @abstractmethod
    def predict(self, X) -> float:
        pass

    @abstractmethod
    def predict_multiple(self, X, count=3) -> List:
        pass

# Functions define #


# Closure & Decorator

