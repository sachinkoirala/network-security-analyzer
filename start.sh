#!/bin/bash

# Network Security Analyzer - Quick Start Script

echo "🚀 Starting Network Security Analyzer..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd dashboard
npm install
cd ..

# Start both Flask API and Next.js dashboard
echo "🚀 Starting Flask API and Next.js dashboard..."

# Start Flask API in background
echo "🔧 Starting Flask API on port 5000..."
python main.py --api &
API_PID=$!

# Wait a moment for API to start
echo "⏳ Waiting for API to initialize..."
sleep 5

# Start Next.js dashboard
echo "🌐 Starting Next.js dashboard on port 3000..."
python main.py --dashboard &
DASHBOARD_PID=$!

# Function to handle cleanup on exit
cleanup() {
    echo "🛑 Shutting down services..."
    kill $API_PID 2>/dev/null
    kill $DASHBOARD_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo "✅ Both services are running!"
echo "🌐 Dashboard: http://localhost:3000"
echo "🔧 API: http://localhost:5000"
echo "Press Ctrl+C to stop both services"

# Wait for both processes
wait
