# 🎯 YouTube Content Researcher Agent

**AI-Powered topic discovery for YouTube creators** - Find trending, monetizable, and high-potential content ideas with multi-dimensional AI evaluation.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/wvlt/youtube-topic-researcher/releases/tag/v1.0.0)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-yellow.svg)](https://www.python.org/)

---

## ✨ Features

### **Multi-Dimensional Topic Evaluation**
Each topic scored 0-100 across 5 dimensions:
- 🎯 **Importance** (25%) - Relevance to channel & audience
- 👁️ **Watchability** (20%) - Engagement potential  
- 💰 **Monetization** (20%) - Revenue potential
- 📈 **Popularity** (20%) - Trend momentum
- ⚡ **Innovation** (15%) - Uniqueness & cutting-edge appeal

### **Intelligent Content Discovery**
- 🔥 YouTube search with niche-focused filtering
- 🤖 AI-generated topic ideas (Claude/GPT)
- 🚫 Automatic filtering of irrelevant content (music, gaming, entertainment)
- 📊 Competitor analysis
- 🌍 Multi-region trending insights

### **Beautiful Interfaces**
- 🖥️ Modern web dashboard with real-time updates
- 💻 Rich CLI with color-coded output
- 📱 Responsive design
- 📊 Interactive analytics

### **Production Ready**
- 💾 Persistent TinyDB storage
- 🔄 Session tracking & analytics
- 📤 CSV export functionality
- 🔌 REST API for integration
- 🎨 Customizable AI prompts

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.9+
- YouTube Data API credentials ([Get them here](https://console.cloud.google.com/))
- Anthropic API key ([Get it here](https://console.anthropic.com/))

### **Installation (5 minutes)**

```bash
# 1. Clone repository
git clone https://github.com/wvlt/youtube-topic-researcher.git
cd youtube-topic-researcher

# 2. Run setup
./scripts/setup.sh

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Add YouTube OAuth credentials
# Download from Google Cloud Console → save as config/client_secrets.json

# 5. Start the web UI
./scripts/run_ui.sh
# Visit http://localhost:8080
```

**That's it!** You're ready to discover amazing content topics.

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [SETUP.md](SETUP.md) | Complete setup guide with troubleshooting |
| [USAGE.md](USAGE.md) | Usage examples and workflows |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Developer guide, API docs, architecture |
| [CHANGELOG.md](CHANGELOG.md) | Version history and release notes |

---

## 💡 Use Cases

### **For Content Creators**
- Discover trending topics before they peak
- Find monetizable content opportunities
- Identify content gaps in your niche
- Plan content calendar with data

### **For Agencies**
- Research multiple channels
- Bulk topic discovery
- Performance tracking
- Client reporting

---

## 🎯 Example Output

```
📊 Research Results (Score: 0-100)

┌────┬─────────────────────────────────┬───────┬────────────┐
│ #  │ Topic                           │ Score │ Category   │
├────┼─────────────────────────────────┼───────┼────────────┤
│ 1  │ Complete AI Course for Beginners│  87   │ Tutorial   │
│ 2  │ AI Tools for Learning 2025      │  84   │ Review     │
│ 3  │ Python AI Programming Guide     │  82   │ Tutorial   │
└────┴─────────────────────────────────┴───────┴────────────┘

✅ Topics: Relevant, high-quality, monetizable
❌ Filtered out: Music videos, gaming, entertainment noise
```

---

## 🔄 Integration with Agent Ecosystem

This is **Agent #6** in the Amir Charkhi agent ecosystem. It feeds:
- **SEO Optimizer Agent** - Provides topics + keywords
- **Title Generator Agent** - Supplies topics + angles
- **Script Writer Agent** - Delivers topic briefs
- **Thumbnail Designer** - Gives visual context

**Time Saved**: ~2 hours/week  
**ROI**: Data-driven decisions, higher monetization

---

## 🏗️ Architecture

```
youtube-topic-researcher/
├── src/                    # Core agent logic
│   ├── main.py            # Orchestrator
│   ├── youtube/           # YouTube API modules
│   ├── ai/                # AI evaluation
│   ├── storage/           # TinyDB wrapper
│   └── utils/             # Logging & helpers
├── web/                   # Web interface
│   ├── api.py             # Flask API
│   ├── agent_wrapper.py   # Agent wrapper
│   └── static/templates/  # UI files
├── config/                # Configuration
│   ├── settings.yaml      # Agent settings
│   └── research_prompts.yaml  # AI prompts
└── scripts/               # Setup & run scripts
```

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- API documentation
- Architecture details
- Testing guidelines

---

## 📊 Project Status

- ✅ **v1.0.0** - Stable release (Production ready)
- 🎯 **Active** - Being used for Amir Charkhi YouTube channel
- 📈 **Maintained** - Regular updates and improvements

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:
- **Claude AI** (Anthropic) - Multi-dimensional topic evaluation
- **YouTube Data API v3** - Video and trend data
- **Flask** - Web API server
- **TinyDB** - Lightweight data storage
- **Rich** - Beautiful terminal output

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/wvlt/youtube-topic-researcher/issues)
- **Documentation**: See docs above
- **Examples**: Check [USAGE.md](USAGE.md)

---

**Part of the Amir Charkhi Agent Ecosystem** | Priority Agent #6 | Saves 2 hrs/week

*Discover. Evaluate. Create.* 🚀
