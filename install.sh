#!/bin/bash

# Exit on error
set -e

# Check Python version
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "🔁 Virtual environment already exists."
fi

# Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated."

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "📄 Installing from requirements.txt..."
    pip install -r requirements.txt
    echo "✅ All dependencies installed."
else
    echo "⚠️ requirements.txt not found. Please add your dependencies there."
fi
