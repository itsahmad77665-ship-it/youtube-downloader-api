# Deploying Flask Backend to PythonAnywhere

PythonAnywhere is a great platform for hosting Python web applications. Since they don't support Docker or Node.js native server deployments on their standard web apps, this Flask refactor is perfectly suited for it.

## Prerequisites
1. Create a free or paid account at [PythonAnywhere](https://www.pythonanywhere.com/).
2. You will need internet access from within PythonAnywhere to reach YouTube. **Note:** Free accounts on PythonAnywhere have restricted outbound internet access (whitelist only). YouTube might be blocked on the free tier. If so, a paid "Hacker" plan ($5/mo) is required to use `yt-dlp` because it removes the whitelist.

## Deployment Steps

### 1. Upload Your Code
1. Go to the **Files** tab on your PythonAnywhere dashboard.
2. Under `Directories`, you can create a new folder, e.g., `youtube_downloader_backend`.
3. Upload all the files from your local `/backend` folder (`app.py`, `requirements.txt`, `/routes`, `/services`, `/utils`) into this directory.
4. Alternatively, use the **Consoles** tab to start a `Bash` console, `git clone` your repository, or use `unzip` to extract your uploaded files.

### 2. Set Up a Virtual Environment
From a **Bash** console in PythonAnywhere:
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
workon myenv
cd ~/youtube_downloader_backend
pip install -r requirements.txt
```

### 3. Create the Web App
1. Go to the **Web** tab.
2. Click **Add a new web app**.
3. Choose **Manual configuration** (do NOT choose the Flask auto-config, manual is better for existing apps).
4. Choose **Python 3.10**.

### 4. Configure Virtualenv and WSGI
1. Once the web app is created, scroll down to the **Virtualenv** section on the Web tab.
2. Enter the path to the virtual environment you created: `/home/YOUR-USERNAME/.virtualenvs/myenv`.
3. Scroll up to the **Code** section.
4. Set the **Source code** directory to `/home/devShahid/youtube_downloader_backend`.
5. Click on the **WSGI configuration file** link (it will look like `/var/www/your_username_pythonanywhere_com_wsgi.py`).

### 5. Edit the WSGI File
Replace the contents of the WSGI file with the following:

```python
import sys
import os
from dotenv import load_dotenv

# 1. Add your project directory to the sys.path
project_home = '/home/devShahid/youtube_downloader_backend'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# 2. Load environment variables if you have an .env file
load_dotenv(os.path.join(project_home, '.env'))

# 3. Import your Flask app
from app import app as application
```
*(Make sure to replace `YOUR-USERNAME` with your actual PythonAnywhere username)*.

### 6. Set Up Temp Directory
Your app downloads files to a `temp` folder. Ensure this exists and won't bloat your storage:
```bash
mkdir -p ~/youtube_downloader_backend/temp
```
*Note: You might want to set up a scheduled task (in the **Tasks** tab) to clean up old files in the `temp` directory automatically so you don't run out of disk space, e.g., `find /home/YOUR-USERNAME/youtube_downloader_backend/temp -type f -mmin +120 -delete` to delete files older than 2 hours.*

### 7. Reload and Test
1. Go back to the **Web** tab.
2. Click the big green **Reload** button at the top.
3. Your API is now live at `https://devShahid.pythonanywhere.com/api`!

## Example API Calls

### Get Video Info
```bash
curl -X GET "https://devShahid.pythonanywhere.com/api/info?url=https://www.youtube.com/watch?v=w6uX9jamcwQ"
```

### Download Video (MP4)
```bash
curl -X POST "http://127.0.0.1:4000/api/download" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=w6uX9jamcwQ", "format": "mp4"}' \
     --output video.mp4
```

### Download Audio (MP3)
```bash
curl -X POST "http://127.0.0.1:4000/api/mp3" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=w6uX9jamcwQ"}' \
     --output audio.mp3
```
### run locally on Powershell
curl.exe -X POST "http://127.0.0.1:4000/api/download" -H "Content-Type: application/json" -d "{\`"url\`": \`"https://www.youtube.com/watch?v=w6uX9jamcwQ\`", \`"format\`": \`"mp4\`"}" --output video.mp4
