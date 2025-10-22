# YouTube API Credentials Setup

## Quick Steps to Get OAuth Credentials

### 1. Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### 2. Create or Select Project
- Click "Select a project" → "New Project"
- Name it: "YouTube Content Researcher"
- Click "Create"

### 3. Enable YouTube Data API v3
- In the search bar, type "YouTube Data API v3"
- Click on it
- Click "Enable"

### 4. Create OAuth Credentials
- Go to "Credentials" (left sidebar)
- Click "Create Credentials" → "OAuth client ID"
- If prompted, configure OAuth consent screen:
  - User Type: External
  - App name: YouTube Content Researcher
  - User support email: Your email
  - Developer contact: Your email
  - Click "Save and Continue" through the scopes
  - Add yourself as a test user
  - Click "Save and Continue"

### 5. Create OAuth Client ID
- Application type: **Desktop app**
- Name: YouTube Researcher Desktop
- Click "Create"

### 6. Download Credentials
- Click "Download JSON" button
- Save the file as: `config/client_secrets.json`

## File Location
```
youtube-topic-researcher/
└── config/
    └── client_secrets.json  ← Put downloaded file here
```

## Verify Setup
```bash
# Check file exists
ls -la config/client_secrets.json

# Should show a JSON file with client_id and client_secret
```

## Security Note
⚠️ **Never commit this file to Git!** It's already in .gitignore.

## Need Help?
The file should look like this:
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

