"""
Network Security Analyzer - Consolidated Module

This module provides comprehensive network security analysis capabilities including
data processing, anomaly detection, and visualization for network flow data.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkDataProcessor:
    """Handles preprocessing of network flow data for anomaly detection."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca_2d = None
        self.pca_3d = None
        self.feature_columns = None
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load network flow data from CSV file."""
        try:
            logger.info(f"Loading data from {file_path}")
            data = pd.read_csv(file_path)
            logger.info(f"Data loaded successfully. Shape: {data.shape}")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def preprocess_data(self, data: pd.DataFrame, target_column: str = 'Label') -> pd.DataFrame:
        """Preprocess the network flow data."""
        logger.info("Starting data preprocessing...")
        
        processed_data = data.copy()
        
        # Check for missing values
        null_columns = processed_data.columns[processed_data.isnull().any()]
        if len(null_columns) > 0:
            logger.info(f"Found null values in columns: {list(null_columns)}")
            processed_data = processed_data.dropna()
            logger.info("Dropped rows with null values")
        
        # Clean column names
        processed_data.columns = processed_data.columns.str.strip()
        
        # Drop target column if it exists
        if target_column in processed_data.columns:
            processed_data = processed_data.drop([target_column], axis=1)
            logger.info(f"Dropped target column: {target_column}")
        
        # Handle infinite values
        inf_count = np.isinf(processed_data.select_dtypes(include=[np.number])).sum().sum()
        if inf_count > 0:
            logger.info(f"Found {inf_count} infinite values. Replacing with NaN and dropping.")
            processed_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            processed_data = processed_data.dropna()
        
        self.feature_columns = processed_data.columns.tolist()
        logger.info(f"Preprocessing completed. Final shape: {processed_data.shape}")
        return processed_data
    
    def scale_features(self, data: pd.DataFrame, fit: bool = True) -> np.ndarray:
        """Scale features using StandardScaler."""
        logger.info("Scaling features...")
        
        if fit:
            scaled_data = self.scaler.fit_transform(data)
            logger.info("Scaler fitted and data transformed")
        else:
            scaled_data = self.scaler.transform(data)
            logger.info("Data transformed using existing scaler")
        
        return scaled_data
    
    def apply_pca(self, scaled_data: np.ndarray, n_components: int = 2) -> tuple:
        """Apply PCA for dimensionality reduction."""
        logger.info(f"Applying PCA with {n_components} components...")
        
        pca = PCA(n_components=n_components)
        pca_result = pca.fit_transform(scaled_data)
        
        if n_components == 2:
            self.pca_2d = pca
        elif n_components == 3:
            self.pca_3d = pca
        
        explained_variance = pca.explained_variance_ratio_
        logger.info(f"PCA completed. Explained variance ratio: {explained_variance}")
        
        return pca_result, pca
    
    def create_pca_dataframe(self, pca_result: np.ndarray, n_components: int) -> pd.DataFrame:
        """Create a DataFrame from PCA results."""
        if n_components == 2:
            columns = ['PC1', 'PC2']
        elif n_components == 3:
            columns = ['PC1', 'PC2', 'PC3']
        else:
            columns = [f'PC{i+1}' for i in range(n_components)]
        
        pca_df = pd.DataFrame(pca_result, columns=columns)
        return pca_df
    
    def get_feature_importance(self, n_components: int = 2) -> pd.DataFrame:
        """Get feature importance from PCA components."""
        pca_obj = self.pca_2d if n_components == 2 else self.pca_3d
        
        if pca_obj is None:
            raise ValueError("PCA must be fitted first")
        
        feature_importance = pd.DataFrame(
            pca_obj.components_.T,
            columns=[f'PC{i+1}' for i in range(n_components)],
            index=self.feature_columns
        )
        
        return feature_importance


class NetworkAnomalyDetector:
    """Detects anomalies in network flow data using machine learning."""
    
    def __init__(self, algorithm: str = 'isolation_forest'):
        self.algorithm = algorithm
        self.model = None
        self.is_fitted = False
        
    def fit(self, data: np.ndarray, contamination: float = 0.1) -> None:
        """Fit the anomaly detection model."""
        logger.info(f"Fitting {self.algorithm} model with contamination={contamination}")
        
        if self.algorithm == 'isolation_forest':
            self.model = IsolationForest(
                contamination=contamination,
                random_state=42,
                n_estimators=100
            )
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        
        self.model.fit(data)
        self.is_fitted = True
        logger.info("Model fitted successfully")
    
    def predict(self, data: np.ndarray) -> np.ndarray:
        """Predict anomalies in the data."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        predictions = self.model.predict(data)
        return predictions
    
    def score_samples(self, data: np.ndarray) -> np.ndarray:
        """Get anomaly scores for samples."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before scoring samples")
        
        scores = self.model.score_samples(data)
        return scores
    
    def generate_report(self, predictions: np.ndarray, scores: np.ndarray) -> dict:
        """Generate a comprehensive analysis report."""
        total_samples = len(predictions)
        normal_count = int(np.sum(predictions == 1))
        anomaly_count = int(np.sum(predictions == -1))
        anomaly_percentage = (anomaly_count / total_samples) * 100
        
        report = {
            'algorithm': self.algorithm,
            'total_samples': int(total_samples),
            'normal_count': int(normal_count),
            'anomaly_count': int(anomaly_count),
            'anomaly_percentage': round(anomaly_percentage, 2),
            'score_statistics': {
                'min_score': float(np.min(scores)),
                'max_score': float(np.max(scores)),
                'mean_score': float(np.mean(scores)),
                'std_score': float(np.std(scores))
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return report


class AnomalyAlertSystem:
    """Manages anomaly alerts and notifications."""
    
    def __init__(self, threshold: float = -0.2):
        self.threshold = threshold
        
    def generate_alerts(self, predictions: np.ndarray, scores: np.ndarray, 
                       original_data: pd.DataFrame) -> pd.DataFrame:
        """Generate alerts for high-confidence anomalies."""
        # Get indices of anomalies below threshold
        anomaly_indices = np.where((predictions == -1) & (scores < self.threshold))[0]
        
        if len(anomaly_indices) == 0:
            return pd.DataFrame()
        
        # Create alerts DataFrame
        alerts_data = []
        for idx in anomaly_indices:
            alert = {
                'anomaly_score': float(scores[idx]),
                'severity': 'High' if scores[idx] < -0.5 else 'Medium',
                'timestamp': datetime.now().isoformat()
            }
            
            # Add relevant features from original data
            if idx < len(original_data):
                for col in original_data.columns:
                    if col in ['Destination Port', 'Flow Duration', 'Total Fwd Packets', 
                              'Total Backward Packets', 'Flow Bytes/s']:
                        alert[col] = original_data.iloc[idx][col]
            
            alerts_data.append(alert)
        
        alerts_df = pd.DataFrame(alerts_data)
        return alerts_df


class NetworkSecurityAnalyzer:
    """Main class that orchestrates the entire analysis pipeline."""
    
    def __init__(self):
        self.data_processor = NetworkDataProcessor()
        self.anomaly_detector = NetworkAnomalyDetector()
        self.alert_system = AnomalyAlertSystem()
        
    def analyze_network(self, data_path: str, contamination: float = 0.1, 
                       threshold: float = -0.2) -> dict:
        """Run complete network security analysis."""
        logger.info("Starting network security analysis...")
        
        # Load and preprocess data
        raw_data = self.data_processor.load_data(data_path)
        processed_data = self.data_processor.preprocess_data(raw_data)
        scaled_data = self.data_processor.scale_features(processed_data)
        
        # Apply PCA
        pca_2d_result, pca_2d_obj = self.data_processor.apply_pca(scaled_data, n_components=2)
        pca_3d_result, pca_3d_obj = self.data_processor.apply_pca(scaled_data, n_components=3)
        
        # Create PCA DataFrames
        pca_2d_df = self.data_processor.create_pca_dataframe(pca_2d_result, 2)
        pca_3d_df = self.data_processor.create_pca_dataframe(pca_3d_result, 3)
        
        # Detect anomalies
        self.anomaly_detector.fit(scaled_data, contamination)
        predictions = self.anomaly_detector.predict(scaled_data)
        anomaly_scores = self.anomaly_detector.score_samples(scaled_data)
        
        # Generate report and alerts
        report = self.anomaly_detector.generate_report(predictions, anomaly_scores)
        self.alert_system.threshold = threshold
        alerts = self.alert_system.generate_alerts(predictions, anomaly_scores, processed_data)
        
        # Prepare results
        results = {
            'report': report,
            'pca_2d': {
                'data': pca_2d_df.to_dict('records'),
                'explained_variance': [float(x) for x in pca_2d_obj.explained_variance_ratio_.tolist()]
            },
            'pca_3d': {
                'data': pca_3d_df.to_dict('records'),
                'explained_variance': [float(x) for x in pca_3d_obj.explained_variance_ratio_.tolist()]
            },
            'predictions': [int(x) for x in predictions.tolist()],
            'anomaly_scores': [float(x) for x in anomaly_scores.tolist()],
            'alerts': alerts.astype(str).to_dict('records') if not alerts.empty else [],
            'feature_importance': {k: {kk: float(vv) for kk, vv in v.items()} 
                                 for k, v in self.data_processor.get_feature_importance(n_components=2).to_dict('index').items()},
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info("Network security analysis completed successfully")
        return results


def main():
    """Example usage of the NetworkSecurityAnalyzer."""
    analyzer = NetworkSecurityAnalyzer()
    
    # Run analysis
    results = analyzer.analyze_network(
        data_path='data/sample_network_data.csv',
        contamination=0.1,
        threshold=-0.2
    )
    
    print("Analysis completed successfully!")
    print(f"Total samples: {results['report']['total_samples']}")
    print(f"Anomalies detected: {results['report']['anomaly_count']}")
    print(f"Alert count: {len(results['alerts'])}")


if __name__ == "__main__":
    main()
