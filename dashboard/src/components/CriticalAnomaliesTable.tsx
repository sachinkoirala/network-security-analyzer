'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AlertTriangle, Shield, Activity } from 'lucide-react';

interface CriticalAnomaly {
  destination_port: number;
  flow_duration: number;
  fwd_packets: number;
  back_packets: number;
  flow_bytes_s: number;
  anomaly_score: number;
  severity: string;
  protocol: string;
  local_ip: string;
  remote_ip: string;
  status: string;
  timestamp: string;
}

interface CriticalAnomaliesTableProps {
  anomalies: CriticalAnomaly[];
}

export const CriticalAnomaliesTable = ({ anomalies }: CriticalAnomaliesTableProps) => {
  if (!anomalies || !Array.isArray(anomalies) || anomalies.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-green-600" />
            Critical Anomalies
          </CardTitle>
          <CardDescription>High-confidence security threats detected</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <Shield className="h-12 w-12 text-green-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-green-600 mb-2">All Clear!</h3>
            <p className="text-gray-600">No critical anomalies detected in the current analysis.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const getSeverityColor = (severity: string) => {
    switch (severity?.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'low': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getSeverityLabel = (severity: string) => {
    return severity || 'Unknown';
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-gray-800">
          <AlertTriangle className="h-5 w-5 text-red-600" />
          Critical Anomalies
          <Badge variant="destructive" className="ml-2">
            {anomalies.length}
          </Badge>
        </CardTitle>
        <CardDescription className="text-gray-600">
          High-confidence security threats requiring immediate attention
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b">
                <th className="text-left p-3 font-semibold text-gray-700">Severity</th>
                <th className="text-left p-3 font-semibold text-gray-700">Destination Port</th>
                <th className="text-left p-3 font-semibold text-gray-700">Flow Duration</th>
                <th className="text-left p-3 font-semibold text-gray-700">Fwd Packets</th>
                <th className="text-left p-3 font-semibold text-gray-700">Back Packets</th>
                <th className="text-left p-3 font-semibold text-gray-700">Flow Bytes/s</th>
                <th className="text-left p-3 font-semibold text-gray-700">Protocol</th>
                <th className="text-left p-3 font-semibold text-gray-700">Remote IP</th>
                <th className="text-left p-3 font-semibold text-gray-700">Anomaly Score</th>
              </tr>
            </thead>
            <tbody>
              {anomalies.slice(0, 20).map((anomaly, index) => (
                <tr key={index} className="border-b hover:bg-gray-50">
                  <td className="p-3">
                    <Badge 
                      className={`${getSeverityColor(anomaly.severity)} border`}
                    >
                      {getSeverityLabel(anomaly.severity)}
                    </Badge>
                  </td>
                  <td className="p-3 font-mono text-sm text-gray-800">
                    {anomaly.destination_port || 'N/A'}
                  </td>
                  <td className="p-3 text-sm text-gray-800">
                    {typeof anomaly.flow_duration === 'number' ? anomaly.flow_duration.toFixed(2) + 's' : 'N/A'}
                  </td>
                  <td className="p-3 text-sm text-gray-800">
                    {typeof anomaly.fwd_packets === 'number' ? anomaly.fwd_packets.toLocaleString() : 'N/A'}
                  </td>
                  <td className="p-3 text-sm text-gray-800">
                    {typeof anomaly.back_packets === 'number' ? anomaly.back_packets.toLocaleString() : 'N/A'}
                  </td>
                  <td className="p-3 text-sm text-gray-800">
                    {typeof anomaly.flow_bytes_s === 'number' ? anomaly.flow_bytes_s.toLocaleString() : 'N/A'}
                  </td>
                  <td className="p-3 text-sm text-gray-800">
                    <Badge variant="outline" className="text-blue-600">
                      {anomaly.protocol || 'Unknown'}
                    </Badge>
                  </td>
                  <td className="p-3 font-mono text-sm text-gray-800">
                    {anomaly.remote_ip || 'N/A'}
                  </td>
                  <td className="p-3 font-mono text-sm">
                    <span className={`px-2 py-1 rounded ${
                      typeof anomaly.anomaly_score === 'number' && anomaly.anomaly_score < -0.5 ? 'bg-red-100 text-red-800' :
                      typeof anomaly.anomaly_score === 'number' && anomaly.anomaly_score < -0.3 ? 'bg-orange-100 text-orange-800' :
                      typeof anomaly.anomaly_score === 'number' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {typeof anomaly.anomaly_score === 'number' ? anomaly.anomaly_score.toFixed(3) : 'N/A'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {anomalies.length > 20 && (
          <div className="mt-4 text-center text-sm text-gray-600">
            Showing top 20 of {anomalies.length} critical anomalies
          </div>
        )}

        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="font-semibold text-red-800 mb-1">⚠️ Security Alert</h4>
              <p className="text-sm text-red-700">
                {anomalies.length} critical anomalies detected. Review these connections immediately 
                and consider implementing additional security measures.
              </p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
