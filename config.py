"""
Configuration settings for the InnerTube API
"""
from typing import Dict, Any

# API Metadata
API_TITLE = "InnerTube API"
API_DESCRIPTION = """
🚀 **Powerful & Unlimited YouTube API Wrapper**

A premium-quality, open-access localhost API that provides comprehensive access to YouTube's InnerTube API.
No API keys, no authentication, no limits - just pure power at your fingertips!

## Features
- 🎥 **Full YouTube Access**: Search, videos, channels, playlists, comments
- 🎵 **YouTube Music**: Complete music API support
- ⚡ **High Performance**: Intelligent caching and async operations
- 🔄 **Batch Requests**: Process multiple requests in one call
- 📊 **Rich Data**: Get detailed metadata, statistics, and more
- 🎨 **Beautiful UI**: Interactive API explorer with premium design
- 🌐 **Multiple Formats**: JSON, XML, CSV output support
- 🔒 **No Authentication**: Completely open for everyone

## Client Types
Supports multiple YouTube client types for maximum compatibility:
- WEB (Desktop browser)
- ANDROID (Android app)
- IOS (iOS app)
- MWEB (Mobile web)
- TV (Smart TV)
- MUSIC (YouTube Music)

---
**Created with ❤️ by Kobir Shah 🇧🇩 (Bangladesh)**
"""
API_VERSION = "1.0.0"
API_HOST = "0.0.0.0"
API_PORT = 8000

# CORS Settings
CORS_ORIGINS = ["*"]
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Cache Settings
CACHE_ENABLED = True
CACHE_TTL: Dict[str, int] = {
    "search": 300,          # 5 minutes
    "video": 600,           # 10 minutes
    "channel": 1800,        # 30 minutes
    "playlist": 900,        # 15 minutes
    "comments": 300,        # 5 minutes
    "trending": 600,        # 10 minutes
    "music": 300,           # 5 minutes
    "default": 300          # 5 minutes default
}

# InnerTube Client Settings
INNERTUBE_CLIENTS = ["WEB", "ANDROID", "IOS", "MWEB", "TV"]
INNERTUBE_MUSIC_CLIENTS = ["WEB_REMIX", "ANDROID_MUSIC", "IOS_MUSIC"]
DEFAULT_CLIENT = "WEB"
DEFAULT_MUSIC_CLIENT = "WEB_REMIX"

# Request Settings
MAX_BATCH_SIZE = 10
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3

# Response Settings
PRETTY_JSON = True
DEFAULT_FORMAT = "json"

# Pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100
