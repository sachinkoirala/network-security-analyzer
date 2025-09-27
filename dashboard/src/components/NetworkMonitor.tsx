'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { RefreshCw, Wifi, Activity, Shield } from 'lucide-react';
import { NetworkInfo, useAnalysis } from '@/contexts/AnalysisContext';

interface NetworkMonitorProps {
  networkInfo: NetworkInfo | null;
}

export const NetworkMonitor = ({ networkInfo }: NetworkMonitorProps) => {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const { getNetworkInfo } = useAnalysis();

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await getNetworkInfo();
    setIsRefreshing(false);
  };

  if (!networkInfo) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Wifi className="h-5 w-5" />
            Network Monitor
          </CardTitle>
          <CardDescription>
            Real-time network interface and connection monitoring
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <Button onClick={handleRefresh} disabled={isRefreshing}>
              {isRefreshing ? (
                <>
                  <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                  Loading...
                </>
              ) : (
                <>
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Load Network Info
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Network Interfaces */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <Wifi className="h-5 w-5" />
            Network Interfaces
            <Button
              onClick={handleRefresh}
              disabled={isRefreshing}
              size="sm"
              variant="outline"
            >
              {isRefreshing ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                <RefreshCw className="h-4 w-4" />
              )}
            </Button>
          </CardTitle>
          <CardDescription className="text-gray-600">
            Active network interfaces and their IP addresses
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {networkInfo.interfaces && Array.isArray(networkInfo.interfaces) && networkInfo.interfaces.length > 0 ? networkInfo.interfaces.map((iface, index) => (
              <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <Wifi className="h-4 w-4 text-blue-600" />
                  <div>
                    <div className="font-medium text-gray-800">{iface.name}</div>
                    <div className="text-sm text-gray-600">
                      {iface.ip} / {iface.netmask}
                    </div>
                  </div>
                </div>
                <Badge variant="outline">Active</Badge>
              </div>
            )) : (
              <div className="text-center py-8">
                <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                  <Wifi className="h-8 w-8 text-gray-400" />
                </div>
                <p className="text-gray-600 mb-2">No network interfaces detected</p>
                <p className="text-sm text-gray-500">Click refresh to scan for network interfaces</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Active Connections */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <Activity className="h-5 w-5" />
            Active Connections
            <Badge variant="secondary">
              {networkInfo.connections ? networkInfo.connections.length : 0}
            </Badge>
          </CardTitle>
          <CardDescription className="text-gray-600">
            Current network connections and their status
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {networkInfo.connections && Array.isArray(networkInfo.connections) && networkInfo.connections.length > 0 ? (
              networkInfo.connections.map((conn, index) => (
                <div key={index} className="flex items-center justify-between p-2 border rounded text-sm">
                  <div className="flex items-center gap-3">
                    <Activity className="h-3 w-3 text-green-600" />
                    <div>
                      <div className="font-mono text-xs text-gray-800">
                        {conn.local_address} → {conn.remote_address}
                      </div>
                      <div className="text-xs text-gray-600">
                        PID: {conn.pid || 'N/A'} | Status: {conn.status}
                      </div>
                    </div>
                  </div>
                  <Badge variant="outline" className="text-xs">
                    {conn.status}
                  </Badge>
                </div>
              ))
            ) : (
              <div className="text-center py-8">
                <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                  <Activity className="h-8 w-8 text-gray-400" />
                </div>
                <p className="text-gray-600 mb-2">No active connections detected</p>
                <p className="text-sm text-gray-500">This could mean no network activity or API not running</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Security Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <Shield className="h-5 w-5" />
            Security Status
          </CardTitle>
          <CardDescription className="text-gray-600">
            Current network security assessment
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-4 border rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {networkInfo.interfaces ? networkInfo.interfaces.length : 0}
              </div>
              <div className="text-sm text-gray-600">Active Interfaces</div>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {networkInfo.connections ? networkInfo.connections.length : 0}
              </div>
              <div className="text-sm text-gray-600">Active Connections</div>
            </div>
          </div>
          <div className="mt-4 text-xs text-gray-500">
            Last updated: {new Date(networkInfo.timestamp).toLocaleString()}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
