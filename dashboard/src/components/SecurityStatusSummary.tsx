'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Shield, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

interface SecurityStatusSummaryProps {
  analysisResults: any;
}

export const SecurityStatusSummary = ({ analysisResults }: SecurityStatusSummaryProps) => {
  if (!analysisResults) {
    return (
      <Card className="bg-gradient-to-br from-white to-gray-50 border-gray-200">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <Shield className="h-5 w-5" />
            Security Status
          </CardTitle>
          <CardDescription className="text-gray-600">
            Run analysis to see your network security status
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
              <Shield className="h-8 w-8 text-gray-400" />
            </div>
            <p className="text-gray-500">No analysis data available</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const { report, alerts } = analysisResults;
  const anomalyCount = report.anomaly_count;
  const totalSamples = report.total_samples;
  const anomalyRate = report.anomaly_percentage;
  const criticalAlerts = alerts ? alerts.length : 0;

  // Determine security status
  let status = 'SAFE';
  let statusColor = 'green';
  let statusIcon = CheckCircle;
  let statusMessage = 'Your network is secure!';
  let recommendations = ['Continue monitoring your network regularly'];

  if (criticalAlerts > 0) {
    status = 'CRITICAL';
    statusColor = 'red';
    statusIcon = XCircle;
    statusMessage = 'Immediate action required!';
    recommendations = [
      'Review the Critical Anomalies tab immediately',
      'Block suspicious IP addresses',
      'Check for unauthorized access',
      'Consider increasing security measures'
    ];
  } else if (anomalyRate > 5) {
    status = 'WARNING';
    statusColor = 'orange';
    statusIcon = AlertTriangle;
    statusMessage = 'High number of suspicious activities detected';
    recommendations = [
      'Review network traffic patterns',
      'Check for potential security threats',
      'Consider tightening security policies',
      'Monitor for unusual behavior'
    ];
  } else if (anomalyRate > 1) {
    status = 'CAUTION';
    statusColor = 'yellow';
    statusIcon = AlertTriangle;
    statusMessage = 'Some suspicious activities detected';
    recommendations = [
      'Keep monitoring your network',
      'Review any unusual patterns',
      'Consider additional security measures'
    ];
  }

  const StatusIcon = statusIcon;

  return (
    <Card className={`bg-gradient-to-br from-white to-${statusColor}-50 border-${statusColor}-200`}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-gray-800">
          <Shield className="h-5 w-5" />
          Security Status Summary
        </CardTitle>
        <CardDescription className="text-gray-600">
          Overall assessment of your network security
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Status Badge */}
        <div className="text-center">
          <div className={`inline-flex items-center gap-3 px-6 py-4 rounded-lg bg-${statusColor}-100 border-2 border-${statusColor}-200`}>
            <StatusIcon className={`h-8 w-8 text-${statusColor}-600`} />
            <div>
              <div className={`text-2xl font-bold text-${statusColor}-800`}>{status}</div>
              <div className={`text-sm text-${statusColor}-700`}>{statusMessage}</div>
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center p-4 bg-white rounded-lg border">
            <div className="text-2xl font-bold text-gray-800">{totalSamples.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Total Connections</div>
          </div>
          <div className="text-center p-4 bg-white rounded-lg border">
            <div className={`text-2xl font-bold ${anomalyCount > 0 ? 'text-red-600' : 'text-green-600'}`}>
              {anomalyCount.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Suspicious Activities</div>
          </div>
        </div>

        {/* Threat Level */}
        <div className="text-center p-4 bg-white rounded-lg border">
          <div className="text-lg font-semibold text-gray-800 mb-2">Threat Level</div>
          <div className="flex justify-center">
            <Badge 
              className={`px-4 py-2 text-lg ${
                status === 'CRITICAL' ? 'bg-red-100 text-red-800 border-red-200' :
                status === 'WARNING' ? 'bg-orange-100 text-orange-800 border-orange-200' :
                status === 'CAUTION' ? 'bg-yellow-100 text-yellow-800 border-yellow-200' :
                'bg-green-100 text-green-800 border-green-200'
              }`}
            >
              {anomalyRate.toFixed(1)}% Suspicious
            </Badge>
          </div>
        </div>

        {/* Recommendations */}
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 className="font-semibold text-blue-800 mb-3 flex items-center gap-2">
            <AlertTriangle className="h-4 w-4" />
            Recommendations
          </h4>
          <ul className="text-sm text-blue-700 space-y-2">
            {recommendations.map((rec, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Critical Alerts */}
        {criticalAlerts > 0 && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <h4 className="font-semibold text-red-800 mb-2 flex items-center gap-2">
              <XCircle className="h-4 w-4" />
              Critical Alerts
            </h4>
            <p className="text-sm text-red-700">
              {criticalAlerts} high-confidence security threats detected. 
              Check the Critical Anomalies tab for detailed information.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
