from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class SocialMediaPostResponse(BaseModel):
    id: int
    platform: str
    post_id: str
    content: str
    author: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    hazard_keywords: Optional[List[str]]
    sentiment_score: Optional[float]
    hazard_probability: Optional[float]
    engagement_metrics: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class HazardAnalysisResponse(BaseModel):
    hazard_posts_count: int
    recent_reports_count: int
    sentiment_analysis: Dict[str, Any]
    trending_keywords: List[Dict[str, Any]]
    risk_score: float
    timestamp: datetime

class TextAnalysisRequest(BaseModel):
    text: str
    platform: str = "unknown"

class TextAnalysisResponse(BaseModel):
    text: str
    processed_text: str
    hazard_keywords: List[str]
    sentiment_score: float
    hazard_probability: float
    is_hazard_related: bool