from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import text
import redis
import json
from datetime import datetime, timedelta
from typing import List, Optional
import os
from dotenv import load_dotenv

from database import get_db, engine
from models import User, HazardReport, SocialMediaPost, Hotspot, Alert, UserAlert
from schemas import (
    UserCreate, UserResponse, UserLogin, 
    HazardReportCreate, HazardReportResponse,
    SocialMediaPostResponse, HotspotResponse, AlertResponse
)
from auth import create_access_token, verify_token, get_password_hash, verify_password
from utils import generate_h3_index, calculate_distance

load_dotenv()

app = FastAPI(
    title="Data Dolphins API",
    description="Ocean Hazard Monitoring Platform API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
security = HTTPBearer()

@app.get("/")
async def root():
    return {"message": "Data Dolphins API - Ocean Hazard Monitoring Platform"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Authentication endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role,
        language=user_data.language
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse.from_orm(db_user)

@app.post("/auth/login")
async def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }

# Hazard report endpoints
@app.post("/reports", response_model=HazardReportResponse)
async def create_hazard_report(
    title: str = Form(...),
    description: str = Form(...),
    hazard_type: str = Form(...),
    severity: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # Validate hazard type
    valid_hazard_types = [
        'tsunami', 'storm_surge', 'high_waves', 'swell_surge',
        'coastal_current', 'flooding', 'abnormal_tide', 'other'
    ]
    if hazard_type not in valid_hazard_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid hazard type. Must be one of: {valid_hazard_types}"
        )
    
    # Handle file upload
    media_urls = []
    if file:
        # Save file to uploads directory
        file_path = f"uploads/{datetime.utcnow().timestamp()}_{file.filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        media_urls.append(file_path)
    
    # Create hazard report
    report = HazardReport(
        user_id=current_user.id,
        title=title,
        description=description,
        hazard_type=hazard_type,
        severity=severity,
        location=f"POINT({longitude} {latitude})",
        media_urls=media_urls
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    # Trigger hotspot generation
    await generate_hotspots_async(db)
    
    # Publish to Redis for real-time updates
    redis_client.publish("new_report", json.dumps({
        "id": report.id,
        "title": report.title,
        "hazard_type": report.hazard_type,
        "severity": report.severity,
        "latitude": latitude,
        "longitude": longitude,
        "created_at": report.created_at.isoformat()
    }))
    
    return HazardReportResponse.from_orm(report)

@app.get("/reports", response_model=List[HazardReportResponse])
async def get_hazard_reports(
    skip: int = 0,
    limit: int = 100,
    hazard_type: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(HazardReport)
    
    if hazard_type:
        query = query.filter(HazardReport.hazard_type == hazard_type)
    if severity:
        query = query.filter(HazardReport.severity == severity)
    
    reports = query.offset(skip).limit(limit).all()
    return [HazardReportResponse.from_orm(report) for report in reports]

@app.get("/reports/{report_id}", response_model=HazardReportResponse)
async def get_hazard_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(HazardReport).filter(HazardReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hazard report not found"
        )
    return HazardReportResponse.from_orm(report)

@app.put("/reports/{report_id}/verify")
async def verify_hazard_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    if current_user.role not in ['analyst', 'official']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only analysts and officials can verify reports"
        )
    
    report = db.query(HazardReport).filter(HazardReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hazard report not found"
        )
    
    report.is_verified = True
    report.verified_by = current_user.id
    report.verified_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Report verified successfully"}

# Social media endpoints
@app.get("/social-media", response_model=List[SocialMediaPostResponse])
async def get_social_media_posts(
    platform: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(SocialMediaPost)
    
    if platform:
        query = query.filter(SocialMediaPost.platform == platform)
    
    posts = query.offset(skip).limit(limit).all()
    return [SocialMediaPostResponse.from_orm(post) for post in posts]

# Hotspots endpoints
@app.get("/hotspots", response_model=List[HotspotResponse])
async def get_hotspots(db: Session = Depends(get_db)):
    hotspots = db.query(Hotspot).filter(Hotspot.expires_at > datetime.utcnow()).all()
    return [HotspotResponse.from_orm(hotspot) for hotspot in hotspots]

# Alerts endpoints
@app.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Alert).filter(Alert.is_active == True)
    
    if user_id:
        # Get alerts for specific user based on location
        user_alerts = db.query(UserAlert).filter(UserAlert.user_id == user_id).all()
        alert_ids = [ua.alert_id for ua in user_alerts]
        query = query.filter(Alert.id.in_(alert_ids))
    
    alerts = query.all()
    return [AlertResponse.from_orm(alert) for alert in alerts]

# Statistics endpoints
@app.get("/stats/dashboard")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    # Get report counts by type
    report_stats = db.execute(text("""
        SELECT hazard_type, COUNT(*) as count, severity
        FROM hazard_reports 
        WHERE created_at >= NOW() - INTERVAL '24 hours'
        GROUP BY hazard_type, severity
    """)).fetchall()
    
    # Get social media activity
    social_stats = db.execute(text("""
        SELECT platform, COUNT(*) as count
        FROM social_media_posts 
        WHERE created_at >= NOW() - INTERVAL '24 hours'
        GROUP BY platform
    """)).fetchall()
    
    # Get hotspot count
    hotspot_count = db.query(Hotspot).filter(Hotspot.expires_at > datetime.utcnow()).count()
    
    return {
        "reports_by_type": [{"hazard_type": row[0], "count": row[1], "severity": row[2]} for row in report_stats],
        "social_media_activity": [{"platform": row[0], "count": row[1]} for row in social_stats],
        "active_hotspots": hotspot_count,
        "timestamp": datetime.utcnow().isoformat()
    }

# Real-time endpoints
@app.get("/realtime/stream")
async def stream_reports():
    """WebSocket endpoint for real-time report streaming"""
    # This would be implemented with WebSocket in a production environment
    # For now, return recent reports
    return {"message": "Real-time streaming endpoint - WebSocket implementation needed"}

# Utility functions
async def generate_hotspots_async(db: Session):
    """Generate hotspots based on recent reports"""
    try:
        db.execute(text("SELECT generate_hotspots()"))
        db.commit()
    except Exception as e:
        print(f"Error generating hotspots: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)