"""
Anomaly Detection Module for NetFlow Analysis

This module implements anomaly detection algorithms for network flow data,
primarily using Isolation Forest but extensible to other algorithms.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
import joblib
import logging
from typing import Dict, Tuple, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkAnomalyDetector:
    """
    Implements various anomaly detection algorithms for network flow analysis.
    """
    
    def __init__(self, algorithm: str = 'isolation_forest', **kwargs):
        """
        Initialize the anomaly detector.
        
        Args:
            algorithm (str): Algorithm to use ('isolation_forest', 'one_class_svm', 'lof')
            **kwargs: Algorithm-specific parameters
        """
        self.algorithm = algorithm
        self.model = None
        self.is_fitted = False
        self.feature_names = None
        
        # Default parameters for each algorithm
        self.default_params = {
            'isolation_forest': {
                'n_estimators': 100,
                'contamination': 0.1,
                'random_state': 42,
                'n_jobs': -1
            },
            'one_class_svm': {
                'kernel': 'rbf',
                'gamma': 'scale',
                'nu': 0.1
            },
            'lof': {
                'n_neighbors': 20,
                'contamination': 0.1,
                'n_jobs': -1
            }
        }
        
        # Merge default params with user-provided params
        self.params = self.default_params.get(algorithm, {})
        self.params.update(kwargs)
        
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the model based on the selected algorithm."""
        if self.algorithm == 'isolation_forest':
            self.model = IsolationForest(**self.params)
        elif self.algorithm == 'one_class_svm':
            self.model = OneClassSVM(**self.params)
        elif self.algorithm == 'lof':
            self.model = LocalOutlierFactor(**self.params)
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
        
        logger.info(f"Initialized {self.algorithm} with parameters: {self.params}")
    
    def fit(self, X: np.ndarray, feature_names: Optional[list] = None) -> 'NetworkAnomalyDetector':
        """
        Fit the anomaly detection model.
        
        Args:
            X (np.ndarray): Training data
            feature_names (list, optional): Names of features
            
        Returns:
            NetworkAnomalyDetector: Self for method chaining
        """
        logger.info(f"Fitting {self.algorithm} model on data shape: {X.shape}")
        
        self.feature_names = feature_names
        
        try:
            if self.algorithm == 'lof':
                # LOF doesn't have a separate fit method, it fits during predict
                self.model.fit_predict(X)
            else:
                self.model.fit(X)
            
            self.is_fitted = True
            logger.info("Model fitted successfully")
            
        except Exception as e:
            logger.error(f"Error fitting model: {str(e)}")
            raise
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict anomalies in the data.
        
        Args:
            X (np.ndarray): Data to predict on
            
        Returns:
            np.ndarray: Predictions (1 for normal, -1 for anomaly)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        logger.info(f"Predicting anomalies for data shape: {X.shape}")
        
        try:
            if self.algorithm == 'lof':
                # For LOF, we need to refit on the new data
                predictions = self.model.fit_predict(X)
            else:
                predictions = self.model.predict(X)
            
            anomaly_count = np.sum(predictions == -1)
            normal_count = np.sum(predictions == 1)
            
            logger.info(f"Predictions completed: {normal_count} normal, {anomaly_count} anomalies")
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise
    
    def decision_function(self, X: np.ndarray) -> np.ndarray:
        """
        Get anomaly scores for the data.
        
        Args:
            X (np.ndarray): Data to score
            
        Returns:
            np.ndarray: Anomaly scores (lower = more anomalous)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before scoring")
        
        if self.algorithm == 'lof':
            logger.warning("LOF doesn't support decision_function, using negative_outlier_factor_")
            return self.model.negative_outlier_factor_
        
        try:
            scores = self.model.decision_function(X)
            logger.info(f"Anomaly scores computed for {len(scores)} samples")
            return scores
            
        except Exception as e:
            logger.error(f"Error computing decision function: {str(e)}")
            raise
    
    def get_anomaly_report(self, X: np.ndarray, original_data: Optional[pd.DataFrame] = None) -> Dict:
        """
        Generate a comprehensive anomaly report.
        
        Args:
            X (np.ndarray): Scaled data for prediction
            original_data (pd.DataFrame, optional): Original unscaled data
            
        Returns:
            Dict: Comprehensive anomaly report
        """
        predictions = self.predict(X)
        
        try:
            scores = self.decision_function(X)
        except:
            scores = np.zeros_like(predictions)  # Fallback for algorithms without decision function
        
        # Basic statistics
        total_samples = len(predictions)
        anomaly_count = np.sum(predictions == -1)
        normal_count = np.sum(predictions == 1)
        anomaly_percentage = (anomaly_count / total_samples) * 100
        
        report = {
            'algorithm': self.algorithm,
            'total_samples': total_samples,
            'normal_count': normal_count,
            'anomaly_count': anomaly_count,
            'anomaly_percentage': round(anomaly_percentage, 2),
            'score_statistics': {
                'min_score': float(np.min(scores)),
                'max_score': float(np.max(scores)),
                'mean_score': float(np.mean(scores)),
                'std_score': float(np.std(scores))
            }
        }
        
        # Add anomaly details if original data is provided
        if original_data is not None:
            anomaly_indices = np.where(predictions == -1)[0]
            if len(anomaly_indices) > 0:
                anomaly_data = original_data.iloc[anomaly_indices].copy()
                anomaly_data['anomaly_score'] = scores[anomaly_indices]
                anomaly_data['prediction'] = predictions[anomaly_indices]
                
                # Get top 10 most anomalous samples
                top_anomalies = anomaly_data.nsmallest(10, 'anomaly_score')
                report['top_anomalies'] = top_anomalies.to_dict('records')
        
        logger.info(f"Generated anomaly report: {anomaly_count}/{total_samples} anomalies detected")
        return report
    
    def save_model(self, filepath: str):
        """
        Save the trained model to disk.
        
        Args:
            filepath (str): Path to save the model
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        model_data = {
            'model': self.model,
            'algorithm': self.algorithm,
            'params': self.params,
            'feature_names': self.feature_names,
            'is_fitted': self.is_fitted
        }
        
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """
        Load a trained model from disk.
        
        Args:
            filepath (str): Path to the saved model
        """
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.algorithm = model_data['algorithm']
        self.params = model_data['params']
        self.feature_names = model_data.get('feature_names')
        self.is_fitted = model_data['is_fitted']
        
        logger.info(f"Model loaded from {filepath}")
    
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """
        Get feature importance if available for the algorithm.
        
        Returns:
            np.ndarray or None: Feature importance scores
        """
        if self.algorithm == 'isolation_forest' and self.is_fitted:
            # For Isolation Forest, we can compute feature importance
            # based on the path lengths in the trees
            try:
                return self.model.score_samples(np.eye(len(self.feature_names)))
            except:
                logger.warning("Feature importance not available for this model configuration")
                return None
        else:
            logger.warning(f"Feature importance not implemented for {self.algorithm}")
            return None


class AnomalyAlertSystem:
    """
    Handles anomaly alerts and threshold-based detection.
    """
    
    def __init__(self, threshold: float = -0.2):
        """
        Initialize the alert system.
        
        Args:
            threshold (float): Anomaly score threshold for alerts
        """
        self.threshold = threshold
        self.alert_history = []
    
    def generate_alerts(self, 
                       data: pd.DataFrame, 
                       anomaly_scores: np.ndarray, 
                       predictions: np.ndarray,
                       important_columns: Optional[list] = None) -> pd.DataFrame:
        """
        Generate alerts for anomalies below threshold.
        
        Args:
            data (pd.DataFrame): Original data
            anomaly_scores (np.ndarray): Anomaly scores
            predictions (np.ndarray): Anomaly predictions
            important_columns (list, optional): Important columns to include in alerts
            
        Returns:
            pd.DataFrame: Alert DataFrame
        """
        # Combine data with scores and predictions
        alert_data = data.copy()
        alert_data['anomaly_score'] = anomaly_scores
        alert_data['prediction'] = predictions
        
        # Filter for high-confidence anomalies
        alerts = alert_data[
            (alert_data['anomaly_score'] < self.threshold) & 
            (alert_data['prediction'] == -1)
        ]
        
        if len(alerts) > 0:
            logger.warning(f"🚨 ALERT: {len(alerts)} high-confidence anomalies detected!")
            
            # Select important columns for the alert
            if important_columns:
                alert_columns = important_columns + ['anomaly_score', 'prediction']
                alert_info = alerts[alert_columns]
            else:
                alert_info = alerts
            
            # Store in alert history
            self.alert_history.append({
                'timestamp': pd.Timestamp.now(),
                'alert_count': len(alerts),
                'threshold': self.threshold,
                'alerts': alert_info
            })
            
            return alert_info
        else:
            logger.info("✅ No high-confidence anomalies detected.")
            return pd.DataFrame()
    
    def save_alerts(self, alerts: pd.DataFrame, filepath: str):
        """
        Save alerts to CSV file.
        
        Args:
            alerts (pd.DataFrame): Alert data
            filepath (str): Output file path
        """
        if not alerts.empty:
            alerts.to_csv(filepath, index=False)
            logger.info(f"Alerts saved to {filepath}")
        else:
            logger.info("No alerts to save")


def main():
    """
    Example usage of the NetworkAnomalyDetector class.
    """
    # Example with synthetic data
    np.random.seed(42)
    X_normal = np.random.normal(0, 1, (1000, 10))
    X_anomaly = np.random.normal(3, 1, (100, 10))
    X = np.vstack([X_normal, X_anomaly])
    
    # Initialize detector
    detector = NetworkAnomalyDetector(algorithm='isolation_forest')
    
    # Fit and predict
    detector.fit(X)
    predictions = detector.predict(X)
    scores = detector.decision_function(X)
    
    # Generate report
    report = detector.get_anomaly_report(X)
    print("Anomaly Detection Report:")
    print(f"Algorithm: {report['algorithm']}")
    print(f"Total samples: {report['total_samples']}")
    print(f"Anomalies detected: {report['anomaly_count']} ({report['anomaly_percentage']}%)")


if __name__ == "__main__":
    main()
