'use client';

import { useState, useEffect } from 'react';
import { useAnalysis } from '@/contexts/AnalysisContext';
import { AnalysisControls, AnalysisResults } from './Analysis';
import { NetworkMonitor } from './NetworkMonitor';
import { VisualizationTabs } from './VisualizationTabs';
import { ErrorBoundary } from './ErrorBoundary';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export const NetworkSecurityDashboard = () => {
  const { analysisStatus, analysisResults, networkInfo, error, getNetworkInfo } = useAnalysis();
  const [activeTab, setActiveTab] = useState('analysis');

  useEffect(() => {
    // Load network info on component mount
    getNetworkInfo();
  }, [getNetworkInfo]);

  return (
    <div className="space-y-6">
      {/* Error Display */}
      {error && (
        <Alert variant="destructive" className="border-red-200 bg-red-50">
          <AlertDescription className="text-red-800">{error}</AlertDescription>
        </Alert>
      )}

      {/* Main Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 bg-white shadow-lg rounded-lg p-1">
          <TabsTrigger
            value="analysis"
            className="data-[state=active]:bg-blue-600 data-[state=active]:text-white font-semibold text-gray-700"
          >
            🔍 Analysis
          </TabsTrigger>
          <TabsTrigger
            value="monitor"
            className="data-[state=active]:bg-green-600 data-[state=active]:text-white font-semibold text-gray-700"
          >
            📊 Network Monitor
          </TabsTrigger>
          <TabsTrigger
            value="visualizations"
            className="data-[state=active]:bg-purple-600 data-[state=active]:text-white font-semibold text-gray-700"
          >
            📈 Visualizations
          </TabsTrigger>
        </TabsList>

        <TabsContent value="analysis" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ErrorBoundary>
              <AnalysisControls />
            </ErrorBoundary>
            <ErrorBoundary>
              <AnalysisResults />
            </ErrorBoundary>
          </div>
        </TabsContent>

        <TabsContent value="monitor" className="space-y-6">
          <ErrorBoundary>
            <NetworkMonitor networkInfo={networkInfo} />
          </ErrorBoundary>
        </TabsContent>

        <TabsContent value="visualizations" className="space-y-6">
          <ErrorBoundary>
            {analysisResults ? (
              <VisualizationTabs results={analysisResults} />
            ) : (
              <div className="text-center py-12">
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No Analysis Results
                </h3>
                <p className="text-gray-500">
                  Run an analysis first to see visualizations
                </p>
              </div>
            )}
          </ErrorBoundary>
        </TabsContent>
      </Tabs>
    </div>
  );
};
