from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from database import Base
from datetime import datetime

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