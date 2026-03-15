import os
import yt_dlp
from werkzeug.utils import secure_filename
from utils.helpers import is_duration_acceptable

TEMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')

# Ensure temp directory exists
os.makedirs(TEMP_DIR, exist_ok=True)

def get_video_info(url: str):
    """Fetch video metadata using yt-dlp."""
    ydl_opts = {
        'extract_flat': False,
        'no_playlist': True,
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            
            # Filter formats for typical usage
            formats = []
            if 'formats' in info:
                for f in info['formats']:
                    formats.append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'resolution': f.get('resolution', 'audio only' if f.get('vcodec') == 'none' else 'unknown'),
                        'filesize': f.get('filesize'),
                        'url': f.get('url'),
                        'acodec': f.get('acodec'),
                        'vcodec': f.get('vcodec'),
                    })
                    
            return {
                'title': info.get('title'),
                'duration': info.get('duration'),
                'thumbnail': info.get('thumbnail'),
                'formats': formats
            }
        except Exception as e:
            raise ValueError(f"Failed to fetch info: {str(e)}")

def download_video(url: str, format_ext: str = 'mp4'):
    """Download video using yt_dlp to temp directory."""
    # First get info to check duration
    info = get_video_info(url)
    if not is_duration_acceptable(info.get('duration')):
        raise ValueError("Video is too long to download.")
        
    output_filename = f"%(title).100B.%(ext)s"
    output_template = os.path.join(TEMP_DIR, output_filename)
    
    if format_ext == 'mp4':
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
            'no_playlist': True,
            'restrictfilenames': True,  # Fixes Errno 22 Invalid Argument for Windows
            'windowsfilenames': True,
            'quiet': True,
        }
    else:
        # Default best fallback
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
            'no_playlist': True,
            'restrictfilenames': True,
            'windowsfilenames': True,
            'quiet': True,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            download_filepath = ydl.prepare_filename(info_dict)
            # if we merge formats, yt-dlp might change the extension in prepare_filename
            # but usually info_dict['ext'] has the final ext
            return os.path.basename(download_filepath)
        except Exception as e:
            raise RuntimeError(f"Download failed: {str(e)}")

def download_audio(url: str):
    """Extract audio from video as MP3."""
    info = get_video_info(url)
    if not is_duration_acceptable(info.get('duration')):
        raise ValueError("Video is too long to download.")
        
    output_filename = f"%(title).100B.%(ext)s"
    output_template = os.path.join(TEMP_DIR, output_filename)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'no_playlist': True,
        'restrictfilenames': True,
        'windowsfilenames': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            # yt-dlp changes the extension to mp3 during postprocessing
            base_filename, _ = os.path.splitext(ydl.prepare_filename(info_dict))
            return os.path.basename(base_filename + '.mp3')
        except Exception as e:
            raise RuntimeError(f"Audio extraction failed: {str(e)}")
