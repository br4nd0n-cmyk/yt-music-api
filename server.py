from flask import Flask, request, jsonify
from flask_cors import CORS
from ytmusicapi import YTMusic
import os

app = Flask(__name__)
CORS(app)  # This allows your Android app to call this server

# Initialize the YouTube Music API without a user account
# It will work in a "browsing" mode, which is perfect for searching.
yt = YTMusic()

@app.route('/search', methods=['GET'])
def search_song():
    """Endpoint for your Android app to call."""
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing 'q' parameter"}), 400

    print(f"Searching for: {query}")
    try:
        # Search on YouTube Music
        search_results = yt.search(query, filter="songs")

        if not search_results:
            return jsonify({"error": "No results found"}), 404

        # Get the first result (the best match)
        top_result = search_results[0]
        video_id = top_result['videoId']
        
        # Fetch more details for the selected song
        # We need to get the streaming URL from the watch playlist
        watch_playlist = yt.get_watch_playlist(video_id)
        
        # The first item in the playlist is the song we requested
        if not watch_playlist or not watch_playlist.get('tracks'):
            return jsonify({"error": "Could not get stream URL"}), 404

        track = watch_playlist['tracks'][0]
        song_title = track['title']
        artist_name = track['artists'][0]['name'] if track.get('artists') else "Unknown Artist"
        audio_url = track.get('audioEndpoint', {}).get('streamingUrl', "URL not found")
        thumbnail_url = track.get('thumbnails', [{}])[-1].get('url', "")

        # Prepare the response for your app
        response_data = {
            "title": song_title,
            "artist": artist_name,
            "videoId": video_id,
            "audioUrl": audio_url,
            "thumbnailUrl": thumbnail_url,
            "duration": track.get('duration', "N/A")
        }
        print(f"Found: {song_title} by {artist_name}")
        return jsonify(response_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Get the port from the environment variable (for cloud hosting)
    port = int(os.environ.get('PORT', 8080))
    # Run the server
    app.run(host='0.0.0.0', port=port)