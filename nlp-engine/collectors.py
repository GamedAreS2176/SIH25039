import tweepy
import requests
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import asyncio
import aiohttp
from datetime import datetime, timedelta
import json

load_dotenv()

class TwitterCollector:
    def __init__(self):
        # Twitter API credentials (would be set via environment variables)
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        # Initialize Twitter API client
        if self.bearer_token:
            self.client = tweepy.Client(bearer_token=self.bearer_token)
        else:
            self.client = None
    
    async def collect_posts(self) -> List[Dict[str, Any]]:
        """Collect recent tweets related to ocean hazards"""
        if not self.client:
            print("Twitter API not configured")
            return []
        
        try:
            # Search for ocean hazard related keywords
            search_terms = [
                "tsunami", "storm surge", "high waves", "coastal flooding",
                "ocean hazard", "sea level", "tidal wave", "coastal current"
            ]
            
            posts = []
            for term in search_terms:
                try:
                    tweets = self.client.search_recent_tweets(
                        query=f"{term} -is:retweet lang:en",
                        max_results=10,
                        tweet_fields=['created_at', 'author_id', 'public_metrics', 'geo']
                    )
                    
                    if tweets.data:
                        for tweet in tweets.data:
                            post_data = {
                                'platform': 'twitter',
                                'post_id': tweet.id,
                                'content': tweet.text,
                                'author': str(tweet.author_id),
                                'created_at': tweet.created_at.isoformat(),
                                'engagement_metrics': {
                                    'likes': tweet.public_metrics.get('like_count', 0),
                                    'retweets': tweet.public_metrics.get('retweet_count', 0),
                                    'replies': tweet.public_metrics.get('reply_count', 0)
                                }
                            }
                            
                            # Add location if available
                            if hasattr(tweet, 'geo') and tweet.geo:
                                post_data['location'] = {
                                    'latitude': tweet.geo.coordinates[0],
                                    'longitude': tweet.geo.coordinates[1]
                                }
                            
                            posts.append(post_data)
                
                except Exception as e:
                    print(f"Error collecting tweets for term '{term}': {e}")
                    continue
            
            return posts
            
        except Exception as e:
            print(f"Error in Twitter collection: {e}")
            return []

class FacebookCollector:
    def __init__(self):
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.base_url = "https://graph.facebook.com/v18.0"
    
    async def collect_posts(self) -> List[Dict[str, Any]]:
        """Collect Facebook posts related to ocean hazards"""
        if not self.access_token:
            print("Facebook API not configured")
            return []
        
        try:
            # Search for public posts (this is a simplified example)
            # In reality, you'd need proper Facebook API permissions
            search_terms = [
                "tsunami", "storm surge", "coastal flooding", "ocean hazard"
            ]
            
            posts = []
            for term in search_terms:
                try:
                    # This is a placeholder - actual implementation would use Facebook Graph API
                    # with proper permissions for public posts
                    url = f"{self.base_url}/search"
                    params = {
                        'q': term,
                        'type': 'post',
                        'access_token': self.access_token,
                        'limit': 5
                    }
                    
                    # Note: This is a simplified example
                    # Real implementation would handle pagination and proper API calls
                    posts.append({
                        'platform': 'facebook',
                        'post_id': f"fb_{term}_{datetime.now().timestamp()}",
                        'content': f"Sample Facebook post about {term}",
                        'author': 'sample_user',
                        'created_at': datetime.now().isoformat(),
                        'engagement_metrics': {
                            'likes': 0,
                            'shares': 0,
                            'comments': 0
                        }
                    })
                
                except Exception as e:
                    print(f"Error collecting Facebook posts for term '{term}': {e}")
                    continue
            
            return posts
            
        except Exception as e:
            print(f"Error in Facebook collection: {e}")
            return []

class YouTubeCollector:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    async def collect_posts(self) -> List[Dict[str, Any]]:
        """Collect YouTube comments and video metadata related to ocean hazards"""
        if not self.api_key:
            print("YouTube API not configured")
            return []
        
        try:
            search_terms = [
                "tsunami", "storm surge", "coastal flooding", "ocean hazard"
            ]
            
            posts = []
            for term in search_terms:
                try:
                    # Search for videos
                    search_url = f"{self.base_url}/search"
                    params = {
                        'part': 'snippet',
                        'q': f"{term} ocean hazard",
                        'type': 'video',
                        'key': self.api_key,
                        'maxResults': 5,
                        'publishedAfter': (datetime.now() - timedelta(days=7)).isoformat() + 'Z'
                    }
                    
                    # This is a placeholder - actual implementation would make HTTP requests
                    posts.append({
                        'platform': 'youtube',
                        'post_id': f"yt_{term}_{datetime.now().timestamp()}",
                        'content': f"Sample YouTube video about {term}",
                        'author': 'sample_channel',
                        'created_at': datetime.now().isoformat(),
                        'engagement_metrics': {
                            'views': 0,
                            'likes': 0,
                            'comments': 0
                        }
                    })
                
                except Exception as e:
                    print(f"Error collecting YouTube content for term '{term}': {e}")
                    continue
            
            return posts
            
        except Exception as e:
            print(f"Error in YouTube collection: {e}")
            return []

# Mock data collector for demonstration
class MockSocialMediaCollector:
    def __init__(self):
        self.sample_posts = [
            {
                'platform': 'twitter',
                'post_id': 'tweet_001',
                'content': 'High waves observed at Marina Beach Chennai. Water levels rising rapidly. #OceanHazard #Chennai',
                'author': 'coastal_observer',
                'created_at': datetime.now().isoformat(),
                'engagement_metrics': {'likes': 15, 'retweets': 8, 'replies': 3}
            },
            {
                'platform': 'facebook',
                'post_id': 'fb_001',
                'content': 'Storm surge warning issued for coastal areas. Residents advised to stay away from beaches.',
                'author': 'weather_alert',
                'created_at': datetime.now().isoformat(),
                'engagement_metrics': {'likes': 25, 'shares': 12, 'comments': 7}
            },
            {
                'platform': 'youtube',
                'post_id': 'yt_001',
                'content': 'Tsunami preparedness video: What to do when you see unusual ocean behavior',
                'author': 'disaster_prep_channel',
                'created_at': datetime.now().isoformat(),
                'engagement_metrics': {'views': 1500, 'likes': 45, 'comments': 12}
            },
            {
                'platform': 'twitter',
                'post_id': 'tweet_002',
                'content': 'Abnormal tide patterns observed in Mumbai. Water levels much higher than normal.',
                'author': 'mumbai_coast',
                'created_at': datetime.now().isoformat(),
                'engagement_metrics': {'likes': 8, 'retweets': 4, 'replies': 2}
            }
        ]
    
    async def collect_posts(self) -> List[Dict[str, Any]]:
        """Return sample posts for demonstration"""
        return self.sample_posts