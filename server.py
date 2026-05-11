from flask import Flask, request, jsonify
from flask_cors import CORS
from ytmusicapi import YTMusic
import os

app = Flask(__name__)
CORS(app)

# Initialize YouTube Music API
yt = YTMusic()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "YouTube Music API is running",
        "endpoints": {
            "search": "/search?q=song_name"
        }
    })

@app.route('/search', methods=['GET'])
def search_song():
    """Search for a song on YouTube Music"""
    query = request.args.get('q')
    
    if not query:
        return jsonify({"error": "Missing 'q' parameter"}), 400
    
    print(f"Searching for: {query}")
    
    try:
        # Search for songs
        search_results = yt.search(query, filter="songs")
        
        if not search_results:
            return jsonify({"error": "No results found"}), 404
        
        # Get the first result
        top_result = search_results[0]
        video_id = top_result['videoId']
        
        # Get streaming URL
        watch_playlist = yt.get_watch_playlist(video_id)
        
        if not watch_playlist or not watch_playlist.get('tracks'):
            return jsonify({"error": "Could not get stream URL"}), 404
        
        track = watch_playlist['tracks'][0]
        
        # Extract artist name
        artist_name = "Unknown Artist"
        if track.get('artists'):
            artist_name = track['artists'][0]['name']
        
        # Extract audio URL
        audio_url = ""
        if track.get('audioEndpoint', {}).get('streamingUrl'):
            audio_url = track['audioEndpoint']['streamingUrl']
        elif track.get('videoId'):
            audio_url = f"https://www.youtube.com/watch?v={track['videoId']}"
        
        # Extract thumbnail
        thumbnail_url = ""
        if track.get('thumbnails'):
            thumbnail_url = track['thumbnails'][-1]['url']
        
        response_data = {
            "title": track.get('title', query),
            "artist": artist_name,
            "videoId": video_id,
            "audioUrl": audio_url,
            "thumbnailUrl": thumbnail_url,
            "duration": track.get('duration', 'N/A')
        }
        
        print(f"Found: {response_data['title']} by {response_data['artist']}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)