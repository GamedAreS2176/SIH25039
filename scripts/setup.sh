#!/bin/bash

# Data Dolphins Setup Script
# This script sets up the development environment for the Ocean Hazard Monitoring Platform

echo "🐬 Setting up Data Dolphins - Ocean Hazard Monitoring Platform"
echo "=============================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads
mkdir -p logs
mkdir -p data/postgres

# Set permissions
chmod 755 uploads
chmod 755 logs
chmod 755 data

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your API keys and configuration"
fi

# Build and start services
echo "🔨 Building Docker containers..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."

# Check PostgreSQL
if docker-compose exec postgres pg_isready -U postgres; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL is not running"
fi

# Check Redis
if docker-compose exec redis redis-cli ping; then
    echo "✅ Redis is running"
else
    echo "❌ Redis is not running"
fi

# Check Backend API
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is running"
else
    echo "❌ Backend API is not responding"
fi

# Check Frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend is not responding"
fi

# Check NLP Service
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ NLP Service is running"
else
    echo "❌ NLP Service is not responding"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📱 Access the application:"
echo "   • Web Dashboard: http://localhost:3000"
echo "   • Backend API: http://localhost:8000"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • NLP Service: http://localhost:8001"
echo ""
echo "📱 Mobile App:"
echo "   • Run 'cd mobile && npm install' to install dependencies"
echo "   • Run 'cd mobile && npm start' to start the mobile app"
echo ""
echo "🔧 Useful commands:"
echo "   • View logs: docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Restart services: docker-compose restart"
echo "   • Update services: docker-compose pull && docker-compose up -d"
echo ""
echo "⚠️  Remember to:"
echo "   1. Update the .env file with your API keys"
echo "   2. Configure social media API credentials"
echo "   3. Set up INCOIS integration credentials"
echo "   4. Configure notification services"