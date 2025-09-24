"""
Alert Service for Data Dolphins
Handles alert generation, distribution, and management
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
import redis
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from database import get_db
from models import Alert, User, HazardReport, UserAlert
from schemas import AlertResponse

class AlertService:
    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
        
        # Notification service credentials
        self.twilio_client = None  # Initialize with credentials
        self.smtp_server = None   # Initialize with SMTP settings
        
        # Alert templates
        self.alert_templates = {
            'tsunami': {
                'title': 'Tsunami Alert',
                'message': 'A tsunami alert has been issued for your area. Please move to higher ground immediately.',
                'priority': 'critical'
            },
            'storm_surge': {
                'title': 'Storm Surge Warning',
                'message': 'Storm surge conditions are expected. Avoid coastal areas and follow evacuation orders.',
                'priority': 'high'
            },
            'high_waves': {
                'title': 'High Wave Warning',
                'message': 'Dangerous wave conditions are expected. Stay away from beaches and coastal areas.',
                'priority': 'medium'
            },
            'flooding': {
                'title': 'Coastal Flooding Alert',
                'message': 'Coastal flooding is expected. Avoid low-lying areas and follow local authorities.',
                'priority': 'high'
            }
        }
    
    async def create_alert(self, alert_type: str, title: str, message: str, 
                          severity: str, affected_area: Optional[str] = None,
                          source: str = 'system') -> Alert:
        """Create a new alert"""
        db = next(get_db())
        
        try:
            alert = Alert(
                alert_type=alert_type,
                title=title,
                message=message,
                severity=severity,
                source=source,
                affected_area=affected_area,
                is_active=True,
                created_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            
            db.add(alert)
            db.commit()
            db.refresh(alert)
            
            # Notify users
            await self._notify_users(alert, db)
            
            # Publish to Redis for real-time updates
            await self._publish_alert(alert)
            
            return alert
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    async def _notify_users(self, alert: Alert, db: Session):
        """Notify users about the alert"""
        try:
            # Get users in affected area (simplified - would use spatial queries)
            users = db.query(User).all()
            
            for user in users:
                # Create user alert record
                user_alert = UserAlert(
                    user_id=user.id,
                    alert_id=alert.id,
                    is_read=False
                )
                db.add(user_alert)
            
            db.commit()
            
            # Send notifications
            await self._send_notifications(alert, users)
            
        except Exception as e:
            print(f"Error notifying users: {e}")
    
    async def _send_notifications(self, alert: Alert, users: List[User]):
        """Send notifications via multiple channels"""
        for user in users:
            try:
                # Email notification
                await self._send_email_notification(user, alert)
                
                # SMS notification (if phone number available)
                if hasattr(user, 'phone_number') and user.phone_number:
                    await self._send_sms_notification(user, alert)
                
                # Push notification
                await self._send_push_notification(user, alert)
                
            except Exception as e:
                print(f"Error sending notification to user {user.id}: {e}")
    
    async def _send_email_notification(self, user: User, alert: Alert):
        """Send email notification"""
        try:
            # This would integrate with an email service like SendGrid, AWS SES, etc.
            print(f"Sending email alert to {user.email}: {alert.title}")
            
            # Placeholder for actual email sending
            # email_service.send_email(
            #     to=user.email,
            #     subject=f"Alert: {alert.title}",
            #     body=alert.message
            # )
            
        except Exception as e:
            print(f"Error sending email to {user.email}: {e}")
    
    async def _send_sms_notification(self, user: User, alert: Alert):
        """Send SMS notification"""
        try:
            # This would integrate with Twilio, AWS SNS, etc.
            print(f"Sending SMS alert to {user.phone_number}: {alert.title}")
            
            # Placeholder for actual SMS sending
            # sms_service.send_sms(
            #     to=user.phone_number,
            #     message=f"ALERT: {alert.title} - {alert.message}"
            # )
            
        except Exception as e:
            print(f"Error sending SMS to {user.phone_number}: {e}")
    
    async def _send_push_notification(self, user: User, alert: Alert):
        """Send push notification"""
        try:
            # This would integrate with Firebase Cloud Messaging
            print(f"Sending push notification to user {user.id}: {alert.title}")
            
            # Placeholder for actual push notification
            # push_service.send_notification(
            #     user_id=user.id,
            #     title=alert.title,
            #     body=alert.message,
            #     data={'alert_id': alert.id, 'alert_type': alert.alert_type}
            # )
            
        except Exception as e:
            print(f"Error sending push notification to user {user.id}: {e}")
    
    async def _publish_alert(self, alert: Alert):
        """Publish alert to Redis for real-time updates"""
        try:
            alert_data = {
                'id': alert.id,
                'alert_type': alert.alert_type,
                'title': alert.title,
                'message': alert.message,
                'severity': alert.severity,
                'source': alert.source,
                'created_at': alert.created_at.isoformat(),
                'expires_at': alert.expires_at.isoformat() if alert.expires_at else None
            }
            
            self.redis_client.publish('new_alert', json.dumps(alert_data))
            
        except Exception as e:
            print(f"Error publishing alert to Redis: {e}")
    
    async def get_user_alerts(self, user_id: int, unread_only: bool = False) -> List[AlertResponse]:
        """Get alerts for a specific user"""
        db = next(get_db())
        
        try:
            query = db.query(Alert).join(UserAlert).filter(
                UserAlert.user_id == user_id,
                Alert.is_active == True,
                Alert.expires_at > datetime.utcnow()
            )
            
            if unread_only:
                query = query.filter(UserAlert.is_read == False)
            
            alerts = query.order_by(Alert.created_at.desc()).all()
            return [AlertResponse.from_orm(alert) for alert in alerts]
            
        except Exception as e:
            print(f"Error getting user alerts: {e}")
            return []
        finally:
            db.close()
    
    async def mark_alert_read(self, user_id: int, alert_id: int):
        """Mark an alert as read for a user"""
        db = next(get_db())
        
        try:
            user_alert = db.query(UserAlert).filter(
                UserAlert.user_id == user_id,
                UserAlert.alert_id == alert_id
            ).first()
            
            if user_alert:
                user_alert.is_read = True
                db.commit()
            
        except Exception as e:
            print(f"Error marking alert as read: {e}")
            db.rollback()
        finally:
            db.close()
    
    async def generate_alert_from_report(self, report: HazardReport) -> Optional[Alert]:
        """Generate an alert based on a hazard report"""
        try:
            # Check if report severity warrants an alert
            if report.severity not in ['high', 'critical']:
                return None
            
            # Check if similar alert already exists
            existing_alert = db.query(Alert).filter(
                Alert.alert_type == report.hazard_type,
                Alert.is_active == True,
                Alert.created_at >= datetime.utcnow() - timedelta(hours=1)
            ).first()
            
            if existing_alert:
                return existing_alert
            
            # Generate alert based on report
            template = self.alert_templates.get(report.hazard_type, {
                'title': f'{report.hazard_type.title()} Alert',
                'message': f'A {report.hazard_type} has been reported in your area.',
                'priority': 'medium'
            })
            
            alert = await self.create_alert(
                alert_type=report.hazard_type,
                title=template['title'],
                message=f"{template['message']} Location: {report.title}",
                severity=report.severity,
                source='crowdsourced'
            )
            
            return alert
            
        except Exception as e:
            print(f"Error generating alert from report: {e}")
            return None
    
    async def cleanup_expired_alerts(self):
        """Clean up expired alerts"""
        db = next(get_db())
        
        try:
            # Deactivate expired alerts
            expired_alerts = db.query(Alert).filter(
                Alert.expires_at < datetime.utcnow(),
                Alert.is_active == True
            ).all()
            
            for alert in expired_alerts:
                alert.is_active = False
            
            db.commit()
            print(f"Deactivated {len(expired_alerts)} expired alerts")
            
        except Exception as e:
            print(f"Error cleaning up expired alerts: {e}")
            db.rollback()
        finally:
            db.close()

# Background tasks
async def periodic_alert_cleanup():
    """Periodic task to clean up expired alerts"""
    service = AlertService()
    
    while True:
        try:
            await service.cleanup_expired_alerts()
            await asyncio.sleep(3600)  # Run every hour
        except Exception as e:
            print(f"Error in periodic alert cleanup: {e}")
            await asyncio.sleep(300)  # 5 minutes on error

async def process_report_alerts():
    """Process new reports and generate alerts if needed"""
    service = AlertService()
    db = next(get_db())
    
    try:
        # Get recent high-severity reports
        recent_reports = db.query(HazardReport).filter(
            HazardReport.severity.in_(['high', 'critical']),
            HazardReport.created_at >= datetime.utcnow() - timedelta(hours=1),
            HazardReport.is_verified == True
        ).all()
        
        for report in recent_reports:
            await service.generate_alert_from_report(report)
    
    except Exception as e:
        print(f"Error processing report alerts: {e}")
    finally:
        db.close()