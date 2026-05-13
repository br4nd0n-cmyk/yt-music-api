import os
import uuid
import shutil
import threading
import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

# Configuration
DOWNLOAD_FOLDER = "downloads"
ALLOWED_EXTENSIONS = {'mp3'}
MAX_FILE_AGE_SECONDS = 300  # 5 minutes

# Ensure download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Store token to file mapping
tokens = {}

def cleanup_old_files():
    """Background thread to remove expired files"""
    while True:
        time.sleep(60)  # Check every minute
        current_time = time.time()
        to_delete = []
        for token, info in tokens.items():
            if current_time - info['timestamp'] > MAX_FILE_AGE_SECONDS:
                to_delete.append(token)
        for token in to_delete:
            file_path = tokens[token]['file_path']
            if os.path.exists(file_path):
                os.remove(file_path)
            del tokens[token]

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

def download_audio(video_url):
    """Download audio from YouTube and convert to MP3"""
    try:
        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        output_template = os.path.join(DOWNLOAD_FOLDER, f"audio_{unique_id}.%(ext)s")
        
        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'
            
            return mp3_filename, info.get('title', 'audio')
            
    except Exception as e:
        print(f"Download error: {str(e)}")
        return None, None

@app.route('/')
def convert():
    """Endpoint to convert YouTube video to MP3"""
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    
    # Validate YouTube URL
    if 'youtube.com/watch' not in video_url and 'youtu.be' not in video_url:
        return jsonify({"error": "Invalid YouTube URL"}), 400
    
    # Generate a token
    token = str(uuid.uuid4())
    
    # Start download in background
    def process_download():
        mp3_file, title = download_audio(video_url)
        if mp3_file and os.path.exists(mp3_file):
            tokens[token] = {
                'file_path': mp3_file,
                'timestamp': time.time(),
                'title': title
            }
    
    # Run download in background thread
    thread = threading.Thread(target=process_download)
    thread.start()
    
    return jsonify({
        "token": token,
        "message": "Conversion started. Use /download?token=YOUR_TOKEN to get the file.",
        "status": "processing"
    })

@app.route('/download')
def download():
    """Download the converted MP3 file"""
    token = request.args.get('token')
    
    if not token:
        return jsonify({"error": "Missing 'token' parameter"}), 400
    
    if token not in tokens:
        return jsonify({"error": "Invalid or expired token"}), 404
    
    file_path = tokens[token]['file_path']
    title = tokens[token].get('title', 'audio')
    
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    # Send file with proper filename
    safe_title = "".join(c for c in title if c.isalnum() or c in ' ._-')[:50]
    return send_file(
        file_path,
        as_attachment=True,
        download_name=f"{safe_title}.mp3",
        mimetype="audio/mpeg"
    )

@app.route('/status')
def status():
    """Check if API is running"""
    return jsonify({
        "status": "online",
        "message": "YouTube Audio API is running",
        "endpoints": {
            "convert": "/?url=YOUTUBE_URL",
            "download": "/download?token=TOKEN",
            "status": "/status"
        }
    })

if __name__ == '__main__':
    # Use PORT environment variable for Render compatibility
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)