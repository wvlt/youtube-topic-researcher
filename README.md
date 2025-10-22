# 🎯 YouTube Content Researcher Agent

An AI-powered content research agent that discovers trending, monetizable, and high-potential topics for YouTube creators. Built with Claude AI and YouTube Data API.

## 🌟 Features

### Multi-Dimensional Topic Evaluation
- **Importance Score** (0-100): Relevance to channel niche and audience
- **Watchability Score** (0-100): Entertainment and engagement potential
- **Monetization Score** (0-100): Revenue potential (ads, sponsors, products)
- **Popularity Score** (0-100): Current trend momentum
- **Innovation Score** (0-100): Uniqueness and cutting-edge appeal

### Intelligent Discovery
- 🔥 Trending video analysis
- 🔍 Keyword-based search discovery
- 🤖 AI-generated topic ideas
- 📊 Competitor channel analysis
- 📈 Performance metrics tracking

### Beautiful Command Center UI
- Real-time research dashboard
- Interactive topic cards with detailed analytics
- Session analytics and insights
- Export capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- YouTube Data API credentials
- Anthropic API key (or OpenAI)

### Installation

1. **Clone and setup**
```bash
cd /path/to/youtube-topic-researcher
chmod +x scripts/setup.sh
./scripts/setup.sh
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required in `.env`:
```env
CHANNEL_ID=UCHSCEq2xAxnBnZhr5uDtk1A
ANTHROPIC_API_KEY=your-key-here
AI_PROVIDER=anthropic
AI_MODEL=claude-3-5-sonnet-20241022
```

3. **Get YouTube OAuth2 Credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project and enable YouTube Data API v3
   - Create OAuth2 credentials (Desktop app)
   - Download as `config/client_secrets.json`

### Run the Agent

#### Command Line Interface
```bash
# Basic research
./scripts/run.sh

# With specific keywords
./scripts/run.sh --keywords "AI" "coding" "tutorial"

# Show detailed analysis
./scripts/run.sh --details

# View analytics
./scripts/run.sh --analytics --days 30

# Export topics
./scripts/run.sh --export topics.csv --days 30
```

#### Web UI (Recommended)
```bash
./scripts/run_ui.sh
# Open http://localhost:8080
```

## 📊 How It Works

### Phase 1: Discovery
1. **Channel Analysis**: Analyzes your channel's content, performance, and niche
2. **Trend Discovery**: Finds trending videos in your niche
3. **Search Research**: Discovers popular topics via keyword search
4. **AI Generation**: Uses AI to generate unique topic ideas

### Phase 2: AI Evaluation
Each topic is evaluated by Claude AI across 5 dimensions:
- Importance (25% weight)
- Watchability (20% weight)
- Monetization (20% weight)
- Popularity (20% weight)
- Innovation (15% weight)

### Phase 3: Prioritization
- Topics are filtered by minimum score (default: 60/100)
- Sorted by total weighted score
- Saved to database with full analysis

## 🎯 Use Cases

### For Content Creators
- Discover trending topics before they peak
- Find monetizable content opportunities
- Identify content gaps in your niche
- Plan content calendar with data

### For Content Strategists
- Analyze competitor strategies
- Track trending themes
- Evaluate content potential
- Export data for reporting

### For Agency Teams
- Research multiple channels
- Bulk topic discovery
- Performance tracking
- Client reporting

## 📁 Project Structure

```
youtube-topic-researcher/
├── src/
│   ├── main.py                 # Main agent orchestrator
│   ├── youtube/                # YouTube API modules
│   │   ├── auth.py            # Authentication
│   │   ├── video_analyzer.py  # Video analysis
│   │   ├── trending.py        # Trending discovery
│   │   ├── search.py          # Search & discovery
│   │   └── competitor.py      # Competitor analysis
│   ├── ai/                    # AI modules
│   │   └── topic_evaluator.py # AI evaluation engine
│   ├── storage/               # Data storage
│   │   └── database.py        # TinyDB wrapper
│   └── utils/                 # Utilities
│       └── logger.py          # Logging & display
├── web/                       # Web interface
│   ├── api.py                 # Flask API server
│   ├── agent_wrapper.py       # Agent wrapper
│   ├── templates/             # HTML templates
│   └── static/                # CSS & JS
├── config/                    # Configuration
│   ├── settings.yaml          # Agent settings
│   └── research_prompts.yaml  # AI prompts
├── data/                      # Research data
└── logs/                      # Log files
```

## ⚙️ Configuration

### settings.yaml
Customize research behavior:
```yaml
research_criteria:
  importance_weight: 0.25
  watchability_weight: 0.20
  monetization_weight: 0.20
  popularity_weight: 0.20
  innovation_weight: 0.15
  min_total_score: 60
```

### research_prompts.yaml
Customize AI evaluation prompts for your needs.

## 🔄 Integration with Other Agents

This agent is designed to work with your agent ecosystem:

### 1. SEO Optimizer Agent
- Receives high-scoring topics with keywords
- Optimizes titles, descriptions, tags

### 2. Title/Hook Generator Agent
- Uses researched topics and angles
- Generates compelling titles

### 3. Script Writer Agent
- Receives topic briefs with AI analysis
- Generates scripts based on recommended angles

### 4. Thumbnail Designer Agent
- Gets topic context and keywords
- Creates relevant thumbnails

## 📊 API Endpoints

### Web API
```
GET  /api/status              - Agent status
POST /api/research            - Start research session
GET  /api/topics              - Get saved topics
GET  /api/analytics           - Get analytics
POST /api/competitors         - Analyze competitors
```

### Agent Contract (Minimal)
```python
# Input
{
    "keywords": ["AI", "coding"],
    "max_topics": 20
}

# Output
{
    "topics": [
        {
            "title": "Topic title",
            "total_score": 85,
            "importance_score": 90,
            "watchability_score": 85,
            "monetization_score": 80,
            "popularity_score": 85,
            "innovation_score": 80,
            "keywords": ["keyword1", "keyword2"],
            "recommended_angle": "Unique approach...",
            "competition_level": "Medium",
            "category": "Tutorial"
        }
    ]
}
```

## 📈 Analytics & Tracking

The agent tracks:
- Total research sessions
- Topics researched
- High-quality topic count
- Average scores
- Research duration
- Success rates

Access via:
- Web UI analytics panel
- CLI: `--analytics` flag
- Database: `data/research.json`

## 🤝 Contributing

This is part of the Amir Charkhi agent ecosystem. Focus areas:
- [ ] Advanced trend prediction
- [ ] More data sources (Twitter, Reddit, etc.)
- [ ] Multi-channel support
- [ ] A/B testing recommendations
- [ ] Thumbnail effectiveness prediction

## 📝 License

MIT License - See LICENSE file

## 🎯 Roadmap

### Phase 1 (Complete) ✅
- [x] Multi-dimensional topic evaluation
- [x] YouTube API integration
- [x] AI-powered analysis
- [x] Web UI
- [x] Basic analytics

### Phase 2 (Next)
- [ ] Competitor tracking automation
- [ ] Trend prediction (30/60/90 days)
- [ ] Integration with other agents
- [ ] Advanced filtering
- [ ] Batch processing

### Phase 3 (Future)
- [ ] Multi-channel management
- [ ] Social media integration
- [ ] Content calendar planning
- [ ] A/B testing insights
- [ ] Machine learning optimization

## 💡 Tips

1. **Run regularly**: Research weekly to stay ahead of trends
2. **Use filters**: Focus on high-score topics (80+)
3. **Analyze competitors**: Learn from successful channels
4. **Mix sources**: Combine trending + AI-generated topics
5. **Export data**: Keep records for content planning

## 🐛 Troubleshooting

### "Agent not initialized"
- Check API keys in `.env`
- Verify `config/client_secrets.json` exists
- Run OAuth flow

### "Quota exceeded"
- YouTube API has daily quotas
- Use smart_mode in settings.yaml
- Reduce max_topics

### "AI evaluation slow"
- Normal for Claude API
- Each topic takes ~3-5 seconds
- Use max_topics to limit

## 📞 Support

For issues or questions:
- Check logs in `logs/`
- Review configuration in `config/`
- See example: `/youtube-comment-agent`

## 🎉 Built With

- **Claude AI**: Multi-dimensional topic evaluation
- **YouTube Data API**: Video and trend data
- **Flask**: Web API server
- **TinyDB**: Lightweight data storage
- **Rich**: Beautiful terminal output

---

**Part of the Amir Charkhi Agent Ecosystem**
Priority Agent #6 | Content Researcher Agent | Saves 2 hrs/week

Next: SEO Optimizer, Title Generator, Script Writer

