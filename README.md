# Network Security Analyzer

A comprehensive machine learning system for detecting anomalous network traffic patterns and potential cybersecurity threats in real-time.

## 🚀 Features

- **Real-time Anomaly Detection**: Identifies suspicious network connections using advanced ML algorithms
- **Multiple Detection Algorithms**: Isolation Forest, One-Class SVM, and Local Outlier Factor
- **Interactive Visualizations**: 2D and 3D plots with interactive exploration capabilities
- **Automated Alerting**: High-confidence anomaly alerts with detailed reporting
- **Batch Processing**: Analyze multiple datasets and compare different algorithms
- **Production Ready**: Modular design with comprehensive logging and error handling

## 📁 Project Structure

```
network-security-analyzer/
├── src/                          # Core modules
│   ├── __init__.py              # Package initialization
│   ├── data_processor.py        # Data loading and preprocessing
│   ├── anomaly_detector.py      # ML algorithms for anomaly detection
│   └── visualizer.py            # Visualization functions
├── scripts/                      # Executable scripts
│   ├── run_2d_analysis.py       # 2D anomaly detection
│   ├── run_3d_analysis.py       # 3D anomaly detection
│   └── batch_processor.py       # Batch processing and comparisons
├── data/                         # Sample datasets
│   └── sample_network_data.csv  # Sample network flow dataset
├── docs/                         # Documentation
│   └── usage_guide.md           # Detailed usage guide
├── requirements.txt              # Python dependencies
├── setup.py                      # Package installation
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd network-security-analyzer
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

### Basic 2D Analysis
```bash
python scripts/run_2d_analysis.py --data data/sample_network_data.csv --output results --save-plots
```

### 3D Analysis with Interactive Plots
```bash
python scripts/run_3d_analysis.py --data data/sample_network_data.csv --output results --interactive --save-plots
```

### Compare Multiple Algorithms
```bash
python scripts/batch_processor.py --mode comparative --data data/sample_network_data.csv --output results
```

## 📊 Understanding the Output

### Generated Files
- **Model Files**: `.joblib` files containing trained models
- **Results CSV**: PCA coordinates with anomaly scores and predictions
- **Alert Files**: High-confidence anomalies meeting threshold criteria
- **Reports**: Detailed text reports with statistics and analysis
- **Plots**: PNG files and HTML interactive visualizations

### Key Metrics
- **Anomaly Percentage**: Percentage of flows classified as anomalous
- **Anomaly Scores**: Lower scores indicate higher anomaly confidence
- **PCA Explained Variance**: How much information is retained in reduced dimensions

## 🔧 Configuration Options

### Command Line Arguments

#### run_2d_analysis.py / run_3d_analysis.py
- `--data, -d`: Path to CSV data file
- `--output, -o`: Output directory for results
- `--contamination, -c`: Expected contamination rate (0.1 = 10%)
- `--threshold, -t`: Anomaly score threshold for alerts
- `--save-plots, -p`: Save plots to files
- `--show-plots, -s`: Display plots interactively
- `--interactive, -i`: Create interactive 3D plots (3D only)

#### batch_processor.py
- `--mode, -m`: Analysis mode (comparative, sensitivity, batch)
- `--data, -d`: Data file or directory
- `--files, -f`: List of files to process
- `--output, -o`: Output directory

## 🎯 Use Cases

### Cybersecurity Teams
- **Threat Detection**: Identify potential attacks and suspicious activities
- **Network Monitoring**: Continuous monitoring of network traffic patterns
- **Incident Response**: Quick identification of security incidents

### IT Administrators
- **Network Health**: Monitor overall network performance and usage
- **Capacity Planning**: Understand traffic patterns for infrastructure planning
- **Compliance**: Ensure network security meets regulatory requirements

### Security Researchers
- **Algorithm Comparison**: Test different ML approaches on network data
- **Parameter Tuning**: Optimize detection algorithms for specific environments
- **Research Analysis**: Study network behavior patterns and anomalies

## 🔍 How It Works

1. **Data Ingestion**: Loads network flow data from CSV files
2. **Preprocessing**: Cleans and normalizes the data for analysis
3. **Feature Engineering**: Applies PCA for dimensionality reduction
4. **Model Training**: Trains ML algorithms to learn normal traffic patterns
5. **Anomaly Detection**: Identifies deviations from normal behavior
6. **Visualization**: Creates interactive plots and reports
7. **Alerting**: Generates alerts for high-confidence anomalies

## 📈 Performance

### Dataset Size Recommendations
- **Small (< 10K records)**: All algorithms work well
- **Medium (10K - 100K records)**: Use Isolation Forest or One-Class SVM
- **Large (> 100K records)**: Consider sampling or streaming approaches

### Hardware Requirements
- **RAM**: 4GB+ for datasets under 100K records
- **CPU**: Multi-core recommended for faster training
- **Storage**: Sufficient space for models and output files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions and support:
- Create an issue on GitHub
- Check the documentation in the `docs/` directory
- Review the example scripts for usage patterns

## 🔮 Roadmap

- [ ] Real-time streaming processing
- [ ] Web dashboard interface
- [ ] REST API endpoints
- [ ] Docker containerization
- [ ] Advanced deep learning models
- [ ] Integration with SIEM systems
