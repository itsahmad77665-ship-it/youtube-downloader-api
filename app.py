from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

from routes.info import info_bp
from routes.download import download_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Basic rate limiting setup
# You can customize storage backend (e.g. Redis) for production use
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Register blueprints under /api prefix
app.register_blueprint(info_bp, url_prefix='/api')
app.register_blueprint(download_bp, url_prefix='/api')

# Apply stricter rate limits to download and mp3 routes
limiter.limit("10 per minute")(download_bp)

@app.route('/', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "Backend is running!"}), 200

# Error handlers for rate limiting and other global errors
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": f"Rate limit exceeded: {e.description}"}), 429

if __name__ == '__main__':
    # Run server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
