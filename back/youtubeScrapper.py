from fastapi import FastAPI, Request, HTTPException, Depends, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
import yt_dlp as youtube_dl
import ssl
import certifi
from dotenv import load_dotenv
load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
DOWNLOAD_DIRECTORY = "videos"
DIRECTORY = "http://cdn.krbdn.com/content/videos/"
TOKEN_VALIDITY = 600
    
app = FastAPI()

# Token Generator Setup
token_serializer = URLSafeTimedSerializer(SECRET_KEY)

# Security
auth_scheme = HTTPBearer()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def create_ssl_context():
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())
    return ssl_context

def generate_token():
    token = token_serializer.dumps({})
    return token

def validate_token(auth: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        token_serializer.loads(auth.credentials, max_age=TOKEN_VALIDITY)
    except (SignatureExpired, BadSignature):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# FastAPI Endpoints
@app.post("/api/generate-token")
@limiter.limit("5/minute") 
async def generate_download_token(request: Request):
    return {"token": generate_token()}

@app.post("/api/download-video")
@limiter.limit("5/minute")
async def download_video(request: Request, url: str = Form(...), auth: HTTPAuthorizationCredentials = Depends(validate_token)):
    ssl_context = create_ssl_context()
    ydl_opts = {
        'ssl_context': ssl_context,
        'writethumbnail': True,
        'outtmpl': os.path.join(DOWNLOAD_DIRECTORY, '%(id)s.%(ext)s'),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url)
        video_id = result.get('id')
        video_title = result.get('title')
        file_ext = result.get('ext', 'mp4')
        filepath = f"{DIRECTORY}{video_id}.{file_ext}"
        thumbnail_path = None
        for ext in ['jpg', 'png', 'webp']:
            potential_path = f"{DOWNLOAD_DIRECTORY}{video_id}.{ext}"
            if os.path.isfile(potential_path):
                thumbnail_path = potential_path
                break
        duration = result.get('duration', '')
        uploader = result.get('uploader', '')
        uploader_url = result.get('uploader_url', '')
        channel_url = result.get('channel_url', '')
        view_count = result.get('view_count', '')
        like_count = result.get('like_count', '')
        dislike_count = result.get('dislike_count', '')
        uploader_id = result.get('uploader_id', '')
        channel_id = result.get('channel_id', '')
    return {
        "message": "Download OK",
        "title": video_title, 
        "filepath": filepath,
        "thumbnail": thumbnail_path,
        "duration": duration,
        "uploader": uploader,
        "uploader_url": uploader_url,
        "uploader_id": uploader_id,
        "channel_url": channel_url,
        "channel_id": channel_id,
        "view_count": view_count,
        "like_count": like_count,
        "dislike_count": dislike_count
    }
