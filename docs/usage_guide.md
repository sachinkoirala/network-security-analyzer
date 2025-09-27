# Network Security Analyzer - Usage Guide

## Quick Start

### 1. Setup Environment
```bash
cd network-security-analyzer
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Analysis
```bash
# 2D Analysis
python scripts/run_2d_analysis.py --data data/sample_network_data.csv --output results --save-plots

# 3D Analysis with Interactive Plots
python scripts/run_3d_analysis.py --data data/sample_network_data.csv --output results --interactive --save-plots
```

## Understanding the Results

### Generated Files
- `security_model_*.joblib` - Trained ML models
- `pca_results_*.csv` - PCA coordinates with predictions
- `security_alerts_*.csv` - High-confidence security alerts
- `security_analysis_report_*.txt` - Detailed analysis reports
- `*.png` - Static visualization plots
- `interactive_security_analysis.html` - Interactive 3D plot

### Key Metrics
- **Anomaly Percentage**: % of traffic classified as suspicious
- **Anomaly Scores**: Lower scores = more suspicious
- **PCA Explained Variance**: Information retained in visualizations

## Customization

### Adjust Detection Sensitivity
```bash
# More sensitive (detects more anomalies)
python scripts/run_2d_analysis.py --contamination 0.2 --threshold -0.1

# Less sensitive (fewer, high-confidence alerts)
python scripts/run_2d_analysis.py --contamination 0.05 --threshold -0.5
```

### Use Your Own Data
1. Place your CSV file in the `data/` directory
2. Ensure it has network flow features (ports, durations, packet counts, etc.)
3. Run analysis: `python scripts/run_2d_analysis.py --data data/your_data.csv`

## Advanced Usage

### Batch Processing
```bash
# Compare multiple algorithms
python scripts/batch_processor.py --mode comparative --data data/sample_network_data.csv

# Test parameter sensitivity
python scripts/batch_processor.py --mode sensitivity --data data/sample_network_data.csv
```

### Programmatic Usage
```python
from src.data_processor import NetworkDataProcessor
from src.anomaly_detector import NetworkAnomalyDetector
from src.visualizer import NetworkFlowVisualizer

# Initialize components
processor = NetworkDataProcessor()
detector = NetworkAnomalyDetector(algorithm='isolation_forest')
visualizer = NetworkFlowVisualizer()

# Process data
data = processor.load_data('data/sample_network_data.csv')
processed_data = processor.preprocess_data(data)
scaled_data = processor.scale_features(processed_data)

# Detect anomalies
detector.fit(scaled_data)
predictions = detector.predict(scaled_data)
scores = detector.decision_function(scaled_data)

# Create visualizations
pca_2d, _ = processor.apply_pca(scaled_data, n_components=2)
pca_df = processor.create_pca_dataframe(pca_2d, 2)
visualizer.plot_pca_2d(pca_df, predictions)
```

## Troubleshooting

### Common Issues
1. **Memory Issues**: Use smaller datasets or reduce PCA components
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **File Path Issues**: Use absolute paths or ensure correct working directory
4. **Visualization Issues**: Use `--save-plots` instead of `--show-plots` on servers

### Performance Tips
- For large datasets (>100K records), consider sampling
- Use 2D analysis for faster processing
- Adjust contamination rate based on expected anomaly percentage
- Save models for reuse with new data

## Support
- Check the README.md for complete documentation
- Review the source code in `src/` directory
- Create issues on GitHub for bugs or feature requests
