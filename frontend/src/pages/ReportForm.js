import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, Upload, AlertTriangle, Camera } from 'lucide-react';
import { api } from '../services/api';
import toast from 'react-hot-toast';

function ReportForm() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    hazard_type: 'high_waves',
    severity: 'medium',
    latitude: 13.0827, // Default to Chennai
    longitude: 80.2707
  });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showLocationPicker, setShowLocationPicker] = useState(false);
  
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.size > 10 * 1024 * 1024) { // 10MB limit
        toast.error('File size must be less than 10MB');
        return;
      }
      setFile(selectedFile);
    }
  };

  const handleLocationClick = (lat, lng) => {
    setFormData({
      ...formData,
      latitude: lat,
      longitude: lng
    });
    setShowLocationPicker(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('title', formData.title);
      formDataToSend.append('description', formData.description);
      formDataToSend.append('hazard_type', formData.hazard_type);
      formDataToSend.append('severity', formData.severity);
      formDataToSend.append('latitude', formData.latitude.toString());
      formDataToSend.append('longitude', formData.longitude.toString());
      
      if (file) {
        formDataToSend.append('file', file);
      }

      await api.post('/reports', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast.success('Hazard report submitted successfully!');
      navigate('/');
    } catch (error) {
      toast.error('Failed to submit report. Please try again.');
      console.error('Error submitting report:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h1 className="text-2xl font-bold text-gray-900 flex items-center">
              <AlertTriangle className="h-6 w-6 mr-2 text-blue-600" />
              Report Ocean Hazard
            </h1>
            <p className="mt-1 text-sm text-gray-600">
              Help us monitor ocean hazards by reporting what you observe
            </p>
          </div>

          <form onSubmit={handleSubmit} className="p-6 space-y-6">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                Report Title *
              </label>
              <input
                type="text"
                id="title"
                name="title"
                required
                value={formData.title}
                onChange={handleChange}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Brief description of the hazard"
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                Detailed Description *
              </label>
              <textarea
                id="description"
                name="description"
                rows={4}
                required
                value={formData.description}
                onChange={handleChange}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Provide detailed information about the hazard you observed"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="hazard_type" className="block text-sm font-medium text-gray-700">
                  Hazard Type *
                </label>
                <select
                  id="hazard_type"
                  name="hazard_type"
                  required
                  value={formData.hazard_type}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
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
                <label htmlFor="severity" className="block text-sm font-medium text-gray-700">
                  Severity Level *
                </label>
                <select
                  id="severity"
                  name="severity"
                  required
                  value={formData.severity}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Location *
              </label>
              <div className="flex items-center space-x-4">
                <div className="flex-1">
                  <input
                    type="number"
                    step="any"
                    placeholder="Latitude"
                    value={formData.latitude}
                    onChange={(e) => setFormData({...formData, latitude: parseFloat(e.target.value)})}
                    className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div className="flex-1">
                  <input
                    type="number"
                    step="any"
                    placeholder="Longitude"
                    value={formData.longitude}
                    onChange={(e) => setFormData({...formData, longitude: parseFloat(e.target.value)})}
                    className="block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <button
                  type="button"
                  onClick={() => setShowLocationPicker(!showLocationPicker)}
                  className="flex items-center px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <MapPin className="h-4 w-4 mr-2" />
                  Pick Location
                </button>
              </div>
              {showLocationPicker && (
                <div className="mt-4 p-4 border border-gray-300 rounded-md bg-gray-50">
                  <p className="text-sm text-gray-600 mb-2">Quick location selection:</p>
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      type="button"
                      onClick={() => handleLocationClick(13.0827, 80.2707)}
                      className="text-left p-2 border border-gray-300 rounded hover:bg-blue-50"
                    >
                      Chennai, Tamil Nadu
                    </button>
                    <button
                      type="button"
                      onClick={() => handleLocationClick(19.0760, 72.8777)}
                      className="text-left p-2 border border-gray-300 rounded hover:bg-blue-50"
                    >
                      Mumbai, Maharashtra
                    </button>
                    <button
                      type="button"
                      onClick={() => handleLocationClick(12.9716, 77.5946)}
                      className="text-left p-2 border border-gray-300 rounded hover:bg-blue-50"
                    >
                      Bangalore, Karnataka
                    </button>
                    <button
                      type="button"
                      onClick={() => handleLocationClick(22.5726, 88.3639)}
                      className="text-left p-2 border border-gray-300 rounded hover:bg-blue-50"
                    >
                      Kolkata, West Bengal
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div>
              <label htmlFor="file" className="block text-sm font-medium text-gray-700">
                Photo/Video (Optional)
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-gray-400 transition-colors">
                <div className="space-y-1 text-center">
                  <Camera className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="flex text-sm text-gray-600">
                    <label
                      htmlFor="file"
                      className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500"
                    >
                      <span>Upload a file</span>
                      <input
                        id="file"
                        name="file"
                        type="file"
                        accept="image/*,video/*"
                        onChange={handleFileChange}
                        className="sr-only"
                      />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs text-gray-500">PNG, JPG, MP4 up to 10MB</p>
                </div>
              </div>
              {file && (
                <div className="mt-2 text-sm text-gray-600">
                  Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </div>
              )}
            </div>

            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => navigate('/')}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Submitting...' : 'Submit Report'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ReportForm;