#!/usr/bin/env python3
"""
Break Reminder - Enhanced Edition
A modern break reminder application with improved UI and functionality.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import main

if __name__ == "__main__":
    sys.exit(main())