# 🐬 Data Dolphins - Working Prototype Demonstration

## 🌊 Ocean Hazard Monitoring Platform
**Smart India Hackathon 2025 - Complete Working Solution**

---

## 🎯 **Platform Overview**

Data Dolphins is a comprehensive ocean hazard monitoring platform that integrates:
- **Crowdsourced Citizen Reports** (Mobile & Web)
- **Social Media Analytics** (AI-powered NLP)
- **INCOIS Early Warning Integration**
- **Real-time Dashboard & Alerts**
- **Offline Mobile Capabilities**

---

## 🏗️ **Architecture Components**

### 1. **Backend Services** (FastAPI + Python)
```
📁 backend/
├── main.py              # Core API endpoints
├── models.py            # Database models
├── auth.py              # Authentication system
├── incois_integration.py # INCOIS early warning
├── alert_service.py     # Alert management
└── utils.py            # Utility functions
```

**Key Features:**
- ✅ RESTful API with comprehensive endpoints
- ✅ JWT Authentication & Role-based access
- ✅ PostgreSQL + PostGIS for spatial data
- ✅ Redis for real-time caching
- ✅ File upload handling for media
- ✅ INCOIS integration for early warnings

### 2. **Web Dashboard** (React + Leaflet)
```
📁 frontend/
├── src/
│   ├── pages/
│   │   ├── Dashboard.js      # Interactive map dashboard
│   │   ├── Login.js          # User authentication
│   │   ├── ReportForm.js     # Hazard reporting
│   │   └── ReportsList.js    # Report management
│   ├── components/
│   │   └── Navbar.js         # Navigation
│   └── services/
│       └── api.js            # API integration
```

**Key Features:**
- ✅ Interactive maps with real-time markers
- ✅ Dynamic hotspot visualization
- ✅ Statistical charts and analytics
- ✅ Real-time data updates
- ✅ Responsive design for all devices

### 3. **Mobile App** (React Native + Expo)
```
📁 mobile/
├── src/
│   ├── screens/
│   │   ├── DashboardScreen.js    # Mobile dashboard
│   │   ├── LoginScreen.js        # Mobile auth
│   │   └── ReportScreen.js       # Mobile reporting
│   ├── contexts/
│   │   ├── AuthContext.js        # Authentication
│   │   └── OfflineContext.js     # Offline sync
│   └── services/
│       └── syncService.js        # Background sync
```

**Key Features:**
- ✅ Offline reporting capabilities
- ✅ GPS location services
- ✅ Media capture (photos/videos)
- ✅ Automatic background sync
- ✅ Push notifications
- ✅ Cross-platform (iOS/Android)

### 4. **NLP Engine** (Python + spaCy)
```
📁 nlp-engine/
├── main.py              # NLP API service
├── processors.py        # Text processing
├── collectors.py        # Social media APIs
└── schemas.py          # Data models
```

**Key Features:**
- ✅ Social media data collection
- ✅ Hazard detection algorithms
- ✅ Sentiment analysis
- ✅ Real-time text processing
- ✅ Multi-platform integration

---

## 🚀 **Live Demo Features**

### 1. **User Authentication System**
```python
# Registration
POST /auth/register
{
  "username": "citizen_user",
  "email": "user@datadolphins.in",
  "password": "secure123",
  "role": "citizen",
  "language": "en"
}

# Login
POST /auth/login
{
  "email": "user@datadolphins.in",
  "password": "secure123"
}
```

### 2. **Hazard Report Submission**
```python
# Mobile/Web Report
POST /reports
{
  "title": "High waves at Marina Beach",
  "description": "Dangerous wave conditions observed",
  "hazard_type": "high_waves",
  "severity": "high",
  "latitude": 13.0827,
  "longitude": 80.2707,
  "media_file": "wave_photo.jpg"
}
```

### 3. **NLP Text Analysis**
```python
# Social Media Analysis
POST /analyze/text
{
  "text": "Tsunami warning issued! Evacuate coastal areas immediately!",
  "platform": "twitter"
}

# Response
{
  "hazard_probability": 0.95,
  "sentiment_score": -0.8,
  "hazard_keywords": ["tsunami", "warning", "evacuate"],
  "is_hazard_related": true
}
```

### 4. **Real-time Dashboard**
```python
# Dashboard Statistics
GET /stats/dashboard
{
  "reports_by_type": [
    {"hazard_type": "high_waves", "count": 15, "severity": "high"},
    {"hazard_type": "flooding", "count": 8, "severity": "critical"}
  ],
  "social_media_activity": [
    {"platform": "twitter", "count": 45},
    {"platform": "facebook", "count": 23}
  ],
  "active_hotspots": 3
}
```

---

## 📱 **Mobile App Features**

### Offline Capabilities
- **📱 Report Submission**: Works without internet
- **🔄 Auto Sync**: Syncs when connection restored
- **💾 Local Storage**: SQLite database for offline data
- **📸 Media Capture**: Photos/videos with compression

### User Experience
- **🎯 GPS Location**: Automatic location detection
- **📊 Dashboard**: Real-time statistics
- **🔔 Notifications**: Push alerts for hazards
- **🌐 Multilingual**: Regional language support

---

## 🗺️ **Interactive Dashboard**

### Map Visualization
- **📍 Real-time Markers**: Hazard report locations
- **🔥 Hotspot Clusters**: Dynamic danger zones
- **🎨 Color Coding**: Severity levels
- **🔍 Filtering**: By type, date, severity

### Analytics Dashboard
- **📈 Charts**: Report trends and statistics
- **📊 Social Media**: Sentiment analysis
- **⚠️ Alerts**: Active warnings
- **👥 Users**: Role-based access

---

## 🤖 **AI-Powered Features**

### Social Media Processing
```python
# Automated hazard detection
hazard_keywords = {
    'tsunami': ['tsunami', 'tidal wave', 'seismic wave'],
    'storm_surge': ['storm surge', 'coastal flooding'],
    'high_waves': ['high waves', 'rough seas', 'dangerous waves'],
    'flooding': ['flood', 'inundation', 'rising water']
}

# Sentiment analysis
sentiment_score = analyze_sentiment(text)  # -1 to 1
hazard_probability = calculate_hazard_risk(text, keywords)
```

### Risk Assessment
- **🎯 Pattern Recognition**: Identifies hazard patterns
- **📊 Trend Analysis**: Monitors social media trends
- **⚠️ Early Warning**: Proactive alert generation
- **🔍 Verification**: Cross-references multiple sources

---

## 🚨 **Alert System**

### Multi-Channel Notifications
```python
# Alert Generation
alert = {
    "alert_type": "tsunami",
    "title": "Tsunami Warning",
    "message": "Evacuate coastal areas immediately",
    "severity": "critical",
    "affected_area": "coastal_zone_polygon",
    "channels": ["email", "sms", "push", "web"]
}
```

### INCOIS Integration
- **🌊 Official Warnings**: Direct INCOIS data feed
- **⚡ Real-time Updates**: Automatic alert distribution
- **📍 Geographic Targeting**: Location-based notifications
- **🔄 Verification**: Cross-validation with reports

---

## 🗄️ **Database Schema**

### Core Tables
```sql
-- Users with role-based access
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    role VARCHAR(20), -- citizen, analyst, official
    language VARCHAR(10)
);

-- Hazard reports with spatial data
CREATE TABLE hazard_reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(200),
    description TEXT,
    hazard_type VARCHAR(50),
    severity VARCHAR(20),
    location GEOMETRY(POINT, 4326),
    h3_index VARCHAR(20), -- Spatial clustering
    media_urls TEXT[],
    is_verified BOOLEAN DEFAULT FALSE
);

-- Social media posts with NLP analysis
CREATE TABLE social_media_posts (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(20),
    content TEXT,
    hazard_keywords TEXT[],
    sentiment_score FLOAT,
    hazard_probability FLOAT,
    location GEOMETRY(POINT, 4326)
);

-- Dynamic hotspots
CREATE TABLE hotspots (
    id SERIAL PRIMARY KEY,
    center_location GEOMETRY(POINT, 4326),
    radius_meters INTEGER,
    report_count INTEGER,
    severity_level VARCHAR(20),
    hazard_types TEXT[]
);
```

---

## 🔧 **Technical Implementation**

### API Endpoints
```python
# Core API Routes
GET  /                    # API status
GET  /health             # Health check
POST /auth/register      # User registration
POST /auth/login         # User login
GET  /reports            # List hazard reports
POST /reports            # Submit hazard report
GET  /hotspots           # Get active hotspots
GET  /alerts             # Get active alerts
GET  /stats/dashboard     # Dashboard statistics
POST /analyze/text        # NLP text analysis
```

### Real-time Features
```python
# Redis Pub/Sub for real-time updates
redis_client.publish("new_report", json.dumps({
    "id": report.id,
    "title": report.title,
    "hazard_type": report.hazard_type,
    "severity": report.severity,
    "latitude": latitude,
    "longitude": longitude
}))
```

---

## 🚀 **Deployment Ready**

### Docker Configuration
```yaml
# docker-compose.yml
services:
  postgres:     # PostgreSQL + PostGIS
  redis:        # Redis cache
  backend:      # FastAPI service
  frontend:     # React dashboard
  nlp-service: # NLP processing
```

### Environment Setup
```bash
# Quick start
./scripts/setup.sh      # Setup environment
./scripts/test.sh       # Run tests
docker-compose up -d    # Start services
```

### Access Points
- **🌐 Web Dashboard**: http://localhost:3000
- **🔧 Backend API**: http://localhost:8000
- **📚 API Docs**: http://localhost:8000/docs
- **🤖 NLP Service**: http://localhost:8001
- **📱 Mobile App**: React Native with Expo

---

## 🎯 **Key Achievements**

### ✅ **Problem Statement Requirements Met**
- **Citizen Reporting**: ✅ Mobile/web apps with geotagged reports
- **Social Media Integration**: ✅ Real-time monitoring and NLP
- **Interactive Dashboard**: ✅ Dynamic maps with hotspots
- **INCOIS Integration**: ✅ Early warning system connectivity
- **Multilingual Support**: ✅ Framework for regional languages
- **Offline Sync**: ✅ Mobile app works in remote areas
- **Role-based Access**: ✅ Different interfaces for users
- **Real-time Updates**: ✅ Live data streaming

### 🏆 **Innovation Highlights**
- **🤖 AI-Powered**: Advanced NLP for hazard detection
- **📱 Offline-First**: Mobile app works without internet
- **🌊 Spatial Intelligence**: H3 indexing for efficient clustering
- **⚡ Real-time**: Live updates across all platforms
- **🔔 Smart Alerts**: Multi-channel notification system
- **📊 Analytics**: Comprehensive dashboard and reporting

---

## 🐬 **Data Dolphins - Making Ocean Safety Accessible to Everyone!**

**🌊 Smart India Hackathon 2025 - Complete Working Solution**

*Real-time Ocean Hazard Monitoring with AI & Social Media Analytics*