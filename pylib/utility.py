#!/usr/bin/env python3
""" utility.py
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

import numpy as np
from typing import List

# Data Structures define - class #


# Functions define #

def window_indexing(sequence: List, window_size=16):
    size = len(sequence)
    X = [sequence[i:i + window_size] for i in range(size - window_size)]
    y = [sequence[i + window_size] for i in range(size - window_size)]
    X = np.array(X); y = np.array(y)
    
    return X, y

def update_window(X, x):
    return np.concatenate((X[1:], np.array(x).reshape((1,))))

# Closure & Decorator

