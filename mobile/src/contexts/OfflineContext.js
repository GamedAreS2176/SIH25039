import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Network from 'expo-network';

const OfflineContext = createContext();

export function useOffline() {
  return useContext(OfflineContext);
}

export function OfflineProvider({ children }) {
  const [isOnline, setIsOnline] = useState(true);
  const [offlineReports, setOfflineReports] = useState([]);
  const [pendingSync, setPendingSync] = useState(false);

  useEffect(() => {
    checkNetworkStatus();
    loadOfflineReports();
  }, []);

  const checkNetworkStatus = async () => {
    try {
      const networkState = await Network.getNetworkStateAsync();
      setIsOnline(networkState.isConnected);
    } catch (error) {
      console.error('Error checking network status:', error);
    }
  };

  const loadOfflineReports = async () => {
    try {
      const stored = await AsyncStorage.getItem('offline_reports');
      if (stored) {
        setOfflineReports(JSON.parse(stored));
      }
    } catch (error) {
      console.error('Error loading offline reports:', error);
    }
  };

  const saveOfflineReport = async (report) => {
    try {
      const newReport = {
        ...report,
        id: Date.now().toString(),
        created_at: new Date().toISOString(),
        is_offline: true
      };
      
      const updatedReports = [...offlineReports, newReport];
      setOfflineReports(updatedReports);
      
      await AsyncStorage.setItem('offline_reports', JSON.stringify(updatedReports));
      
      return newReport;
    } catch (error) {
      console.error('Error saving offline report:', error);
      throw error;
    }
  };

  const removeOfflineReport = async (reportId) => {
    try {
      const updatedReports = offlineReports.filter(report => report.id !== reportId);
      setOfflineReports(updatedReports);
      
      await AsyncStorage.setItem('offline_reports', JSON.stringify(updatedReports));
    } catch (error) {
      console.error('Error removing offline report:', error);
    }
  };

  const syncOfflineReports = async () => {
    if (!isOnline || pendingSync) return;
    
    setPendingSync(true);
    
    try {
      const { api } = require('../services/api');
      
      for (const report of offlineReports) {
        try {
          // Convert offline report to API format
          const formData = new FormData();
          formData.append('title', report.title);
          formData.append('description', report.description);
          formData.append('hazard_type', report.hazard_type);
          formData.append('severity', report.severity);
          formData.append('latitude', report.latitude.toString());
          formData.append('longitude', report.longitude.toString());
          
          if (report.media_path) {
            formData.append('file', {
              uri: report.media_path,
              type: report.media_type,
              name: report.media_name
            });
          }
          
          await api.post('/reports', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          
          // Remove from offline storage after successful sync
          await removeOfflineReport(report.id);
          
        } catch (error) {
          console.error(`Error syncing report ${report.id}:`, error);
        }
      }
      
      setPendingSync(false);
    } catch (error) {
      console.error('Error during sync:', error);
      setPendingSync(false);
    }
  };

  const value = {
    isOnline,
    offlineReports,
    pendingSync,
    saveOfflineReport,
    removeOfflineReport,
    syncOfflineReports,
    checkNetworkStatus
  };

  return (
    <OfflineContext.Provider value={value}>
      {children}
    </OfflineContext.Provider>
  );
}