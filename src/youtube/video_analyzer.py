"""
YouTube Video Analyzer
Analyzes video performance, engagement, and content
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import statistics


logger = logging.getLogger("content_researcher.video_analyzer")


class VideoAnalyzer:
    """Analyzes YouTube videos for research insights"""
    
    def __init__(self, youtube_client):
        """
        Initialize video analyzer
        
        Args:
            youtube_client: Authenticated YouTube API client
        """
        self.youtube = youtube_client
    
    def get_channel_videos(self, 
                          channel_id: str,
                          max_results: int = 50,
                          days: int = 90) -> List[dict]:
        """
        Get recent videos from a channel
        
        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos
            days: Only videos from last N days
            
        Returns:
            List of video data
        """
        try:
            # Get uploads playlist
            channel_response = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            ).execute()
            
            if not channel_response.get('items'):
                logger.warning(f"Channel not found: {channel_id}")
                return []
            
            uploads_playlist = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Calculate date cutoff (timezone-aware)
            from datetime import timezone
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            # Get videos from playlist
            videos = []
            next_page_token = None
            
            while len(videos) < max_results:
                playlist_response = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=uploads_playlist,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token
                ).execute()
                
                for item in playlist_response.get('items', []):
                    try:
                        published_at = datetime.fromisoformat(
                            item['snippet']['publishedAt'].replace('Z', '+00:00')
                        )
                    except Exception:
                        # If datetime parsing fails, skip this video
                        continue
                    
                    if published_at < cutoff_date:
                        break
                    
                    videos.append({
                        'video_id': item['contentDetails']['videoId'],
                        'title': item['snippet']['title'],
                        'published_at': item['snippet']['publishedAt'],
                        'thumbnail': item['snippet']['thumbnails']['default']['url']
                    })
                
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
            
            # Get detailed video statistics
            if videos:
                videos = self._enrich_video_stats(videos)
            
            logger.info(f"Retrieved {len(videos)} videos from channel {channel_id}")
            return videos
        
        except Exception as e:
            logger.error(f"Error getting channel videos: {e}")
            return []
    
    def _enrich_video_stats(self, videos: List[dict]) -> List[dict]:
        """
        Add detailed statistics to videos
        
        Args:
            videos: List of video data
            
        Returns:
            Enriched video data
        """
        video_ids = [v['video_id'] for v in videos]
        
        # Batch request for statistics (max 50 per request)
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            
            try:
                stats_response = self.youtube.videos().list(
                    part="statistics,contentDetails,snippet",
                    id=','.join(batch_ids)
                ).execute()
                
                # Create stats lookup
                stats_lookup = {
                    item['id']: item for item in stats_response.get('items', [])
                }
                
                # Enrich videos
                for video in videos[i:i+50]:
                    video_id = video['video_id']
                    if video_id in stats_lookup:
                        item = stats_lookup[video_id]
                        stats = item['statistics']
                        
                        video['view_count'] = int(stats.get('viewCount', 0))
                        video['like_count'] = int(stats.get('likeCount', 0))
                        video['comment_count'] = int(stats.get('commentCount', 0))
                        video['duration'] = item['contentDetails']['duration']
                        video['tags'] = item['snippet'].get('tags', [])
                        video['category_id'] = item['snippet'].get('categoryId', '')
                        
                        # Calculate engagement rate
                        if video['view_count'] > 0:
                            video['engagement_rate'] = (
                                (video['like_count'] + video['comment_count']) 
                                / video['view_count'] * 100
                            )
                        else:
                            video['engagement_rate'] = 0
            
            except Exception as e:
                logger.error(f"Error enriching video stats: {e}")
        
        return videos
    
    def analyze_video_performance(self, videos: List[dict]) -> dict:
        """
        Analyze overall video performance metrics
        
        Args:
            videos: List of video data with statistics
            
        Returns:
            Performance analysis
        """
        if not videos:
            return {}
        
        view_counts = [v.get('view_count', 0) for v in videos if v.get('view_count')]
        engagement_rates = [v.get('engagement_rate', 0) for v in videos if v.get('engagement_rate')]
        
        return {
            'total_videos': len(videos),
            'avg_views': statistics.mean(view_counts) if view_counts else 0,
            'median_views': statistics.median(view_counts) if view_counts else 0,
            'max_views': max(view_counts) if view_counts else 0,
            'min_views': min(view_counts) if view_counts else 0,
            'avg_engagement_rate': statistics.mean(engagement_rates) if engagement_rates else 0,
            'top_performing': sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)[:5],
            'best_engagement': sorted(videos, key=lambda x: x.get('engagement_rate', 0), reverse=True)[:5]
        }
    
    def get_video_details(self, video_id: str) -> Optional[dict]:
        """
        Get detailed information about a specific video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Video details or None
        """
        try:
            response = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            ).execute()
            
            if not response.get('items'):
                return None
            
            item = response['items'][0]
            stats = item['statistics']
            snippet = item['snippet']
            
            return {
                'video_id': video_id,
                'title': snippet['title'],
                'description': snippet['description'],
                'channel_id': snippet['channelId'],
                'channel_title': snippet['channelTitle'],
                'published_at': snippet['publishedAt'],
                'view_count': int(stats.get('viewCount', 0)),
                'like_count': int(stats.get('likeCount', 0)),
                'comment_count': int(stats.get('commentCount', 0)),
                'duration': item['contentDetails']['duration'],
                'tags': snippet.get('tags', []),
                'category_id': snippet.get('categoryId', ''),
                'thumbnail': snippet['thumbnails']['high']['url']
            }
        
        except Exception as e:
            logger.error(f"Error getting video details: {e}")
            return None
    
    def extract_keywords_from_videos(self, videos: List[dict]) -> List[str]:
        """
        Extract common keywords from video titles and tags
        
        Args:
            videos: List of video data
            
        Returns:
            List of keywords
        """
        keywords = {}
        
        for video in videos:
            # Extract from title
            title_words = video.get('title', '').lower().split()
            for word in title_words:
                if len(word) > 3:  # Skip short words
                    keywords[word] = keywords.get(word, 0) + 2  # Title words weighted higher
            
            # Extract from tags
            for tag in video.get('tags', []):
                tag_lower = tag.lower()
                keywords[tag_lower] = keywords.get(tag_lower, 0) + 1
        
        # Sort by frequency
        sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
        
        return [k[0] for k in sorted_keywords[:50]]

