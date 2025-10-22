# API Documentation - YouTube Content Researcher Agent

## Overview

The Content Researcher Agent provides both a Python API and REST API for integration with other agents and systems.

## Python API

### Basic Usage

```python
from src.main import ContentResearcherAgent

# Initialize agent
agent = ContentResearcherAgent()
agent.initialize()

# Run research
topics = agent.research_topics(
    keywords=['AI', 'machine learning'],
    max_topics=20
)

# Access results
for topic in topics:
    print(f"{topic['title']}: {topic['total_score']}")
```

### ContentResearcherAgent

#### `__init__(config_dir="config")`
Initialize the agent with configuration directory.

#### `initialize()`
Initialize all components (YouTube API, AI, Database).

**Example:**
```python
agent = ContentResearcherAgent()
agent.initialize()
```

#### `research_topics(keywords=None, use_trending=True, use_ai_generation=True, max_topics=None)`
Run comprehensive topic research.

**Parameters:**
- `keywords` (list): Seed keywords for research
- `use_trending` (bool): Include trending videos
- `use_ai_generation` (bool): Generate AI topic ideas
- `max_topics` (int): Maximum topics to evaluate

**Returns:**
```python
[
    {
        'title': 'Topic Title',
        'total_score': 85.5,
        'importance_score': 90,
        'watchability_score': 85,
        'monetization_score': 80,
        'popularity_score': 85,
        'innovation_score': 85,
        'category': 'Tutorial',
        'keywords': ['keyword1', 'keyword2'],
        'recommended_angle': 'Unique approach...',
        'competition_level': 'Medium',
        'notes': 'Strategic insights...',
        'ai_analysis': 'Full AI response...',
        'timestamp': '2025-10-22T10:00:00',
        'source': 'trending',
        'views_potential': 100000
    },
    ...
]
```

#### `analyze_competitors(competitor_ids)`
Analyze competitor channels.

**Parameters:**
- `competitor_ids` (list): List of YouTube channel IDs

**Returns:**
```python
{
    'competitors': [...],
    'best_engagement': 'Channel Name',
    'most_views': 'Channel Name',
    'common_themes': ['theme1', 'theme2'],
    'avg_subscriber_count': 250000
}
```

#### `show_analytics(days=7)`
Display analytics for past days.

#### `export_topics(output_path, days=30)`
Export topics to CSV file.

### ResearchDatabase

```python
from src.storage.database import ResearchDatabase

db = ResearchDatabase('data/research.json')

# Get topics
topics = db.get_topics(
    min_score=70,
    category='Tutorial',
    days=30,
    limit=100
)

# Save topic
db.save_topic({
    'title': 'Topic',
    'total_score': 85,
    ...
})

# Get analytics
analytics = db.get_analytics(days=7)
```

### TopicEvaluator

```python
from src.ai.topic_evaluator import TopicEvaluator

evaluator = TopicEvaluator(
    provider='anthropic',
    model='claude-3-5-sonnet-20241022'
)

# Evaluate single topic
evaluation = evaluator.evaluate_topic(
    topic='How to use AI for content creation',
    channel_context={
        'channel_title': 'Tech Channel',
        'subscriber_count': 50000,
        'niche': 'Technology'
    },
    trends=['AI', 'automation'],
    competitors=[]
)

# Generate topics
topics = evaluator.generate_topic_ideas(
    channel_context={...},
    count=10
)
```

### YouTube Modules

#### VideoAnalyzer
```python
from src.youtube.video_analyzer import VideoAnalyzer

analyzer = VideoAnalyzer(youtube_client)

# Get channel videos
videos = analyzer.get_channel_videos(
    channel_id='UCxxx',
    max_results=50,
    days=90
)

# Analyze performance
performance = analyzer.analyze_video_performance(videos)
```

#### TrendingAnalyzer
```python
from src.youtube.trending import TrendingAnalyzer

trending = TrendingAnalyzer(youtube_client)

# Get trending videos
videos = trending.get_trending_videos(
    region_code='US',
    category_id='28',  # Science & Technology
    max_results=50
)
```

#### YouTubeSearch
```python
from src.youtube.search import YouTubeSearch

search = YouTubeSearch(youtube_client)

# Search videos
results = search.search_videos(
    query='AI tutorial',
    max_results=50,
    order='viewCount'
)

# Analyze competition
competition = search.analyze_competition('AI tutorial')
```

#### CompetitorAnalyzer
```python
from src.youtube.competitor import CompetitorAnalyzer

competitor = CompetitorAnalyzer(youtube_client)

# Analyze single competitor
analysis = competitor.analyze_competitor(
    channel_id='UCxxx',
    days=90
)

# Compare multiple
comparison = competitor.compare_competitors([
    'UCxxx',
    'UCyyy',
    'UCzzz'
])
```

## REST API

### Base URL
```
http://localhost:8080
```

### Endpoints

#### GET /api/status
Check agent status.

**Response:**
```json
{
    "status": "ready|error",
    "message": "Agent is ready"
}
```

#### POST /api/research
Start new research session.

**Request:**
```json
{
    "keywords": ["AI", "coding"],
    "max_topics": 20
}
```

**Response:**
```json
{
    "success": true,
    "topics": [...],
    "count": 15
}
```

#### GET /api/topics
Get saved topics with filters.

**Parameters:**
- `days` (int): Days to look back (default: 7)
- `min_score` (float): Minimum score (default: 60)

**Example:**
```
GET /api/topics?days=30&min_score=70
```

**Response:**
```json
{
    "success": true,
    "topics": [...],
    "count": 42
}
```

#### GET /api/analytics
Get research analytics.

**Parameters:**
- `days` (int): Days to analyze (default: 7)

**Response:**
```json
{
    "success": true,
    "analytics": {
        "total_sessions": 10,
        "topics_researched": 250,
        "high_quality_topics": 87,
        "avg_score": 72.5,
        "total_duration": 3600,
        "avg_topics_per_session": 25
    }
}
```

#### POST /api/competitors
Analyze competitor channels.

**Request:**
```json
{
    "channel_ids": [
        "UCxxx",
        "UCyyy"
    ]
}
```

**Response:**
```json
{
    "success": true,
    "analysis": {
        "competitors": [...],
        "best_engagement": "Channel Name",
        "common_themes": [...]
    }
}
```

## Agent Contract (Inter-Agent Communication)

### Input Schema
```json
{
    "action": "research",
    "parameters": {
        "keywords": ["keyword1", "keyword2"],
        "max_topics": 20,
        "filters": {
            "min_score": 70,
            "categories": ["Tutorial", "Review"],
            "competition": "low"
        }
    }
}
```

### Output Schema
```json
{
    "status": "success",
    "agent": "content-researcher",
    "timestamp": "2025-10-22T10:00:00Z",
    "data": {
        "topics": [
            {
                "id": "topic_123",
                "title": "How to Build AI Apps",
                "scores": {
                    "total": 85,
                    "importance": 90,
                    "watchability": 85,
                    "monetization": 80,
                    "popularity": 85,
                    "innovation": 85
                },
                "metadata": {
                    "category": "Tutorial",
                    "keywords": ["AI", "coding"],
                    "angle": "Practical guide...",
                    "competition": "Medium"
                },
                "recommendations": {
                    "best_for": "Script Writer Agent",
                    "timing": "Produce within 7 days",
                    "format": "10-15 minute tutorial"
                }
            }
        ],
        "summary": {
            "total_researched": 50,
            "high_quality": 15,
            "avg_score": 72.5
        }
    }
}
```

## Error Handling

### Error Response Format
```json
{
    "success": false,
    "error": "Error message",
    "code": "ERROR_CODE",
    "details": {
        "field": "Additional info"
    }
}
```

### Common Error Codes
- `AUTH_ERROR`: Authentication failed
- `QUOTA_EXCEEDED`: API quota exceeded
- `INVALID_INPUT`: Invalid parameters
- `NOT_FOUND`: Resource not found
- `INTERNAL_ERROR`: Server error

## Rate Limits

### YouTube API
- 10,000 units per day
- Each search: ~100 units
- Each video detail: ~3 units

### AI API
- Anthropic: 50 requests/minute
- OpenAI: 60 requests/minute

## Webhooks (Future)

### Register Webhook
```python
agent.register_webhook(
    url='https://your-service.com/webhook',
    events=['research_complete', 'high_score_topic']
)
```

### Webhook Payload
```json
{
    "event": "research_complete",
    "timestamp": "2025-10-22T10:00:00Z",
    "data": {
        "session_id": "session_123",
        "topics_count": 15,
        "high_quality_count": 5
    }
}
```

## Integration Examples

### With Script Writer Agent
```python
# In Script Writer Agent
from youtube_topic_researcher.src.main import ContentResearcherAgent

researcher = ContentResearcherAgent()
researcher.initialize()

# Get high-scoring topics
topics = researcher.db.get_topics(min_score=80, days=7)

# Generate scripts for each
for topic in topics:
    script = script_writer.generate(
        title=topic['title'],
        keywords=topic['keywords'],
        angle=topic['recommended_angle']
    )
```

### With SEO Optimizer Agent
```python
# Research → SEO flow
topics = researcher.research_topics(keywords=['AI'])

for topic in topics:
    optimized = seo_optimizer.optimize(
        title=topic['title'],
        keywords=topic['keywords'],
        competition=topic['competition_level']
    )
```

### With Thumbnail Designer Agent
```python
# Get visual context from research
topics = researcher.db.get_topics(min_score=75, category='Tutorial')

for topic in topics:
    thumbnail = designer.create(
        title=topic['title'],
        style='modern',
        keywords=topic['keywords'][:3]
    )
```

## Best Practices

1. **Initialize once**: Reuse agent instance
2. **Handle rate limits**: Implement exponential backoff
3. **Cache results**: Store topics in database
4. **Batch operations**: Process multiple topics together
5. **Error handling**: Always check `success` field
6. **Async operations**: Use background tasks for research
7. **Monitor quota**: Track API usage

## Testing

### Unit Tests
```python
import pytest
from src.main import ContentResearcherAgent

def test_research_topics():
    agent = ContentResearcherAgent()
    agent.initialize()
    
    topics = agent.research_topics(
        keywords=['test'],
        max_topics=5
    )
    
    assert len(topics) <= 5
    assert all('total_score' in t for t in topics)
```

### Integration Tests
```bash
# Test API endpoints
curl http://localhost:8080/api/status
curl -X POST http://localhost:8080/api/research \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["AI"], "max_topics": 5}'
```

---

**For more examples, see USAGE.md**

