'use client';

import React, { createContext, useContext, useState, useCallback } from 'react';

export interface AnalysisResults {
  report: {
    algorithm: string;
    total_samples: number;
    normal_count: number;
    anomaly_count: number;
    anomaly_percentage: number;
    score_statistics: {
      min_score: number;
      max_score: number;
      mean_score: number;
      std_score: number;
    };
  };
  pca_2d: {
    data: Array<{ PC1: number; PC2: number }>;
    explained_variance: number[];
  };
  pca_3d: {
    data: Array<{ PC1: number; PC2: number; PC3: number }>;
    explained_variance: number[];
  };
  predictions: number[];
  anomaly_scores: number[];
  alerts: Array<Record<string, any>>;
  feature_importance: Record<string, { PC1: number; PC2: number }>;
  timestamp: string;
}

export interface NetworkInfo {
  interfaces: Array<{
    name: string;
    ip: string;
    netmask: string;
  }>;
  connections: Array<{
    local_address: string;
    remote_address: string;
    status: string;
    pid: number | null;
  }>;
  timestamp: string;
}

interface AnalysisContextType {
  analysisStatus: 'idle' | 'running' | 'completed' | 'error';
  analysisResults: AnalysisResults | null;
  networkInfo: NetworkInfo | null;
  error: string | null;
  runAnalysis: (dataPath?: string, contamination?: number, threshold?: number) => Promise<void>;
  getNetworkInfo: () => Promise<void>;
  clearResults: () => void;
}

const AnalysisContext = createContext<AnalysisContextType | undefined>(undefined);

export const useAnalysis = () => {
  const context = useContext(AnalysisContext);
  if (context === undefined) {
    throw new Error('useAnalysis must be used within an AnalysisProvider');
  }
  return context;
};

export const AnalysisProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [analysisStatus, setAnalysisStatus] = useState<'idle' | 'running' | 'completed' | 'error'>('idle');
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
  const [networkInfo, setNetworkInfo] = useState<NetworkInfo | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runAnalysis = useCallback(async (
    dataPath: string = 'data/sample_network_data.csv',
    contamination: number = 0.1,
    threshold: number = -0.2
  ) => {
    setAnalysisStatus('running');
    setError(null);

    try {
      // Check if Flask API is running
      let apiRunning = false;
      try {
        const healthResponse = await fetch('http://localhost:5000/api/health', {
          method: 'GET',
          signal: AbortSignal.timeout(2000)
        });
        if (healthResponse.ok) {
          apiRunning = true;
        }
      } catch (apiError) {
        apiRunning = false;
      }

      if (!apiRunning) {
        setError('🚀 Flask API is not running. Please start it manually by running: python api/app.py');
        setAnalysisStatus('error');
        return;
      }

      // Run the analysis
      setError('🔄 Running analysis... This may take a moment.');
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          data_path: dataPath,
          contamination,
          threshold,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setAnalysisResults(data.results);
        setAnalysisStatus('completed');
        setError(null);
      } else {
        setError(data.error || 'Analysis failed');
        setAnalysisStatus('error');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Network error');
      setAnalysisStatus('error');
    }
  }, []);

  const getNetworkInfo = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:5000/api/network/info');
      const data = await response.json();

      if (response.ok) {
        // Ensure the data has the expected structure
        const networkData = {
          interfaces: Array.isArray(data.interfaces) ? data.interfaces : [],
          connections: Array.isArray(data.connections) ? data.connections : [],
          timestamp: data.timestamp || new Date().toISOString()
        };
        setNetworkInfo(networkData);
      } else {
        setError(data.error || 'Failed to get network info');
        // Set empty network info to prevent crashes
        setNetworkInfo({
          interfaces: [],
          connections: [],
          timestamp: new Date().toISOString()
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Network error');
      // Set empty network info to prevent crashes
      setNetworkInfo({
        interfaces: [],
        connections: [],
        timestamp: new Date().toISOString()
      });
    }
  }, []);

  const clearResults = useCallback(() => {
    setAnalysisResults(null);
    setAnalysisStatus('idle');
    setError(null);
  }, []);

  const value: AnalysisContextType = {
    analysisStatus,
    analysisResults,
    networkInfo,
    error,
    runAnalysis,
    getNetworkInfo,
    clearResults,
  };

  return (
    <AnalysisContext.Provider value={value}>
      {children}
    </AnalysisContext.Provider>
  );
};
