from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(String(20), default="citizen")
    language = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    hazard_reports = relationship("HazardReport", back_populates="user")
    verified_reports = relationship("HazardReport", foreign_keys="HazardReport.verified_by", back_populates="verifier")

class HazardReport(Base):
    __tablename__ = "hazard_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200))
    description = Column(Text)
    hazard_type = Column(String(50))
    severity = Column(String(20), default="medium")
    location = Column(Geometry("POINT", srid=4326))
    h3_index = Column(String(20))
    media_urls = Column(ARRAY(String))
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("users.id"))
    verified_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="hazard_reports")
    verifier = relationship("User", foreign_keys=[verified_by], back_populates="verified_reports")

class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(20))
    post_id = Column(String(100))
    content = Column(Text)
    author = Column(String(100))
    location = Column(Geometry("POINT", srid=4326))
    hazard_keywords = Column(ARRAY(String))
    sentiment_score = Column(Float)
    hazard_probability = Column(Float)
    engagement_metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, default=datetime.utcnow)

class Hotspot(Base):
    __tablename__ = "hotspots"
    
    id = Column(Integer, primary_key=True, index=True)
    center_location = Column(Geometry("POINT", srid=4326))
    radius_meters = Column(Integer)
    report_count = Column(Integer, default=0)
    severity_level = Column(String(20), default="medium")
    hazard_types = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String(50))
    title = Column(String(200))
    message = Column(Text)
    affected_area = Column(Geometry("POLYGON", srid=4326))
    severity = Column(String(20))
    source = Column(String(50), default="incois")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class UserAlert(Base):
    __tablename__ = "user_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)