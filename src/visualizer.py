"""
Visualization Module for NetFlow Anomaly Detection

This module provides various visualization functions for analyzing
network flow anomalies in 2D and 3D space.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import seaborn as sns
from typing import Optional, Tuple, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style for matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class NetworkFlowVisualizer:
    """
    Provides visualization capabilities for network flow anomaly detection.
    """
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Initialize the visualizer.
        
        Args:
            figsize (tuple): Default figure size for matplotlib plots
        """
        self.figsize = figsize
        self.color_map = {1: 'Normal', -1: 'Anomaly'}
        self.colors = {'Normal': 'blue', 'Anomaly': 'red'}
    
    def plot_anomaly_scores_distribution(self, 
                                       anomaly_scores: np.ndarray, 
                                       threshold: Optional[float] = None,
                                       save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot the distribution of anomaly scores.
        
        Args:
            anomaly_scores (np.ndarray): Array of anomaly scores
            threshold (float, optional): Threshold line to display
            save_path (str, optional): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create histogram
        ax.hist(anomaly_scores, bins=50, color='skyblue', alpha=0.7, edgecolor='black')
        
        # Add threshold line if provided
        if threshold is not None:
            ax.axvline(x=threshold, color='red', linestyle='--', linewidth=2, 
                      label=f'Threshold: {threshold}')
            ax.legend()
        
        # Formatting
        ax.set_title('Distribution of Anomaly Scores', fontsize=16, fontweight='bold')
        ax.set_xlabel('Anomaly Score', fontsize=12)
        ax.set_ylabel('Number of Flows', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Add statistics text
        stats_text = f'Mean: {np.mean(anomaly_scores):.3f}\\nStd: {np.std(anomaly_scores):.3f}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")
        
        return fig
    
    def plot_pca_2d(self, 
                    pca_df: pd.DataFrame, 
                    predictions: np.ndarray,
                    title: str = "2D PCA of Network Traffic",
                    save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a 2D PCA scatter plot with anomalies highlighted.
        
        Args:
            pca_df (pd.DataFrame): DataFrame with PC1 and PC2 columns
            predictions (np.ndarray): Anomaly predictions (1 for normal, -1 for anomaly)
            title (str): Plot title
            save_path (str, optional): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Add predictions to dataframe
        plot_df = pca_df.copy()
        plot_df['prediction'] = predictions
        plot_df['label'] = plot_df['prediction'].map(self.color_map)
        
        # Plot normal points
        normal_data = plot_df[plot_df['prediction'] == 1]
        ax.scatter(normal_data['PC1'], normal_data['PC2'], 
                  c=self.colors['Normal'], label='Normal', alpha=0.6, s=30)
        
        # Plot anomaly points
        anomaly_data = plot_df[plot_df['prediction'] == -1]
        ax.scatter(anomaly_data['PC1'], anomaly_data['PC2'], 
                  c=self.colors['Anomaly'], label='Anomaly', alpha=0.8, s=40, marker='^')
        
        # Formatting
        ax.set_xlabel('Principal Component 1', fontsize=12)
        ax.set_ylabel('Principal Component 2', fontsize=12)
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add count information
        normal_count = len(normal_data)
        anomaly_count = len(anomaly_data)
        count_text = f'Normal: {normal_count}\\nAnomalies: {anomaly_count}'
        ax.text(0.02, 0.98, count_text, transform=ax.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")
        
        return fig
    
    def plot_pca_3d_matplotlib(self, 
                              pca_df: pd.DataFrame, 
                              predictions: np.ndarray,
                              title: str = "3D PCA of Network Traffic",
                              save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a 3D PCA scatter plot using matplotlib.
        
        Args:
            pca_df (pd.DataFrame): DataFrame with PC1, PC2, PC3 columns
            predictions (np.ndarray): Anomaly predictions
            title (str): Plot title
            save_path (str, optional): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Add predictions to dataframe
        plot_df = pca_df.copy()
        plot_df['prediction'] = predictions
        
        # Plot normal points
        normal_data = plot_df[plot_df['prediction'] == 1]
        ax.scatter(normal_data['PC1'], normal_data['PC2'], normal_data['PC3'],
                  c=self.colors['Normal'], label='Normal', alpha=0.5, s=20)
        
        # Plot anomaly points
        anomaly_data = plot_df[plot_df['prediction'] == -1]
        ax.scatter(anomaly_data['PC1'], anomaly_data['PC2'], anomaly_data['PC3'],
                  c=self.colors['Anomaly'], label='Anomaly', alpha=0.8, s=30, marker='^')
        
        # Formatting
        ax.set_xlabel('Principal Component 1', fontsize=12)
        ax.set_ylabel('Principal Component 2', fontsize=12)
        ax.set_zlabel('Principal Component 3', fontsize=12)
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")
        
        return fig
    
    def plot_pca_3d_interactive(self, 
                               merged_df: pd.DataFrame,
                               hover_columns: Optional[list] = None,
                               title: str = "3D PCA Interactive Anomaly Detection",
                               save_path: Optional[str] = None) -> go.Figure:
        """
        Create an interactive 3D PCA scatter plot using Plotly.
        
        Args:
            merged_df (pd.DataFrame): DataFrame with PCA components and original features
            hover_columns (list, optional): Columns to show in hover information
            title (str): Plot title
            save_path (str, optional): Path to save the plot
            
        Returns:
            go.Figure: The created Plotly figure
        """
        # Ensure we have the required columns
        required_cols = ['PC1', 'PC2', 'PC3', 'prediction']
        missing_cols = [col for col in required_cols if col not in merged_df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Create color mapping
        plot_df = merged_df.copy()
        plot_df['label'] = plot_df['prediction'].map(self.color_map)
        
        # Set default hover columns if not provided
        if hover_columns is None:
            numeric_cols = plot_df.select_dtypes(include=[np.number]).columns
            hover_columns = [col for col in numeric_cols if col not in ['PC1', 'PC2', 'PC3', 'prediction']][:5]
        
        # Create the interactive 3D scatter plot
        fig = px.scatter_3d(
            plot_df, 
            x='PC1', y='PC2', z='PC3',
            color='label',
            color_discrete_map={'Normal': 'blue', 'Anomaly': 'red'},
            hover_data=hover_columns,
            opacity=0.7,
            title=title
        )
        
        # Update layout
        fig.update_layout(
            scene=dict(
                xaxis_title='Principal Component 1',
                yaxis_title='Principal Component 2',
                zaxis_title='Principal Component 3'
            ),
            width=900,
            height=700,
            font=dict(size=12)
        )
        
        if save_path:
            fig.write_html(save_path)
            logger.info(f"Interactive plot saved to {save_path}")
        
        return fig
    
    def plot_feature_correlation_heatmap(self, 
                                       data: pd.DataFrame,
                                       title: str = "Feature Correlation Heatmap",
                                       save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a correlation heatmap of features.
        
        Args:
            data (pd.DataFrame): DataFrame with features
            title (str): Plot title
            save_path (str, optional): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        # Calculate correlation matrix
        correlation_matrix = data.corr()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Create heatmap
        sns.heatmap(correlation_matrix, 
                    annot=False, 
                    cmap='coolwarm', 
                    center=0,
                    square=True,
                    ax=ax,
                    cbar_kws={'shrink': 0.8})
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Heatmap saved to {save_path}")
        
        return fig
    
    def plot_anomaly_timeline(self, 
                            alerts_df: pd.DataFrame,
                            time_column: str = 'timestamp',
                            title: str = "Anomaly Detection Timeline",
                            save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a timeline plot of detected anomalies.
        
        Args:
            alerts_df (pd.DataFrame): DataFrame with anomaly alerts
            time_column (str): Name of the timestamp column
            title (str): Plot title
            save_path (str, optional): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        if time_column not in alerts_df.columns:
            logger.warning(f"Time column '{time_column}' not found. Cannot create timeline.")
            return None
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Group by time periods and count anomalies
        alerts_df[time_column] = pd.to_datetime(alerts_df[time_column])
        alerts_df['hour'] = alerts_df[time_column].dt.floor('H')
        hourly_counts = alerts_df.groupby('hour').size()
        
        # Create line plot
        ax.plot(hourly_counts.index, hourly_counts.values, marker='o', linewidth=2, markersize=6)
        ax.fill_between(hourly_counts.index, hourly_counts.values, alpha=0.3)
        
        # Formatting
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Number of Anomalies', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Timeline plot saved to {save_path}")
        
        return fig
    
    def create_dashboard_plots(self, 
                             pca_2d_df: pd.DataFrame,
                             pca_3d_df: pd.DataFrame,
                             predictions: np.ndarray,
                             anomaly_scores: np.ndarray,
                             save_dir: Optional[str] = None) -> Dict[str, plt.Figure]:
        """
        Create a comprehensive set of dashboard plots.
        
        Args:
            pca_2d_df (pd.DataFrame): 2D PCA results
            pca_3d_df (pd.DataFrame): 3D PCA results
            predictions (np.ndarray): Anomaly predictions
            anomaly_scores (np.ndarray): Anomaly scores
            save_dir (str, optional): Directory to save plots
            
        Returns:
            Dict[str, plt.Figure]: Dictionary of created figures
        """
        figures = {}
        
        # 1. Anomaly scores distribution
        figures['scores_dist'] = self.plot_anomaly_scores_distribution(
            anomaly_scores, 
            threshold=-0.2,
            save_path=f"{save_dir}/anomaly_scores_distribution.png" if save_dir else None
        )
        
        # 2. 2D PCA plot
        figures['pca_2d'] = self.plot_pca_2d(
            pca_2d_df, 
            predictions,
            save_path=f"{save_dir}/pca_2d_anomalies.png" if save_dir else None
        )
        
        # 3. 3D PCA plot
        figures['pca_3d'] = self.plot_pca_3d_matplotlib(
            pca_3d_df, 
            predictions,
            save_path=f"{save_dir}/pca_3d_anomalies.png" if save_dir else None
        )
        
        logger.info(f"Created {len(figures)} dashboard plots")
        return figures
    
    def show_all_plots(self):
        """Display all created plots."""
        plt.show()
    
    def close_all_plots(self):
        """Close all matplotlib plots to free memory."""
        plt.close('all')


def main():
    """
    Example usage of the NetworkFlowVisualizer class.
    """
    # Generate example data
    np.random.seed(42)
    
    # Create synthetic PCA data
    normal_2d = np.random.normal(0, 1, (1000, 2))
    anomaly_2d = np.random.normal(3, 0.5, (100, 2))
    pca_2d_data = np.vstack([normal_2d, anomaly_2d])
    
    normal_3d = np.random.normal(0, 1, (1000, 3))
    anomaly_3d = np.random.normal(3, 0.5, (100, 3))
    pca_3d_data = np.vstack([normal_3d, anomaly_3d])
    
    # Create predictions and scores
    predictions = np.array([1] * 1000 + [-1] * 100)
    anomaly_scores = np.random.normal(0, 1, 1100)
    anomaly_scores[-100:] -= 2  # Make anomalies have lower scores
    
    # Create DataFrames
    pca_2d_df = pd.DataFrame(pca_2d_data, columns=['PC1', 'PC2'])
    pca_3d_df = pd.DataFrame(pca_3d_data, columns=['PC1', 'PC2', 'PC3'])
    
    # Initialize visualizer
    visualizer = NetworkFlowVisualizer()
    
    # Create plots
    fig1 = visualizer.plot_anomaly_scores_distribution(anomaly_scores, threshold=-1.0)
    fig2 = visualizer.plot_pca_2d(pca_2d_df, predictions)
    fig3 = visualizer.plot_pca_3d_matplotlib(pca_3d_df, predictions)
    
    print("Visualization examples created successfully!")
    
    # Show plots
    visualizer.show_all_plots()


if __name__ == "__main__":
    main()
