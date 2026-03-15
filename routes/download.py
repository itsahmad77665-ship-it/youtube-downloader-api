from flask import Blueprint, request, jsonify, send_from_directory, current_app
import os
from services.ytdlp_service import download_video, download_audio, TEMP_DIR
from utils.helpers import is_valid_youtube_url

download_bp = Blueprint('download', __name__)

@download_bp.route('/download', methods=['POST'])
def handle_download():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL parameter is required in JSON body."}), 400
        
    url = data['url']
    format_ext = data.get('format', 'mp4')
    
    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL provided."}), 400
        
    try:
        filename = download_video(url, format_ext)
        # return the file
        return send_from_directory(TEMP_DIR, filename, as_attachment=True)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Server error while downloading video."}), 500

@download_bp.route('/mp3', methods=['POST'])
def handle_mp3():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL parameter is required in JSON body."}), 400
        
    url = data['url']
    
    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL provided."}), 400
        
    try:
        filename = download_audio(url)
        # return the file
        return send_from_directory(TEMP_DIR, filename, as_attachment=True)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Server error while extracting audio."}), 500
