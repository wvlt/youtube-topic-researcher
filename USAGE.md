# Usage Guide - YouTube Content Researcher Agent

## Quick Start Examples

### 1. Basic Research (Automatic)
```bash
./scripts/run.sh
```
- Analyzes your channel
- Discovers trending topics
- Generates AI topic ideas
- Evaluates all topics
- Shows top results

### 2. Research with Keywords
```bash
./scripts/run.sh --keywords "AI" "machine learning" "tutorial"
```
- Uses your seed keywords
- Finds related topics
- Expands with variations

### 3. Detailed Analysis
```bash
./scripts/run.sh --details
```
- Shows top 5 topics with full details
- Includes AI analysis
- Shows recommended angles
- Lists keywords

### 4. Quick Research (Limited)
```bash
./scripts/run.sh --max-topics 10
```
- Faster execution
- Evaluates only 10 topics
- Good for quick checks

## Command Line Options

```bash
./scripts/run.sh [OPTIONS]

Options:
  --keywords, -k TEXT     Seed keywords (can use multiple times)
  --max-topics INTEGER    Maximum topics to research (default: 50)
  --details              Show detailed analysis for top topics
  --analytics            Show analytics and exit
  --export PATH          Export topics to CSV file
  --days INTEGER         Days for analytics/export (default: 7)
  --help                 Show help message
```

## Web UI Usage

### Starting the UI
```bash
./scripts/run_ui.sh
# Open http://localhost:8080
```

### UI Features

#### 1. Research Panel
- **Keywords**: Optional seed keywords (comma-separated)
- **Max Topics**: Number of topics to research (5-100)
- **Start Research**: Begins discovery process
- Real-time status updates

#### 2. Results Panel
- **Filter by Days**: Show topics from last N days
- **Min Score**: Filter by minimum score
- **Refresh**: Reload latest data
- Click any topic for detailed view

#### 3. Topic Cards
Each card shows:
- Topic title
- Total score (0-100)
- Category
- Competition level
- 5 dimension scores

#### 4. Topic Detail Modal
Click any topic to see:
- Full AI analysis
- Recommended angle
- Keywords
- Detailed scores
- Strategic notes
- Timestamp

#### 5. Analytics Dashboard
Shows:
- Total research sessions
- Topics researched
- High-quality topic count
- Average score

## Workflow Examples

### Weekly Content Planning

**Monday Morning Routine:**
```bash
# 1. Run comprehensive research
./scripts/run.sh --details

# 2. Review top topics in UI
./scripts/run_ui.sh

# 3. Export for team review
./scripts/run.sh --export weekly-topics.csv --days 7

# 4. Select 2-3 topics for week
# 5. Feed to Script Writer Agent
```

### Competitor Analysis

```python
# Use programmatically
from src.main import ContentResearcherAgent

agent = ContentResearcherAgent()
agent.initialize()

# Analyze competitors
competitors = [
    'UCcompetitor1',
    'UCcompetitor2',
    'UCcompetitor3'
]

analysis = agent.analyze_competitors(competitors)
print(analysis['common_themes'])
print(analysis['best_engagement'])
```

### Trend Monitoring

**Daily Quick Check:**
```bash
# Check trending topics only
./scripts/run.sh --max-topics 15

# View recent high-quality topics
./scripts/run.sh --analytics --days 1
```

### Content Calendar Planning

**Monthly Planning:**
```bash
# Research with diverse keywords
./scripts/run.sh -k "tutorial" -k "review" -k "comparison" -k "tips" --max-topics 40 --details

# Export full month data
./scripts/run.sh --export content-calendar-$(date +%Y%m).csv --days 30
```

## Understanding Scores

### Total Score Ranges
- **80-100**: Excellent opportunity! High priority
- **60-79**: Good potential, worth considering
- **40-59**: Moderate potential, evaluate carefully
- **0-39**: Low potential, likely skip

### Dimension Scores

#### Importance (25% weight)
- 90-100: Perfect fit for channel
- 70-89: Good alignment
- 50-69: Somewhat relevant
- <50: Off-topic

#### Watchability (20% weight)
- 90-100: Highly engaging content
- 70-89: Good entertainment value
- 50-69: Moderate interest
- <50: Low engagement potential

#### Monetization (20% weight)
- 90-100: High CPM + sponsorship potential
- 70-89: Good ad revenue potential
- 50-69: Average monetization
- <50: Limited revenue potential

#### Popularity (20% weight)
- 90-100: Viral/trending now
- 70-89: Popular and growing
- 50-69: Steady interest
- <50: Niche or declining

#### Innovation (15% weight)
- 90-100: Cutting-edge, unique angle
- 70-89: Fresh perspective
- 50-69: Some uniqueness
- <50: Saturated topic

## Advanced Usage

### Custom Configuration

Edit `config/settings.yaml`:
```yaml
research_criteria:
  # Adjust weights for your priorities
  importance_weight: 0.30      # Prioritize relevance
  monetization_weight: 0.25    # Focus on revenue
  popularity_weight: 0.15      # Less trend-chasing
  
  min_total_score: 70          # Higher quality bar
```

### Automated Scheduling

**Linux/Mac Cron:**
```bash
# Edit crontab
crontab -e

# Add weekly Monday 9 AM research
0 9 * * 1 cd /path/to/youtube-topic-researcher && ./scripts/run.sh --export ~/research-$(date +\%Y\%m\%d).csv

# Add daily quick check
0 8 * * * cd /path/to/youtube-topic-researcher && ./scripts/run.sh --max-topics 10
```

**GitHub Actions (for teams):**
```yaml
name: Weekly Research
on:
  schedule:
    - cron: '0 9 * * 1'
jobs:
  research:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Research
        run: ./scripts/run.sh --export topics.csv
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: research-topics
          path: topics.csv
```

### Integration with Other Agents

#### 1. Feed to SEO Optimizer
```bash
# Export high-scoring topics
./scripts/run.sh --export seo-topics.csv --days 7

# Use in SEO Optimizer Agent
cd ../seo-optimizer-agent
./scripts/optimize.sh --input ../youtube-topic-researcher/seo-topics.csv
```

#### 2. Script Writer Integration
```python
# In Script Writer Agent
from youtube_topic_researcher.src.storage.database import ResearchDatabase

db = ResearchDatabase()
topics = db.get_topics(min_score=80, days=7)

for topic in topics:
    script = generate_script(
        title=topic['title'],
        angle=topic['recommended_angle'],
        keywords=topic['keywords']
    )
```

#### 3. Title Generator
```python
# Use researched topics for title generation
topics = db.get_topics(min_score=75, category='Tutorial')

for topic in topics:
    titles = generate_titles(
        base_topic=topic['title'],
        keywords=topic['keywords'],
        angle=topic['recommended_angle']
    )
```

## Best Practices

### 1. Research Frequency
- **Daily**: Quick checks (10-15 topics)
- **Weekly**: Full research (40-50 topics)
- **Monthly**: Comprehensive + export

### 2. Topic Selection
- Focus on 80+ scores for immediate production
- Bank 70-79 scores for future content
- Use 60-69 scores as inspiration

### 3. Keyword Strategy
- Start broad: "AI", "coding"
- Use channel themes
- Mix trending + evergreen
- Test variations

### 4. Quality Control
- Read full AI analysis
- Check competition level
- Verify alignment with channel
- Consider production capability

### 5. Data Management
- Export monthly for records
- Archive old research
- Track which topics produced
- Measure actual performance vs predicted

## Troubleshooting

### Slow Research
**Problem**: Takes too long
**Solutions**:
- Reduce `--max-topics`
- Disable AI generation in settings
- Use faster AI model
- Check internet connection

### Low Quality Topics
**Problem**: All scores below 60
**Solutions**:
- Adjust weights in settings
- Use better seed keywords
- Check channel context accuracy
- Increase research scope

### Duplicate Topics
**Problem**: Same topics repeatedly
**Solutions**:
- Clear old topics: `rm data/research.json`
- Adjust deduplication logic
- Use different keywords
- Increase time range

### API Quota Issues
**Problem**: "Quota exceeded"
**Solutions**:
- Enable `smart_mode: true`
- Reduce `max_results`
- Wait until quota resets
- Request quota increase

## Tips & Tricks

### 1. Maximize Discovery
```bash
# Use multiple keyword variations
./scripts/run.sh \
  -k "tutorial" -k "how to" \
  -k "guide" -k "tips" \
  -k "explained" \
  --max-topics 50
```

### 2. Find Trending Topics
- Run during trending hours (US: 2-6 PM EST)
- Check results immediately
- Compare with previous day

### 3. Competitive Intelligence
```bash
# Export competitor analysis
python -c "
from src.main import ContentResearcherAgent
agent = ContentResearcherAgent()
agent.initialize()
analysis = agent.analyze_competitors(['UC...', 'UC...'])
print(analysis)
"
```

### 4. Track Success Rate
```bash
# View analytics trends
./scripts/run.sh --analytics --days 30
./scripts/run.sh --analytics --days 7

# Compare week over week
```

### 5. Build Topic Library
```bash
# Monthly export
./scripts/run.sh --export topics-$(date +%Y%m).csv --days 30

# Combine all months
cat topics-*.csv > topic-library.csv
```

## Next Steps

1. Run your first research session
2. Review top 10 topics
3. Select 2-3 for production
4. Track performance
5. Refine configuration
6. Integrate with other agents

---

**Need Help?**
- Check logs: `tail -f logs/researcher.log`
- Review README.md
- See SETUP.md for configuration
- Test with `--analytics` first

