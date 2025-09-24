# Data Dolphins - Ocean Hazard Monitoring Platform

A comprehensive platform for real-time ocean hazard monitoring using crowdsourced reports and social media analytics, developed for Smart India Hackathon 2025.

## 🐬 Overview

Data Dolphins is an integrated software platform that enables citizens, coastal residents, volunteers, and disaster managers to report observations during hazardous ocean events and monitor public communication trends via social media. The platform provides real-time monitoring, early warning integration, and comprehensive analytics for ocean hazard management.

## ✨ Features

### 🚨 Real-time Hazard Monitoring
- **Citizen Reporting**: Mobile and web apps for geotagged hazard reports with photos/videos
- **Social Media Integration**: Real-time monitoring of Twitter, Facebook, YouTube for hazard discussions
- **Interactive Dashboard**: Dynamic map visualization with hotspots and filtering
- **NLP Processing**: Automated hazard detection and sentiment analysis

### 🚨 Early Warning Systems
- **INCOIS Integration**: Connection with Indian National Centre for Ocean Information Services
- **Automated Alerts**: Real-time notifications to users in affected zones
- **Risk Assessment**: AI-powered risk scoring based on multiple data sources

### 🌐 Multi-platform Access
- **Web Dashboard**: React-based interactive dashboard with real-time updates
- **Mobile App**: React Native app with offline sync capabilities
- **Multilingual Support**: Regional language accessibility
- **Role-based Access**: Different interfaces for citizens, analysts, and officials

## 🏗️ Architecture

### Backend Services
- **FastAPI Backend**: RESTful API with PostgreSQL + PostGIS for spatial data
- **NLP Engine**: Social media processing with spaCy and machine learning
- **Redis**: Real-time data caching and pub/sub messaging
- **Celery**: Background task processing

### Frontend Applications
- **React Dashboard**: Interactive web interface with Leaflet maps
- **React Native Mobile**: Cross-platform mobile app with offline capabilities
- **Real-time Updates**: WebSocket connections for live data

### Data Processing
- **Spatial Analysis**: H3 indexing for efficient geospatial queries
- **Machine Learning**: Hazard detection and sentiment analysis
- **Social Media APIs**: Twitter, Facebook, YouTube integration
- **Alert System**: Multi-channel notification delivery

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js (for mobile app development)
- Python 3.11+ (for local development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/GamedAreS2176/SIH25039.git
   cd SIH25039
   ```

2. **Run the setup script**
   ```bash
   ./scripts/setup.sh
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Start the services**
   ```bash
   docker-compose up -d
   ```

### Access the Application

- **Web Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **NLP Service**: http://localhost:8001

### Mobile App Development

```bash
cd mobile
npm install
npm start
```

## 🧪 Testing

Run the test suite to verify all components:

```bash
./scripts/test.sh
```

## 📱 Mobile App Features

### Offline Capabilities
- **Offline Reporting**: Submit reports without internet connection
- **Automatic Sync**: Sync reports when connection is restored
- **Local Storage**: SQLite database for offline data
- **Background Sync**: Automatic synchronization in background

### User Experience
- **Intuitive Interface**: Easy-to-use reporting forms
- **Location Services**: Automatic GPS location detection
- **Media Upload**: Photo and video capture with compression
- **Push Notifications**: Real-time alert delivery

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ocean_hazards

# Social Media APIs
TWITTER_API_KEY=your_twitter_api_key
FACEBOOK_ACCESS_TOKEN=your_facebook_token
YOUTUBE_API_KEY=your_youtube_key

# INCOIS Integration
INCOIS_BASE_URL=https://www.incois.gov.in
INCOIS_API_KEY=your_incois_key

# Notification Services
TWILIO_ACCOUNT_SID=your_twilio_sid
SMTP_SERVER=smtp.gmail.com
```

### API Keys Setup

1. **Twitter API**: Get keys from Twitter Developer Portal
2. **Facebook API**: Create app in Facebook Developers
3. **YouTube API**: Enable YouTube Data API v3
4. **INCOIS**: Contact INCOIS for API access
5. **Twilio**: Sign up for SMS notifications
6. **Firebase**: Setup for push notifications

## 🗄️ Database Schema

### Core Tables
- **users**: User accounts with role-based access
- **hazard_reports**: Citizen-submitted hazard reports
- **social_media_posts**: Processed social media content
- **hotspots**: Dynamic hazard hotspots
- **alerts**: System and INCOIS alerts
- **user_alerts**: User-specific alert notifications

### Spatial Features
- **PostGIS**: Advanced geospatial queries
- **H3 Indexing**: Efficient spatial clustering
- **Geofencing**: Location-based alert delivery

## 🔄 Data Flow

1. **Data Collection**
   - Citizens submit reports via mobile/web apps
   - Social media APIs collect relevant posts
   - INCOIS provides official warnings

2. **Processing**
   - NLP engine analyzes social media content
   - Spatial analysis identifies hotspots
   - Risk assessment algorithms evaluate threats

3. **Visualization**
   - Real-time dashboard updates
   - Interactive map with filtering
   - Statistical charts and trends

4. **Alerting**
   - Automated alert generation
   - Multi-channel notifications
   - Integration with emergency services

## 🚨 Alert System

### Alert Types
- **Tsunami Warnings**: Based on seismic data and reports
- **Storm Surge Alerts**: Weather-based predictions
- **High Wave Warnings**: Oceanographic conditions
- **Flooding Alerts**: Coastal inundation risks

### Notification Channels
- **Email**: Detailed alert information
- **SMS**: Critical alerts via Twilio
- **Push Notifications**: Mobile app alerts
- **Web Dashboard**: Real-time updates

## 🌍 Multilingual Support

Supported languages:
- English (default)
- Hindi (हिंदी)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Bengali (বাংলা)

## 🔒 Security Features

- **JWT Authentication**: Secure API access
- **Role-based Authorization**: Different access levels
- **Data Encryption**: Sensitive data protection
- **Input Validation**: SQL injection prevention
- **Rate Limiting**: API abuse protection

## 📊 Analytics & Reporting

### Dashboard Metrics
- **Report Statistics**: By type, severity, location
- **Social Media Trends**: Sentiment analysis
- **Hotspot Analysis**: Geographic clustering
- **Alert Effectiveness**: Response times and coverage

### Export Options
- **CSV Reports**: Data export for analysis
- **PDF Summaries**: Executive reports
- **API Access**: Programmatic data retrieval

## 🚀 Deployment

### Production Deployment

1. **Cloud Infrastructure**
   ```bash
   # AWS/GCP/Azure deployment
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Environment Configuration**
   ```bash
   # Set production environment variables
   export NODE_ENV=production
   export DATABASE_URL=your_production_db_url
   ```

3. **SSL/TLS Setup**
   ```bash
   # Configure HTTPS certificates
   # Update nginx configuration
   ```

### Scaling Considerations

- **Horizontal Scaling**: Multiple API instances
- **Database Optimization**: Read replicas and caching
- **CDN Integration**: Static asset delivery
- **Load Balancing**: Traffic distribution

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is developed for Smart India Hackathon 2025. See the problem statement for detailed requirements.

## 🆘 Support

For technical support or questions:
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check the `/docs` directory
- **API Reference**: Available at `/docs` endpoint

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Core platform development
- ✅ Mobile app with offline sync
- ✅ Social media integration
- ✅ INCOIS integration

### Phase 2 (Future)
- 🔄 AI-powered risk prediction
- 🔄 Advanced analytics dashboard
- 🔄 Integration with more agencies
- 🔄 International expansion

---

**Data Dolphins** - Making ocean safety accessible to everyone! 🐬🌊