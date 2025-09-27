# 🛡️ Network Security Analyzer

A comprehensive network security analysis platform that combines machine learning-powered anomaly detection with an intuitive web dashboard. Detect suspicious network activities, visualize traffic patterns, and monitor network health in real-time.

## ✨ Features

- **🔍 Advanced Anomaly Detection**: Uses Isolation Forest algorithm to identify suspicious network activities
- **📊 Interactive Visualizations**: 2D and 3D PCA plots with real-time data exploration
- **🌐 Real-time Network Monitoring**: Live network interface and connection monitoring
- **📈 Threat Analysis**: Comprehensive threat scoring and alert system
- **🎨 Modern Web Dashboard**: Built with Next.js and TypeScript for optimal user experience
- **⚡ High Performance**: Handles large datasets (200K+ records) efficiently
- **🔧 Easy Setup**: One-command installation and deployment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │   Flask API     │    │   Python ML     │
│   Dashboard     │◄──►│   (Port 5000)   │◄──►│   Engine        │
│   (Port 3000)   │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

- **Frontend**: Next.js 15 with TypeScript, Tailwind CSS, and Plotly.js
- **Backend**: Flask API with CORS support
- **ML Engine**: Python with scikit-learn, pandas, and numpy
- **Visualization**: Interactive 2D/3D plots with Plotly.js

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 18+** with npm
- **Git** for cloning the repository

**Windows Users:**
- **PowerShell 5.1+** or **Command Prompt**
- **Windows 10/11** (recommended)
- **Administrator privileges** (for network monitoring)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sachinkoirala/network-security-analyzer.git
   cd network-security-analyzer
   ```

2. **Run the setup script**

   **Linux/macOS:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   **Windows:**
   Follow the manual setup instructions below.

3. **Start the application**

   **Linux/macOS:**
   ```bash
   ./start.sh
   ```

   **Windows:**
   Follow the manual start instructions below.

4. **Open your browser**
   Navigate to `http://localhost:3000`

## 📖 Detailed Setup

### Windows Setup (Manual)

**Step 1: Open Command Prompt as Administrator**
- Press `Win + R`, type `cmd`, press `Ctrl + Shift + Enter`
- Or search "Command Prompt" → Right-click → "Run as administrator"

**Note:** You can also use PowerShell if you prefer. The commands are the same.

**Step 2: Navigate to project directory**
```cmd
cd C:\path\to\your\project\network-security-analyzer
```

**Step 3: Create Python virtual environment**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Step 4: Install Python dependencies**
```cmd
pip install -r requirements.txt
pip install -r api\requirements.txt
```

**Step 5: Install Node.js dependencies**
```cmd
cd dashboard
npm install
cd ..
```

**Step 6: Start the application**
```cmd
REM Option 1: Start both services
python main.py --both

REM Option 2: Start separately (in different Command Prompt windows)
REM Window 1:
python main.py --api
REM Window 2:
python main.py --dashboard
```

### Manual Installation (Linux/macOS)

#### 1. Python Environment Setup

**Linux/macOS:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install -r api/requirements.txt
```

**Windows:**
```cmd
REM Create virtual environment
python -m venv venv
venv\Scripts\activate

REM Install Python dependencies
pip install -r requirements.txt
pip install -r api\requirements.txt
```

#### 2. Node.js Setup

**Linux/macOS:**
```bash
# Install Node.js dependencies
cd dashboard
npm install
cd ..
```

**Windows:**
```cmd
REM Install Node.js dependencies
cd dashboard
npm install
cd ..
```

#### 3. Start Services

**Option A: Start both services**

**Linux/macOS:**
```bash
python main.py --both
```

**Windows:**
```cmd
python main.py --both
```

**Option B: Start services separately**

**Linux/macOS:**
```bash
# Terminal 1: Start Flask API
python main.py --api

# Terminal 2: Start Dashboard
python main.py --dashboard
```

**Windows:**
```cmd
REM Command Prompt 1: Start Flask API
python main.py --api

REM Command Prompt 2: Start Dashboard
python main.py --dashboard
```

## 🎯 Usage

### 1. Running Analysis

1. **Open the dashboard** at `http://localhost:3000`
2. **Click "🚀 Start Analysis"** to begin network security analysis
3. **View results** in the Visualizations tab:
   - **Status**: Overall security assessment
   - **2D View**: Interactive 2D PCA visualization
   - **3D View**: Interactive 3D PCA visualization  
   - **Threats**: Anomaly score distribution
   - **Critical**: High-confidence anomaly alerts

### 2. Understanding Results

#### Status Tab
- **Overall Security Assessment**: Safe, Caution, Warning, or Critical
- **Key Metrics**: Total connections, suspicious activities, anomaly rate
- **Recommendations**: Actionable security advice

#### 2D/3D Visualizations
- **Blue dots**: Normal network connections (safe)
- **Red triangles/diamonds**: Suspicious activities detected
- **Clusters**: Similar traffic patterns grouped together
- **Outliers**: Unusual connections that stand out

#### Threat Analysis
- **Anomaly Scores**: Lower scores indicate higher threat levels
- **Threshold Line**: Red dashed line shows alert threshold
- **Statistics**: Mean, standard deviation, and distribution metrics

#### Critical Anomalies
- **High-confidence alerts**: Anomalies requiring immediate attention
- **Detailed information**: Port numbers, flow duration, packet counts
- **Severity levels**: Critical, High, Medium based on anomaly scores

### 3. Network Monitoring

The **Network Monitor** tab provides real-time information about:
- **Active Network Interfaces**: IP addresses and network masks
- **Current Connections**: Established network connections
- **Security Status**: Overall network health assessment

## 🔧 Configuration

### Analysis Parameters

- **Contamination Rate**: Expected percentage of anomalies (default: 0.1 = 10%)
- **Alert Threshold**: Score threshold for critical alerts (default: -0.2)

### Data Sources

The system uses sample network data by default (`data/sample_network_data.csv`). To use your own data:

1. **Prepare your CSV file** with network flow features
2. **Update the data path** in the analysis request
3. **Ensure proper column names** for optimal results

### API Endpoints

- `GET /api/health` - Health check
- `POST /api/analyze` - Run network analysis
- `GET /api/analysis/status` - Get analysis status
- `GET /api/analysis/results` - Get analysis results
- `GET /api/network/info` - Get network information

## 📁 Project Structure

```
network-security-analyzer/
├── api/                    # Flask API server
│   ├── app.py             # Main API application
│   └── requirements.txt   # Python API dependencies
├── dashboard/             # Next.js frontend
│   ├── src/
│   │   ├── app/          # Next.js app directory
│   │   ├── components/   # React components
│   │   ├── contexts/     # React contexts
│   │   └── lib/          # Utility libraries
│   └── package.json      # Node.js dependencies
├── src/                   # Python ML modules
│   └── network_analyzer.py # Consolidated ML engine
├── data/                  # Sample data
│   └── sample_network_data.csv
├── main.py               # Application entry point
├── setup.sh             # Setup script
├── start.sh             # Start script
└── requirements.txt     # Python dependencies
```

## 🛠️ Development

### Running in Development Mode

```bash
# Start Flask API in development mode
cd api
python app.py

# Start Next.js dashboard in development mode
cd dashboard
npm run dev
```

### Building for Production

```bash
# Build Next.js dashboard
cd dashboard
npm run build

# Start production server
npm start
```

## 🧪 Testing

### Test the API

```bash
# Health check
curl http://localhost:5000/api/health

# Run analysis
curl -X POST -H "Content-Type: application/json" \
  -d '{"data_path": "data/sample_network_data.csv", "contamination": 0.1, "threshold": -0.2}' \
  http://localhost:5000/api/analyze
```

### Test the Dashboard

1. Open `http://localhost:3000`
2. Click "🚀 Start Analysis"
3. Verify all visualizations load correctly
4. Check that network monitoring works

## 🔍 Troubleshooting

### Common Issues

**1. "Flask API is not running" error**
- Solution: Start the Flask API manually with `python main.py --api`

**2. "Maximum call stack size exceeded" error**
- Solution: This has been fixed in the latest version. Update your code.

**3. "Module not found" errors**
- Solution: Ensure virtual environment is activated and dependencies are installed

**4. Port conflicts**
- Solution: Check if ports 3000 or 5000 are already in use and kill those processes

**5. Windows-specific issues**
- **"python is not recognized"**: Add Python to PATH or use `py` instead of `python`
- **"node is not recognized"**: Add Node.js to PATH or reinstall Node.js
- **Permission denied**: Run Command Prompt as Administrator
- **Virtual environment issues**: Use `python -m venv venv` instead of `python3 -m venv venv`

### Debug Mode

Enable debug logging by setting environment variables:

**Linux/macOS:**
```bash
export FLASK_DEBUG=1
export NEXT_DEBUG=1
```

**Windows:**
```cmd
set FLASK_DEBUG=1
set NEXT_DEBUG=1
```

## 📊 Performance

- **Dataset Size**: Tested with 225,000+ network flow records
- **Analysis Time**: ~30-60 seconds for large datasets
- **Memory Usage**: ~500MB for typical analysis
- **Response Time**: <2 seconds for API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **scikit-learn** for machine learning algorithms
- **Plotly.js** for interactive visualizations
- **Next.js** for the modern web framework
- **Flask** for the lightweight API server
- **Tailwind CSS** for beautiful styling

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/sachinkoirala/network-security-analyzer/issues)
3. Create a new issue with detailed information

---

**Made with ❤️ for All**