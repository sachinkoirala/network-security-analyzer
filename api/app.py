"""
Flask API for Network Security Analyzer
Provides REST endpoints for ML analysis and network monitoring
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import os
import sys
from pathlib import Path
import logging
import subprocess
import psutil
import socket
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from network_analyzer import NetworkSecurityAnalyzer
from network_capture import NetworkTrafficCapture, capture_network_sample

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables for analysis state
current_analysis = None
analysis_results = None

class NetworkSecurityAPI:
    def __init__(self):
        self.analyzer = NetworkSecurityAnalyzer()
        
    def run_unified_analysis(self, data_path: str = None, contamination: float = 0.1, threshold: float = -0.2):
        """Run unified 2D and 3D analysis on real network traffic"""
        try:
            logger.info("Starting unified network security analysis...")
            
            connection_details = None
            
            # If no data path provided or it's the sample file, capture real network traffic
            if data_path is None or 'sample_network_data.csv' in data_path:
                logger.info("Capturing real network traffic...")
                capturer = NetworkTrafficCapture()  # Use random duration
                capturer.capture_traffic()
                connection_details = capturer.get_connection_details()
                
                # Save the captured data with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                data_path = capturer.save_to_csv(f"data/live_network_data_{timestamp}.csv")
                logger.info(f"Network traffic captured and saved to: {data_path}")
            
            results = self.analyzer.analyze_network(data_path, contamination, threshold, connection_details)
            
            # Add connection details to results for critical anomalies
            if connection_details:
                results['connection_details'] = connection_details
                logger.info(f"Added {len(connection_details)} connection details to results")
            
            logger.info("Analysis completed successfully")
            return results
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            raise
    
    def get_network_info(self):
        """Get current network information"""
        try:
            # Get network interfaces
            interfaces = []
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        interfaces.append({
                            'name': interface,
                            'ip': addr.address,
                            'netmask': addr.netmask
                        })
            
            # Get active connections
            connections = []
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED':
                    connections.append({
                        'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        'status': conn.status,
                        'pid': conn.pid
                    })
            
            return {
                'interfaces': interfaces,
                'connections': connections[:50],  # Limit to 50 connections
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting network info: {str(e)}")
            return {'error': str(e)}

# Initialize API
api = NetworkSecurityAPI()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/analyze', methods=['POST'])
def analyze_network():
    """Run network security analysis"""
    global current_analysis, analysis_results
    
    try:
        data = request.get_json() or {}
        data_path = data.get('data_path')  # Will capture real traffic if None
        contamination = data.get('contamination', 0.1)
        threshold = data.get('threshold', -0.2)
        
        logger.info("Starting analysis on real network traffic...")
        current_analysis = "running"
        
        # Run analysis (will capture real network traffic)
        results = api.run_unified_analysis(data_path, contamination, threshold)
        analysis_results = results
        current_analysis = "completed"
        
        return jsonify({
            'status': 'success',
            'analysis_status': current_analysis,
            'results': results
        })
        
    except Exception as e:
        current_analysis = "error"
        logger.error(f"Analysis failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'analysis_status': current_analysis,
            'error': str(e)
        }), 500

@app.route('/api/analysis/status', methods=['GET'])
def get_analysis_status():
    """Get current analysis status"""
    return jsonify({
        'status': current_analysis,
        'has_results': analysis_results is not None
    })

@app.route('/api/analysis/results', methods=['GET'])
def get_analysis_results():
    """Get analysis results"""
    if analysis_results is None:
        return jsonify({'error': 'No analysis results available'}), 404
    
    return jsonify(analysis_results)

@app.route('/api/network/info', methods=['GET'])
def get_network_info():
    """Get current network information"""
    try:
        network_info = api.get_network_info()
        return jsonify(network_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/network/monitor', methods=['GET'])
def monitor_network():
    """Start network monitoring"""
    try:
        # This would typically start a background monitoring process
        # For now, return current network state
        network_info = api.get_network_info()
        return jsonify({
            'status': 'monitoring',
            'data': network_info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
