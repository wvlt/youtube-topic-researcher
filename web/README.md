# Web Interface - YouTube Content Researcher

## Overview

Dead simple command center UI for the Content Researcher Agent. Built with Flask, vanilla JavaScript, and modern CSS.

## Architecture

```
web/
├── api.py              # Flask API server
├── agent_wrapper.py    # Agent wrapper for web access
├── templates/
│   └── index.html      # Main UI
└── static/
    ├── style.css       # Styling
    └── app.js          # Frontend logic
```

## Starting the Server

```bash
./scripts/run_ui.sh
# or
cd web && python api.py
```

Access at: http://localhost:8080

## Features

### 1. Real-Time Status
- Agent ready indicator
- Connection status
- Live updates

### 2. Research Interface
- Keyword input
- Topic limit control
- One-click research start
- Progress feedback

### 3. Results Dashboard
- Filterable topic list
- Score-based color coding
- Click for details
- Multi-dimension scores

### 4. Analytics Panel
- Session statistics
- Quality metrics
- Performance tracking

### 5. Topic Detail Modal
- Full AI analysis
- Recommended angles
- Keywords
- Strategic notes

## API Endpoints

See API.md for full documentation.

### Quick Reference

```javascript
// Check status
fetch('/api/status')

// Start research
fetch('/api/research', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        keywords: ['AI', 'coding'],
        max_topics: 20
    })
})

// Get topics
fetch('/api/topics?days=7&min_score=60')

// Get analytics
fetch('/api/analytics?days=7')
```

## Customization

### Styling

Edit `static/style.css`:

```css
:root {
    --primary: #3b82f6;        /* Primary color */
    --success: #10b981;         /* Success color */
    --danger: #ef4444;          /* Error color */
    /* ... */
}
```

### Behavior

Edit `static/app.js`:

```javascript
// Change auto-refresh interval
setInterval(loadTopics, 60000); // Every 60 seconds

// Customize score thresholds
const scoreClass = score >= 85 ? 'high-score' : 
                   score >= 70 ? 'medium-score' : '';
```

## Deployment

### Development
```bash
# Debug mode (auto-reload)
python web/api.py
```

### Production

**Option 1: Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 web.api:app
```

**Option 2: Docker**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "web/api.py"]
```

**Option 3: Nginx + Gunicorn**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Security

### For Production:

1. **Add authentication**:
```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Implement your auth logic
    pass

@app.route('/api/research')
@auth.login_required
def research():
    # ...
```

2. **Enable HTTPS**:
```python
# Use SSL
app.run(ssl_context='adhoc')
# or use proper certificates
app.run(ssl_context=('cert.pem', 'key.pem'))
```

3. **Rate limiting**:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/research')
@limiter.limit("10 per hour")
def research():
    # ...
```

4. **Environment-based config**:
```python
app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
```

## Troubleshooting

### UI Not Loading
- Check Flask server is running
- Verify port 8080 is available
- Check browser console for errors

### API Errors
- Verify agent is initialized
- Check .env configuration
- Review server logs

### Slow Performance
- Reduce max_topics
- Enable caching
- Use production server (Gunicorn)

## Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] Batch research queue
- [ ] Topic comparison view
- [ ] Export to multiple formats
- [ ] Dark mode
- [ ] Mobile responsive improvements
- [ ] Team collaboration features
- [ ] Scheduled research jobs

## Contributing

To add new features:

1. Add API endpoint in `api.py`
2. Add frontend function in `app.js`
3. Update UI in `index.html`
4. Style in `style.css`
5. Document in this README

---

**Simple, Fast, Effective**

