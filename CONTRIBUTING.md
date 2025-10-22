# 🤝 Contributing to YouTube Content Researcher

Developer guide for contributing to the project.

---

## 📋 Table of Contents

1. [Development Setup](#development-setup)
2. [Project Architecture](#project-architecture)
3. [API Documentation](#api-documentation)
4. [Testing](#testing)
5. [Debugging](#debugging)
6. [Code Style](#code-style)
7. [Pull Requests](#pull-requests)

---

## 🛠️ Development Setup

### **1. Fork & Clone**
```bash
git clone https://github.com/YOUR_USERNAME/youtube-topic-researcher.git
cd youtube-topic-researcher
```

### **2. Install Dependencies**
```bash
./scripts/setup.sh
source venv/bin/activate
```

### **3. Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

### **4. Run in Development Mode**
```bash
# Run with debug logging
export LOG_LEVEL=DEBUG
./scripts/run_ui.sh
```

---

## 🏗️ Project Architecture

### **Directory Structure**
```
youtube-topic-researcher/
├── src/                      # Core agent logic
│   ├── main.py              # Main orchestrator
│   ├── youtube/             # YouTube API modules
│   │   ├── auth.py          # OAuth2 authentication
│   │   ├── video_analyzer.py  # Video analysis
│   │   ├── trending.py      # Trending discovery
│   │   ├── search.py        # Search & discovery
│   │   └── competitor.py    # Competitor analysis
│   ├── ai/                  # AI modules
│   │   └── topic_evaluator.py  # AI evaluation engine
│   ├── storage/             # Data storage
│   │   └── database.py      # TinyDB wrapper
│   └── utils/               # Utilities
│       └── logger.py        # Logging & display
├── web/                     # Web interface
│   ├── api.py               # Flask API server
│   ├── agent_wrapper.py     # Agent wrapper
│   ├── templates/           # HTML templates
│   └── static/              # CSS & JS
├── config/                  # Configuration
│   ├── settings.yaml        # Agent settings
│   └── research_prompts.yaml  # AI prompts
└── scripts/                 # Setup & run scripts
```

### **Core Components**

#### **1. ContentResearcherAgent** (`src/main.py`)
Main orchestrator that coordinates all components.

```python
from src.main import ContentResearcherAgent

agent = ContentResearcherAgent()
agent.initialize()
topics = agent.research_topics(keywords=['AI'], max_topics=20)
```

#### **2. YouTube Modules** (`src/youtube/`)
- **YouTubeAuth**: OAuth2 authentication
- **VideoAnalyzer**: Video & channel analysis
- **TrendingAnalyzer**: Trending video discovery
- **YouTubeSearch**: Keyword-based search
- **CompetitorAnalyzer**: Competitor intelligence

#### **3. AI Evaluation** (`src/ai/`)
- **TopicEvaluator**: Multi-dimensional AI scoring
- Supports Anthropic (Claude) and OpenAI (GPT)
- Customizable prompts in `config/research_prompts.yaml`

#### **4. Data Storage** (`src/storage/`)
- **ResearchDatabase**: TinyDB wrapper
- Stores topics, sessions, analytics
- Persistent across restarts

---

## 📡 API Documentation

### **Python API**

#### **Initialize Agent**
```python
from src.main import ContentResearcherAgent

agent = ContentResearcherAgent(config_dir="config")
agent.initialize()
```

#### **Research Topics**
```python
topics = agent.research_topics(
    keywords=['AI', 'machine learning'],
    use_trending=False,  # Skip trending videos
    use_ai_generation=True,  # Use AI to generate topics
    max_topics=20
)

# Returns list of dicts with scores
for topic in topics:
    print(f"{topic['title']}: {topic['total_score']}")
```

#### **Access Database**
```python
from src.storage.database import ResearchDatabase

db = ResearchDatabase('data/research.json')

# Get topics
topics = db.get_topics(min_score=70, days=30, limit=100)

# Save topic
db.save_topic({
    'title': 'Topic',
    'total_score': 85,
    ...
})

# Get analytics
analytics = db.get_analytics(days=7)
```

### **REST API**

Base URL: `http://localhost:8080`

#### **GET /api/status**
Check agent status.

**Response:**
```json
{
    "status": "ready",
    "message": "Agent is ready"
}
```

#### **POST /api/research**
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

#### **GET /api/topics**
Get saved topics.

**Parameters:**
- `days` (int): Days to look back (default: 7)
- `min_score` (float): Minimum score (default: 60)

**Example:**
```
GET /api/topics?days=30&min_score=70
```

#### **GET /api/analytics**
Get research analytics.

**Response:**
```json
{
    "success": true,
    "analytics": {
        "total_sessions": 10,
        "topics_researched": 250,
        "high_quality_topics": 87,
        "avg_score": 72.5
    }
}
```

---

## 🧪 Testing

### **Manual Testing**
```bash
# Test CLI
./scripts/run.sh --max-topics 5 --keywords "test"

# Test Web UI
./scripts/run_ui.sh
```

### **Unit Tests** (TODO)
```bash
pytest tests/
```

---

## 🐛 Debugging

### **Common Issues**

#### **1. Database Corruption**
**Symptom**: `'list' object has no attribute 'items'`

**Fix**:
```bash
# Delete corrupted database
rm data/research.json

# Let TinyDB recreate it (proper structure)
echo '{"_default": {}, "topics": {}, "sessions": {}, "trends": {}}' > data/research.json
```

**Why**: TinyDB expects dict tables (`{}`), not lists (`[]`)

#### **2. Datetime Comparison Error**
**Symptom**: `can't compare offset-naive and offset-aware datetimes`

**Fix**: Use timezone-aware datetimes:
```python
from datetime import datetime, timezone
cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
```

#### **3. Content Filtering Not Working**
**Check**: `src/main.py` line ~391 (blacklist) and ~404 (whitelist)

**Customize**:
```python
# Add your own filters
irrelevant_keywords = [
    'music video', 'gaming',
    'your_custom_filter'  # Add here
]
```

### **Debug Logging**
```bash
# Enable debug mode
export LOG_LEVEL=DEBUG
./scripts/run_ui.sh

# Check logs
tail -f logs/researcher.log
```

---

## 🎨 Code Style

### **Python**
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Max line length: 100 characters

```python
def example_function(param: str, count: int = 10) -> List[dict]:
    """
    Brief description.
    
    Args:
        param: Description
        count: Description
        
    Returns:
        Description
    """
    pass
```

### **JavaScript**
- Use ES6+ features
- Camel case for variables
- Add JSDoc comments

```javascript
/**
 * Brief description
 * @param {string} param - Description
 * @returns {Promise<Object>} Description
 */
async function exampleFunction(param) {
    // ...
}
```

---

## 🔄 Pull Request Process

### **1. Create PR**
- Clear title describing the change
- Reference any related issues
- Include screenshots for UI changes

### **2. PR Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### **3. Review Process**
- Code review by maintainer
- All checks must pass
- Squash and merge to main

---

## 📚 Key Design Decisions

### **1. Content Filtering**
- **Why**: Trending videos are dominated by music, gaming, entertainment
- **How**: Blacklist + whitelist system in `_is_relevant_to_channel()`
- **Customize**: Edit keywords in `src/main.py`

### **2. TinyDB vs PostgreSQL**
- **Why TinyDB**: Simple, no setup, JSON-based, perfect for single-user
- **Trade-off**: Not suitable for multi-user or high-concurrency
- **Future**: Could migrate to PostgreSQL for production

### **3. AI Provider Support**
- **Anthropic (Claude)**: Better at nuanced evaluation, recommended
- **OpenAI (GPT)**: Alternative option, similar results
- **Extensible**: Easy to add more providers

---

## 🎯 Contribution Ideas

### **Features to Add**
- [ ] Unit tests (pytest)
- [ ] Favoriting/starring topics
- [ ] Topic categories/tags
- [ ] A/B title testing suggestions
- [ ] Integration with other agents
- [ ] Multi-channel support
- [ ] Scheduled research jobs
- [ ] Webhook notifications

### **Improvements Needed**
- [ ] Better error handling
- [ ] Performance optimization
- [ ] Caching layer
- [ ] Rate limit handling
- [ ] UI/UX enhancements

---

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/wvlt/youtube-topic-researcher/issues)
- **Discussions**: Use GitHub Discussions
- **Documentation**: Check README, SETUP, USAGE

---

**Thank you for contributing!** 🙏

