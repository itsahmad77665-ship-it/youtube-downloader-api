from flask import Blueprint, request, jsonify
from services.ytdlp_service import get_video_info
from utils.helpers import is_valid_youtube_url

info_bp = Blueprint('info', __name__)

@info_bp.route('/info', methods=['GET'])
def fetch_info():
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "URL parameter is required."}), 400
        
    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL provided."}), 400
        
    try:
        data = get_video_info(url)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Server error while fetching info."}), 500
