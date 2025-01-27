from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

class Config:
    YOUTUBE_API_KEY = os.environ.get("Youtube_API", "youtube_api")
    SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "spotify_client_id")
    SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "spotify client secret")
    SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI", "spotify_redirect_uri")
    HF_API_TOKEN = os.environ.get("HF_ACCESS_TOKEN")
    SPOTIFY_USER_ID = "xq7dp9tfkzicm5s"
    SPOTIFY_ACCESS_TOKEN = os.environ.get("SPOTIFY_ACCESS_TOKEN", "")
    SPOTIFY_BASE_URL = 'https://api.spotify.com/v1'
