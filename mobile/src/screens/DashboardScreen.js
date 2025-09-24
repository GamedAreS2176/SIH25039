import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { Card, Title, Paragraph, Chip, FAB, ActivityIndicator } from 'react-native-paper';
import { MaterialIcons } from '@expo/vector-icons';
import { useAuth } from '../contexts/AuthContext';
import { useOffline } from '../contexts/OfflineContext';
import { api } from '../services/api';

export default function DashboardScreen({ navigation }) {
  const [reports, setReports] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const { user } = useAuth();
  const { isOnline, offlineReports, syncOfflineReports } = useOffline();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [reportsRes, statsRes] = await Promise.all([
        api.get('/reports?limit=10'),
        api.get('/stats/dashboard')
      ]);

      setReports(reportsRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchDashboardData();
    if (isOnline) {
      await syncOfflineReports();
    }
    setRefreshing(false);
  };

  const getSeverityColor = (severity) => {
    const colors = {
      low: '#4CAF50',
      medium: '#FF9800',
      high: '#FF5722',
      critical: '#F44336'
    };
    return colors[severity] || colors.medium;
  };

  const getHazardTypeIcon = (hazardType) => {
    const icons = {
      tsunami: 'waves',
      storm_surge: 'thunderstorm',
      high_waves: 'waves',
      flooding: 'water',
      abnormal_tide: 'tide',
      other: 'warning'
    };
    return icons[hazardType] || 'warning';
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* Status Card */}
        <Card style={styles.card}>
          <Card.Content>
            <Title>Welcome, {user?.username}!</Title>
            <Paragraph>
              {isOnline ? 'Online' : 'Offline'} • {offlineReports.length} pending reports
            </Paragraph>
          </Card.Content>
        </Card>

        {/* Stats Cards */}
        {stats && (
          <View style={styles.statsContainer}>
            <Card style={styles.statCard}>
              <Card.Content style={styles.statContent}>
                <MaterialIcons name="warning" size={24} color="#2196F3" />
                <Title style={styles.statNumber}>{stats.reports_by_type?.length || 0}</Title>
                <Paragraph style={styles.statLabel}>Total Reports</Paragraph>
              </Card.Content>
            </Card>

            <Card style={styles.statCard}>
              <Card.Content style={styles.statContent}>
                <MaterialIcons name="location-on" size={24} color="#4CAF50" />
                <Title style={styles.statNumber}>{stats.active_hotspots || 0}</Title>
                <Paragraph style={styles.statLabel}>Active Hotspots</Paragraph>
              </Card.Content>
            </Card>
          </View>
        )}

        {/* Recent Reports */}
        <Card style={styles.card}>
          <Card.Content>
            <Title>Recent Hazard Reports</Title>
            {reports.length === 0 ? (
              <Paragraph style={styles.emptyText}>
                No recent reports found
              </Paragraph>
            ) : (
              reports.slice(0, 5).map((report) => (
                <Card key={report.id} style={styles.reportCard}>
                  <Card.Content>
                    <View style={styles.reportHeader}>
                      <Title style={styles.reportTitle}>{report.title}</Title>
                      <Chip
                        style={[styles.severityChip, { backgroundColor: getSeverityColor(report.severity) }]}
                        textStyle={styles.severityText}
                      >
                        {report.severity.toUpperCase()}
                      </Chip>
                    </View>
                    
                    <Paragraph style={styles.reportDescription}>
                      {report.description}
                    </Paragraph>
                    
                    <View style={styles.reportFooter}>
                      <View style={styles.reportMeta}>
                        <MaterialIcons 
                          name={getHazardTypeIcon(report.hazard_type)} 
                          size={16} 
                          color="#666" 
                        />
                        <Paragraph style={styles.reportMetaText}>
                          {report.hazard_type.replace('_', ' ')}
                        </Paragraph>
                      </View>
                      
                      <Paragraph style={styles.reportTime}>
                        {new Date(report.created_at).toLocaleDateString()}
                      </Paragraph>
                    </View>
                  </Card.Content>
                </Card>
              ))
            )}
          </Card.Content>
        </Card>

        {/* Offline Reports */}
        {offlineReports.length > 0 && (
          <Card style={styles.card}>
            <Card.Content>
              <Title>Offline Reports ({offlineReports.length})</Title>
              <Paragraph>
                You have {offlineReports.length} reports waiting to be synced.
                {isOnline ? ' They will be synced automatically.' : ' Connect to internet to sync.'}
              </Paragraph>
              <Button
                mode="outlined"
                onPress={() => navigation.navigate('OfflineReports')}
                style={styles.offlineButton}
              >
                View Offline Reports
              </Button>
            </Card.Content>
          </Card>
        )}
      </ScrollView>

      <FAB
        style={styles.fab}
        icon="plus"
        onPress={() => navigation.navigate('Report')}
        label="Report Hazard"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  scrollView: {
    flex: 1,
    padding: 16,
  },
  card: {
    marginBottom: 16,
    elevation: 2,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  statCard: {
    flex: 1,
    marginHorizontal: 4,
    elevation: 2,
  },
  statContent: {
    alignItems: 'center',
    paddingVertical: 16,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2196F3',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
  },
  reportCard: {
    marginBottom: 8,
    elevation: 1,
  },
  reportHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  reportTitle: {
    fontSize: 16,
    flex: 1,
    marginRight: 8,
  },
  severityChip: {
    height: 24,
  },
  severityText: {
    color: 'white',
    fontSize: 10,
    fontWeight: 'bold',
  },
  reportDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  reportFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  reportMeta: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  reportMetaText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 4,
  },
  reportTime: {
    fontSize: 12,
    color: '#999',
  },
  emptyText: {
    textAlign: 'center',
    color: '#666',
    fontStyle: 'italic',
  },
  offlineButton: {
    marginTop: 8,
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#2196F3',
  },
});