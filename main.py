import os
import uuid
import threading
import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

tokens = {}

def download_audio(video_url, token):
    """Download audio and return direct MP3 URL"""
    try:
        unique_id = str(uuid.uuid4())[:8]
        output_template = os.path.join(DOWNLOAD_FOLDER, f"audio_{unique_id}.%(ext)s")
        
        # Optimized yt-dlp options for direct MP3 streaming
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            mp3_filename = output_template.replace('%(ext)s', 'mp3')
            
            if os.path.exists(mp3_filename):
                tokens[token] = {
                    'file_path': mp3_filename,
                    'timestamp': time.time(),
                    'title': info.get('title', 'audio'),
                    'ready': True
                }
                print(f"Download complete for token: {token}")
                return True
            else:
                print(f"File not created: {mp3_filename}")
                return False
                
    except Exception as e:
        print(f"Download error: {str(e)}")
        tokens[token] = {
            'error': str(e),
            'ready': False
        }
        return False

@app.route('/')
def convert():
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    
    if 'youtube.com/watch' not in video_url and 'youtu.be' not in video_url:
        return jsonify({"error": "Invalid YouTube URL"}), 400
    
    token = str(uuid.uuid4())
    
    # Start download in background
    thread = threading.Thread(target=download_audio, args=(video_url, token))
    thread.start()
    
    return jsonify({
        "token": token,
        "message": "Conversion started",
        "status": "processing"
    })

@app.route('/download')
def download():
    token = request.args.get('token')
    
    if not token:
        return jsonify({"error": "Missing 'token' parameter"}), 400
    
    if token not in tokens:
        return jsonify({"error": "Invalid token"}), 404
    
    if not tokens[token].get('ready', False):
        return jsonify({"error": "File not ready yet", "status": "processing"}), 202
    
    if 'error' in tokens[token]:
        return jsonify({"error": tokens[token]['error']}), 500
    
    file_path = tokens[token]['file_path']
    
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    safe_title = "".join(c for c in tokens[token]['title'] if c.isalnum() or c in ' ._-')[:50]
    return send_file(
        file_path,
        as_attachment=True,
        download_name=f"{safe_title}.mp3",
        mimetype="audio/mpeg"
    )

@app.route('/status')
def status():
    return jsonify({
        "status": "online",
        "message": "YouTube Audio API is running",
        "tokens": len(tokens)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)