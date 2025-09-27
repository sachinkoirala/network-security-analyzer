'use client';

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { PCAPlot2D, PCAPlot3D, AnomalyScoresPlot } from './Visualizations';
import { CriticalAnomaliesTable } from './CriticalAnomaliesTable';
import { SecurityStatusSummary } from './SecurityStatusSummary';
import { AnalysisResults } from '@/contexts/AnalysisContext';

interface VisualizationTabsProps {
  results: AnalysisResults;
}

export const VisualizationTabs = ({ results }: VisualizationTabsProps) => {
  return (
    <Tabs defaultValue="status" className="w-full">
      <TabsList className="grid w-full grid-cols-5 bg-white shadow-lg rounded-lg p-1">
        <TabsTrigger value="status" className="data-[state=active]:bg-purple-600 data-[state=active]:text-white text-gray-700 font-semibold">🛡️ Status</TabsTrigger>
        <TabsTrigger value="2d" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white text-gray-700 font-semibold">📊 2D View</TabsTrigger>
        <TabsTrigger value="3d" className="data-[state=active]:bg-green-600 data-[state=active]:text-white text-gray-700 font-semibold">🌐 3D View</TabsTrigger>
        <TabsTrigger value="scores" className="data-[state=active]:bg-orange-600 data-[state=active]:text-white text-gray-700 font-semibold">📈 Threats</TabsTrigger>
        <TabsTrigger value="critical" className="data-[state=active]:bg-red-600 data-[state=active]:text-white text-gray-700 font-semibold">🚨 Critical</TabsTrigger>
      </TabsList>

      <TabsContent value="status" className="mt-6">
        <SecurityStatusSummary analysisResults={results} />
      </TabsContent>

      <TabsContent value="2d" className="mt-6">
        <PCAPlot2D 
          data={results.pca_2d.data}
          predictions={results.predictions}
          explainedVariance={results.pca_2d.explained_variance}
        />
      </TabsContent>

      <TabsContent value="3d" className="mt-6">
        <PCAPlot3D 
          data={results.pca_3d.data}
          predictions={results.predictions}
          explainedVariance={results.pca_3d.explained_variance}
        />
      </TabsContent>

      <TabsContent value="scores" className="mt-6">
        <AnomalyScoresPlot 
          scores={results.anomaly_scores}
          threshold={-0.2}
        />
      </TabsContent>

      <TabsContent value="critical" className="mt-6">
        <CriticalAnomaliesTable anomalies={results.alerts} />
      </TabsContent>
    </Tabs>
  );
};
