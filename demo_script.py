#!/usr/bin/env python3
"""
Data Dolphins Demo Script
Demonstrates the key features of the Ocean Hazard Monitoring Platform
"""

import requests
import json
import time
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:8000"
NLP_API_URL = "http://localhost:8001"

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🐬 {title}")
    print(f"{'='*60}")

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_api_endpoints():
    """Demonstrate the API endpoints"""
    print_header("DATA DOLPHINS API DEMONSTRATION")
    
    # Test health endpoints
    print_section("Health Check")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is healthy")
            print(f"   Response: {response.json()}")
        else:
            print("❌ Backend API is not responding")
    except Exception as e:
        print(f"❌ Backend API error: {e}")
    
    try:
        response = requests.get(f"{NLP_API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ NLP Service is healthy")
            print(f"   Response: {response.json()}")
        else:
            print("❌ NLP Service is not responding")
    except Exception as e:
        print(f"❌ NLP Service error: {e}")

def demo_user_registration():
    """Demonstrate user registration"""
    print_section("User Registration")
    
    user_data = {
        "username": "demo_user",
        "email": "demo@datadolphins.in",
        "password": "demo123456",
        "role": "citizen",
        "language": "en"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json=user_data)
        if response.status_code == 200:
            print("✅ User registration successful")
            print(f"   User ID: {response.json().get('id')}")
            return response.json()
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def demo_user_login():
    """Demonstrate user login"""
    print_section("User Login")
    
    login_data = {
        "email": "demo@datadolphins.in",
        "password": "demo123456"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ User login successful")
            token = response.json().get('access_token')
            print(f"   Token: {token[:20]}...")
            return token
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def demo_hazard_report(token):
    """Demonstrate hazard report submission"""
    print_section("Hazard Report Submission")
    
    if not token:
        print("❌ No authentication token available")
        return
    
    report_data = {
        "title": "High waves observed at Marina Beach",
        "description": "Unusually high waves hitting the shore with strong currents. Water levels rising rapidly.",
        "hazard_type": "high_waves",
        "severity": "high",
        "latitude": 13.0827,
        "longitude": 80.2707
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{API_BASE_URL}/reports", 
                                data=report_data, 
                                headers=headers)
        if response.status_code == 200:
            print("✅ Hazard report submitted successfully")
            print(f"   Report ID: {response.json().get('id')}")
            print(f"   Title: {response.json().get('title')}")
            print(f"   Severity: {response.json().get('severity')}")
        else:
            print(f"❌ Report submission failed: {response.text}")
    except Exception as e:
        print(f"❌ Report submission error: {e}")

def demo_nlp_analysis():
    """Demonstrate NLP text analysis"""
    print_section("NLP Text Analysis")
    
    text_samples = [
        "High waves observed at the beach. Very dangerous conditions.",
        "Tsunami warning issued for coastal areas. Evacuate immediately!",
        "Beautiful sunny day at the beach. Perfect for swimming.",
        "Storm surge expected. Water levels rising rapidly."
    ]
    
    for i, text in enumerate(text_samples, 1):
        print(f"\n   Sample {i}: '{text}'")
        
        try:
            response = requests.post(f"{NLP_API_URL}/analyze/text", 
                                   json={"text": text, "platform": "twitter"})
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Analysis complete:")
                print(f"      Hazard Probability: {data.get('hazard_probability', 0):.2f}")
                print(f"      Sentiment Score: {data.get('sentiment_score', 0):.2f}")
                print(f"      Hazard Keywords: {data.get('hazard_keywords', [])}")
                print(f"      Is Hazard Related: {data.get('is_hazard_related', False)}")
            else:
                print(f"   ❌ Analysis failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Analysis error: {e}")

def demo_dashboard_stats():
    """Demonstrate dashboard statistics"""
    print_section("Dashboard Statistics")
    
    try:
        response = requests.get(f"{API_BASE_URL}/stats/dashboard")
        if response.status_code == 200:
            print("✅ Dashboard statistics retrieved")
            stats = response.json()
            print(f"   Total Reports: {len(stats.get('reports_by_type', []))}")
            print(f"   Active Hotspots: {stats.get('active_hotspots', 0)}")
            print(f"   Social Media Activity: {len(stats.get('social_media_activity', []))}")
            print(f"   Timestamp: {stats.get('timestamp', 'N/A')}")
        else:
            print(f"❌ Statistics retrieval failed: {response.text}")
    except Exception as e:
        print(f"❌ Statistics error: {e}")

def demo_social_media_processing():
    """Demonstrate social media processing"""
    print_section("Social Media Processing")
    
    try:
        response = requests.get(f"{API_BASE_URL}/social-media?limit=5")
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ Retrieved {len(posts)} social media posts")
            for i, post in enumerate(posts[:3], 1):
                print(f"   Post {i}:")
                print(f"      Platform: {post.get('platform', 'N/A')}")
                print(f"      Content: {post.get('content', 'N/A')[:50]}...")
                print(f"      Hazard Probability: {post.get('hazard_probability', 0):.2f}")
                print(f"      Sentiment: {post.get('sentiment_score', 0):.2f}")
        else:
            print(f"❌ Social media retrieval failed: {response.text}")
    except Exception as e:
        print(f"❌ Social media error: {e}")

def demo_hotspots():
    """Demonstrate hotspot generation"""
    print_section("Hotspot Analysis")
    
    try:
        response = requests.get(f"{API_BASE_URL}/hotspots")
        if response.status_code == 200:
            hotspots = response.json()
            print(f"✅ Retrieved {len(hotspots)} hotspots")
            for i, hotspot in enumerate(hotspots[:3], 1):
                print(f"   Hotspot {i}:")
                print(f"      Location: ({hotspot.get('latitude', 0):.4f}, {hotspot.get('longitude', 0):.4f})")
                print(f"      Report Count: {hotspot.get('report_count', 0)}")
                print(f"      Severity: {hotspot.get('severity_level', 'N/A')}")
                print(f"      Hazard Types: {hotspot.get('hazard_types', [])}")
        else:
            print(f"❌ Hotspot retrieval failed: {response.text}")
    except Exception as e:
        print(f"❌ Hotspot error: {e}")

def demo_alerts():
    """Demonstrate alert system"""
    print_section("Alert System")
    
    try:
        response = requests.get(f"{API_BASE_URL}/alerts")
        if response.status_code == 200:
            alerts = response.json()
            print(f"✅ Retrieved {len(alerts)} active alerts")
            for i, alert in enumerate(alerts[:3], 1):
                print(f"   Alert {i}:")
                print(f"      Type: {alert.get('alert_type', 'N/A')}")
                print(f"      Title: {alert.get('title', 'N/A')}")
                print(f"      Severity: {alert.get('severity', 'N/A')}")
                print(f"      Source: {alert.get('source', 'N/A')}")
        else:
            print(f"❌ Alert retrieval failed: {response.text}")
    except Exception as e:
        print(f"❌ Alert error: {e}")

def main():
    """Main demonstration function"""
    print_header("DATA DOLPHINS - OCEAN HAZARD MONITORING PLATFORM")
    print("🐬 Smart India Hackathon 2025 - Working Prototype Demo")
    print("🌊 Real-time Ocean Hazard Monitoring with AI & Social Media Analytics")
    
    # Test API endpoints
    demo_api_endpoints()
    
    # User authentication flow
    print_section("User Authentication Flow")
    user = demo_user_registration()
    token = demo_user_login()
    
    # Hazard reporting
    demo_hazard_report(token)
    
    # NLP analysis
    demo_nlp_analysis()
    
    # Dashboard features
    demo_dashboard_stats()
    demo_social_media_processing()
    demo_hotspots()
    demo_alerts()
    
    print_header("DEMO COMPLETED")
    print("🎉 Data Dolphins Platform Demo Successfully Completed!")
    print("\n📱 Platform Features Demonstrated:")
    print("   ✅ User Registration & Authentication")
    print("   ✅ Hazard Report Submission")
    print("   ✅ NLP Text Analysis & Sentiment Detection")
    print("   ✅ Social Media Processing")
    print("   ✅ Hotspot Generation & Analysis")
    print("   ✅ Alert System & Notifications")
    print("   ✅ Dashboard Statistics & Analytics")
    
    print("\n🌐 Access Points:")
    print("   • Web Dashboard: http://localhost:3000")
    print("   • Backend API: http://localhost:8000")
    print("   • API Documentation: http://localhost:8000/docs")
    print("   • NLP Service: http://localhost:8001")
    
    print("\n📱 Mobile App:")
    print("   • React Native app with offline sync")
    print("   • GPS location services")
    print("   • Media capture and upload")
    print("   • Push notifications")
    
    print("\n🚨 Key Capabilities:")
    print("   • Real-time hazard monitoring")
    print("   • Social media sentiment analysis")
    print("   • INCOIS early warning integration")
    print("   • Multi-channel alert delivery")
    print("   • Offline mobile reporting")
    print("   • Role-based access control")
    
    print("\n🐬 Data Dolphins - Making Ocean Safety Accessible to Everyone! 🌊")

if __name__ == "__main__":
    main()