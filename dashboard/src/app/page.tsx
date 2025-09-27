'use client';

import { useState, useEffect } from 'react';
import { NetworkSecurityDashboard } from '@/components/NetworkSecurityDashboard';
import { AnalysisProvider } from '@/contexts/AnalysisContext';

export default function Home() {
  return (
    <AnalysisProvider>
      <main className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
                    <h1 className="text-5xl font-bold text-gray-800 mb-4">
                      Network Security Analyzer
                    </h1>
                    <p className="text-xl text-gray-600 mb-6">
                      🛡️ Real-time network traffic analysis and anomaly detection
                    </p>
            <div className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
              System Ready
            </div>
          </div>
          <NetworkSecurityDashboard />
        </div>
      </main>
    </AnalysisProvider>
  );
}