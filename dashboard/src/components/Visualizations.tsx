'use client';

import { useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { createPlot, purgePlot } from '@/lib/plotly';

// 2D PCA Plot Component
interface PCAPlot2DProps {
  data: Array<{ PC1: number; PC2: number }>;
  predictions: number[];
  explainedVariance: number[];
}

export const PCAPlot2D = ({ data, predictions, explainedVariance }: PCAPlot2DProps) => {
  const plotRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const createPlotAsync = async () => {
      if (!plotRef.current || !data || !Array.isArray(data) || data.length === 0) return;

      const normalPoints = data.filter((_, index) => predictions[index] === 1);
      const anomalyPoints = data.filter((_, index) => predictions[index] === -1);

      const normalX = normalPoints.map(point => point.PC1);
      const normalY = normalPoints.map(point => point.PC2);
      const anomalyX = anomalyPoints.map(point => point.PC1);
      const anomalyY = anomalyPoints.map(point => point.PC2);

      const trace1 = {
        x: normalX,
        y: normalY,
        mode: 'markers',
        type: 'scatter',
        name: 'Normal',
        marker: { color: 'blue', size: 6, opacity: 0.6 }
      };

      const trace2 = {
        x: anomalyX,
        y: anomalyY,
        mode: 'markers',
        type: 'scatter',
        name: 'Anomaly',
        marker: { color: 'red', size: 8, opacity: 0.8, symbol: 'triangle-up' }
      };

      const layout = {
        title: {
          text: `2D PCA Analysis - Normal vs Anomalous Traffic<br><sub>PC1: ${(explainedVariance[0] * 100).toFixed(1)}% variance | PC2: ${(explainedVariance[1] * 100).toFixed(1)}% variance</sub>`,
          font: { size: 16 }
        },
        xaxis: { title: 'Principal Component 1', showgrid: true },
        yaxis: { title: 'Principal Component 2', showgrid: true },
        legend: { x: 0.02, y: 0.98 },
        margin: { t: 80, r: 20, b: 60, l: 60 },
        width: 800,
        height: 600
      };

      const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
      };

      await createPlot(plotRef.current, [trace1, trace2], layout, config);
    };

    createPlotAsync();
    return () => {
      if (plotRef.current) {
        purgePlot(plotRef.current);
      }
    };
  }, [data, predictions, explainedVariance]);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-gray-800">🕵️ Network Traffic Analysis</CardTitle>
        <CardDescription className="text-gray-600">
          This graph shows your network traffic patterns. Blue dots are normal connections, red triangles are suspicious activities that need attention.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex gap-6">
          <div className="flex-1">
            <div ref={plotRef} className="w-full" style={{ height: '500px' }} />
          </div>
          <div className="w-80 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-3">📊 What This Shows:</h4>
            <ul className="text-sm text-blue-700 space-y-2">
              <li>• <strong>Blue dots:</strong> Normal network connections (safe)</li>
              <li>• <strong>Red triangles:</strong> Suspicious activities detected</li>
              <li>• <strong>Clusters:</strong> Similar traffic patterns grouped together</li>
              <li>• <strong>Outliers:</strong> Unusual connections that stand out</li>
            </ul>
            <div className="mt-4 p-3 bg-white rounded border">
              <div className="text-xs text-blue-600 space-y-1">
                <p><strong>Normal connections:</strong> {data.filter((_, index) => predictions[index] === 1).length}</p>
                <p><strong>Suspicious:</strong> {data.filter((_, index) => predictions[index] === -1).length}</p>
                <p><strong>Total analyzed:</strong> {data.length}</p>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// 3D PCA Plot Component
interface PCAPlot3DProps {
  data: Array<{ PC1: number; PC2: number; PC3: number }>;
  predictions: number[];
  explainedVariance: number[];
}

export const PCAPlot3D = ({ data, predictions, explainedVariance }: PCAPlot3DProps) => {
  const plotRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const createPlotAsync = async () => {
      if (!plotRef.current || !data || !Array.isArray(data) || data.length === 0) return;

      const normalPoints = data.filter((_, index) => predictions[index] === 1);
      const anomalyPoints = data.filter((_, index) => predictions[index] === -1);

      const normalX = normalPoints.map(point => point.PC1);
      const normalY = normalPoints.map(point => point.PC2);
      const normalZ = normalPoints.map(point => point.PC3);
      const anomalyX = anomalyPoints.map(point => point.PC1);
      const anomalyY = anomalyPoints.map(point => point.PC2);
      const anomalyZ = anomalyPoints.map(point => point.PC3);

      const trace1 = {
        x: normalX,
        y: normalY,
        z: normalZ,
        mode: 'markers',
        type: 'scatter3d',
        name: 'Normal',
        marker: { color: 'blue', size: 4, opacity: 0.6 }
      };

      const trace2 = {
        x: anomalyX,
        y: anomalyY,
        z: anomalyZ,
        mode: 'markers',
        type: 'scatter3d',
        name: 'Anomaly',
        marker: { color: 'red', size: 6, opacity: 0.8, symbol: 'diamond' }
      };

      const layout = {
        title: {
          text: `3D PCA Analysis - Normal vs Anomalous Traffic<br><sub>PC1: ${(explainedVariance[0] * 100).toFixed(1)}% | PC2: ${(explainedVariance[1] * 100).toFixed(1)}% | PC3: ${(explainedVariance[2] * 100).toFixed(1)}%</sub>`,
          font: { size: 16 }
        },
        scene: {
          xaxis: { title: 'Principal Component 1' },
          yaxis: { title: 'Principal Component 2' },
          zaxis: { title: 'Principal Component 3' },
          camera: { eye: { x: 1.5, y: 1.5, z: 1.5 } }
        },
        legend: { x: 0.02, y: 0.98 },
        margin: { t: 80, r: 20, b: 60, l: 60 },
        width: 800,
        height: 600
      };

      const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
      };

      await createPlot(plotRef.current, [trace1, trace2], layout, config);
    };

    createPlotAsync();
    return () => {
      if (plotRef.current) {
        purgePlot(plotRef.current);
      }
    };
  }, [data, predictions, explainedVariance]);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-gray-800">🌐 3D Network Traffic View</CardTitle>
        <CardDescription className="text-gray-600">
          Interactive 3D view of your network traffic. Rotate and zoom to explore suspicious patterns from different angles.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex gap-6">
          <div className="flex-1">
            <div ref={plotRef} className="w-full" style={{ height: '500px' }} />
          </div>
          <div className="w-80 p-4 bg-green-50 border border-green-200 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-3">🎯 How to Use This 3D View:</h4>
            <ul className="text-sm text-green-700 space-y-2">
              <li>• <strong>Mouse:</strong> Click and drag to rotate the view</li>
              <li>• <strong>Scroll:</strong> Zoom in/out to see details</li>
              <li>• <strong>Blue dots:</strong> Normal traffic (safe)</li>
              <li>• <strong>Red diamonds:</strong> Suspicious activities</li>
              <li>• <strong>Clusters:</strong> Similar traffic patterns</li>
            </ul>
            <div className="mt-4 p-3 bg-white rounded border">
              <div className="text-xs text-green-600 space-y-1">
                <p><strong>Normal:</strong> {data.filter((_, index) => predictions[index] === 1).length}</p>
                <p><strong>Suspicious:</strong> {data.filter((_, index) => predictions[index] === -1).length}</p>
                <p><strong>Total analyzed:</strong> {data.length}</p>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// Anomaly Scores Plot Component
interface AnomalyScoresPlotProps {
  scores: number[];
  threshold: number;
}

export const AnomalyScoresPlot = ({ scores, threshold }: AnomalyScoresPlotProps) => {
  const plotRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let isMounted = true;

    const createPlotAsync = async () => {
      if (!isMounted || !plotRef.current || !scores || !Array.isArray(scores) || scores.length === 0) return;

      try {
        const histogram = {
          x: scores,
          type: 'histogram',
          nbinsx: 50,
          marker: {
            color: 'rgba(55, 128, 191, 0.7)',
            line: { color: 'rgba(55, 128, 191, 1)', width: 1 }
          },
          name: 'Anomaly Scores'
        };

        const maxScore = scores.length > 0 ? scores.reduce((max, score) => Math.max(max, score), scores[0]) : 1;
        const thresholdLine = {
          x: [threshold, threshold],
          y: [0, maxScore],
          type: 'scatter',
          mode: 'lines',
          line: { color: 'red', width: 2, dash: 'dash' },
          name: `Threshold: ${threshold.toFixed(2)}`,
          showlegend: true
        };

        const layout = {
          title: { text: 'Distribution of Anomaly Scores', font: { size: 16 } },
          xaxis: { title: 'Anomaly Score', showgrid: true },
          yaxis: { title: 'Number of Flows', showgrid: true },
          legend: { x: 0.02, y: 0.98 },
          margin: { t: 60, r: 20, b: 60, l: 60 },
          width: 800,
          height: 500
        };

        const config = {
          responsive: true,
          displayModeBar: true,
          modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
        };

        if (isMounted && plotRef.current) {
          await createPlot(plotRef.current, [histogram, thresholdLine], layout, config);
        }
      } catch (error) {
        console.error('Error creating plot:', error);
      }
    };

    createPlotAsync();
    return () => {
      isMounted = false;
      if (plotRef.current) {
        purgePlot(plotRef.current);
      }
    };
  }, [scores, threshold]);

  const meanScore = scores && Array.isArray(scores) && scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
  const stdScore = scores && Array.isArray(scores) && scores.length > 0 ? Math.sqrt(scores.reduce((a, b) => a + Math.pow(b - meanScore, 2), 0) / scores.length) : 0;
  const belowThreshold = scores && Array.isArray(scores) ? scores.filter(score => score < threshold).length : 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-gray-800">📊 Threat Level Distribution</CardTitle>
        <CardDescription className="text-gray-600">
          This chart shows how suspicious each network connection is. Lower scores = more dangerous threats.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex gap-6">
          <div className="flex-1">
            <div ref={plotRef} className="w-full" style={{ height: '500px' }} />
          </div>
          <div className="w-80 p-4 bg-orange-50 border border-orange-200 rounded-lg">
            <h4 className="font-semibold text-orange-800 mb-3">📈 Understanding Threat Scores:</h4>
            <div className="space-y-3 text-sm">
              <div className="p-3 bg-white rounded border">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-orange-700">Average Threat Level:</span>
                    <span className="font-mono text-orange-800">{meanScore.toFixed(3)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-orange-700">Variation:</span>
                    <span className="font-mono text-orange-800">{stdScore.toFixed(3)}</span>
                  </div>
                </div>
              </div>
              <div className="p-3 bg-white rounded border">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-orange-700">High Threats:</span>
                    <span className="text-red-600 font-bold">{belowThreshold.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-orange-700">Total Connections:</span>
                    <span className="text-orange-800">{scores.length.toLocaleString()}</span>
                  </div>
                </div>
              </div>
            </div>
            <div className="mt-3 text-xs text-orange-600 p-2 bg-yellow-50 rounded">
              <p><strong>💡 Lower scores = More dangerous threats</strong></p>
              <p>Red line shows alert threshold</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
