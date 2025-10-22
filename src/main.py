"""
YouTube Content Researcher Agent - Main Orchestration
Discovers trending, monetizable, and high-potential content topics
"""

import os
import time
import yaml
import click
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from typing import Optional, List

from .youtube.auth import YouTubeAuth
from .youtube.video_analyzer import VideoAnalyzer
from .youtube.trending import TrendingAnalyzer
from .youtube.search import YouTubeSearch
from .youtube.competitor import CompetitorAnalyzer
from .ai.topic_evaluator import TopicEvaluator
from .storage.database import ResearchDatabase
from .utils.logger import setup_logger, AgentLogger


# Load environment variables
load_dotenv()


class ContentResearcherAgent:
    """Main orchestrator for YouTube content research"""
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize Content Researcher Agent
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        
        # Load configurations
        self.settings = self._load_yaml(self.config_dir / "settings.yaml")
        self.prompts = self._load_yaml(self.config_dir / "research_prompts.yaml")
        
        # Setup logging
        log_config = self.settings.get('monitoring', {})
        self.logger = setup_logger(
            log_level=log_config.get('log_level', 'INFO'),
            log_file=log_config.get('log_file')
        )
        self.agent_logger = AgentLogger()
        
        # Initialize database
        self.db = ResearchDatabase(
            os.getenv('DATABASE_PATH', 'data/research.json')
        )
        
        # YouTube components
        self.yt_auth = None
        self.youtube_client = None
        self.video_analyzer = None
        self.trending_analyzer = None
        self.search_engine = None
        self.competitor_analyzer = None
        
        # AI components
        self.topic_evaluator = None
        
        # Channel info
        self.channel_id = os.getenv('CHANNEL_ID')
        self.channel_info = None
        
        # Session stats
        self.session_stats = {
            'topics_researched': 0,
            'high_quality_count': 0,
            'videos_analyzed': 0,
            'competitors_checked': 0,
            'start_time': None
        }
    
    def _load_yaml(self, path: Path) -> dict:
        """Load YAML configuration file"""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"Configuration file not found: {path}")
            return {}
    
    def initialize(self):
        """Initialize all components"""
        self.agent_logger.print_header("YouTube Content Researcher Agent")
        self.logger.info("Initializing agent...")
        
        # Authenticate with YouTube
        self.logger.info("Authenticating with YouTube API...")
        self.yt_auth = YouTubeAuth()
        self.youtube_client = self.yt_auth.authenticate()
        
        # Get channel info
        if self.channel_id:
            self.channel_info = self.yt_auth.get_channel_info(self.channel_id)
            self.logger.info(f"Researching for channel: {self.channel_info['title']}")
            self.logger.info(f"Subscribers: {self.channel_info['subscriber_count']:,}")
        else:
            self.logger.warning("No CHANNEL_ID specified in .env")
            self.channel_info = {'title': 'Unknown', 'subscriber_count': 0}
        
        # Initialize YouTube components
        self.video_analyzer = VideoAnalyzer(self.youtube_client)
        self.trending_analyzer = TrendingAnalyzer(self.youtube_client)
        self.search_engine = YouTubeSearch(self.youtube_client)
        self.competitor_analyzer = CompetitorAnalyzer(self.youtube_client)
        
        # Initialize AI
        ai_provider = os.getenv('AI_PROVIDER', 'anthropic')
        ai_model = os.getenv('AI_MODEL', 'claude-3-5-sonnet-20241022')
        
        self.logger.info(f"Initializing AI with {ai_provider}/{ai_model}...")
        self.topic_evaluator = TopicEvaluator(
            provider=ai_provider,
            model=ai_model,
            prompts_config=self.prompts
        )
        
        self.logger.info("✅ Agent initialized successfully!")
    
    def research_topics(self, 
                       keywords: List[str] = None,
                       use_trending: bool = True,
                       use_ai_generation: bool = True,
                       max_topics: int = None) -> List[dict]:
        """
        Research and evaluate content topics
        
        Args:
            keywords: Seed keywords (if None, derives from channel)
            use_trending: Include trending topics
            use_ai_generation: Use AI to generate topic ideas
            max_topics: Maximum topics to research
            
        Returns:
            List of evaluated topics
        """
        self.agent_logger.print_section("Phase 1: Topic Discovery")
        
        max_topics = max_topics or int(os.getenv('MAX_TOPICS_PER_RUN', 50))
        all_topics = []
        
        # 1. Analyze own channel for context
        channel_context = self._build_channel_context()
        
        # 2. Get seed keywords
        if not keywords:
            keywords = self._derive_keywords_from_channel(channel_context)
        
        self.logger.info(f"Using seed keywords: {', '.join(keywords[:10])}")
        
        # 3. Discover topics from multiple sources
        
        # 3a. Trending videos
        if use_trending:
            self.agent_logger.print_info("Discovering trending topics...")
            trending_topics = self._discover_from_trending()
            all_topics.extend(trending_topics)
            self.logger.info(f"Found {len(trending_topics)} trending topics")
        
        # 3b. Search-based discovery
        self.agent_logger.print_info("Searching related topics...")
        search_topics = self._discover_from_search(keywords)
        all_topics.extend(search_topics)
        self.logger.info(f"Found {len(search_topics)} search-based topics")
        
        # 3c. AI-generated topics
        if use_ai_generation:
            self.agent_logger.print_info("Generating AI topic ideas...")
            ai_topics = self.topic_evaluator.generate_topic_ideas(
                channel_context=channel_context,
                count=20,
                trends=[t['title'] for t in all_topics[:15]]
            )
            # Convert to dict format
            ai_topics = [{'title': topic, 'source': 'ai_generated'} for topic in ai_topics]
            all_topics.extend(ai_topics)
            self.logger.info(f"Generated {len(ai_topics)} AI topics")
        
        # 4. Remove duplicates
        unique_topics = self._deduplicate_topics(all_topics)
        self.logger.info(f"Total unique topics discovered: {len(unique_topics)}")
        
        # 5. Evaluate topics with AI
        self.agent_logger.print_section("Phase 2: AI Evaluation")
        
        # Limit topics to evaluate
        topics_to_evaluate = unique_topics[:max_topics]
        
        # Get trends and competitor data for context
        try:
            trends = self.trending_analyzer.get_trending_videos(max_results=20)
            trend_titles = [v.get('title', '') for v in trends] if isinstance(trends, list) else []
        except Exception as e:
            self.logger.warning(f"Could not get trending videos: {e}")
            trend_titles = []
        
        self.agent_logger.print_info(f"Evaluating {len(topics_to_evaluate)} topics...")
        
        evaluated_topics = []
        for i, topic_data in enumerate(topics_to_evaluate):
            self.logger.info(f"Evaluating {i+1}/{len(topics_to_evaluate)}: {topic_data['title']}")
            
            try:
                evaluation = self.topic_evaluator.evaluate_topic(
                    topic=topic_data['title'],
                    channel_context=channel_context,
                    trends=trend_titles,
                    competitors=None
                )
            except Exception as e:
                self.logger.error(f"Error evaluating topic '{topic_data['title']}': {e}")
                # Use default scores if evaluation fails
                evaluation = {
                    'importance_score': 50,
                    'watchability_score': 50,
                    'monetization_score': 50,
                    'popularity_score': 50,
                    'innovation_score': 50,
                    'total_score': 50,
                    'recommended_angle': 'Standard approach',
                    'keywords': [],
                    'competition_level': 'Medium',
                    'notes': f'Evaluation failed: {str(e)}'
                }
            
            # Merge with original data
            evaluated_topic = {
                **topic_data,
                **evaluation,
                'category': self._categorize_topic(topic_data['title'])
            }
            
            evaluated_topics.append(evaluated_topic)
            self.session_stats['topics_researched'] += 1
            
            # Save to database
            self.db.save_topic(evaluated_topic)
        
        # 6. Filter and sort by quality
        self.agent_logger.print_section("Phase 3: Filtering & Prioritization")
        
        min_score = self.settings.get('research_criteria', {}).get('min_total_score', 60)
        high_quality = [t for t in evaluated_topics if t['total_score'] >= min_score]
        
        self.session_stats['high_quality_count'] = len(high_quality)
        
        # Sort by total score
        high_quality.sort(key=lambda x: x['total_score'], reverse=True)
        
        self.logger.info(f"High quality topics (>= {min_score}): {len(high_quality)}")
        
        return high_quality
    
    def _build_channel_context(self) -> dict:
        """Build channel context for AI evaluation"""
        context = {
            'channel_id': self.channel_id,
            'channel_title': self.channel_info.get('title', 'Unknown'),
            'subscriber_count': self.channel_info.get('subscriber_count', 0),
            'niche': 'General',
            'avg_views': 0,
            'recent_themes': []
        }
        
        if self.channel_id:
            # Get recent videos
            recent_videos = self.video_analyzer.get_channel_videos(
                self.channel_id,
                max_results=20,
                days=90
            )
            
            if recent_videos:
                # Calculate average views
                context['avg_views'] = sum(v.get('view_count', 0) for v in recent_videos) / len(recent_videos)
                
                # Extract themes
                keywords = self.video_analyzer.extract_keywords_from_videos(recent_videos)
                context['recent_themes'] = keywords[:10]
                
                # Try to identify niche
                context['niche'] = self._identify_niche(keywords)
                
                self.session_stats['videos_analyzed'] += len(recent_videos)
        
        return context
    
    def _identify_niche(self, keywords: List[str]) -> str:
        """Identify channel niche from keywords"""
        tech_keywords = ['tech', 'software', 'coding', 'programming', 'developer', 'ai', 'ml', 'data']
        business_keywords = ['business', 'entrepreneur', 'startup', 'marketing', 'finance', 'money']
        education_keywords = ['tutorial', 'learn', 'course', 'guide', 'explained', 'education']
        
        keyword_str = ' '.join(keywords).lower()
        
        if any(k in keyword_str for k in tech_keywords):
            return 'Technology'
        elif any(k in keyword_str for k in business_keywords):
            return 'Business & Finance'
        elif any(k in keyword_str for k in education_keywords):
            return 'Education'
        else:
            return 'General'
    
    def _derive_keywords_from_channel(self, channel_context: dict) -> List[str]:
        """Derive seed keywords from channel"""
        keywords = channel_context.get('recent_themes', [])
        
        # Add default keywords if none found
        if not keywords:
            keywords = ['trending', 'popular', 'viral', 'top', 'best']
        
        return keywords[:10]
    
    def _discover_from_trending(self) -> List[dict]:
        """Discover topics from trending videos - ONLY if relevant to channel niche"""
        # Skip trending if we have a specific channel focus
        # Trending often returns irrelevant viral content (music, entertainment, etc.)
        # Only use trending for broad discovery or as supplementary data
        
        # For focused channels, skip trending entirely
        if self.channel_info and self.channel_info.get('subscriber_count', 0) > 0:
            self.logger.info("Skipping trending videos - focusing on channel-relevant content")
            return []
        
        return []
    
    def _discover_from_search(self, keywords: List[str]) -> List[dict]:
        """Discover topics from search - focused on channel niche"""
        topics = []
        
        # Add channel niche keywords to ensure relevance
        niche_keywords = self._get_niche_focused_keywords(keywords)
        
        for keyword in niche_keywords[:5]:  # Limit to avoid API quota
            # Get keyword variations (but fewer to stay focused)
            variations = self.search_engine.get_keyword_suggestions(keyword)
            
            # Search for top videos with more recent focus
            for variation in variations[:2]:  # Only top 2 variations per keyword
                results = self.search_engine.search_videos(
                    query=variation,
                    max_results=10,  # Get more results to filter
                    order="relevance"  # Relevance over views for better match
                )
                
                # Filter out clearly irrelevant content
                for video in results:
                    if self._is_relevant_to_channel(video):
                        topics.append({
                            'title': video['title'],
                            'source': f'search:{keyword}',
                            'views_potential': video.get('view_count', 0),
                            'reference_video_id': video.get('video_id')
                        })
        
        return topics
    
    def _deduplicate_topics(self, topics: List[dict]) -> List[dict]:
        """Remove duplicate topics"""
        seen_titles = set()
        unique = []
        
        for topic in topics:
            title_lower = topic['title'].lower()
            
            # Simple deduplication based on title
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique.append(topic)
        
        return unique
    
    def _get_niche_focused_keywords(self, user_keywords: List[str]) -> List[str]:
        """Combine user keywords with channel niche for better relevance"""
        niche = self._build_channel_context().get('niche', 'General')
        
        # Add niche-specific qualifiers to user keywords
        focused = []
        for keyword in user_keywords:
            # Add the original keyword
            focused.append(keyword)
            
            # Add niche-qualified versions
            if niche == 'Technology':
                focused.append(f"{keyword} tech")
                focused.append(f"{keyword} programming")
            elif niche == 'Business & Finance':
                focused.append(f"{keyword} business")
                focused.append(f"{keyword} entrepreneur")
            elif niche == 'Education':
                focused.append(f"{keyword} tutorial")
                focused.append(f"{keyword} course")
        
        return focused
    
    def _is_relevant_to_channel(self, video: dict) -> bool:
        """Filter out irrelevant content based on channel niche"""
        title = video.get('title', '').lower()
        
        # Blacklist: Filter out entertainment/music/gaming if not in that niche
        irrelevant_keywords = [
            'music video', 'official video', 'mv', 'trailer', 'teaser',
            'gameplay', 'let\'s play', 'gaming', 'fortnite', 'roblox',
            'tiktok', 'brainrot', 'steal a', 'admin abuse',
            'official music', 'ft.', 'feat.', 'prod. by',
            '(official', 'official trailer'
        ]
        
        for keyword in irrelevant_keywords:
            if keyword in title:
                return False
        
        # Whitelist: Ensure it has educational/tech/business keywords
        relevant_keywords = [
            'tutorial', 'guide', 'how to', 'learn', 'course', 'lesson',
            'tech', 'ai', 'programming', 'code', 'software', 'data',
            'business', 'startup', 'entrepreneur', 'marketing', 'strategy',
            'explained', 'introduction', 'beginner', 'advanced', 'tips',
            'review', 'comparison', 'vs', 'best', 'top'
        ]
        
        # Must have at least one relevant keyword
        has_relevant = any(keyword in title for keyword in relevant_keywords)
        
        return has_relevant
    
    def _categorize_topic(self, title: str) -> str:
        """Categorize topic based on title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['tutorial', 'how to', 'guide', 'learn']):
            return 'Tutorial'
        elif any(word in title_lower for word in ['review', 'unbox', 'test']):
            return 'Review'
        elif any(word in title_lower for word in ['vs', 'versus', 'comparison', 'compare']):
            return 'Comparison'
        elif any(word in title_lower for word in ['tips', 'tricks', 'hacks']):
            return 'Tips & Tricks'
        elif any(word in title_lower for word in ['news', 'update', 'announcement']):
            return 'News'
        else:
            return 'General'
    
    def analyze_competitors(self, competitor_ids: List[str]) -> dict:
        """
        Analyze competitor channels
        
        Args:
            competitor_ids: List of competitor channel IDs
            
        Returns:
            Competitor analysis
        """
        self.agent_logger.print_section("Competitor Analysis")
        
        analysis = self.competitor_analyzer.compare_competitors(competitor_ids)
        
        self.session_stats['competitors_checked'] = len(competitor_ids)
        
        return analysis
    
    def run(self, 
           keywords: List[str] = None,
           max_topics: int = None,
           show_details: bool = False):
        """
        Run the research agent
        
        Args:
            keywords: Seed keywords
            max_topics: Maximum topics to research
            show_details: Show detailed analysis
        """
        self.session_stats['start_time'] = time.time()
        
        try:
            # Research topics
            topics = self.research_topics(
                keywords=keywords,
                max_topics=max_topics
            )
            
            # Display results
            self.agent_logger.print_section("Research Results")
            
            if topics:
                self.agent_logger.print_topics_table(topics)
                
                # Show details for top topics
                if show_details:
                    self.agent_logger.print_section("Top Topic Details")
                    for topic in topics[:5]:
                        self.agent_logger.print_topic_detail(topic)
                        print()
            else:
                self.agent_logger.print_warning("No high-quality topics found")
        
        finally:
            # Record session
            duration = time.time() - self.session_stats['start_time']
            
            self.db.save_session({
                'topics_researched': self.session_stats['topics_researched'],
                'high_quality_count': self.session_stats['high_quality_count'],
                'videos_analyzed': self.session_stats['videos_analyzed'],
                'competitors_checked': self.session_stats['competitors_checked'],
                'duration_seconds': duration
            })
            
            # Show summary
            success_rate = (
                self.session_stats['high_quality_count'] / self.session_stats['topics_researched']
                if self.session_stats['topics_researched'] > 0 else 0
            )
            
            summary = {
                **self.session_stats,
                'duration_seconds': duration,
                'success_rate': success_rate
            }
            
            self.agent_logger.print_research_summary(summary)
    
    def show_analytics(self, days: int = 7):
        """Show analytics"""
        self.agent_logger.print_header(f"Research Analytics - Last {days} Days")
        analytics = self.db.get_analytics(days)
        
        print(f"\nTotal Sessions: {analytics['total_sessions']}")
        print(f"Topics Researched: {analytics['topics_researched']}")
        print(f"High Quality Topics: {analytics['high_quality_topics']}")
        print(f"Average Score: {analytics['avg_score']:.1f}/100")
        print(f"Total Duration: {analytics['total_duration']:.1f}s")
    
    def export_topics(self, output_path: str, days: int = 30):
        """Export topics to CSV"""
        self.db.export_topics_csv(output_path, days=days)
        self.agent_logger.print_success(f"Topics exported to {output_path}")


@click.command()
@click.option('--keywords', '-k', multiple=True, help='Seed keywords for research')
@click.option('--max-topics', default=None, type=int, help='Maximum topics to research')
@click.option('--details', is_flag=True, help='Show detailed analysis')
@click.option('--analytics', is_flag=True, help='Show analytics and exit')
@click.option('--export', type=str, help='Export topics to CSV file')
@click.option('--days', default=7, type=int, help='Days for analytics/export')
def main(keywords, max_topics, details, analytics, export, days):
    """YouTube Content Researcher Agent - Discover high-potential content topics"""
    
    # Check for environment file
    if not os.path.exists('.env'):
        click.echo("⚠️  .env file not found. Please copy .env.example and configure it.")
        return
    
    # Initialize agent
    agent = ContentResearcherAgent()
    
    try:
        agent.initialize()
        
        if analytics:
            agent.show_analytics(days)
        elif export:
            agent.export_topics(export, days)
        else:
            agent.run(
                keywords=list(keywords) if keywords else None,
                max_topics=max_topics,
                show_details=details
            )
    
    except KeyboardInterrupt:
        click.echo("\n\nInterrupted by user")
    except Exception as e:
        click.echo(f"\n❌ Error: {e}")
        raise
    finally:
        agent.db.close()


if __name__ == '__main__':
    main()

