"""
INCOIS Integration Module
Handles integration with Indian National Centre for Ocean Information Services
for early warning systems and alert mechanisms
"""

import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
import os
from dotenv import load_dotenv

from database import get_db
from models import Alert, User, HazardReport
from schemas import AlertResponse

load_dotenv()

class INCOISIntegration:
    def __init__(self):
        self.base_url = os.getenv('INCOIS_BASE_URL', 'https://www.incois.gov.in')
        self.api_key = os.getenv('INCOIS_API_KEY')
        self.alert_endpoints = {
            'tsunami': '/api/tsunami-alerts',
            'storm_surge': '/api/storm-surge-alerts',
            'high_waves': '/api/wave-alerts',
            'coastal_current': '/api/current-alerts'
        }
    
    async def fetch_incois_alerts(self) -> List[Dict[str, Any]]:
        """Fetch alerts from INCOIS API"""
        alerts = []
        
        try:
            async with httpx.AsyncClient() as client:
                for alert_type, endpoint in self.alert_endpoints.items():
                    try:
                        response = await client.get(
                            f"{self.base_url}{endpoint}",
                            headers={'Authorization': f'Bearer {self.api_key}'} if self.api_key else {},
                            timeout=30.0
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            alerts.extend(self._process_incois_data(data, alert_type))
                    
                    except Exception as e:
                        print(f"Error fetching {alert_type} alerts: {e}")
                        continue
            
            return alerts
            
        except Exception as e:
            print(f"Error in INCOIS integration: {e}")
            return []
    
    def _process_incois_data(self, data: Dict[str, Any], alert_type: str) -> List[Dict[str, Any]]:
        """Process INCOIS API response data"""
        alerts = []
        
        # This is a simplified processing - actual implementation would depend on INCOIS API structure
        if 'alerts' in data:
            for alert_data in data['alerts']:
                processed_alert = {
                    'alert_type': alert_type,
                    'title': alert_data.get('title', f'{alert_type.title()} Alert'),
                    'message': alert_data.get('description', ''),
                    'severity': self._map_severity(alert_data.get('severity', 'medium')),
                    'source': 'incois',
                    'affected_area': self._create_affected_area(alert_data.get('coordinates', [])),
                    'created_at': datetime.utcnow(),
                    'expires_at': self._calculate_expiry(alert_data.get('duration', 24))
                }
                alerts.append(processed_alert)
        
        return alerts
    
    def _map_severity(self, incois_severity: str) -> str:
        """Map INCOIS severity levels to our system"""
        severity_mapping = {
            'low': 'low',
            'moderate': 'medium',
            'high': 'high',
            'severe': 'critical',
            'extreme': 'critical'
        }
        return severity_mapping.get(incois_severity.lower(), 'medium')
    
    def _create_affected_area(self, coordinates: List[List[float]]) -> Optional[str]:
        """Create PostGIS polygon from coordinates"""
        if not coordinates or len(coordinates) < 3:
            return None
        
        # Create a simple polygon from coordinates
        coord_pairs = [f"{lon} {lat}" for lat, lon in coordinates]
        polygon_wkt = f"POLYGON(({', '.join(coord_pairs)}))"
        return polygon_wkt
    
    def _calculate_expiry(self, duration_hours: int) -> datetime:
        """Calculate alert expiry time"""
        return datetime.utcnow() + timedelta(hours=duration_hours)
    
    async def store_alerts(self, alerts: List[Dict[str, Any]], db: Session):
        """Store INCOIS alerts in database"""
        for alert_data in alerts:
            try:
                # Check if alert already exists
                existing_alert = db.query(Alert).filter(
                    Alert.alert_type == alert_data['alert_type'],
                    Alert.title == alert_data['title'],
                    Alert.source == 'incois'
                ).first()
                
                if not existing_alert:
                    alert = Alert(
                        alert_type=alert_data['alert_type'],
                        title=alert_data['title'],
                        message=alert_data['message'],
                        severity=alert_data['severity'],
                        source=alert_data['source'],
                        affected_area=alert_data.get('affected_area'),
                        is_active=True,
                        created_at=alert_data['created_at'],
                        expires_at=alert_data['expires_at']
                    )
                    
                    db.add(alert)
                    db.commit()
                    
                    # Notify users in affected areas
                    await self._notify_affected_users(alert, db)
            
            except Exception as e:
                print(f"Error storing alert: {e}")
                db.rollback()
    
    async def _notify_affected_users(self, alert: Alert, db: Session):
        """Notify users in affected areas about the alert"""
        try:
            # Get users within affected area (simplified - would use PostGIS spatial queries)
            users = db.query(User).all()  # In real implementation, filter by location
            
            for user in users:
                # Create user alert record
                user_alert = UserAlert(
                    user_id=user.id,
                    alert_id=alert.id,
                    is_read=False
                )
                db.add(user_alert)
            
            db.commit()
            
            # Send push notifications (would integrate with FCM/APNS)
            await self._send_push_notifications(alert, users)
            
        except Exception as e:
            print(f"Error notifying users: {e}")
    
    async def _send_push_notifications(self, alert: Alert, users: List[User]):
        """Send push notifications to users"""
        # This would integrate with Firebase Cloud Messaging or Apple Push Notifications
        # For now, just log the notification
        print(f"Sending alert notification to {len(users)} users: {alert.title}")
    
    async def sync_with_incois(self):
        """Main sync function to fetch and store INCOIS alerts"""
        try:
            db = next(get_db())
            
            # Fetch alerts from INCOIS
            alerts = await self.fetch_incois_alerts()
            
            if alerts:
                # Store alerts in database
                await self.store_alerts(alerts, db)
                print(f"Synced {len(alerts)} alerts from INCOIS")
            else:
                print("No new alerts from INCOIS")
            
        except Exception as e:
            print(f"Error in INCOIS sync: {e}")
        finally:
            db.close()

class AlertProcessor:
    """Process and analyze alerts for risk assessment"""
    
    def __init__(self):
        self.risk_thresholds = {
            'low': 0.3,
            'medium': 0.5,
            'high': 0.7,
            'critical': 0.9
        }
    
    def analyze_alert_risk(self, alert: Alert, recent_reports: List[HazardReport]) -> float:
        """Analyze risk level based on alert and recent reports"""
        base_risk = self.risk_thresholds.get(alert.severity, 0.5)
        
        # Increase risk if there are recent verified reports of the same type
        matching_reports = [
            r for r in recent_reports 
            if r.hazard_type == alert.alert_type and r.is_verified
        ]
        
        if matching_reports:
            base_risk += 0.2
        
        return min(base_risk, 1.0)
    
    def generate_alert_summary(self, alerts: List[Alert]) -> Dict[str, Any]:
        """Generate summary of active alerts"""
        if not alerts:
            return {"total_alerts": 0, "by_severity": {}, "by_type": {}}
        
        by_severity = {}
        by_type = {}
        
        for alert in alerts:
            by_severity[alert.severity] = by_severity.get(alert.severity, 0) + 1
            by_type[alert.alert_type] = by_type.get(alert.alert_type, 0) + 1
        
        return {
            "total_alerts": len(alerts),
            "by_severity": by_severity,
            "by_type": by_type,
            "most_common_type": max(by_type.items(), key=lambda x: x[1])[0] if by_type else None,
            "highest_severity": max(by_severity.keys(), key=lambda x: ['low', 'medium', 'high', 'critical'].index(x)) if by_severity else None
        }

# Background task for periodic INCOIS sync
async def periodic_incois_sync():
    """Periodic task to sync with INCOIS (run every 15 minutes)"""
    integration = INCOISIntegration()
    
    while True:
        try:
            await integration.sync_with_incois()
            await asyncio.sleep(900)  # 15 minutes
        except Exception as e:
            print(f"Error in periodic INCOIS sync: {e}")
            await asyncio.sleep(300)  # 5 minutes on error

# API endpoints for INCOIS integration
async def get_incois_alerts(db: Session = Depends(get_db)) -> List[AlertResponse]:
    """Get active INCOIS alerts"""
    alerts = db.query(Alert).filter(
        Alert.source == 'incois',
        Alert.is_active == True,
        Alert.expires_at > datetime.utcnow()
    ).all()
    
    return [AlertResponse.from_orm(alert) for alert in alerts]

async def trigger_incois_sync():
    """Manually trigger INCOIS sync"""
    integration = INCOISIntegration()
    await integration.sync_with_incois()
    return {"message": "INCOIS sync triggered"}

async def get_alert_summary(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get alert summary statistics"""
    processor = AlertProcessor()
    
    active_alerts = db.query(Alert).filter(
        Alert.is_active == True,
        Alert.expires_at > datetime.utcnow()
    ).all()
    
    recent_reports = db.query(HazardReport).filter(
        HazardReport.created_at >= datetime.utcnow() - timedelta(hours=24)
    ).all()
    
    summary = processor.generate_alert_summary(active_alerts)
    
    # Add risk analysis
    if active_alerts:
        avg_risk = sum(
            processor.analyze_alert_risk(alert, recent_reports) 
            for alert in active_alerts
        ) / len(active_alerts)
        summary["average_risk_score"] = avg_risk
    
    return summary