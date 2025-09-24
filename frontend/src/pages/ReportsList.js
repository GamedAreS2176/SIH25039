import React, { useState, useEffect } from 'react';
import { MapPin, Clock, CheckCircle, AlertTriangle, Filter } from 'lucide-react';
import { api } from '../services/api';

function ReportsList() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    hazard_type: '',
    severity: '',
    verified: ''
  });

  useEffect(() => {
    fetchReports();
  }, [filters]);

  const fetchReports = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.hazard_type) params.append('hazard_type', filters.hazard_type);
      if (filters.severity) params.append('severity', filters.severity);
      
      const response = await api.get(`/reports?${params.toString()}`);
      let reportsData = response.data;
      
      if (filters.verified === 'verified') {
        reportsData = reportsData.filter(report => report.is_verified);
      } else if (filters.verified === 'unverified') {
        reportsData = reportsData.filter(report => !report.is_verified);
      }
      
      setReports(reportsData);
    } catch (error) {
      console.error('Error fetching reports:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters({
      ...filters,
      [key]: value
    });
  };

  const getSeverityColor = (severity) => {
    const colors = {
      low: 'bg-green-100 text-green-800',
      medium: 'bg-yellow-100 text-yellow-800',
      high: 'bg-orange-100 text-orange-800',
      critical: 'bg-red-100 text-red-800'
    };
    return colors[severity] || colors.medium;
  };

  const getHazardTypeColor = (hazardType) => {
    const colors = {
      tsunami: 'text-red-600',
      storm_surge: 'text-orange-600',
      high_waves: 'text-yellow-600',
      flooding: 'text-blue-600',
      abnormal_tide: 'text-purple-600',
      other: 'text-gray-600'
    };
    return colors[hazardType] || colors.other;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Hazard Reports</h1>
          <p className="mt-2 text-gray-600">View and filter all reported ocean hazards</p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-center mb-4">
            <Filter className="h-5 w-5 mr-2 text-gray-500" />
            <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Hazard Type
              </label>
              <select
                value={filters.hazard_type}
                onChange={(e) => handleFilterChange('hazard_type', e.target.value)}
                className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Types</option>
                <option value="tsunami">Tsunami</option>
                <option value="storm_surge">Storm Surge</option>
                <option value="high_waves">High Waves</option>
                <option value="swell_surge">Swell Surge</option>
                <option value="coastal_current">Coastal Current</option>
                <option value="flooding">Flooding</option>
                <option value="abnormal_tide">Abnormal Tide</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Severity
              </label>
              <select
                value={filters.severity}
                onChange={(e) => handleFilterChange('severity', e.target.value)}
                className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Severities</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Verification Status
              </label>
              <select
                value={filters.verified}
                onChange={(e) => handleFilterChange('verified', e.target.value)}
                className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Reports</option>
                <option value="verified">Verified Only</option>
                <option value="unverified">Unverified Only</option>
              </select>
            </div>

            <div className="flex items-end">
              <button
                onClick={() => setFilters({ hazard_type: '', severity: '', verified: '' })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Clear Filters
              </button>
            </div>
          </div>
        </div>

        {/* Reports List */}
        <div className="space-y-6">
          {reports.length === 0 ? (
            <div className="text-center py-12">
              <AlertTriangle className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No reports found</h3>
              <p className="mt-1 text-sm text-gray-500">
                Try adjusting your filters or check back later.
              </p>
            </div>
          ) : (
            reports.map((report) => (
              <div key={report.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {report.title}
                    </h3>
                    <p className="text-gray-600 mb-3">{report.description}</p>
                    
                    <div className="flex flex-wrap items-center gap-3 mb-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(report.severity)}`}>
                        {report.severity.toUpperCase()}
                      </span>
                      
                      <span className={`text-sm font-medium ${getHazardTypeColor(report.hazard_type)}`}>
                        {report.hazard_type.replace('_', ' ').toUpperCase()}
                      </span>
                      
                      {report.is_verified && (
                        <span className="flex items-center text-sm text-green-600">
                          <CheckCircle className="h-4 w-4 mr-1" />
                          Verified
                        </span>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center text-sm text-gray-500">
                    <Clock className="h-4 w-4 mr-1" />
                    {new Date(report.created_at).toLocaleString()}
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center text-sm text-gray-500">
                    <MapPin className="h-4 w-4 mr-1" />
                    {report.latitude.toFixed(4)}, {report.longitude.toFixed(4)}
                  </div>
                  
                  {report.media_urls && report.media_urls.length > 0 && (
                    <div className="text-sm text-blue-600">
                      {report.media_urls.length} media file(s)
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Pagination would go here in a real implementation */}
        {reports.length > 0 && (
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-500">
              Showing {reports.length} report(s)
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ReportsList;