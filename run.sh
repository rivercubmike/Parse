#!/bin/bash

# Startup script for ZOHO Lead Parser

echo "Starting ZOHO Lead Parser..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found!"
    echo "Please create .env file from .env.example and add your ZOHO credentials"
    exit 1
fi

# Run the application
echo "Starting server on http://localhost:8000"
echo "API documentation available at http://localhost:8000/docs"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
