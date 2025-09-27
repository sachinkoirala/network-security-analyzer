#!/usr/bin/env python3
"""
Network Security Analyzer - Main Entry Point

This is the unified entry point for the Network Security Analyzer.
It provides options to run the Flask API server or the Next.js dashboard.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_flask_api():
    """Start the Flask API server"""
    print("🚀 Starting Flask API server...")
    api_dir = Path(__file__).parent / "api"
    os.chdir(api_dir)
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  Not in virtual environment. Consider running ./start.sh instead.")
    
    # Install requirements if needed
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements. Please run: pip install -r requirements.txt")
        return
    
    # Start Flask app
    subprocess.run([sys.executable, "app.py"], check=True)

def run_dashboard():
    """Start the Next.js dashboard"""
    print("🚀 Starting Next.js dashboard...")
    dashboard_dir = Path(__file__).parent / "dashboard"
    os.chdir(dashboard_dir)
    
    # Install dependencies if needed
    subprocess.run(["npm", "install"], check=True)
    
    # Start Next.js dev server
    subprocess.run(["npm", "run", "dev"], check=True)

def run_dashboard_only():
    """Start only the Next.js dashboard (Flask API will start on demand)"""
    print("🚀 Starting Next.js dashboard...")
    print("💡 Flask API will start automatically when you run analysis")
    run_dashboard()

def run_both():
    """Start both Flask API and Next.js dashboard"""
    print("🚀 Starting both Flask API and Next.js dashboard...")
    
    # Start Flask API in background
    api_process = subprocess.Popen([
        sys.executable, "main.py", "--api"
    ], cwd=Path(__file__).parent)
    
    # Wait a moment for API to start
    import time
    time.sleep(3)
    
    # Start Next.js dashboard
    try:
        run_dashboard()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        api_process.terminate()
        api_process.wait()

def main():
    parser = argparse.ArgumentParser(description='Network Security Analyzer')
    parser.add_argument('--api', action='store_true', help='Run only the Flask API server')
    parser.add_argument('--dashboard', action='store_true', help='Run only the Next.js dashboard')
    parser.add_argument('--both', action='store_true', help='Run both API and dashboard')
    
    args = parser.parse_args()
    
    if args.api:
        run_flask_api()
    elif args.dashboard:
        run_dashboard()
    elif args.both:
        run_both()
    else:
        # Default: run only dashboard (API starts on demand)
        run_dashboard_only()

if __name__ == "__main__":
    main()
