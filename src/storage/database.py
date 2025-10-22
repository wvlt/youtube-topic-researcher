"""
Database storage for research data
Uses TinyDB for simple JSON-based storage
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from tinydb import TinyDB, Query
import logging


logger = logging.getLogger("content_researcher.database")


class ResearchDatabase:
    """Manages storage of research data and sessions"""
    
    def __init__(self, db_path: str = "data/research.json"):
        """Initialize database"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.db = TinyDB(self.db_path)
        self.topics_table = self.db.table('topics')
        self.sessions_table = self.db.table('sessions')
        self.trends_table = self.db.table('trends')
        
        logger.info(f"Database initialized: {self.db_path}")
    
    def save_topic(self, topic: dict) -> int:
        """
        Save researched topic
        
        Args:
            topic: Topic data with scores and metadata
            
        Returns:
            Document ID
        """
        try:
            # Ensure topic is a dict
            if not isinstance(topic, dict):
                logger.error(f"Cannot save topic: not a dict, got {type(topic)}")
                return -1
            
            topic['timestamp'] = datetime.now().isoformat()
            # Initialize favorited field if not present
            if 'favorited' not in topic:
                topic['favorited'] = False
            
            doc_id = self.topics_table.insert(topic)
            logger.debug(f"Saved topic: {topic.get('title', 'Unknown')} (ID: {doc_id})")
            return doc_id
        except Exception as e:
            logger.error(f"Error saving topic: {e}")
            return -1
    
    def get_topics(self, 
                   min_score: float = 0,
                   category: Optional[str] = None,
                   days: int = 30,
                   limit: int = 100,
                   favorited_only: bool = False) -> List[dict]:
        """
        Retrieve topics with filters
        
        Args:
            min_score: Minimum total score
            category: Filter by category
            days: Only topics from last N days
            limit: Max number of results
            favorited_only: Only return favorited topics
            
        Returns:
            List of topics
        """
        Topic = Query()
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        # Build query
        query = Topic.total_score >= min_score
        query &= Topic.timestamp >= cutoff_date
        
        if category:
            query &= Topic.category == category
        
        if favorited_only:
            query &= Topic.favorited == True
        
        # Search and include doc_id in results
        results = self.topics_table.search(query)
        
        # TinyDB doesn't include doc_id by default, so we need to add it
        topics = []
        for doc in results:
            topic_with_id = dict(doc)
            topic_with_id['doc_id'] = doc.doc_id
            topics.append(topic_with_id)
        
        # Sort by total score
        topics.sort(key=lambda x: x.get('total_score', 0), reverse=True)
        
        return topics[:limit]
    
    def toggle_favorite(self, topic_id: int) -> bool:
        """
        Toggle favorite status of a topic
        
        Args:
            topic_id: Document ID of the topic
            
        Returns:
            New favorite status (True if now favorited, False if unfavorited)
        """
        try:
            topic = self.topics_table.get(doc_id=topic_id)
            if not topic:
                logger.error(f"Topic not found: {topic_id}")
                return False
            
            # Toggle the favorited status
            new_status = not topic.get('favorited', False)
            self.topics_table.update({'favorited': new_status}, doc_ids=[topic_id])
            
            logger.info(f"Topic {topic_id} favorited: {new_status}")
            return new_status
        except Exception as e:
            logger.error(f"Error toggling favorite for topic {topic_id}: {e}")
            return False
    
    def get_favorite_count(self) -> int:
        """
        Get count of favorited topics
        
        Returns:
            Number of favorited topics
        """
        Topic = Query()
        favorites = self.topics_table.search(Topic.favorited == True)
        return len(favorites)
    
    def topic_exists(self, title: str, days: int = 7) -> bool:
        """
        Check if topic was recently researched
        
        Args:
            title: Topic title
            days: Check last N days
            
        Returns:
            True if topic exists
        """
        Topic = Query()
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        results = self.topics_table.search(
            (Topic.title == title) & (Topic.timestamp >= cutoff_date)
        )
        
        return len(results) > 0
    
    def save_session(self, session_data: dict) -> int:
        """
        Save research session
        
        Args:
            session_data: Session metrics and metadata
            
        Returns:
            Document ID
        """
        session_data['timestamp'] = datetime.now().isoformat()
        doc_id = self.sessions_table.insert(session_data)
        logger.info(f"Saved session (ID: {doc_id})")
        return doc_id
    
    def get_analytics(self, days: int = 7) -> dict:
        """
        Get research analytics
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Analytics data
        """
        Session = Query()
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        sessions = self.sessions_table.search(Session.timestamp >= cutoff_date)
        
        if not sessions:
            return {
                'total_sessions': 0,
                'topics_researched': 0,
                'high_quality_topics': 0,
                'avg_score': 0,
                'total_duration': 0
            }
        
        # Calculate metrics
        total_topics = sum(s.get('topics_researched', 0) for s in sessions)
        high_quality = sum(s.get('high_quality_count', 0) for s in sessions)
        total_duration = sum(s.get('duration_seconds', 0) for s in sessions)
        
        # Get topics for this period
        topics = self.get_topics(days=days, limit=1000)
        avg_score = sum(t.get('total_score', 0) for t in topics) / len(topics) if topics else 0
        
        return {
            'total_sessions': len(sessions),
            'topics_researched': total_topics,
            'high_quality_topics': high_quality,
            'avg_score': avg_score,
            'total_duration': total_duration,
            'avg_topics_per_session': total_topics / len(sessions) if sessions else 0
        }
    
    def save_trend(self, trend_data: dict) -> int:
        """
        Save trend data
        
        Args:
            trend_data: Trend information
            
        Returns:
            Document ID
        """
        trend_data['timestamp'] = datetime.now().isoformat()
        doc_id = self.trends_table.insert(trend_data)
        return doc_id
    
    def get_trends(self, days: int = 7) -> List[dict]:
        """
        Get recent trends
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of trends
        """
        Trend = Query()
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        trends = self.trends_table.search(Trend.timestamp >= cutoff_date)
        trends.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return trends
    
    def export_topics_csv(self, output_path: str, days: int = 30):
        """
        Export topics to CSV
        
        Args:
            output_path: Output file path
            days: Days to export
        """
        import csv
        
        topics = self.get_topics(days=days, limit=10000)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if not topics:
                return
            
            writer = csv.DictWriter(f, fieldnames=topics[0].keys())
            writer.writeheader()
            writer.writerows(topics)
        
        logger.info(f"Exported {len(topics)} topics to {output_path}")
    
    def close(self):
        """Close database"""
        self.db.close()
        logger.info("Database closed")

