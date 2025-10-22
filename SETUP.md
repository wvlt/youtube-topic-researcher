# Setup Guide - YouTube Content Researcher Agent

## Prerequisites

### 1. System Requirements
- Python 3.9 or higher
- pip (Python package manager)
- Git
- 4GB RAM minimum
- Internet connection

### 2. API Keys Required

#### YouTube Data API (Required)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **YouTube Data API v3**
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Choose "Desktop app" as application type
6. Download credentials JSON file
7. Save as `config/client_secrets.json`

**Important**: Keep this file secure and never commit to Git!

#### Anthropic API (Required - Recommended) OR OpenAI API
**Option A: Anthropic (Recommended)**
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create account / Sign in
3. Navigate to API Keys
4. Create new API key
5. Copy key for `.env` file

**Option B: OpenAI**
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create account / Sign in
3. Navigate to API Keys
4. Create new API key
5. Copy key for `.env` file

## Installation Steps

### Step 1: Clone/Navigate to Project
```bash
cd /Users/amircharkhi/Documents/projects/agentic-ai/youtube-topic-researcher
```

### Step 2: Run Setup Script
```bash
chmod +x scripts/setup.sh scripts/run.sh scripts/run_ui.sh
./scripts/setup.sh
```

This will:
- Create virtual environment
- Install all dependencies
- Create necessary directories
- Copy `.env.example` to `.env`

### Step 3: Configure Environment
```bash
nano .env
# or
code .env
```

Required configuration:
```env
# Your YouTube Channel ID
CHANNEL_ID=UCHSCEq2xAxnBnZhr5uDtk1A

# AI Provider (anthropic or openai)
AI_PROVIDER=anthropic
AI_MODEL=claude-3-5-sonnet-20241022

# API Keys
ANTHROPIC_API_KEY=sk-ant-xxxxx
# OR
OPENAI_API_KEY=sk-xxxxx

# Optional Settings
RESEARCH_MODE=comprehensive
MAX_TOPICS_PER_RUN=50
DATABASE_PATH=data/research.json
```

### Step 4: Add YouTube Credentials
1. Download OAuth2 credentials from Google Cloud Console
2. Save as `config/client_secrets.json`
3. Format should be:
```json
{
  "installed": {
    "client_id": "xxxxx.apps.googleusercontent.com",
    "project_id": "your-project",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_secret": "xxxxx",
    ...
  }
}
```

### Step 5: First Run - OAuth Authentication
```bash
source venv/bin/activate
python -m src.main
```

On first run:
1. Browser will open for Google OAuth
2. Sign in with your YouTube account
3. Grant permissions
4. Token will be saved as `token.pickle`

## Verification

### Test CLI
```bash
./scripts/run.sh --analytics
```

Should show:
```
YouTube Content Researcher Agent
Agent initialized successfully!
Analytics - Last 7 Days
...
```

### Test Web UI
```bash
./scripts/run_ui.sh
```

Then open: http://localhost:8080

Should see:
- ✅ "Ready" status indicator
- Research form
- Analytics dashboard

## Configuration Files

### config/settings.yaml
Main agent configuration:
- Research criteria weights
- API limits
- Filter rules
- Content preferences

### config/research_prompts.yaml
AI prompts for topic evaluation. Customize to match your channel's needs.

## Troubleshooting

### "Module not found" error
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Credentials file not found"
- Ensure `config/client_secrets.json` exists
- Check file permissions
- Verify JSON format

### "API key invalid"
- Check `.env` file exists
- Verify API key is correct
- Check for extra spaces/newlines

### "YouTube API quota exceeded"
- Daily quota: 10,000 units
- Each search: ~100 units
- Reset at midnight Pacific Time
- Use `smart_mode: true` in settings.yaml

### OAuth browser doesn't open
```bash
# Manual OAuth
python -c "from src.youtube.auth import YouTubeAuth; YouTubeAuth().authenticate()"
```

## Directory Structure

After setup, you should have:
```
youtube-topic-researcher/
├── venv/                    # Virtual environment
├── config/
│   ├── client_secrets.json  # YouTube OAuth (you add this)
│   ├── settings.yaml        # Agent settings
│   └── research_prompts.yaml
├── data/                    # Research data (created)
│   └── research.json
├── logs/                    # Log files (created)
│   └── researcher.log
├── .env                     # Environment vars (you configure)
└── token.pickle            # OAuth token (auto-created)
```

## Next Steps

1. **Run first research**:
   ```bash
   ./scripts/run.sh --details
   ```

2. **Use Web UI**:
   ```bash
   ./scripts/run_ui.sh
   ```

3. **Schedule regular research**:
   ```bash
   # Add to crontab for weekly research
   0 9 * * 1 cd /path/to/youtube-topic-researcher && ./scripts/run.sh
   ```

4. **Integrate with other agents**:
   - Export topics: `./scripts/run.sh --export topics.csv`
   - Use topics in Script Writer Agent
   - Feed to SEO Optimizer Agent

## Security Best Practices

1. **Never commit secrets**:
   - `.env` is in `.gitignore`
   - `config/client_secrets.json` is ignored
   - `token.pickle` is ignored

2. **Rotate API keys** periodically

3. **Use environment-specific configs**:
   - Development: `.env.development`
   - Production: `.env.production`

4. **Backup research data**:
   ```bash
   cp data/research.json backups/research-$(date +%Y%m%d).json
   ```

## Getting Help

1. Check logs: `tail -f logs/researcher.log`
2. Run with debug: Edit `.env` → `LOG_LEVEL=DEBUG`
3. Review README.md for usage examples
4. Check existing youtube-comment-agent for patterns

## Performance Tips

1. **Optimize quota usage**:
   - Enable `smart_mode: true`
   - Reduce `max_results` in settings
   - Use cached data when possible

2. **Speed up AI evaluation**:
   - Use `max_topics` parameter
   - Run during off-peak hours
   - Consider batch processing

3. **Database management**:
   - Archive old topics periodically
   - Export to CSV for analysis
   - Keep database under 10MB

## Upgrade Path

When new versions are released:
```bash
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

**Setup Complete!** 🎉

You're ready to start discovering high-potential content topics for your YouTube channel.

