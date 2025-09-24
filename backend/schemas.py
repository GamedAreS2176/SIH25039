from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    citizen = "citizen"
    analyst = "analyst"
    official = "official"

class HazardType(str, Enum):
    tsunami = "tsunami"
    storm_surge = "storm_surge"
    high_waves = "high_waves"
    swell_surge = "swell_surge"
    coastal_current = "coastal_current"
    flooding = "flooding"
    abnormal_tide = "abnormal_tide"
    other = "other"

class SeverityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class Platform(str, Enum):
    twitter = "twitter"
    facebook = "facebook"
    youtube = "youtube"

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.citizen
    language: str = "en"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Hazard report schemas
class HazardReportBase(BaseModel):
    title: str
    description: str
    hazard_type: HazardType
    severity: SeverityLevel = SeverityLevel.medium

class HazardReportCreate(HazardReportBase):
    latitude: float
    longitude: float
    media_urls: Optional[List[str]] = []

class HazardReportResponse(HazardReportBase):
    id: int
    user_id: int
    latitude: float
    longitude: float
    media_urls: Optional[List[str]] = []
    is_verified: bool
    verified_by: Optional[int]
    verified_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Social media schemas
class SocialMediaPostResponse(BaseModel):
    id: int
    platform: Platform
    post_id: str
    content: str
    author: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    hazard_keywords: Optional[List[str]]
    sentiment_score: Optional[float]
    hazard_probability: Optional[float]
    engagement_metrics: Optional[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Hotspot schemas
class HotspotResponse(BaseModel):
    id: int
    latitude: float
    longitude: float
    radius_meters: int
    report_count: int
    severity_level: str
    hazard_types: List[str]
    created_at: datetime
    expires_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Alert schemas
class AlertResponse(BaseModel):
    id: int
    alert_type: str
    title: str
    message: str
    severity: str
    source: str
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Dashboard stats schema
class DashboardStats(BaseModel):
    reports_by_type: List[dict]
    social_media_activity: List[dict]
    active_hotspots: int
    timestamp: datetime