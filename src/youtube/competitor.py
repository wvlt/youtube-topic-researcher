"""
Competitor Analysis
Analyzes competitor channels and their successful content strategies
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import statistics


logger = logging.getLogger("content_researcher.competitor")


class CompetitorAnalyzer:
    """Analyzes competitor channels"""
    
    def __init__(self, youtube_client):
        """
        Initialize competitor analyzer
        
        Args:
            youtube_client: Authenticated YouTube API client
        """
        self.youtube = youtube_client
    
    def analyze_competitor(self, channel_id: str, days: int = 90) -> dict:
        """
        Analyze a competitor channel
        
        Args:
            channel_id: YouTube channel ID
            days: Days of history to analyze
            
        Returns:
            Competitor analysis
        """
        try:
            # Get channel info
            channel_response = self.youtube.channels().list(
                part="snippet,statistics,contentDetails",
                id=channel_id
            ).execute()
            
            if not channel_response.get('items'):
                logger.warning(f"Channel not found: {channel_id}")
                return {}
            
            channel = channel_response['items'][0]
            snippet = channel['snippet']
            stats = channel['statistics']
            
            # Get recent videos
            uploads_playlist = channel['contentDetails']['relatedPlaylists']['uploads']
            videos = self._get_playlist_videos(uploads_playlist, days=days, max_results=50)
            
            # Analyze performance
            performance = self._analyze_video_performance(videos)
            
            # Extract content themes
            themes = self._extract_content_themes(videos)
            
            return {
                'channel_id': channel_id,
                'channel_title': snippet['title'],
                'description': snippet['description'],
                'subscriber_count': int(stats.get('subscriberCount', 0)),
                'video_count': int(stats.get('videoCount', 0)),
                'view_count': int(stats.get('viewCount', 0)),
                'recent_videos': len(videos),
                'avg_views': performance['avg_views'],
                'median_views': performance['median_views'],
                'avg_engagement_rate': performance['avg_engagement_rate'],
                'top_performing_videos': performance['top_videos'],
                'content_themes': themes,
                'upload_frequency': self._calculate_upload_frequency(videos),
                'best_performing_format': self._identify_best_format(videos)
            }
        
        except Exception as e:
            logger.error(f"Error analyzing competitor {channel_id}: {e}")
            return {}
    
    def _get_playlist_videos(self, playlist_id: str, days: int = 90, max_results: int = 50) -> List[dict]:
        """Get videos from playlist"""
        cutoff_date = datetime.now() - timedelta(days=days)
        videos = []
        next_page_token = None
        
        try:
            while len(videos) < max_results:
                response = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=playlist_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token
                ).execute()
                
                for item in response.get('items', []):
                    published_at = datetime.fromisoformat(
                        item['snippet']['publishedAt'].replace('Z', '+00:00')
                    )
                    
                    if published_at < cutoff_date:
                        break
                    
                    videos.append({
                        'video_id': item['contentDetails']['videoId'],
                        'title': item['snippet']['title'],
                        'published_at': item['snippet']['publishedAt']
                    })
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
            
            # Enrich with stats
            if videos:
                videos = self._enrich_video_stats(videos)
        
        except Exception as e:
            logger.error(f"Error getting playlist videos: {e}")
        
        return videos
    
    def _enrich_video_stats(self, videos: List[dict]) -> List[dict]:
        """Add statistics to videos"""
        video_ids = [v['video_id'] for v in videos]
        
        try:
            for i in range(0, len(video_ids), 50):
                batch_ids = video_ids[i:i+50]
                
                response = self.youtube.videos().list(
                    part="statistics,snippet",
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
                        video['tags'] = item['snippet'].get('tags', [])
                        
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
    
    def _analyze_video_performance(self, videos: List[dict]) -> dict:
        """Analyze video performance metrics"""
        if not videos:
            return {
                'avg_views': 0,
                'median_views': 0,
                'avg_engagement_rate': 0,
                'top_videos': []
            }
        
        view_counts = [v.get('view_count', 0) for v in videos if v.get('view_count')]
        engagement_rates = [v.get('engagement_rate', 0) for v in videos if v.get('engagement_rate')]
        
        return {
            'avg_views': statistics.mean(view_counts) if view_counts else 0,
            'median_views': statistics.median(view_counts) if view_counts else 0,
            'avg_engagement_rate': statistics.mean(engagement_rates) if engagement_rates else 0,
            'top_videos': sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)[:5]
        }
    
    def _extract_content_themes(self, videos: List[dict]) -> List[str]:
        """Extract common content themes"""
        # Extract keywords from titles
        word_freq = {}
        
        for video in videos:
            title = video.get('title', '').lower()
            words = title.split()
            
            for word in words:
                if len(word) > 4:  # Skip short words
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_themes = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [theme[0] for theme in sorted_themes[:10]]
    
    def _calculate_upload_frequency(self, videos: List[dict]) -> dict:
        """Calculate upload frequency"""
        if len(videos) < 2:
            return {'videos_per_week': 0, 'consistency': 'unknown'}
        
        # Calculate days between uploads
        dates = []
        for video in videos:
            try:
                date = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
                dates.append(date)
            except:
                continue
        
        if len(dates) < 2:
            return {'videos_per_week': 0, 'consistency': 'unknown'}
        
        dates.sort()
        total_days = (dates[-1] - dates[0]).days
        
        if total_days == 0:
            return {'videos_per_week': 0, 'consistency': 'unknown'}
        
        videos_per_week = len(videos) / (total_days / 7)
        
        # Determine consistency
        if videos_per_week >= 7:
            consistency = 'daily'
        elif videos_per_week >= 3:
            consistency = 'frequent'
        elif videos_per_week >= 1:
            consistency = 'weekly'
        else:
            consistency = 'occasional'
        
        return {
            'videos_per_week': round(videos_per_week, 1),
            'consistency': consistency
        }
    
    def _identify_best_format(self, videos: List[dict]) -> dict:
        """Identify best performing content format"""
        # Analyze title patterns
        formats = {
            'tutorial': [],
            'how-to': [],
            'review': [],
            'comparison': [],
            'tips': [],
            'guide': [],
            'other': []
        }
        
        for video in videos:
            title = video.get('title', '').lower()
            views = video.get('view_count', 0)
            
            if 'tutorial' in title:
                formats['tutorial'].append(views)
            elif 'how to' in title or 'how-to' in title:
                formats['how-to'].append(views)
            elif 'review' in title:
                formats['review'].append(views)
            elif 'vs' in title or 'versus' in title or 'comparison' in title:
                formats['comparison'].append(views)
            elif 'tips' in title or 'tricks' in title:
                formats['tips'].append(views)
            elif 'guide' in title:
                formats['guide'].append(views)
            else:
                formats['other'].append(views)
        
        # Find best performing format
        format_performance = {}
        for format_type, views_list in formats.items():
            if views_list:
                format_performance[format_type] = {
                    'avg_views': statistics.mean(views_list),
                    'count': len(views_list)
                }
        
        if format_performance:
            best = max(format_performance.items(), key=lambda x: x[1]['avg_views'])
            return {
                'format': best[0],
                'avg_views': best[1]['avg_views'],
                'count': best[1]['count']
            }
        
        return {'format': 'unknown', 'avg_views': 0, 'count': 0}
    
    def compare_competitors(self, channel_ids: List[str]) -> dict:
        """
        Compare multiple competitor channels
        
        Args:
            channel_ids: List of channel IDs
            
        Returns:
            Comparative analysis
        """
        competitors = []
        
        for channel_id in channel_ids:
            analysis = self.analyze_competitor(channel_id)
            if analysis:
                competitors.append(analysis)
        
        if not competitors:
            return {}
        
        # Find best practices
        best_engagement = max(competitors, key=lambda x: x.get('avg_engagement_rate', 0))
        most_views = max(competitors, key=lambda x: x.get('avg_views', 0))
        most_frequent = max(competitors, key=lambda x: x.get('upload_frequency', {}).get('videos_per_week', 0))
        
        return {
            'competitors': competitors,
            'best_engagement': best_engagement['channel_title'],
            'most_views': most_views['channel_title'],
            'most_frequent': most_frequent['channel_title'],
            'avg_subscriber_count': statistics.mean([c['subscriber_count'] for c in competitors]),
            'common_themes': self._find_common_themes(competitors)
        }
    
    def _find_common_themes(self, competitors: List[dict]) -> List[str]:
        """Find common themes across competitors"""
        all_themes = []
        
        for competitor in competitors:
            all_themes.extend(competitor.get('content_themes', []))
        
        # Count theme frequency
        theme_freq = {}
        for theme in all_themes:
            theme_freq[theme] = theme_freq.get(theme, 0) + 1
        
        # Return themes appearing in multiple competitors
        common = [theme for theme, count in theme_freq.items() if count > 1]
        return sorted(common, key=lambda x: theme_freq[x], reverse=True)[:10]

