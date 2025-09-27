"""
Real-time Network Traffic Capture Module

This module captures live network traffic and converts it into features
suitable for anomaly detection analysis.
"""

import psutil
import socket
import time
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from typing import List, Dict, Any
import threading
import queue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkTrafficCapture:
    """Captures real-time network traffic and converts to ML features."""
    
    def __init__(self, capture_duration: int = 30, sample_interval: float = 1.0):
        """
        Initialize network traffic capture.
        
        Args:
            capture_duration: How long to capture traffic (seconds)
            sample_interval: How often to sample (seconds)
        """
        self.capture_duration = capture_duration
        self.sample_interval = sample_interval
        self.traffic_data = []
        self.is_capturing = False
        
    def get_network_connections(self) -> List[Dict[str, Any]]:
        """Get current network connections."""
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    connection_data = {
                        'local_ip': conn.laddr.ip,
                        'local_port': conn.laddr.port,
                        'remote_ip': conn.raddr.ip,
                        'remote_port': conn.raddr.port,
                        'status': conn.status,
                        'pid': conn.pid or 0,
                        'timestamp': datetime.now().isoformat()
                    }
                    connections.append(connection_data)
        except Exception as e:
            logger.error(f"Error getting network connections: {e}")
        
        return connections
    
    def get_network_io_stats(self) -> Dict[str, Any]:
        """Get network I/O statistics."""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout,
                'dropin': net_io.dropin,
                'dropout': net_io.dropout,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting network I/O stats: {e}")
            return {}
    
    def calculate_flow_features(self, connections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate flow-based features from connections."""
        if not connections:
            return self._get_empty_features()
        
        # Basic connection statistics
        total_connections = len(connections)
        unique_remote_ips = len(set(conn['remote_ip'] for conn in connections))
        unique_remote_ports = len(set(conn['remote_port'] for conn in connections))
        
        # Port analysis
        ports = [conn['remote_port'] for conn in connections]
        port_counts = {}
        for port in ports:
            port_counts[port] = port_counts.get(port, 0) + 1
        
        # Common ports analysis
        common_ports = [80, 443, 22, 21, 25, 53, 110, 143, 993, 995]
        common_port_connections = sum(1 for port in ports if port in common_ports)
        
        # High port connections (potential suspicious activity)
        high_port_connections = sum(1 for port in ports if port > 1024)
        
        # Calculate features similar to NetFlow
        features = {
            'total_connections': total_connections,
            'unique_remote_ips': unique_remote_ips,
            'unique_remote_ports': unique_remote_ports,
            'common_port_ratio': common_port_connections / total_connections if total_connections > 0 else 0,
            'high_port_ratio': high_port_connections / total_connections if total_connections > 0 else 0,
            'avg_connections_per_ip': total_connections / unique_remote_ips if unique_remote_ips > 0 else 0,
            'port_entropy': self._calculate_entropy(list(port_counts.values())),
            'timestamp': datetime.now().isoformat()
        }
        
        return features
    
    def _calculate_entropy(self, values: List[int]) -> float:
        """Calculate Shannon entropy."""
        if not values or sum(values) == 0:
            return 0.0
        
        total = sum(values)
        probabilities = [v / total for v in values if v > 0]
        entropy = -sum(p * np.log2(p) for p in probabilities)
        return float(entropy)
    
    def _get_empty_features(self) -> Dict[str, Any]:
        """Return empty features when no data is available."""
        return {
            'total_connections': 0,
            'unique_remote_ips': 0,
            'unique_remote_ports': 0,
            'common_port_ratio': 0.0,
            'high_port_ratio': 0.0,
            'avg_connections_per_ip': 0.0,
            'port_entropy': 0.0,
            'timestamp': datetime.now().isoformat()
        }
    
    def capture_traffic(self) -> List[Dict[str, Any]]:
        """Capture network traffic for the specified duration."""
        logger.info(f"Starting network traffic capture for {self.capture_duration} seconds...")
        self.is_capturing = True
        self.traffic_data = []
        
        start_time = time.time()
        
        while self.is_capturing and (time.time() - start_time) < self.capture_duration:
            try:
                # Get current connections
                connections = self.get_network_connections()
                
                # Get network I/O stats
                io_stats = self.get_network_io_stats()
                
                # Calculate flow features
                flow_features = self.calculate_flow_features(connections)
                
                # Combine all data
                sample_data = {
                    **flow_features,
                    **io_stats,
                    'connection_count': len(connections)
                }
                
                self.traffic_data.append(sample_data)
                logger.info(f"Captured sample {len(self.traffic_data)}: {len(connections)} connections")
                
                # Wait for next sample
                time.sleep(self.sample_interval)
                
            except Exception as e:
                logger.error(f"Error during traffic capture: {e}")
                time.sleep(self.sample_interval)
        
        self.is_capturing = False
        logger.info(f"Traffic capture completed. Collected {len(self.traffic_data)} samples.")
        return self.traffic_data
    
    def stop_capture(self):
        """Stop the traffic capture."""
        self.is_capturing = False
    
    def get_captured_data(self) -> pd.DataFrame:
        """Convert captured data to DataFrame."""
        if not self.traffic_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.traffic_data)
        
        # Add derived features
        if len(df) > 1:
            df['bytes_per_second'] = df['bytes_sent'].diff().fillna(0) / self.sample_interval
            df['packets_per_second'] = df['packets_sent'].diff().fillna(0) / self.sample_interval
            df['connection_rate'] = df['total_connections'].diff().fillna(0) / self.sample_interval
        else:
            df['bytes_per_second'] = 0
            df['packets_per_second'] = 0
            df['connection_rate'] = 0
        
        return df
    
    def save_to_csv(self, filepath: str) -> str:
        """Save captured data to CSV file."""
        df = self.get_captured_data()
        if df.empty:
            raise ValueError("No data captured to save")
        
        df.to_csv(filepath, index=False)
        logger.info(f"Captured data saved to {filepath}")
        return filepath


def capture_network_sample(duration: int = 30, output_file: str = None) -> str:
    """
    Capture a sample of network traffic.
    
    Args:
        duration: Duration to capture (seconds)
        output_file: Output file path (optional)
    
    Returns:
        Path to the saved CSV file
    """
    if output_file is None:
        output_file = f"data/network_capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Ensure data directory exists
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Capture traffic
    capture = NetworkTrafficCapture(capture_duration=duration)
    capture.capture_traffic()
    
    # Save to file
    capture.save_to_csv(output_file)
    return output_file


if __name__ == "__main__":
    # Example usage
    print("Capturing network traffic for 30 seconds...")
    filepath = capture_network_sample(duration=30)
    print(f"Network data saved to: {filepath}")
