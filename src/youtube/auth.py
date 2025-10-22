"""
YouTube API Authentication
Handles OAuth2 flow for YouTube Data API
"""

import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging


logger = logging.getLogger("content_researcher.youtube_auth")

# YouTube API scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]


class YouTubeAuth:
    """Handles YouTube API authentication"""
    
    def __init__(self, credentials_path: str = "config/client_secrets.json"):
        """
        Initialize YouTube authenticator
        
        Args:
            credentials_path: Path to OAuth2 credentials file
        """
        self.credentials_path = Path(credentials_path)
        self.token_path = Path("token.pickle")
        self.credentials = None
        self.youtube_client = None
    
    def authenticate(self):
        """
        Authenticate and return YouTube API client
        
        Returns:
            YouTube API client
        """
        # Load existing token
        if self.token_path.exists():
            logger.info("Loading existing credentials...")
            with open(self.token_path, 'rb') as token:
                self.credentials = pickle.load(token)
        
        # Refresh or create new credentials
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                logger.info("Refreshing access token...")
                self.credentials.refresh(Request())
            else:
                if not self.credentials_path.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}\n"
                        f"Please download OAuth2 credentials from Google Cloud Console."
                    )
                
                logger.info("Starting OAuth2 flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES
                )
                self.credentials = flow.run_local_server(port=0)
            
            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.credentials, token)
            logger.info("Credentials saved")
        
        # Build YouTube client
        self.youtube_client = build('youtube', 'v3', credentials=self.credentials)
        logger.info("✅ YouTube API authenticated successfully")
        
        return self.youtube_client
    
    def get_channel_info(self, channel_id: str = None) -> dict:
        """
        Get channel information
        
        Args:
            channel_id: Channel ID (if None, uses authenticated user's channel)
            
        Returns:
            Channel info dict
        """
        if not self.youtube_client:
            raise RuntimeError("YouTube client not authenticated")
        
        if channel_id:
            request = self.youtube_client.channels().list(
                part="snippet,statistics,contentDetails",
                id=channel_id
            )
        else:
            request = self.youtube_client.channels().list(
                part="snippet,statistics,contentDetails",
                mine=True
            )
        
        response = request.execute()
        
        if not response.get('items'):
            raise ValueError(f"Channel not found: {channel_id}")
        
        channel = response['items'][0]
        
        return {
            'id': channel['id'],
            'title': channel['snippet']['title'],
            'description': channel['snippet']['description'],
            'subscriber_count': int(channel['statistics'].get('subscriberCount', 0)),
            'video_count': int(channel['statistics'].get('videoCount', 0)),
            'view_count': int(channel['statistics'].get('viewCount', 0)),
            'thumbnail': channel['snippet']['thumbnails']['default']['url'],
            'uploads_playlist': channel['contentDetails']['relatedPlaylists']['uploads']
        }

