import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { MapPin, User, LogOut, AlertTriangle } from 'lucide-react';

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <AlertTriangle className="h-8 w-8" />
              <span className="text-xl font-bold">Data Dolphins</span>
            </Link>
          </div>
          
          <div className="flex items-center space-x-4">
            <Link to="/" className="hover:text-blue-200 transition-colors">
              Dashboard
            </Link>
            <Link to="/reports" className="hover:text-blue-200 transition-colors">
              Reports
            </Link>
            
            {user ? (
              <>
                <Link to="/report" className="bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded-md transition-colors">
                  Report Hazard
                </Link>
                <div className="flex items-center space-x-2">
                  <User className="h-5 w-5" />
                  <span className="text-sm">
                    {user.username} ({user.role})
                  </span>
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-1 hover:text-blue-200 transition-colors"
                  >
                    <LogOut className="h-4 w-4" />
                    <span>Logout</span>
                  </button>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-4">
                <Link to="/login" className="hover:text-blue-200 transition-colors">
                  Login
                </Link>
                <Link to="/register" className="bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded-md transition-colors">
                  Register
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;