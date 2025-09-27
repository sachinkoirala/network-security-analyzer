#!/usr/bin/env python3
"""
3D Network Security Analysis Script

This script performs 3D anomaly detection analysis on network traffic data
using machine learning algorithms with interactive visualizations.
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
    Main function to run 3D network security analysis.
    """
    parser = argparse.ArgumentParser(description='Run 3D Network Security Analysis')
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
    parser.add_argument('--interactive', '-i',
                       action='store_true',
                       help='Create interactive 3D plots with Plotly')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    logger.info("Starting 3D Network Security Analysis")
    logger.info(f"Data file: {args.data}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Contamination rate: {args.contamination}")
    logger.info(f"Alert threshold: {args.threshold}")
    logger.info(f"Interactive plots: {args.interactive}")
    
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
        
        # Step 4: Apply PCA for 2D and 3D visualization
        logger.info("Applying PCA transformations...")
        pca_2d_result, pca_2d_obj = data_processor.apply_pca(scaled_data, n_components=2)
        pca_3d_result, pca_3d_obj = data_processor.apply_pca(scaled_data, n_components=3)
        
        pca_2d_df = data_processor.create_pca_dataframe(pca_2d_result, n_components=2)
        pca_3d_df = data_processor.create_pca_dataframe(pca_3d_result, n_components=3)
        
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
        print("NETWORK SECURITY ANALYSIS SUMMARY (3D)")
        print("="*60)
        print(f"Algorithm: {report['algorithm']}")
        print(f"Total samples analyzed: {report['total_samples']:,}")
        print(f"Normal flows: {report['normal_count']:,}")
        print(f"Anomalous flows: {report['anomaly_count']:,}")
        print(f"Anomaly percentage: {report['anomaly_percentage']:.2f}%")
        print(f"Score range: {report['score_statistics']['min_score']:.3f} to {report['score_statistics']['max_score']:.3f}")
        print(f"Mean anomaly score: {report['score_statistics']['mean_score']:.3f}")
        
        # Step 8: Create merged dataframe for interactive plotting
        logger.info("Merging PCA results with original data...")
        
        # Add PCA results and predictions to original data
        merged_df = processed_data.reset_index(drop=True).copy()
        merged_df[['PC1', 'PC2', 'PC3']] = pca_3d_df[['PC1', 'PC2', 'PC3']]
        merged_df['prediction'] = predictions
        merged_df['anomaly_score'] = anomaly_scores
        
        # Step 9: Generate alerts
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
            alert_file = output_dir / "security_alerts_3d.csv"
            alert_system.save_alerts(alerts, alert_file)
        else:
            print(f"\\n✅ No high-confidence security threats detected below threshold {args.threshold}")
        
        # Step 10: Create visualizations
        logger.info("Creating security visualizations...")
        
        # Anomaly scores distribution
        fig_scores = visualizer.plot_anomaly_scores_distribution(
            anomaly_scores, 
            threshold=args.threshold,
            save_path=output_dir / "anomaly_scores_distribution_3d.png" if args.save_plots else None
        )
        
        # 2D PCA plot for comparison
        fig_2d = visualizer.plot_pca_2d(
            pca_2d_df, 
            predictions,
            title="2D Network Security Analysis (for comparison)",
            save_path=output_dir / "security_analysis_2d_comparison.png" if args.save_plots else None
        )
        
        # 3D PCA plot (matplotlib)
        fig_3d = visualizer.plot_pca_3d_matplotlib(
            pca_3d_df, 
            predictions,
            title="3D Network Security Analysis - Normal vs Anomalous Traffic",
            save_path=output_dir / "security_analysis_3d.png" if args.save_plots else None
        )
        
        # Interactive 3D plot (if requested)
        if args.interactive:
            logger.info("Creating interactive 3D visualization...")
            try:
                # Select a subset of hover columns for better performance
                hover_columns = [col for col in existing_important_columns if col in merged_df.columns][:3]
                hover_columns.append('anomaly_score')
                
                fig_interactive = visualizer.plot_pca_3d_interactive(
                    merged_df,
                    hover_columns=hover_columns,
                    title="3D Interactive Network Security Analysis",
                    save_path=output_dir / "interactive_security_analysis.html" if args.save_plots else None
                )
                
                if args.show_plots:
                    fig_interactive.show()
                    
            except Exception as e:
                logger.warning(f"Could not create interactive plot: {str(e)}")
        
        # Step 11: Save model and results
        logger.info("Saving analysis results...")
        
        # Save trained model
        model_file = output_dir / "security_model_3d.joblib"
        anomaly_detector.save_model(model_file)
        
        # Save PCA results
        pca_2d_file = output_dir / "pca_results_2d.csv"
        pca_3d_file = output_dir / "pca_results_3d.csv"
        merged_file = output_dir / "merged_analysis_results.csv"
        
        pca_2d_results = pca_2d_df.copy()
        pca_2d_results['prediction'] = predictions
        pca_2d_results['anomaly_score'] = anomaly_scores
        pca_2d_results.to_csv(pca_2d_file, index=False)
        
        pca_3d_results = pca_3d_df.copy()
        pca_3d_results['prediction'] = predictions
        pca_3d_results['anomaly_score'] = anomaly_scores
        pca_3d_results.to_csv(pca_3d_file, index=False)
        
        # Save subset of merged data to avoid huge files
        key_columns = ['PC1', 'PC2', 'PC3', 'prediction', 'anomaly_score'] + existing_important_columns
        merged_subset = merged_df[key_columns]
        merged_subset.to_csv(merged_file, index=False)
        
        # Save detailed report
        report_file = output_dir / "security_analysis_report_3d.txt"
        with open(report_file, 'w') as f:
            f.write("3D Network Security Analysis Report\\n")
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
            explained_variance_2d = pca_2d_obj.explained_variance_ratio_
            explained_variance_3d = pca_3d_obj.explained_variance_ratio_
            f.write(f"  2D PCA explained variance: {explained_variance_2d.sum():.3f}\\n")
            f.write(f"    PC1: {explained_variance_2d[0]:.3f}\\n")
            f.write(f"    PC2: {explained_variance_2d[1]:.3f}\\n")
            f.write(f"  3D PCA explained variance: {explained_variance_3d.sum():.3f}\\n")
            f.write(f"    PC1: {explained_variance_3d[0]:.3f}\\n")
            f.write(f"    PC2: {explained_variance_3d[1]:.3f}\\n")
            f.write(f"    PC3: {explained_variance_3d[2]:.3f}\\n")
        
        print(f"\\n📊 Results saved to: {output_dir}")
        print(f"  - Model: {model_file}")
        print(f"  - 2D PCA results: {pca_2d_file}")
        print(f"  - 3D PCA results: {pca_3d_file}")
        print(f"  - Merged results: {merged_file}")
        print(f"  - Analysis report: {report_file}")
        if not alerts.empty:
            print(f"  - Security alerts: {output_dir / 'security_alerts_3d.csv'}")
        if args.save_plots:
            print(f"  - Plots: {output_dir / '*.png'}")
            if args.interactive:
                print(f"  - Interactive plot: {output_dir / 'interactive_security_analysis.html'}")
        
        # Step 12: Display plots if requested
        if args.show_plots:
            logger.info("Displaying plots...")
            visualizer.show_all_plots()
        else:
            visualizer.close_all_plots()
        
        # PCA Analysis Summary
        print("\\n" + "="*60)
        print("PCA ANALYSIS SUMMARY")
        print("="*60)
        print(f"2D PCA total explained variance: {explained_variance_2d.sum():.1%}")
        print(f"3D PCA total explained variance: {explained_variance_3d.sum():.1%}")
        print(f"Additional variance captured by 3rd component: {explained_variance_3d[2]:.1%}")
        
        logger.info("3D network security analysis completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise


if __name__ == "__main__":
    main()
