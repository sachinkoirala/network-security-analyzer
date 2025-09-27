"""
Data Processing Module for NetFlow Anomaly Detection

This module handles data loading, preprocessing, and feature engineering
for network flow anomaly detection.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkDataProcessor:
    """
    Handles preprocessing of network flow data for anomaly detection.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca_2d = None
        self.pca_3d = None
        self.feature_columns = None
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load network flow data from CSV file.
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            logger.info(f"Loading data from {file_path}")
            data = pd.read_csv(file_path)
            logger.info(f"Data loaded successfully. Shape: {data.shape}")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def preprocess_data(self, data: pd.DataFrame, target_column: str = 'Label') -> pd.DataFrame:
        """
        Preprocess the network flow data.
        
        Args:
            data (pd.DataFrame): Raw data
            target_column (str): Name of the target/label column to drop
            
        Returns:
            pd.DataFrame: Preprocessed data
        """
        logger.info("Starting data preprocessing...")
        
        # Create a copy to avoid modifying original data
        processed_data = data.copy()
        
        # Check for missing values
        null_columns = processed_data.columns[processed_data.isnull().any()]
        if len(null_columns) > 0:
            logger.info(f"Found null values in columns: {list(null_columns)}")
            processed_data = processed_data.dropna()
            logger.info("Dropped rows with null values")
        
        # Clean column names (remove extra spaces)
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
        
        # Store feature columns for later use
        self.feature_columns = processed_data.columns.tolist()
        
        logger.info(f"Preprocessing completed. Final shape: {processed_data.shape}")
        return processed_data
    
    def scale_features(self, data: pd.DataFrame, fit: bool = True) -> np.ndarray:
        """
        Scale features using StandardScaler.
        
        Args:
            data (pd.DataFrame): Data to scale
            fit (bool): Whether to fit the scaler or use existing fit
            
        Returns:
            np.ndarray: Scaled data
        """
        logger.info("Scaling features...")
        
        if fit:
            scaled_data = self.scaler.fit_transform(data)
            logger.info("Scaler fitted and data transformed")
        else:
            scaled_data = self.scaler.transform(data)
            logger.info("Data transformed using existing scaler")
        
        return scaled_data
    
    def apply_pca(self, scaled_data: np.ndarray, n_components: int = 2) -> tuple:
        """
        Apply PCA for dimensionality reduction.
        
        Args:
            scaled_data (np.ndarray): Scaled input data
            n_components (int): Number of principal components
            
        Returns:
            tuple: (pca_result, pca_object)
        """
        logger.info(f"Applying PCA with {n_components} components...")
        
        pca = PCA(n_components=n_components)
        pca_result = pca.fit_transform(scaled_data)
        
        # Store PCA object for later use
        if n_components == 2:
            self.pca_2d = pca
        elif n_components == 3:
            self.pca_3d = pca
        
        explained_variance = pca.explained_variance_ratio_
        logger.info(f"PCA completed. Explained variance ratio: {explained_variance}")
        
        return pca_result, pca
    
    def create_pca_dataframe(self, pca_result: np.ndarray, n_components: int) -> pd.DataFrame:
        """
        Create a DataFrame from PCA results.
        
        Args:
            pca_result (np.ndarray): PCA transformation result
            n_components (int): Number of components
            
        Returns:
            pd.DataFrame: PCA DataFrame with appropriate column names
        """
        if n_components == 2:
            columns = ['PC1', 'PC2']
        elif n_components == 3:
            columns = ['PC1', 'PC2', 'PC3']
        else:
            columns = [f'PC{i+1}' for i in range(n_components)]
        
        pca_df = pd.DataFrame(pca_result, columns=columns)
        return pca_df
    
    def get_feature_importance(self, n_components: int = 2) -> pd.DataFrame:
        """
        Get feature importance from PCA components.
        
        Args:
            n_components (int): Number of components to analyze
            
        Returns:
            pd.DataFrame: Feature importance DataFrame
        """
        pca_obj = self.pca_2d if n_components == 2 else self.pca_3d
        
        if pca_obj is None:
            raise ValueError("PCA must be fitted first")
        
        # Create feature importance DataFrame
        feature_importance = pd.DataFrame(
            pca_obj.components_.T,
            columns=[f'PC{i+1}' for i in range(n_components)],
            index=self.feature_columns
        )
        
        return feature_importance


def main():
    """
    Example usage of the NetworkDataProcessor class.
    """
    # Initialize processor
    processor = NetworkDataProcessor()
    
    # Load and preprocess data
    data = processor.load_data('Detection.csv')
    processed_data = processor.preprocess_data(data)
    
    # Scale features
    scaled_data = processor.scale_features(processed_data)
    
    # Apply PCA
    pca_2d_result, _ = processor.apply_pca(scaled_data, n_components=2)
    pca_3d_result, _ = processor.apply_pca(scaled_data, n_components=3)
    
    # Create DataFrames
    pca_2d_df = processor.create_pca_dataframe(pca_2d_result, 2)
    pca_3d_df = processor.create_pca_dataframe(pca_3d_result, 3)
    
    print("Data processing completed successfully!")
    print(f"2D PCA shape: {pca_2d_df.shape}")
    print(f"3D PCA shape: {pca_3d_df.shape}")


if __name__ == "__main__":
    main()
