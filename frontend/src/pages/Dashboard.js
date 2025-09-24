import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import { Icon } from 'leaflet';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { MapPin, AlertTriangle, TrendingUp, Users } from 'lucide-react';
import { api } from '../services/api';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in react-leaflet
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

function Dashboard() {
  const [reports, setReports] = useState([]);
  const [hotspots, setHotspots] = useState([]);
  const [socialMedia, setSocialMedia] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [reportsRes, hotspotsRes, socialRes, statsRes] = await Promise.all([
        api.get('/reports?limit=100'),
        api.get('/hotspots'),
        api.get('/social-media?limit=50'),
        api.get('/stats/dashboard')
      ]);

      setReports(reportsRes.data);
      setHotspots(hotspotsRes.data);
      setSocialMedia(socialRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMarkerColor = (hazardType) => {
    const colors = {
      tsunami: '#dc2626',
      storm_surge: '#ea580c',
      high_waves: '#d97706',
      flooding: '#2563eb',
      abnormal_tide: '#7c3aed',
      other: '#6b7280'
    };
    return colors[hazardType] || colors.other;
  };

  const getSeverityColor = (severity) => {
    const colors = {
      low: '#10b981',
      medium: '#f59e0b',
      high: '#f97316',
      critical: '#dc2626'
    };
    return colors[severity] || colors.medium;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Ocean Hazard Monitoring Dashboard</h1>
          <p className="mt-2 text-gray-600">Real-time monitoring of ocean hazards and social media activity</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="stat-card">
            <div className="flex items-center">
              <AlertTriangle className="h-8 w-8 mr-3" />
              <div>
                <p className="text-sm opacity-90">Total Reports</p>
                <p className="text-2xl font-bold">{reports.length}</p>
              </div>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="flex items-center">
              <MapPin className="h-8 w-8 mr-3" />
              <div>
                <p className="text-sm opacity-90">Active Hotspots</p>
                <p className="text-2xl font-bold">{hotspots.length}</p>
              </div>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="flex items-center">
              <TrendingUp className="h-8 w-8 mr-3" />
              <div>
                <p className="text-sm opacity-90">Social Media Posts</p>
                <p className="text-2xl font-bold">{socialMedia.length}</p>
              </div>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="flex items-center">
              <Users className="h-8 w-8 mr-3" />
              <div>
                <p className="text-sm opacity-90">Verified Reports</p>
                <p className="text-2xl font-bold">
                  {reports.filter(r => r.is_verified).length}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Map */}
          <div className="dashboard-card">
            <h2 className="text-xl font-semibold mb-4">Hazard Reports Map</h2>
            <div className="h-96 rounded-lg overflow-hidden">
              <MapContainer
                center={[13.0827, 80.2707]} // Chennai coordinates
                zoom={10}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                
                {/* Report Markers */}
                {reports.map((report) => (
                  <Marker
                    key={report.id}
                    position={[report.latitude, report.longitude]}
                    icon={new Icon({
                      iconUrl: `data:image/svg+xml;base64,${btoa(`
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="${getMarkerColor(report.hazard_type)}">
                          <circle cx="12" cy="12" r="10" stroke="white" stroke-width="2"/>
                          <text x="12" y="16" text-anchor="middle" fill="white" font-size="12" font-weight="bold">!</text>
                        </svg>
                      `)}`,
                      iconSize: [24, 24],
                      iconAnchor: [12, 12]
                    })}
                  >
                    <Popup>
                      <div className="p-2">
                        <h3 className="font-semibold">{report.title}</h3>
                        <p className="text-sm text-gray-600">{report.description}</p>
                        <div className="mt-2 flex items-center space-x-2">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            report.severity === 'critical' ? 'bg-red-100 text-red-800' :
                            report.severity === 'high' ? 'bg-orange-100 text-orange-800' :
                            report.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {report.severity}
                          </span>
                          <span className="text-xs text-gray-500">
                            {new Date(report.created_at).toLocaleString()}
                          </span>
                        </div>
                      </div>
                    </Popup>
                  </Marker>
                ))}
                
                {/* Hotspot Circles */}
                {hotspots.map((hotspot) => (
                  <Circle
                    key={hotspot.id}
                    center={[hotspot.latitude, hotspot.longitude]}
                    radius={hotspot.radius_meters}
                    pathOptions={{
                      fillColor: getSeverityColor(hotspot.severity_level),
                      color: getSeverityColor(hotspot.severity_level),
                      fillOpacity: 0.3,
                      weight: 2
                    }}
                  />
                ))}
              </MapContainer>
            </div>
          </div>

          {/* Charts */}
          <div className="space-y-6">
            {/* Reports by Type */}
            <div className="dashboard-card">
              <h3 className="text-lg font-semibold mb-4">Reports by Hazard Type</h3>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={stats?.reports_by_type || []}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="hazard_type" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3B82F6" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Social Media Activity */}
            <div className="dashboard-card">
              <h3 className="text-lg font-semibold mb-4">Social Media Activity</h3>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={stats?.social_media_activity || []}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ platform, count }) => `${platform}: ${count}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="count"
                  >
                    {stats?.social_media_activity?.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Recent Reports */}
        <div className="mt-8">
          <div className="dashboard-card">
            <h2 className="text-xl font-semibold mb-4">Recent Hazard Reports</h2>
            <div className="space-y-4">
              {reports.slice(0, 5).map((report) => (
                <div key={report.id} className="hazard-card">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold">{report.title}</h3>
                      <p className="text-sm text-gray-600 mt-1">{report.description}</p>
                      <div className="flex items-center space-x-4 mt-2">
                        <span className="text-xs text-gray-500">
                          {report.hazard_type.replace('_', ' ')}
                        </span>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          report.severity === 'critical' ? 'bg-red-100 text-red-800' :
                          report.severity === 'high' ? 'bg-orange-100 text-orange-800' :
                          report.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {report.severity}
                        </span>
                        {report.is_verified && (
                          <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                            Verified
                          </span>
                        )}
                      </div>
                    </div>
                    <span className="text-xs text-gray-500">
                      {new Date(report.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;