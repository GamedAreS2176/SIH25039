import re
import spacy
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Any
import json

class SocialMediaProcessor:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Initialize sentiment analyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Hazard-related keywords
        self.hazard_keywords = {
            'tsunami': ['tsunami', 'tidal wave', 'seismic wave', 'ocean wave'],
            'storm_surge': ['storm surge', 'storm tide', 'coastal flooding', 'storm water'],
            'high_waves': ['high waves', 'big waves', 'rough seas', 'wave height'],
            'flooding': ['flood', 'flooding', 'inundation', 'water level', 'rising water'],
            'coastal_current': ['current', 'rip current', 'undertow', 'strong current'],
            'abnormal_tide': ['tide', 'tidal', 'high tide', 'low tide', 'tide level'],
            'general': ['hazard', 'danger', 'warning', 'alert', 'emergency', 'disaster']
        }
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove user mentions and hashtags (but keep the text)
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?]', '', text)
        
        return text
    
    def extract_entities(self, text: str) -> List[str]:
        """Extract named entities using spaCy"""
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            if ent.label_ in ['GPE', 'LOC', 'ORG']:  # Geopolitical, Location, Organization
                entities.append(ent.text)
        
        return entities
    
    def extract_keywords(self, text: str, n_keywords: int = 10) -> List[str]:
        """Extract important keywords from text"""
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        keywords = []
        
        for token in doc:
            if (token.pos_ in ['NOUN', 'ADJ', 'VERB'] and 
                not token.is_stop and 
                not token.is_punct and 
                len(token.text) > 2):
                keywords.append(token.lemma_)
        
        # Count keyword frequency
        keyword_counts = {}
        for keyword in keywords:
            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        # Return top keywords
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        return [kw[0] for kw in sorted_keywords[:n_keywords]]

class HazardAnalyzer:
    def __init__(self):
        self.processor = SocialMediaProcessor()
        
        # Hazard detection patterns
        self.hazard_patterns = {
            'tsunami': [
                r'\b(tsunami|tidal wave|seismic wave)\b',
                r'\b(wave height|wave size)\b.*\b(high|large|big|massive)\b',
                r'\b(earthquake|seismic).*\b(ocean|sea|coastal)\b'
            ],
            'storm_surge': [
                r'\b(storm surge|storm tide)\b',
                r'\b(coastal flooding|shore flooding)\b',
                r'\b(water level|sea level).*\b(rising|increasing|high)\b'
            ],
            'high_waves': [
                r'\b(high waves|big waves|rough seas)\b',
                r'\b(wave height|wave size).*\b(high|large|big)\b',
                r'\b(dangerous|hazardous).*\b(waves|seas)\b'
            ],
            'flooding': [
                r'\b(flood|flooding|inundation)\b',
                r'\b(water level|water rising)\b',
                r'\b(submerged|underwater|waterlogged)\b'
            ],
            'coastal_current': [
                r'\b(current|rip current|undertow)\b',
                r'\b(strong current|dangerous current)\b',
                r'\b(swimming|drowning).*\b(current|undertow)\b'
            ]
        }
        
        # Sentiment keywords
        self.positive_keywords = ['safe', 'calm', 'normal', 'peaceful', 'clear']
        self.negative_keywords = ['dangerous', 'hazardous', 'risky', 'threatening', 'alarming']
        self.urgency_keywords = ['urgent', 'immediate', 'emergency', 'critical', 'warning']
    
    def extract_hazard_keywords(self, text: str) -> List[str]:
        """Extract hazard-related keywords from text"""
        hazard_keywords = []
        
        for hazard_type, patterns in self.hazard_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    hazard_keywords.append(hazard_type)
        
        # Also check for general hazard keywords
        for keyword in self.processor.hazard_keywords['general']:
            if keyword in text.lower():
                hazard_keywords.append('general_hazard')
        
        return list(set(hazard_keywords))
    
    def calculate_sentiment(self, text: str) -> float:
        """Calculate sentiment score (-1 to 1)"""
        if not text:
            return 0.0
        
        # Use VADER sentiment analyzer
        scores = self.processor.sentiment_analyzer.polarity_scores(text)
        return scores['compound']
    
    def calculate_hazard_probability(self, text: str, hazard_keywords: List[str]) -> float:
        """Calculate probability that text is hazard-related (0 to 1)"""
        if not text:
            return 0.0
        
        probability = 0.0
        
        # Base probability from hazard keywords
        if hazard_keywords:
            probability += 0.3
        
        # Pattern matching
        for hazard_type, patterns in self.hazard_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    probability += 0.2
                    break
        
        # Urgency keywords increase probability
        urgency_count = sum(1 for keyword in self.urgency_keywords if keyword in text.lower())
        probability += min(urgency_count * 0.1, 0.3)
        
        # Negative sentiment increases probability
        sentiment = self.calculate_sentiment(text)
        if sentiment < -0.1:  # Negative sentiment
            probability += 0.2
        
        return min(probability, 1.0)
    
    def extract_trending_keywords(self, posts: List, limit: int = 20) -> List[Dict[str, Any]]:
        """Extract trending keywords from posts"""
        all_keywords = []
        
        for post in posts:
            if hasattr(post, 'hazard_keywords') and post.hazard_keywords:
                all_keywords.extend(post.hazard_keywords)
        
        # Count keyword frequency
        keyword_counts = {}
        for keyword in all_keywords:
            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        # Sort by frequency
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {"keyword": kw, "count": count, "frequency": count / len(posts) if posts else 0}
            for kw, count in sorted_keywords[:limit]
        ]
    
    def analyze_sentiment_trends(self, posts: List) -> Dict[str, Any]:
        """Analyze sentiment trends in posts"""
        if not posts:
            return {"average_sentiment": 0, "sentiment_distribution": {}}
        
        sentiments = []
        for post in posts:
            if hasattr(post, 'sentiment_score') and post.sentiment_score is not None:
                sentiments.append(post.sentiment_score)
        
        if not sentiments:
            return {"average_sentiment": 0, "sentiment_distribution": {}}
        
        # Calculate average sentiment
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        # Categorize sentiments
        positive_count = sum(1 for s in sentiments if s > 0.1)
        negative_count = sum(1 for s in sentiments if s < -0.1)
        neutral_count = len(sentiments) - positive_count - negative_count
        
        return {
            "average_sentiment": avg_sentiment,
            "total_posts": len(sentiments),
            "positive_posts": positive_count,
            "negative_posts": negative_count,
            "neutral_posts": neutral_count,
            "sentiment_distribution": {
                "positive": positive_count / len(sentiments),
                "negative": negative_count / len(sentiments),
                "neutral": neutral_count / len(sentiments)
            }
        }
    
    def calculate_risk_score(self, social_posts: List, hazard_reports: List) -> float:
        """Calculate overall risk score based on social media and reports"""
        risk_score = 0.0
        
        # Factor in social media activity
        if social_posts:
            high_probability_posts = [p for p in social_posts if hasattr(p, 'hazard_probability') and p.hazard_probability > 0.7]
            risk_score += min(len(high_probability_posts) * 0.1, 0.5)
        
        # Factor in verified hazard reports
        if hazard_reports:
            critical_reports = [r for r in hazard_reports if hasattr(r, 'severity') and r.severity == 'critical']
            high_reports = [r for r in hazard_reports if hasattr(r, 'severity') and r.severity == 'high']
            
            risk_score += len(critical_reports) * 0.3
            risk_score += len(high_reports) * 0.2
        
        return min(risk_score, 1.0)