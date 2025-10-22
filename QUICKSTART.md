# 🚀 Quick Start - Get Running in 5 Minutes!

## Prerequisites Check

Before you start, ensure you have:
- ✅ Python 3.9+ installed
- ✅ Anthropic API key (get from https://console.anthropic.com/)
- ✅ Google Cloud project with YouTube Data API enabled

---

## Step 1: Setup (2 minutes)

```bash
cd /Users/amircharkhi/Documents/projects/agentic-ai/youtube-topic-researcher

# Run automated setup
./scripts/setup.sh
```

This will:
- Create virtual environment
- Install all dependencies
- Create necessary directories
- Copy environment template

---

## Step 2: Configure API Keys (2 minutes)

### Edit .env file:
```bash
nano .env
# or
code .env
```

### Add your keys:
```env
CHANNEL_ID=UCHSCEq2xAxnBnZhr5uDtk1A
ANTHROPIC_API_KEY=sk-ant-xxxxx    # ← ADD YOUR KEY HERE
AI_PROVIDER=anthropic
AI_MODEL=claude-3-5-sonnet-20241022
```

### Add YouTube OAuth credentials:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable YouTube Data API v3
3. Create OAuth 2.0 credentials (Desktop app)
4. Download JSON and save as: `config/client_secrets.json`

---

## Step 3: First Run (1 minute)

### Option A: Command Line (Fastest)
```bash
source venv/bin/activate
python -m src.main
```

On first run, you'll authenticate with Google (browser opens automatically).

### Option B: Web UI (Recommended)
```bash
./scripts/run_ui.sh
```

Then open: **http://localhost:8080**

---

## Quick Test Commands

```bash
# View analytics (no research, just check agent status)
./scripts/run.sh --analytics

# Quick research (10 topics)
./scripts/run.sh --max-topics 10

# Full research with details
./scripts/run.sh --details

# Custom keywords
./scripts/run.sh -k "AI" -k "coding" --max-topics 20
```

---

## Your First Research Session

### In Web UI:
1. ✅ Check status indicator is green ("Ready")
2. ✅ Enter keywords (optional): `AI, coding, tutorial`
3. ✅ Set max topics: `15`
4. ✅ Click "Start Research" 🚀
5. ✅ Wait 2-3 minutes
6. ✅ Review results!

### What You'll Get:
- 🎯 15 researched topics
- 📊 Scores for each (0-100)
- 💡 AI recommendations
- 🔑 Keywords for SEO
- 📈 Competition analysis

---

## Understanding Your Results

### Topic Scores:
- **80-100** 🟢 Excellent! High priority
- **60-79** 🟡 Good potential
- **40-59** 🟠 Moderate, evaluate carefully
- **0-39** 🔴 Low priority

### Click Any Topic For:
- Full AI analysis
- Recommended content angle
- Target keywords
- Competition level
- Strategic notes

---

## Next Steps After First Research

### 1. Export Topics
```bash
./scripts/run.sh --export my-topics.csv --days 7
```

### 2. Schedule Weekly Research
Add to crontab:
```bash
# Every Monday at 9 AM
0 9 * * 1 cd /path/to/youtube-topic-researcher && ./scripts/run.sh --max-topics 30
```

### 3. Integrate with Other Agents
Feed topics to:
- SEO Optimizer Agent
- Title Generator Agent
- Script Writer Agent

### 4. Track Performance
```bash
# View weekly analytics
./scripts/run.sh --analytics --days 7

# View monthly trends
./scripts/run.sh --analytics --days 30
```

---

## Troubleshooting Quick Fixes

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Credentials file not found"
- Ensure `config/client_secrets.json` exists
- Check file is valid JSON
- Verify it's in the `config/` directory

### "API key invalid"
- Check `.env` file has no extra spaces
- Verify key is correct
- Try regenerating key

### "Quota exceeded"
- YouTube API limit: 10,000 units/day
- Resets at midnight Pacific Time
- Enable `smart_mode: true` in settings

### Browser doesn't open for OAuth
```bash
python -c "from src.youtube.auth import YouTubeAuth; YouTubeAuth().authenticate()"
```

---

## Common Use Cases

### Daily Quick Check
```bash
./scripts/run.sh --max-topics 10
```
**Time**: 1-2 minutes  
**Use**: Quick trend check

### Weekly Planning
```bash
./scripts/run.sh --max-topics 30 --details
```
**Time**: 4-5 minutes  
**Use**: Content calendar planning

### Comprehensive Research
```bash
./scripts/run.sh -k "keyword1" -k "keyword2" -k "keyword3" --max-topics 50 --details
```
**Time**: 8-10 minutes  
**Use**: Monthly deep dive

---

## Pro Tips

### 1. Use Specific Keywords
❌ Bad: "video"  
✅ Good: "AI tutorial", "coding interview"

### 2. Mix Trending + Evergreen
```bash
./scripts/run.sh -k "AI news" -k "Python basics" -k "coding tips"
```

### 3. Focus on High Scores
Filter results by score 80+ for immediate production.

### 4. Check Competition
Low competition + High score = Golden opportunity!

### 5. Use Recommended Angles
AI provides unique angles - use them!

---

## File Locations

- **Results**: `data/research.json`
- **Logs**: `logs/researcher.log`
- **Config**: `config/settings.yaml`
- **Environment**: `.env`

---

## Getting Help

### Check Logs
```bash
tail -f logs/researcher.log
```

### Enable Debug Mode
Edit `.env`:
```env
LOG_LEVEL=DEBUG
```

### Review Documentation
- `README.md` - Overview
- `SETUP.md` - Detailed setup
- `USAGE.md` - Usage examples
- `API.md` - API documentation

---

## Success Checklist

After first run, you should have:
- ✅ Agent initialized successfully
- ✅ YouTube authentication complete
- ✅ Topics discovered and evaluated
- ✅ Results visible in UI or CLI
- ✅ Data saved to database
- ✅ Analytics showing session data

---

## Example Output

```
🎯 Content Researcher
═══════════════════════════════════════════════════════

✅ Agent initialized successfully!

📊 Phase 1: Topic Discovery
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ️  Found 15 trending topics
ℹ️  Found 23 search-based topics
ℹ️  Generated 10 AI topics

📊 Phase 2: AI Evaluation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Evaluating 20 topics...

📊 Research Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━┓
┃ Rank┃ Topic               ┃ Score┃ Category   ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━┩
│  1  │ How to Build AI... │  87  │ Tutorial   │
│  2  │ Advanced Python... │  84  │ Tutorial   │
│  3  │ AI Trends 2025...  │  82  │ News       │
└─────┴─────────────────────┴──────┴────────────┘

✅ Research Session Complete!
Topics Researched: 20
High Quality Topics: 8
Duration: 185.3s
```

---

## What's Next?

### Immediate
1. ✅ Run your first research
2. ✅ Review top 5 topics
3. ✅ Select 2-3 for production

### This Week
1. Schedule weekly research
2. Integrate with other agents
3. Track actual performance vs predicted

### This Month
1. Build remaining agents
2. Complete agent ecosystem
3. Automate content pipeline
4. Measure ROI

---

## 🎉 You're Ready!

Everything is set up and ready to go. Your YouTube content research is about to become:
- 📊 **Data-driven** instead of guesswork
- ⚡ **10x faster** (2 hours → 15 minutes)
- 🎯 **More accurate** with AI insights
- 🔄 **Automated** and scalable

**Run your first research now!**

```bash
./scripts/run_ui.sh
```

**Happy researching! 🚀**

