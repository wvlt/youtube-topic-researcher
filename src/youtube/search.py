"""
YouTube Search and Discovery
Searches for trending topics, keywords, and content opportunities
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time


logger = logging.getLogger("content_researcher.search")


class YouTubeSearch:
    """Handles YouTube search and discovery"""
    
    def __init__(self, youtube_client):
        """
        Initialize YouTube search
        
        Args:
            youtube_client: Authenticated YouTube API client
        """
        self.youtube = youtube_client
    
    def search_videos(self,
                     query: str,
                     max_results: int = 50,
                     order: str = "relevance",
                     published_after: Optional[datetime] = None,
                     video_duration: str = "any") -> List[dict]:
        """
        Search for videos
        
        Args:
            query: Search query
            max_results: Maximum number of results
            order: Sort order (relevance, date, rating, viewCount)
            published_after: Only videos published after this date
            video_duration: any, short, medium, long
            
        Returns:
            List of video data
        """
        try:
            # Prepare request parameters
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': min(50, max_results),
                'order': order,
                'videoDuration': video_duration,
                'relevanceLanguage': 'en',
                'safeSearch': 'moderate'
            }
            
            if published_after:
                params['publishedAfter'] = published_after.isoformat() + 'Z'
            
            videos = []
            next_page_token = None
            
            while len(videos) < max_results:
                if next_page_token:
                    params['pageToken'] = next_page_token
                
                response = self.youtube.search().list(**params).execute()
                
                for item in response.get('items', []):
                    videos.append({
                        'video_id': item['id']['videoId'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'channel_id': item['snippet']['channelId'],
                        'channel_title': item['snippet']['channelTitle'],
                        'published_at': item['snippet']['publishedAt'],
                        'thumbnail': item['snippet']['thumbnails']['high']['url']
                    })
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token or len(videos) >= max_results:
                    break
                
                time.sleep(0.1)  # Rate limiting
            
            # Enrich with statistics
            if videos:
                videos = self._enrich_video_stats(videos[:max_results])
            
            logger.info(f"Found {len(videos)} videos for query: {query}")
            return videos[:max_results]
        
        except Exception as e:
            logger.error(f"Error searching videos: {e}")
            return []
    
    def _enrich_video_stats(self, videos: List[dict]) -> List[dict]:
        """Add statistics to video data"""
        video_ids = [v['video_id'] for v in videos]
        
        try:
            # Get statistics in batches
            for i in range(0, len(video_ids), 50):
                batch_ids = video_ids[i:i+50]
                
                response = self.youtube.videos().list(
                    part="statistics,contentDetails",
                    id=','.join(batch_ids)
                ).execute()
                
                stats_lookup = {item['id']: item for item in response.get('items', [])}
                
                for video in videos[i:i+50]:
                    video_id = video['video_id']
                    if video_id in stats_lookup:
                        item = stats_lookup[video_id]
                        stats = item['statistics']
                        
                        video['view_count'] = int(stats.get('viewCount', 0))
                        video['like_count'] = int(stats.get('likeCount', 0))
                        video['comment_count'] = int(stats.get('commentCount', 0))
                        video['duration'] = item['contentDetails']['duration']
                        
                        if video['view_count'] > 0:
                            video['engagement_rate'] = (
                                (video['like_count'] + video['comment_count']) 
                                / video['view_count'] * 100
                            )
                        else:
                            video['engagement_rate'] = 0
        
        except Exception as e:
            logger.error(f"Error enriching stats: {e}")
        
        return videos
    
    def find_related_topics(self, seed_keywords: List[str], max_per_keyword: int = 10) -> List[dict]:
        """
        Find related topics based on seed keywords
        
        Args:
            seed_keywords: List of seed keywords
            max_per_keyword: Max results per keyword
            
        Returns:
            List of related video topics
        """
        all_topics = []
        seen_videos = set()
        
        for keyword in seed_keywords:
            logger.info(f"Searching for: {keyword}")
            
            videos = self.search_videos(
                query=keyword,
                max_results=max_per_keyword,
                order="viewCount",
                published_after=datetime.now() - timedelta(days=90)
            )
            
            for video in videos:
                if video['video_id'] not in seen_videos:
                    seen_videos.add(video['video_id'])
                    all_topics.append({
                        **video,
                        'seed_keyword': keyword
                    })
            
            time.sleep(0.2)  # Rate limiting
        
        return all_topics
    
    def analyze_competition(self, keyword: str) -> dict:
        """
        Analyze competition level for a keyword
        
        Args:
            keyword: Search keyword
            
        Returns:
            Competition analysis
        """
        try:
            # Search for recent high-performing videos
            recent_videos = self.search_videos(
                query=keyword,
                max_results=50,
                order="viewCount",
                published_after=datetime.now() - timedelta(days=30)
            )
            
            if not recent_videos:
                return {
                    'keyword': keyword,
                    'competition_level': 0,
                    'avg_views': 0,
                    'top_performer_views': 0,
                    'video_count': 0
                }
            
            view_counts = [v['view_count'] for v in recent_videos]
            
            # Calculate competition metrics
            avg_views = sum(view_counts) / len(view_counts) if view_counts else 0
            top_views = max(view_counts) if view_counts else 0
            
            # Competition level (0-10 scale)
            # Based on: number of results, avg views, and top performer
            competition_level = min(10, (
                (len(recent_videos) / 50 * 3) +  # Video saturation
                (min(avg_views / 100000, 1) * 4) +  # Average performance
                (min(top_views / 1000000, 1) * 3)  # Top performer
            ))
            
            return {
                'keyword': keyword,
                'competition_level': round(competition_level, 1),
                'avg_views': int(avg_views),
                'top_performer_views': int(top_views),
                'video_count': len(recent_videos),
                'top_channels': list(set([v['channel_title'] for v in recent_videos[:10]]))
            }
        
        except Exception as e:
            logger.error(f"Error analyzing competition for {keyword}: {e}")
            return {
                'keyword': keyword,
                'competition_level': 5,
                'error': str(e)
            }
    
    def get_keyword_suggestions(self, base_keyword: str) -> List[str]:
        """
        Generate keyword variations and suggestions
        
        Args:
            base_keyword: Base keyword to expand
            
        Returns:
            List of keyword suggestions
        """
        variations = [
            f"{base_keyword} tutorial",
            f"{base_keyword} guide",
            f"{base_keyword} explained",
            f"{base_keyword} for beginners",
            f"{base_keyword} advanced",
            f"{base_keyword} tips",
            f"{base_keyword} tricks",
            f"{base_keyword} 2025",
            f"how to {base_keyword}",
            f"best {base_keyword}",
            f"{base_keyword} review",
            f"{base_keyword} comparison",
            f"{base_keyword} vs",
            f"why {base_keyword}",
            f"{base_keyword} secrets"
        ]
        
        return variations

