from flask import Flask, request, jsonify
from flask_cors import CORS
from ytmusicapi import YTMusic
import os
import re

app = Flask(__name__)
CORS(app)

yt = YTMusic()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "YouTube Music API is running!",
        "usage": "https://your-url.onrender.com/search?q=song_name"
    })

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    
    if not query:
        return jsonify({"error": "Missing 'q' parameter"}), 400
    
    print(f"Searching for: {query}")
    
    try:
        # Search for songs
        results = yt.search(query, filter="songs", limit=1)
        
        if not results:
            return jsonify({"error": "No results found"}), 404
        
        song = results[0]
        video_id = song['videoId']
        
        # Get the watch playlist to extract stream URL
        watch_playlist = yt.get_watch_playlist(video_id)
        
        audio_url = ""
        
        if watch_playlist and 'tracks' in watch_playlist and len(watch_playlist['tracks']) > 0:
            track = watch_playlist['tracks'][0]
            
            # Method 1: Try to get audio endpoint
            if track.get('audioEndpoint'):
                audio_url = track['audioEndpoint'].get('streamingUrl', '')
            
            # Method 2: Try to get from videoId
            if not audio_url and track.get('videoId'):
                audio_url = f"https://www.youtube.com/watch?v={track['videoId']}"
        
        # Get artist name
        artist = "Unknown"
        if song.get('artists'):
            artist = song['artists'][0]['name']
        
        # Get thumbnail
        thumbnail = ""
        if song.get('thumbnails'):
            thumbnail = song['thumbnails'][-1]['url']
        
        # If audio_url is still empty, try to get from video ID directly
        if not audio_url or "youtube.com/watch" in audio_url:
            # For YouTube video URLs, we can still play them using YouTube player
            # But for audio only, we'll use the video URL as fallback
            audio_url = f"https://www.youtube.com/watch?v={video_id}"
        
        response = {
            "title": song.get('title', query),
            "artist": artist,
            "videoId": video_id,
            "audioUrl": audio_url,
            "thumbnailUrl": thumbnail,
            "duration": song.get('duration', 'N/A')
        }
        
        print(f"Found: {response['title']} - Audio URL: {response['audioUrl'][:50]}...")
        return jsonify(response)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)