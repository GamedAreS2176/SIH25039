from fastapi import FastAPI, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import text
import redis
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

from database import get_db, engine
from models import SocialMediaPost, HazardReport
from schemas import SocialMediaPostResponse, HazardAnalysisResponse
from processors import SocialMediaProcessor, HazardAnalyzer
from collectors import TwitterCollector, FacebookCollector, YouTubeCollector

load_dotenv()

app = FastAPI(
    title="Data Dolphins NLP Engine",
    description="Social Media Processing and Hazard Analysis API",
    version="1.0.0"
)

# Redis connection
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# Initialize processors
social_processor = SocialMediaProcessor()
hazard_analyzer = HazardAnalyzer()

# Initialize collectors
twitter_collector = TwitterCollector()
facebook_collector = FacebookCollector()
youtube_collector = YouTubeCollector()

@app.get("/")
async def root():
    return {"message": "Data Dolphins NLP Engine - Social Media Processing Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/process/social-media")
async def process_social_media(background_tasks: BackgroundTasks):
    """Process social media posts for hazard detection"""
    background_tasks.add_task(collect_and_process_social_media)
    return {"message": "Social media processing started"}

@app.get("/social-media", response_model=List[SocialMediaPostResponse])
async def get_social_media_posts(
    platform: str = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get processed social media posts"""
    query = db.query(SocialMediaPost)
    
    if platform:
        query = query.filter(SocialMediaPost.platform == platform)
    
    posts = query.order_by(SocialMediaPost.created_at.desc()).limit(limit).all()
    return [SocialMediaPostResponse.from_orm(post) for post in posts]

@app.get("/analysis/hazards", response_model=HazardAnalysisResponse)
async def get_hazard_analysis(db: Session = Depends(get_db)):
    """Get hazard analysis from social media and reports"""
    # Get recent social media posts with hazard probability > 0.5
    hazard_posts = db.query(SocialMediaPost).filter(
        SocialMediaPost.hazard_probability > 0.5,
        SocialMediaPost.created_at >= datetime.utcnow() - timedelta(hours=24)
    ).all()
    
    # Get recent hazard reports
    recent_reports = db.query(HazardReport).filter(
        HazardReport.created_at >= datetime.utcnow() - timedelta(hours=24)
    ).all()
    
    # Analyze sentiment trends
    sentiment_analysis = hazard_analyzer.analyze_sentiment_trends(hazard_posts)
    
    # Extract trending keywords
    trending_keywords = hazard_analyzer.extract_trending_keywords(hazard_posts)
    
    # Calculate hazard risk score
    risk_score = hazard_analyzer.calculate_risk_score(hazard_posts, recent_reports)
    
    return HazardAnalysisResponse(
        hazard_posts_count=len(hazard_posts),
        recent_reports_count=len(recent_reports),
        sentiment_analysis=sentiment_analysis,
        trending_keywords=trending_keywords,
        risk_score=risk_score,
        timestamp=datetime.utcnow()
    )

@app.post("/analyze/text")
async def analyze_text(text: str, platform: str = "unknown"):
    """Analyze a single text for hazard indicators"""
    try:
        # Process the text
        processed_text = social_processor.preprocess_text(text)
        
        # Extract hazard keywords
        hazard_keywords = hazard_analyzer.extract_hazard_keywords(processed_text)
        
        # Calculate sentiment
        sentiment_score = hazard_analyzer.calculate_sentiment(processed_text)
        
        # Calculate hazard probability
        hazard_probability = hazard_analyzer.calculate_hazard_probability(
            processed_text, hazard_keywords
        )
        
        return {
            "text": text,
            "processed_text": processed_text,
            "hazard_keywords": hazard_keywords,
            "sentiment_score": sentiment_score,
            "hazard_probability": hazard_probability,
            "is_hazard_related": hazard_probability > 0.5
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/trends/keywords")
async def get_trending_keywords(
    hours: int = 24,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get trending hazard-related keywords"""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    posts = db.query(SocialMediaPost).filter(
        SocialMediaPost.created_at >= since,
        SocialMediaPost.hazard_probability > 0.3
    ).all()
    
    trending_keywords = hazard_analyzer.extract_trending_keywords(posts, limit)
    
    return {
        "trending_keywords": trending_keywords,
        "time_range_hours": hours,
        "total_posts_analyzed": len(posts)
    }

@app.get("/sentiment/trends")
async def get_sentiment_trends(
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get sentiment trends for hazard-related posts"""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    posts = db.query(SocialMediaPost).filter(
        SocialMediaPost.created_at >= since,
        SocialMediaPost.hazard_probability > 0.3
    ).all()
    
    sentiment_trends = hazard_analyzer.analyze_sentiment_trends(posts)
    
    return {
        "sentiment_trends": sentiment_trends,
        "time_range_hours": hours,
        "total_posts_analyzed": len(posts)
    }

async def collect_and_process_social_media():
    """Background task to collect and process social media posts"""
    try:
        # Collect from different platforms
        twitter_posts = await twitter_collector.collect_posts()
        facebook_posts = await facebook_collector.collect_posts()
        youtube_posts = await youtube_collector.collect_posts()
        
        all_posts = twitter_posts + facebook_posts + youtube_posts
        
        # Process each post
        for post_data in all_posts:
            await process_single_post(post_data)
            
        print(f"Processed {len(all_posts)} social media posts")
        
    except Exception as e:
        print(f"Error in social media processing: {e}")

async def process_single_post(post_data: Dict[str, Any]):
    """Process a single social media post"""
    try:
        db = next(get_db())
        
        # Check if post already exists
        existing_post = db.query(SocialMediaPost).filter(
            SocialMediaPost.platform == post_data['platform'],
            SocialMediaPost.post_id == post_data['post_id']
        ).first()
        
        if existing_post:
            return
        
        # Analyze the post
        processed_text = social_processor.preprocess_text(post_data['content'])
        hazard_keywords = hazard_analyzer.extract_hazard_keywords(processed_text)
        sentiment_score = hazard_analyzer.calculate_sentiment(processed_text)
        hazard_probability = hazard_analyzer.calculate_hazard_probability(
            processed_text, hazard_keywords
        )
        
        # Only store posts with some hazard relevance
        if hazard_probability > 0.2:
            social_post = SocialMediaPost(
                platform=post_data['platform'],
                post_id=post_data['post_id'],
                content=post_data['content'],
                author=post_data.get('author'),
                location=post_data.get('location'),
                hazard_keywords=hazard_keywords,
                sentiment_score=sentiment_score,
                hazard_probability=hazard_probability,
                engagement_metrics=post_data.get('engagement_metrics', {})
            )
            
            db.add(social_post)
            db.commit()
            
            # Publish to Redis for real-time updates
            redis_client.publish("new_social_post", json.dumps({
                "platform": post_data['platform'],
                "content": post_data['content'][:100] + "...",
                "hazard_probability": hazard_probability,
                "sentiment_score": sentiment_score,
                "created_at": datetime.utcnow().isoformat()
            }))
            
    except Exception as e:
        print(f"Error processing post: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)