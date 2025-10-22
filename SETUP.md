# 🛠️ Setup Guide

Complete installation and configuration guide for the YouTube Content Researcher Agent.

---

## 📋 Prerequisites

### **System Requirements**
- Python 3.9 or higher
- pip (Python package manager)
- Git
- 4GB RAM minimum
- Internet connection

### **API Keys Required**

#### **1. YouTube Data API** (Required)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **YouTube Data API v3**
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Choose "Desktop app" as application type
6. Download credentials JSON file
7. Save as `config/client_secrets.json`

**Keep this file secure - never commit to Git!**

#### **2. Anthropic API** (Recommended) OR OpenAI API

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

---

## 🚀 Installation

### **Step 1: Clone Repository**
```bash
cd /path/to/your/projects
git clone https://github.com/wvlt/youtube-topic-researcher.git
cd youtube-topic-researcher
```

### **Step 2: Run Setup Script**
```bash
chmod +x scripts/*.sh
./scripts/setup.sh
```

This will:
- Create virtual environment (`venv/`)
- Install all dependencies
- Create necessary directories (`data/`, `logs/`)
- Copy `.env.example` to `.env`

### **Step 3: Configure Environment**
```bash
# Edit the .env file
nano .env
# or
code .env
```

Required configuration:
```env
# Your YouTube Channel ID
# Find it at: https://www.youtube.com/account_advanced
CHANNEL_ID=UCHSCEq2xAxnBnZhr5uDtk1A

# AI Provider (anthropic or openai)
AI_PROVIDER=anthropic
AI_MODEL=claude-3-5-sonnet-20241022

# Add your API key
ANTHROPIC_API_KEY=sk-ant-xxxxx
# OR
OPENAI_API_KEY=sk-xxxxx

# Optional Settings
RESEARCH_MODE=comprehensive
MAX_TOPICS_PER_RUN=50
DATABASE_PATH=data/research.json
LOG_LEVEL=INFO
```

### **Step 4: Add YouTube Credentials**
1. Download OAuth2 credentials from Google Cloud Console (see Prerequisites)
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
    "redirect_uris": ["http://localhost"]
  }
}
```

### **Step 5: First Run - OAuth Authentication**
```bash
source venv/bin/activate
python -m src.main
```

On first run:
1. Browser will open for Google OAuth
2. Sign in with your YouTube account
3. Grant permissions
4. Token will be saved as `token.pickle`

---

## ✅ Verification

### **Test CLI**
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

### **Test Web UI**
```bash
./scripts/run_ui.sh
```

Then open: http://localhost:8080

Should see:
- ✅ "Ready" status indicator
- Research form
- Analytics dashboard

---

## 🐛 Troubleshooting

### **"Module not found" error**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### **"Credentials file not found"**
- Ensure `config/client_secrets.json` exists
- Check file permissions
- Verify JSON format is correct

### **"API key invalid"**
- Check `.env` file exists
- Verify API key is correct
- Check for extra spaces/newlines in the key

### **"YouTube API quota exceeded"**
- Daily quota: 10,000 units
- Each search: ~100 units
- Reset at midnight Pacific Time
- Use `smart_mode: true` in settings.yaml to reduce usage

### **OAuth browser doesn't open**
```bash
# Manual OAuth
python -c "from src.youtube.auth import YouTubeAuth; YouTubeAuth().authenticate()"
```

### **Port 8080 already in use**
```bash
# Find and kill the process
lsof -ti:8080 | xargs kill -9

# Or change port in web/api.py
app.run(port=8081)  # Change to 8081 or any available port
```

---

## 📁 Directory Structure

After setup, you should have:
```
youtube-topic-researcher/
├── venv/                    # Virtual environment
├── config/
│   ├── client_secrets.json  # YouTube OAuth (you add this)
│   ├── settings.yaml        # Agent settings
│   └── research_prompts.yaml
├── data/                    # Research data (auto-created)
│   └── research.json
├── logs/                    # Log files (auto-created)
│   └── researcher.log
├── .env                     # Environment vars (you configure)
└── token.pickle            # OAuth token (auto-created)
```

---

## ⚙️ Configuration Files

### **config/settings.yaml**
Main agent configuration:
- Research criteria weights
- API limits  
- Filter rules
- Content preferences

### **config/research_prompts.yaml**
AI prompts for topic evaluation. Customize to match your channel's needs.

---

## 🔒 Security Best Practices

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

---

## 🚀 Next Steps

1. **Run your first research**:
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
   - Use in Script Writer Agent
   - Feed to SEO Optimizer Agent

---

## 🆘 Getting Help

1. Check logs: `tail -f logs/researcher.log`
2. Run with debug: Edit `.env` → `LOG_LEVEL=DEBUG`
3. Review [USAGE.md](USAGE.md) for usage examples
4. Check [CONTRIBUTING.md](CONTRIBUTING.md) for technical details
5. Open an issue on GitHub

---

**Setup Complete!** 🎉

You're ready to start discovering high-potential content topics for your YouTube channel.
