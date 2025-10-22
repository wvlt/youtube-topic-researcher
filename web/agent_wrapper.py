"""
Agent Wrapper for Web API
Wraps the Content Researcher Agent for web interface
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import ContentResearcherAgent
import logging


logger = logging.getLogger("web.wrapper")


class AgentWrapper:
    """Wraps the research agent for web API access"""
    
    def __init__(self):
        """Initialize agent wrapper"""
        self.agent = None
        self.initialized = False
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the agent"""
        try:
            self.agent = ContentResearcherAgent()
            self.agent.initialize()
            self.initialized = True
            logger.info("Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            self.initialized = False
    
    def is_initialized(self) -> bool:
        """Check if agent is initialized"""
        return self.initialized
    
    def research_topics(self, keywords: list = None, max_topics: int = 20) -> dict:
        """
        Research topics
        
        Args:
            keywords: Seed keywords
            max_topics: Maximum topics to research
            
        Returns:
            Research results
        """
        if not self.initialized:
            raise RuntimeError("Agent not initialized")
        
        try:
            topics = self.agent.research_topics(
                keywords=keywords,
                max_topics=max_topics
            )
            
            # Ensure topics is a list
            if not isinstance(topics, list):
                topics = []
            
            return {
                'success': True,
                'topics': topics,
                'count': len(topics)
            }
        
        except Exception as e:
            logger.error(f"Error researching topics: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e),
                'topics': []
            }
    
    def get_saved_topics(self, days: int = 7, min_score: float = 60, favorited_only: bool = False) -> dict:
        """
        Get previously researched topics
        
        Args:
            days: Days to look back
            min_score: Minimum score filter
            favorited_only: Only return favorited topics
            
        Returns:
            Saved topics
        """
        if not self.initialized:
            raise RuntimeError("Agent not initialized")
        
        try:
            topics = self.agent.db.get_topics(
                min_score=min_score,
                days=days,
                limit=100,
                favorited_only=favorited_only
            )
            
            # Ensure topics is a list
            if not isinstance(topics, list):
                topics = []
            
            return {
                'success': True,
                'topics': topics,
                'count': len(topics)
            }
        
        except Exception as e:
            logger.error(f"Error getting saved topics: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e),
                'topics': []
            }
    
    def toggle_favorite(self, topic_id: int) -> dict:
        """
        Toggle favorite status of a topic
        
        Args:
            topic_id: Document ID of the topic
            
        Returns:
            Result with new favorite status
        """
        if not self.initialized:
            raise RuntimeError("Agent not initialized")
        
        try:
            new_status = self.agent.db.toggle_favorite(topic_id)
            return {
                'success': True,
                'favorited': new_status,
                'topic_id': topic_id
            }
        
        except Exception as e:
            logger.error(f"Error toggling favorite: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_analytics(self, days: int = 7) -> dict:
        """Get analytics"""
        if not self.initialized:
            raise RuntimeError("Agent not initialized")
        
        try:
            analytics = self.agent.db.get_analytics(days)
            
            # Ensure analytics is a dict
            if not isinstance(analytics, dict):
                analytics = {
                    'total_sessions': 0,
                    'topics_researched': 0,
                    'high_quality_topics': 0,
                    'avg_score': 0
                }
            
            return {
                'success': True,
                'analytics': analytics
            }
        
        except Exception as e:
            logger.error(f"Error getting analytics: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_competitors(self, channel_ids: list) -> dict:
        """Analyze competitor channels"""
        if not self.initialized:
            raise RuntimeError("Agent not initialized")
        
        try:
            analysis = self.agent.analyze_competitors(channel_ids)
            return {
                'success': True,
                'analysis': analysis
            }
        
        except Exception as e:
            logger.error(f"Error analyzing competitors: {e}")
            return {
                'success': False,
                'error': str(e)
            }

