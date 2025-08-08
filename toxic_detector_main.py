#!/usr/bin/env python3
"""
Toxic Detector AI - Main Application Entry Point
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from toxic_detector.app import main

if __name__ == "__main__":
    main() 