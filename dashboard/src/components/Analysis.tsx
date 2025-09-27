'use client';

import { useAnalysis } from '@/contexts/AnalysisContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Loader2, Play, RefreshCw, Shield, AlertTriangle, CheckCircle, BarChart3 } from 'lucide-react';

// Analysis Controls Component
export const AnalysisControls = () => {
  const { analysisStatus, runAnalysis, clearResults } = useAnalysis();

  const handleRunAnalysis = async () => {
    await runAnalysis();
  };

  const handleClearResults = () => {
    clearResults();
  };

  const isRunning = analysisStatus === 'running';

  return (
    <Card className="bg-gradient-to-br from-white to-blue-50 border-blue-200 shadow-lg">
      <CardHeader className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-t-lg">
        <CardTitle className="flex items-center gap-2 text-xl">
          <div className="p-2 bg-white/20 rounded-lg">
            <Play className="h-6 w-6" />
          </div>
          Network Security Analysis
        </CardTitle>
        <CardDescription className="text-blue-100 text-lg">
          🚀 Run comprehensive network security analysis
        </CardDescription>
      </CardHeader>
      <CardContent className="p-6">
        <div className="text-center space-y-6">
          <div className="text-gray-600">
            <p className="text-lg mb-2">Ready to analyze your network security?</p>
            <p className="text-sm">This will capture and analyze your live network traffic for 30 seconds to detect potential threats using advanced machine learning.</p>
          </div>

          <div className="flex gap-4 justify-center">
            <Button
              onClick={handleRunAnalysis}
              disabled={isRunning}
              className="bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white font-bold py-3 px-8 rounded-lg shadow-lg transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isRunning ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  🔄 Analyzing...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-5 w-5" />
                  🚀 Start Analysis
                </>
              )}
            </Button>

            <Button
              onClick={handleClearResults}
              variant="outline"
              disabled={isRunning}
              className="border-2 border-gray-300 hover:border-gray-400 text-gray-700 font-semibold py-3 px-6 rounded-lg shadow-lg transform hover:scale-105 transition-all duration-200"
            >
              <RefreshCw className="mr-2 h-5 w-5" />
              Clear
            </Button>
          </div>

          <div className="bg-gradient-to-r from-gray-100 to-gray-200 p-4 rounded-lg">
            <div className="flex items-center justify-center gap-2">
              <div className={`w-3 h-3 rounded-full ${
                analysisStatus === 'running' ? 'bg-yellow-500 animate-pulse' :
                analysisStatus === 'completed' ? 'bg-green-500' :
                analysisStatus === 'error' ? 'bg-red-500' : 'bg-gray-400'
              }`}></div>
              <span className="font-semibold text-gray-700">Status:</span>
              <span className={`font-bold ${
                analysisStatus === 'running' ? 'text-yellow-600' :
                analysisStatus === 'completed' ? 'text-green-600' :
                analysisStatus === 'error' ? 'text-red-600' : 'text-gray-600'
              }`}>
                {analysisStatus === 'running' ? '🔄 Running...' :
                 analysisStatus === 'completed' ? '✅ Completed' :
                 analysisStatus === 'error' ? '❌ Error' : '⏸️ Ready'}
              </span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// Analysis Results Component
export const AnalysisResults = () => {
  const { analysisStatus, analysisResults } = useAnalysis();

  if (analysisStatus === 'idle') {
    return (
      <Card className="bg-gradient-to-br from-white to-purple-50 border-purple-200 shadow-lg">
        <CardHeader className="bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-t-lg">
          <CardTitle className="flex items-center gap-2 text-xl">
            <div className="p-2 bg-white/20 rounded-lg">
              <BarChart3 className="h-6 w-6" />
            </div>
            Analysis Results
          </CardTitle>
          <CardDescription className="text-purple-100 text-lg">
            📊 Results will appear here after running analysis
          </CardDescription>
        </CardHeader>
        <CardContent className="p-8">
          <div className="text-center">
            <div className="w-24 h-24 mx-auto mb-4 bg-gradient-to-r from-purple-100 to-pink-100 rounded-full flex items-center justify-center">
              <BarChart3 className="h-12 w-12 text-purple-500" />
            </div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">Ready to Analyze!</h3>
            <p className="text-gray-500 mb-4">Click "🚀 Run Analysis" to start detecting network anomalies</p>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm text-blue-700">
                💡 The analysis will show you 2D/3D visualizations, anomaly scores, and security alerts
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (analysisStatus === 'running') {
    return (
      <Card className="bg-gradient-to-br from-white to-yellow-50 border-yellow-200 shadow-lg">
        <CardHeader className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white rounded-t-lg">
          <CardTitle className="flex items-center gap-2 text-xl">
            <div className="p-2 bg-white/20 rounded-lg">
              <BarChart3 className="h-6 w-6" />
            </div>
            Analysis Results
          </CardTitle>
          <CardDescription className="text-yellow-100 text-lg">
            🔄 Analysis in progress...
          </CardDescription>
        </CardHeader>
        <CardContent className="p-8">
          <div className="text-center">
            <div className="w-24 h-24 mx-auto mb-4 bg-gradient-to-r from-yellow-100 to-orange-100 rounded-full flex items-center justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-yellow-500"></div>
            </div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">🔄 Capturing Network Traffic...</h3>
            <p className="text-gray-500 mb-4">Capturing live network data for 30 seconds, then analyzing for anomalies</p>
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <p className="text-sm text-yellow-700">
                ⏳ Please wait while we capture and analyze your live network traffic
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (analysisStatus === 'error' || !analysisResults) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Analysis Results
          </CardTitle>
          <CardDescription>
            Error occurred during analysis
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertTitle>Analysis Failed</AlertTitle>
            <AlertDescription>
              Please check the data file and try again.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const { report, alerts } = analysisResults;

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <BarChart3 className="h-5 w-5" />
            Analysis Summary
          </CardTitle>
          <CardDescription className="text-gray-600">
            Algorithm: {report.algorithm} | Completed: {new Date(report.timestamp || Date.now()).toLocaleString()}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">Total Samples</span>
                <Badge variant="outline" className="text-gray-800">{report.total_samples.toLocaleString()}</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">Normal Flows</span>
                <Badge variant="outline" className="text-green-600 bg-green-50">
                  {report.normal_count.toLocaleString()}
                </Badge>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">Anomalies</span>
                <Badge variant="outline" className="text-red-600 bg-red-50">
                  {report.anomaly_count.toLocaleString()}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">Anomaly Rate</span>
                <Badge variant="outline" className="text-orange-600 bg-orange-50">
                  {report.anomaly_percentage.toFixed(2)}%
                </Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <Shield className="h-5 w-5" />
            Score Statistics
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="space-y-1">
              <div className="flex justify-between">
                <span className="text-gray-700">Min Score:</span>
                <span className="font-mono text-gray-800">{report.score_statistics.min_score.toFixed(3)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-700">Max Score:</span>
                <span className="font-mono text-gray-800">{report.score_statistics.max_score.toFixed(3)}</span>
              </div>
            </div>
            <div className="space-y-1">
              <div className="flex justify-between">
                <span className="text-gray-700">Mean Score:</span>
                <span className="font-mono text-gray-800">{report.score_statistics.mean_score.toFixed(3)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-700">Std Dev:</span>
                <span className="font-mono text-gray-800">{report.score_statistics.std_score.toFixed(3)}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <AlertTriangle className="h-5 w-5" />
            Security Alerts
          </CardTitle>
          <CardDescription className="text-gray-600">
            High-confidence anomalies requiring attention
          </CardDescription>
        </CardHeader>
        <CardContent>
          {alerts.length > 0 ? (
            <div className="space-y-2">
              <Alert variant="destructive">
                <AlertTriangle className="h-4 w-4" />
                <AlertTitle>{alerts.length} High-Confidence Anomalies Detected</AlertTitle>
                <AlertDescription>
                  These anomalies scored below the threshold and require immediate attention.
                </AlertDescription>
              </Alert>
              <div className="text-sm text-gray-600">
                Check the Visualizations tab for detailed analysis.
              </div>
            </div>
          ) : (
            <Alert>
              <CheckCircle className="h-4 w-4" />
              <AlertTitle>No High-Confidence Alerts</AlertTitle>
              <AlertDescription>
                No anomalies scored below the alert threshold.
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
