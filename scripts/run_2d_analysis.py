#!/usr/bin/env python3
"""
2D Network Security Analysis Script

This script performs 2D anomaly detection analysis on network traffic data
using machine learning algorithms to identify suspicious patterns.
"""

import sys
import os
import argparse
import pandas as pd
import numpy as np
from pathlib import Path

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processor import NetworkDataProcessor
from anomaly_detector import NetworkAnomalyDetector, AnomalyAlertSystem
from visualizer import NetworkFlowVisualizer

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run 2D network security analysis.
    """
    parser = argparse.ArgumentParser(description='Run 2D Network Security Analysis')
    parser.add_argument('--data', '-d', 
                       default='data/sample_network_data.csv',
                       help='Path to the CSV data file')
    parser.add_argument('--output', '-o',
                       default='results',
                       help='Output directory for results')
    parser.add_argument('--contamination', '-c',
                       type=float, default=0.1,
                       help='Expected contamination rate for Isolation Forest')
    parser.add_argument('--threshold', '-t',
                       type=float, default=-0.2,
                       help='Anomaly score threshold for alerts')
    parser.add_argument('--save-plots', '-p',
                       action='store_true',
                       help='Save plots to files')
    parser.add_argument('--show-plots', '-s',
                       action='store_true',
                       help='Display plots interactively')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    logger.info("Starting 2D Network Security Analysis")
    logger.info(f"Data file: {args.data}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Contamination rate: {args.contamination}")
    logger.info(f"Alert threshold: {args.threshold}")
    
    try:
        # Step 1: Initialize components
        logger.info("Initializing components...")
        data_processor = NetworkDataProcessor()
        anomaly_detector = NetworkAnomalyDetector(
            algorithm='isolation_forest',
            contamination=args.contamination,
            random_state=42
        )
        visualizer = NetworkFlowVisualizer()
        alert_system = AnomalyAlertSystem(threshold=args.threshold)
        
        # Step 2: Load and preprocess data
        logger.info("Loading and preprocessing data...")
        raw_data = data_processor.load_data(args.data)
        processed_data = data_processor.preprocess_data(raw_data, target_column='Label')
        
        # Step 3: Scale features
        logger.info("Scaling features...")
        scaled_data = data_processor.scale_features(processed_data, fit=True)
        
        # Step 4: Apply PCA for 2D visualization
        logger.info("Applying 2D PCA...")
        pca_2d_result, pca_2d_obj = data_processor.apply_pca(scaled_data, n_components=2)
        pca_2d_df = data_processor.create_pca_dataframe(pca_2d_result, n_components=2)
        
        # Step 5: Train anomaly detector
        logger.info("Training anomaly detector...")
        anomaly_detector.fit(scaled_data, feature_names=processed_data.columns.tolist())
        
        # Step 6: Generate predictions and scores
        logger.info("Generating anomaly predictions...")
        predictions = anomaly_detector.predict(scaled_data)
        anomaly_scores = anomaly_detector.decision_function(scaled_data)
        
        # Step 7: Generate comprehensive report
        logger.info("Generating anomaly report...")
        report = anomaly_detector.get_anomaly_report(scaled_data, processed_data)
        
        # Print summary statistics
        print("\\n" + "="*60)
        print("NETWORK SECURITY ANALYSIS SUMMARY (2D)")
        print("="*60)
        print(f"Algorithm: {report['algorithm']}")
        print(f"Total samples analyzed: {report['total_samples']:,}")
        print(f"Normal flows: {report['normal_count']:,}")
        print(f"Anomalous flows: {report['anomaly_count']:,}")
        print(f"Anomaly percentage: {report['anomaly_percentage']:.2f}%")
        print(f"Score range: {report['score_statistics']['min_score']:.3f} to {report['score_statistics']['max_score']:.3f}")
        print(f"Mean anomaly score: {report['score_statistics']['mean_score']:.3f}")
        
        # Step 8: Generate alerts
        logger.info("Generating security alerts...")
        important_columns = [
            'Destination Port', 'Flow Duration', 'Total Fwd Packets', 
            'Total Backward Packets', 'Flow Bytes/s'
        ]
        # Filter important columns that actually exist in the data
        existing_important_columns = [col for col in important_columns if col in processed_data.columns]
        
        alerts = alert_system.generate_alerts(
            processed_data, 
            anomaly_scores, 
            predictions,
            important_columns=existing_important_columns
        )
        
        if not alerts.empty:
            print(f"\\n🚨 SECURITY ALERTS: {len(alerts)} high-confidence anomalies detected!")
            print("Top 5 security alerts:")
            print(alerts.head().to_string())
            
            # Save alerts to CSV
            alert_file = output_dir / "security_alerts_2d.csv"
            alert_system.save_alerts(alerts, alert_file)
        else:
            print(f"\\n✅ No high-confidence security threats detected below threshold {args.threshold}")
        
        # Step 9: Create visualizations
        logger.info("Creating security visualizations...")
        
        # Add predictions and scores to PCA dataframe
        pca_2d_df['prediction'] = predictions
        pca_2d_df['anomaly_score'] = anomaly_scores
        
        # Anomaly scores distribution
        fig_scores = visualizer.plot_anomaly_scores_distribution(
            anomaly_scores, 
            threshold=args.threshold,
            save_path=output_dir / "anomaly_scores_distribution_2d.png" if args.save_plots else None
        )
        
        # 2D PCA plot
        fig_pca = visualizer.plot_pca_2d(
            pca_2d_df, 
            predictions,
            title="2D Network Security Analysis - Normal vs Anomalous Traffic",
            save_path=output_dir / "security_analysis_2d.png" if args.save_plots else None
        )
        
        # Step 10: Save model and results
        logger.info("Saving analysis results...")
        
        # Save trained model
        model_file = output_dir / "security_model_2d.joblib"
        anomaly_detector.save_model(model_file)
        
        # Save PCA results
        pca_results_file = output_dir / "pca_results_2d.csv"
        pca_2d_df.to_csv(pca_results_file, index=False)
        
        # Save detailed report
        report_file = output_dir / "security_analysis_report_2d.txt"
        with open(report_file, 'w') as f:
            f.write("2D Network Security Analysis Report\\n")
            f.write("=" * 50 + "\\n\\n")
            f.write(f"Algorithm: {report['algorithm']}\\n")
            f.write(f"Total samples: {report['total_samples']:,}\\n")
            f.write(f"Normal flows: {report['normal_count']:,}\\n")
            f.write(f"Anomalous flows: {report['anomaly_count']:,}\\n")
            f.write(f"Anomaly percentage: {report['anomaly_percentage']:.2f}%\\n")
            f.write(f"Alert threshold: {args.threshold}\\n")
            f.write(f"High-confidence alerts: {len(alerts)}\\n\\n")
            
            f.write("Score Statistics:\\n")
            f.write(f"  Min score: {report['score_statistics']['min_score']:.3f}\\n")
            f.write(f"  Max score: {report['score_statistics']['max_score']:.3f}\\n")
            f.write(f"  Mean score: {report['score_statistics']['mean_score']:.3f}\\n")
            f.write(f"  Std score: {report['score_statistics']['std_score']:.3f}\\n\\n")
            
            f.write("PCA Information:\\n")
            explained_variance = pca_2d_obj.explained_variance_ratio_
            f.write(f"  PC1 explained variance: {explained_variance[0]:.3f}\\n")
            f.write(f"  PC2 explained variance: {explained_variance[1]:.3f}\\n")
            f.write(f"  Total explained variance: {explained_variance.sum():.3f}\\n")
        
        print(f"\\n📊 Results saved to: {output_dir}")
        print(f"  - Model: {model_file}")
        print(f"  - PCA results: {pca_results_file}")
        print(f"  - Analysis report: {report_file}")
        if not alerts.empty:
            print(f"  - Security alerts: {output_dir / 'security_alerts_2d.csv'}")
        if args.save_plots:
            print(f"  - Plots: {output_dir / '*.png'}")
        
        # Step 11: Display plots if requested
        if args.show_plots:
            logger.info("Displaying plots...")
            visualizer.show_all_plots()
        else:
            visualizer.close_all_plots()
        
        logger.info("2D network security analysis completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise


if __name__ == "__main__":
    main()
