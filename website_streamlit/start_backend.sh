#!/bin/bash

# Start the backend server
echo "Starting RoboInvesting Backend Server..."
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env.example file..."
    echo ""
    echo "Please create a .env file with your OPENAI_API_KEY:"
    echo "OPENAI_API_KEY=your_api_key_here"
    echo ""
    echo "You can get your API key from: https://platform.openai.com/api-keys"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if OPENAI_API_KEY is set in environment
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set in environment variables."
    echo "Checking .env file..."
    if [ -f .env ]; then
        export $(cat .env | grep -v '^#' | xargs)
        echo "✅ Loaded OPENAI_API_KEY from .env file"
    else
        echo "❌ No .env file found and OPENAI_API_KEY not set!"
        echo "Please set OPENAI_API_KEY environment variable or create a .env file"
        exit 1
    fi
else
    echo "✅ OPENAI_API_KEY found in environment"
fi

echo ""
echo "🚀 Starting backend server on http://localhost:8080"
echo "Press Ctrl+C to stop the server"
echo ""

python backend_server.py

