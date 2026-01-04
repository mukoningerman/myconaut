#!/usr/bin/env python3
"""
Myconaut - Runner Script
"""

import sys
import os

# Add the src directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'src'))

try:
    from main import main
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Script directory: {script_dir}")
    print(f"Files in src directory:")
    src_dir = os.path.join(script_dir, 'src')
    if os.path.exists(src_dir):
        for file in os.listdir(src_dir):
            print(f"  - {file}")
    else:
        print(f"src directory does not exist at {src_dir}")
    sys.exit(1)

if __name__ == "__main__":
    main()
