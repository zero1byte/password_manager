#!/bin/bash

# Navigate to the directory where the script is
cd "$(dirname "$0")"

# Activate the virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found! Run setup.sh first."
    exit 1
fi

# Run the Python app
python3 main.py
