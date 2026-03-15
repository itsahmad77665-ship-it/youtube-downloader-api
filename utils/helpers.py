import re

MAX_DURATION_SECONDS = 7200  # 2 hours max duration

def is_valid_youtube_url(url: str) -> bool:
    """Basic check to see if the URL looks like a youtube link"""
    if not url:
        return False
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return bool(re.match(youtube_regex, url))

def is_duration_acceptable(duration) -> bool:
    """Check if the video is under the max duration (in seconds)"""
    if duration is None:
        return True  # sometimes live streams or certain videos don't have duration upfront
    return int(duration) <= MAX_DURATION_SECONDS
