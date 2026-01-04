#!/bin/bash

# Myconaut - Launch Script for Linux/Mac

echo "========================================"
echo "       Launching Myconaut v1.0.0        "
echo "========================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "ERROR: Python 3.8 or higher is required. Found Python $PYTHON_VERSION"
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip3 install colorama --user 2>/dev/null || pip install colorama --user

# Check if colorama is installed
python3 -c "import colorama" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing colorama..."
    pip3 install colorama --user
fi

# Create necessary directories
echo "Creating game directories..."
mkdir -p saves
mkdir -p data

# Run the game
echo "Starting game..."
echo "========================================"
echo ""

# Check for run.py
if [ -f "run.py" ]; then
    python3 run.py
elif [ -f "src/main.py" ]; then
    cd src
    python3 main.py
else
    echo "ERROR: Could not find game files."
    echo "Current directory: $(pwd)"
    echo "Files in directory:"
    ls -la
    exit 1
fi

echo ""
echo "========================================"
echo "        Thanks for playing!             "
echo "========================================"
