<div align="center">

# 🚀 InnerTube API
### The Ultimate Unlimited YouTube API Wrapper

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![InnerTube](https://img.shields.io/badge/InnerTube-Powered-ff0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/tombulled/innertube)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-documentation">Documentation</a> •
  <a href="#-configuration">Configuration</a>
</p>

</div>

---

## ⚡ Overview

**InnerTube API** is a high-performance, open-source REST API that unlocks the full power of YouTube without the limitations. Built on top of the reverse-engineered InnerTube client, it provides **unlimited access** to data that the official Data API hides or restricts.

> 🛑 **No API Keys Required**
> 🔓 **No OAuth Headaches**
> 🚀 **No Rate Limits** (other than YouTube's own)

Whether you're building a music player, a data analysis tool, or a custom YouTube frontend, InnerTube API gives you the raw power you need.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **🎥 Core YouTube** | Search videos, channels, playlists. Get detailed metadata, streaming URLs, and recommendations. |
| **🎵 YouTube Music** | Full support for YouTube Music. Search artists, albums, tracks, and get lyrics. |
| **⚡ High Performance** | Built with **FastAPI** and **AsyncIO**. Includes intelligent **TTL Caching** for blazing fast responses. |
| **🔄 Batch Processing** | Execute up to 10 API calls in a single HTTP request to save bandwidth and latency. |
| **📊 Rich Data** | Access hidden metrics, live stream status, captions/subtitles, and detailed analytics. |
| **🎨 Premium UI** | Comes with a beautiful, glassmorphism-styled **Interactive API Explorer** running on localhost. |

---

## 🚀 Quick Start

### Prerequisites
*   Python 3.8+
*   `pip`

### 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/MohammadKobirShah/InnerTube-API.git
    cd InnerTube-API
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch the Server**
    ```bash
    # Windows
    start_server.bat

    # Linux/Mac
    python main.py
    ```

<div align="center">
  <h3>🎉 You're Live!</h3>
  <p>Open your browser and navigate to:</p>
  <a href="http://localhost:8000"><code>http://localhost:8000</code></a>
</div>

---

## 📚 API Endpoints

### 🔍 Search & Browse
*   `GET /api/search` - Search for videos, channels, playlists
*   `GET /api/browse/{browse_id}` - Browse specific YouTube pages
*   `GET /api/trending` - Get current trending videos
*   `GET /api/homepage` - Get the YouTube homepage feed

### 📺 Video & Player
*   `GET /api/video/{video_id}` - Get comprehensive video metadata
*   `GET /api/player/{video_id}` - Get streaming formats and adaptive streams
*   `GET /api/next/{video_id}` - Get "Up Next" and related videos
*   `GET /api/captions/{video_id}` - Get video subtitles/captions

### 👤 Channels & Playlists
*   `GET /api/channel/{channel_id}` - Get channel profile and stats
*   `GET /api/channel/{channel_id}/videos` - Get all videos from a channel
*   `GET /api/playlist/{playlist_id}` - Get full playlist details

### 🎵 YouTube Music
*   `GET /api/music/search` - Search specifically on YouTube Music
*   `GET /api/music/artist/{artist_id}` - Get artist discography
*   `GET /api/music/album/{album_id}` - Get album tracklist

### 🛠 Advanced
*   `POST /api/batch` - **[POWER FEATURE]** Run multiple requests at once
*   `GET /api/analytics` - View server cache stats and usage

---

## ⚙️ Configuration

Customize your experience in `config.py`:

```python
# Cache Settings (Seconds)
CACHE_TTL = {
    "search": 300,   # 5 mins
    "video": 600,    # 10 mins
    "channel": 1800  # 30 mins
}

# Client Selection
DEFAULT_CLIENT = "WEB"  # Options: WEB, ANDROID, IOS, TV
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

<div align="center">

**Created with ❤️ by Kobir Shah 🇧🇩 (Bangladesh)**

Powered by [FastAPI](https://fastapi.tiangolo.com) & [InnerTube](https://github.com/tombulled/innertube)

</div>
