# 🔌 Port Management Guide

Managing ports across multiple agents and applications.

---

## **Current Port Allocations**

| Agent/App | Port | Status | Repository |
|-----------|------|--------|------------|
| **YouTube Comment Agent** | 8080 | ✅ Active | youtube-comment-agent |
| **YouTube Topic Researcher** | 8081 | ✅ Active | youtube-topic-researcher |
| Script Writer Agent | 8082 | 🔜 Planned | - |
| Shorts Creator Agent | 8083 | 🔜 Planned | - |
| Thumbnail Designer Agent | 8084 | 🔜 Planned | - |
| SEO Optimizer Agent | 8085 | 🔜 Planned | - |
| Title Generator Agent | 8086 | 🔜 Planned | - |
| Community Post Creator Agent | 8087 | 🔜 Planned | - |
| Competitor Monitor Agent | 8088 | 🔜 Planned | - |
| Analytics Tracker Agent | 8089 | 🔜 Planned | - |

**Reserved Range**: 8080-8099 (Agentic AI ecosystem)

---

## **Configuration Methods**

### **Method 1: Environment Variables (Recommended)**

Each agent should support PORT environment variable:

```bash
# Set port before running
export PORT=8081
./scripts/run_ui.sh
```

Or create a `.env` file in each project:

```bash
PORT=8081
HOST=127.0.0.1
DEBUG=True
```

### **Method 2: Command Line Arguments**

```bash
python web/api.py --port 8081
```

### **Method 3: Config File**

Create `config/server.yaml`:

```yaml
server:
  port: 8081
  host: 127.0.0.1
  debug: true
```

---

## **Setup for New Agents**

When creating a new agent:

1. **Copy .env.example**:
   ```bash
   cp .env.example .env
   ```

2. **Edit PORT** in `.env`:
   ```bash
   PORT=8082  # Next available port
   ```

3. **Verify in Flask/FastAPI**:
   ```python
   import os
   port = int(os.getenv('PORT', 8080))
   app.run(host='127.0.0.1', port=port)
   ```

4. **Update PORTS.md** with your allocation

---

## **Port Conflict Resolution**

If you get "Address already in use":

```bash
# Check what's using the port (macOS/Linux)
lsof -i :8081

# Kill the process
kill -9 <PID>

# Or use a different port
export PORT=8090
```

---

## **Best Practices**

✅ **DO**:
- Use environment variables for port configuration
- Document your port allocation in PORTS.md
- Use sequential ports (8080, 8081, 8082...)
- Include `.env.example` in your repo
- Add `.env` to `.gitignore`

❌ **DON'T**:
- Hardcode ports in source code
- Use random ports
- Forget to update PORTS.md
- Commit `.env` with real credentials

---

## **Multi-Agent Development**

When running multiple agents simultaneously:

```bash
# Terminal 1: Comment Agent
cd youtube-comment-agent
export PORT=8080
./scripts/run_ui.sh

# Terminal 2: Topic Researcher
cd youtube-topic-researcher
export PORT=8081
./scripts/run_ui.sh

# Terminal 3: Script Writer (future)
cd youtube-script-writer
export PORT=8082
./scripts/run_ui.sh
```

Access them at:
- http://localhost:8080 (Comment Agent)
- http://localhost:8081 (Topic Researcher)
- http://localhost:8082 (Script Writer)

---

## **Docker Compose (Future)**

For orchestrating all agents:

```yaml
version: '3.8'
services:
  comment-agent:
    build: ./youtube-comment-agent
    ports:
      - "8080:8080"
  
  topic-researcher:
    build: ./youtube-topic-researcher
    ports:
      - "8081:8081"
  
  # Add more agents...
```

---

## **Kubernetes (Production)**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: topic-researcher
spec:
  ports:
    - port: 8081
      targetPort: 8081
  selector:
    app: topic-researcher
```

---

## **Quick Reference**

```bash
# Check your current port
echo $PORT

# Set port for this session
export PORT=8081

# Set port permanently (add to ~/.zshrc or ~/.bashrc)
echo 'export PORT=8081' >> ~/.zshrc

# Use python-dotenv to load .env automatically
pip install python-dotenv

# In your Python code:
from dotenv import load_dotenv
load_dotenv()
port = int(os.getenv('PORT', 8080))
```

---

**Maintained by**: Amir Charkhi  
**Last Updated**: 2025-10-22  
**Version**: 1.1.0
