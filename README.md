Ocean Hazard Reporting Platform - SIH 2025
Problem Statement ID: 25039
Team: Data Dolphins
Theme: Disaster Management

📋 Project Description
An integrated mobile and web platform that combines crowdsourced ocean hazard reporting with social media analytics to create a real-time, dynamic situational awareness dashboard. The system enables citizens to report ocean hazards while providing authorities with comprehensive risk intelligence through multi-source data fusion.

Key Features
Citizen Hazard Reporting: Geotagged reports with photos/videos and timestamp validation
Social Media Monitoring: NLP-powered hazard detection and sentiment analysis
Dynamic Hotspot Detection: Real-time hazard intensity mapping using H3 spatial indexing
Role-Based Access: Differentiated access for citizens, officials, and analysts
Offline-First Architecture: Offline reporting with auto-sync capabilities
Multilingual Support: Regional language support with voice reporting options
INCOIS Integration: Seamless integration with existing warning systems
🛠️ Tech Stack
Frontend
Web: React with Leaflet/OpenLayers for mapping
Mobile: React Native
UI Components: Material-UI/Native Base
Backend
API Server: Node.js with Express
ML Pipeline: FastAPI (Python)
Database: PostgreSQL with PostGIS extension
Spatial Indexing: H3 Spatial Indexing
Services & Tools
Cloud Platform: Google Cloud Platform
Authentication: Firebase Auth
Storage: Firebase Storage
Real-time Updates: Firebase Realtime Database
NLP Processing: spaCy
Mapping: Leaflet, OpenLayers
Containerization: Docker
🔧 Setup Instructions
Prerequisites
Node.js (v16 or higher)
Python 3.8+
PostgreSQL with PostGIS
Firebase project
Google Cloud Platform account
Firebase Configuration
Create a Firebase project at Firebase Console
Enable Authentication, Firestore, and Storage services
Generate Firebase config object
Create a .env file in the root directory:
env
# Firebase Config
REACT_APP_FIREBASE_API_KEY=your_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
REACT_APP_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
REACT_APP_FIREBASE_APP_ID=your_app_id

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/ocean_hazards
POSTGIS_VERSION=3.2

# API Keys
SOCIAL_MEDIA_API_KEY=your_social_media_api_key
INCOIS_API_ENDPOINT=your_incois_endpoint

# Server Config
NODE_ENV=development
PORT=3000
API_PORT=5000
ML_API_PORT=8000
Installation & Setup
Clone the repository
bash
git clone https://github.com/GamedAreS2176/SIH25039.git
cd SIH25039
Install dependencies
bash
# Install root dependencies
npm install

# Install web app dependencies
cd web-app
npm install

# Install mobile app dependencies  
cd ../mobile-app
npm install

# Install backend dependencies
cd ../backend
npm install

# Install ML pipeline dependencies
cd ../ml-pipeline
pip install -r requirements.txt
Database Setup
bash
# Create PostgreSQL database with PostGIS
createdb ocean_hazards
psql -d ocean_hazards -c "CREATE EXTENSION postgis;"

# Run database migrations
cd backend
npm run migrate
Configure Firebase
bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase in your project
firebase init
🚀 Running the Application
Development Mode
Start all services concurrently:

bash
npm run dev:all
Or start services individually:

bash
# Start web application (Port: 3000)
npm run dev:web

# Start mobile application
npm run dev:mobile

# Start backend API server (Port: 5000)
npm run dev:backend

# Start ML pipeline (Port: 8000)
npm run dev:ml

# Start database
npm run db:start
Production Build
bash
# Build web application
npm run build:web

# Build mobile application
npm run build:mobile

# Build and deploy
npm run deploy
📱 Mobile App Development
bash
cd mobile-app

# For iOS
npx react-native run-ios

# For Android
npx react-native run-android

# Build APK
cd android && ./gradlew assembleRelease
🧪 Testing
bash
# Run all tests
npm run test

# Run specific test suites
npm run test:web
npm run test:mobile
npm run test:backend
npm run test:ml
🐳 Docker Setup
bash
# Build and run with Docker Compose
docker-compose up --build

# Run in production mode
docker-compose -f docker-compose.prod.yml up
📊 API Documentation
Backend API: http://localhost:5000/api/docs
ML Pipeline API: http://localhost:8000/docs
🔒 Authentication
The platform uses Firebase Authentication with role-based access:

Citizens: Report hazards and view public information
Officials: Verify reports and manage alerts
Analysts: Access analytics and trend data
📈 Monitoring & Analytics
Real-time dashboard at http://localhost:3000/dashboard
API metrics at http://localhost:5000/metrics
ML model performance at http://localhost:8000/metrics
🌍 Multilingual Support
The platform supports multiple regional languages:

Hindi, Tamil, Telugu, Bengali, Marathi
Voice-to-text reporting
Text-to-speech alerts
🤝 Contributing
Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit changes (git commit -m 'Add amazing feature')
Push to branch (git push origin feature/amazing-feature)
Open a Pull Request
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🏆 Smart India Hackathon 2025
This project is developed for Smart India Hackathon 2025 under the Disaster Management theme, addressing Problem Statement 25039 for creating an integrated platform for crowdsourced ocean hazard reporting and social media analytics.

📞 Support
For support and queries, please contact the Data Dolphins team or create an issue in the repository.

