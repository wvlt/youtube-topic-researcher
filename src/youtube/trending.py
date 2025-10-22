"""
YouTube Trending Analyzer
Discovers and analyzes trending videos
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
import time


logger = logging.getLogger("content_researcher.trending")


class TrendingAnalyzer:
    """Analyzes trending videos on YouTube"""
    
    def __init__(self, youtube_client):
        """
        Initialize trending analyzer
        
        Args:
            youtube_client: Authenticated YouTube API client
        """
        self.youtube = youtube_client
    
    def get_trending_videos(self,
                           region_code: str = "US",
                           category_id: str = None,
                           max_results: int = 50) -> List[dict]:
        """
        Get trending videos
        
        Args:
            region_code: Country code (US, GB, CA, etc.)
            category_id: YouTube category ID (optional)
            max_results: Maximum number of results
            
        Returns:
            List of trending videos
        """
        try:
            params = {
                'part': 'snippet,statistics,contentDetails',
                'chart': 'mostPopular',
                'regionCode': region_code,
                'maxResults': min(50, max_results)
            }
            
            if category_id:
                params['videoCategoryId'] = category_id
            
            videos = []
            next_page_token = None
            
            while len(videos) < max_results:
                if next_page_token:
                    params['pageToken'] = next_page_token
                
                response = self.youtube.videos().list(**params).execute()
                
                for item in response.get('items', []):
                    snippet = item['snippet']
                    stats = item['statistics']
                    
                    videos.append({
                        'video_id': item['id'],
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
                    })
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token or len(videos) >= max_results:
                    break
                
                time.sleep(0.1)  # Rate limiting
            
            logger.info(f"Retrieved {len(videos)} trending videos for {region_code}")
            return videos[:max_results]
        
        except Exception as e:
            logger.error(f"Error getting trending videos: {e}")
            return []
    
    def get_multi_region_trending(self,
                                  regions: List[str] = None,
                                  max_per_region: int = 20) -> Dict[str, List[dict]]:
        """
        Get trending videos from multiple regions
        
        Args:
            regions: List of region codes
            max_per_region: Max videos per region
            
        Returns:
            Dictionary mapping region to videos
        """
        if not regions:
            regions = ['US', 'GB', 'CA', 'AU']
        
        results = {}
        
        for region in regions:
            logger.info(f"Fetching trending videos for {region}")
            videos = self.get_trending_videos(
                region_code=region,
                max_results=max_per_region
            )
            results[region] = videos
            time.sleep(0.2)  # Rate limiting
        
        return results
    
    def analyze_trending_topics(self, videos: List[dict]) -> Dict:
        """
        Analyze common themes in trending videos
        
        Args:
            videos: List of video data
            
        Returns:
            Analysis of trending topics
        """
        # Extract keywords from titles
        word_freq = {}
        tag_freq = {}
        category_freq = {}
        
        for video in videos:
            # Title words
            title_words = video['title'].lower().split()
            for word in title_words:
                if len(word) > 4:  # Skip short words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Tags
            for tag in video.get('tags', []):
                tag_lower = tag.lower()
                tag_freq[tag_lower] = tag_freq.get(tag_lower, 0) + 1
            
            # Categories
            category = video.get('category_id', 'Unknown')
            category_freq[category] = category_freq.get(category, 0) + 1
        
        # Sort by frequency
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        top_tags = sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        top_categories = sorted(category_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Calculate average performance
        avg_views = sum(v['view_count'] for v in videos) / len(videos) if videos else 0
        avg_likes = sum(v['like_count'] for v in videos) / len(videos) if videos else 0
        avg_engagement = (sum(
            (v['like_count'] + v['comment_count']) / v['view_count'] 
            if v['view_count'] > 0 else 0
            for v in videos
        ) / len(videos) * 100) if videos else 0
        
        return {
            'total_videos': len(videos),
            'top_keywords': [k[0] for k in top_keywords],
            'top_tags': [t[0] for t in top_tags],
            'top_categories': dict(top_categories),
            'avg_views': avg_views,
            'avg_likes': avg_likes,
            'avg_engagement_rate': avg_engagement,
            'top_performing': sorted(videos, key=lambda x: x['view_count'], reverse=True)[:5]
        }
    
    def find_emerging_trends(self,
                            current_trending: List[dict],
                            previous_trending: List[dict] = None) -> List[str]:
        """
        Identify emerging trends by comparing current vs previous
        
        Args:
            current_trending: Current trending videos
            previous_trending: Previous trending videos
            
        Returns:
            List of emerging topics
        """
        current_analysis = self.analyze_trending_topics(current_trending)
        
        if not previous_trending:
            # Just return top current topics
            return current_analysis['top_keywords'][:10]
        
        previous_analysis = self.analyze_trending_topics(previous_trending)
        
        # Find keywords that are new or gaining momentum
        emerging = []
        
        current_keywords = set(current_analysis['top_keywords'][:30])
        previous_keywords = set(previous_analysis['top_keywords'][:30])
        
        # New topics
        new_topics = current_keywords - previous_keywords
        emerging.extend(list(new_topics)[:5])
        
        # Growing topics (appear in both but higher in current)
        for keyword in current_keywords & previous_keywords:
            current_pos = current_analysis['top_keywords'].index(keyword) if keyword in current_analysis['top_keywords'] else 100
            previous_pos = previous_analysis['top_keywords'].index(keyword) if keyword in previous_analysis['top_keywords'] else 100
            
            if current_pos < previous_pos - 5:  # Moved up at least 5 positions
                emerging.append(keyword)
        
        return emerging[:15]
    
    def get_category_name(self, category_id: str) -> str:
        """
        Get category name from ID
        
        Args:
            category_id: YouTube category ID
            
        Returns:
            Category name
        """
        categories = {
            '1': 'Film & Animation',
            '2': 'Autos & Vehicles',
            '10': 'Music',
            '15': 'Pets & Animals',
            '17': 'Sports',
            '19': 'Travel & Events',
            '20': 'Gaming',
            '22': 'People & Blogs',
            '23': 'Comedy',
            '24': 'Entertainment',
            '25': 'News & Politics',
            '26': 'Howto & Style',
            '27': 'Education',
            '28': 'Science & Technology',
            '29': 'Nonprofits & Activism'
        }
        
        return categories.get(category_id, 'Unknown')
