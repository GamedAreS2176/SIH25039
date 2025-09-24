import { api } from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Network from 'expo-network';

export const syncOfflineReports = async () => {
  try {
    const networkState = await Network.getNetworkStateAsync();
    if (!networkState.isConnected) {
      return { success: false, message: 'No internet connection' };
    }

    const offlineReports = await AsyncStorage.getItem('offline_reports');
    if (!offlineReports) {
      return { success: true, message: 'No offline reports to sync' };
    }

    const reports = JSON.parse(offlineReports);
    const syncedReports = [];
    const failedReports = [];

    for (const report of reports) {
      try {
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

        syncedReports.push(report.id);
      } catch (error) {
        console.error(`Error syncing report ${report.id}:`, error);
        failedReports.push(report.id);
      }
    }

    // Remove successfully synced reports from offline storage
    if (syncedReports.length > 0) {
      const remainingReports = reports.filter(report => !syncedReports.includes(report.id));
      await AsyncStorage.setItem('offline_reports', JSON.stringify(remainingReports));
    }

    return {
      success: true,
      synced: syncedReports.length,
      failed: failedReports.length,
      message: `Synced ${syncedReports.length} reports, ${failedReports.length} failed`
    };

  } catch (error) {
    console.error('Error in sync service:', error);
    return { success: false, message: 'Sync failed' };
  }
};