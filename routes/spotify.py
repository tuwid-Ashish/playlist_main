from fastapi import APIRouter, HTTPException , Response
from services.spotify import add_track_to_playlist_request, create_playlist_request, search_track_request 
from config import Config
import random , string
import urllib.parse

SPOTIFY_BASE_URL = 'https://api.spotify.com/v1'
state_key = 'spotify_auth_state'
scope = 'user-read-private user-read-email playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public'

def generate_random_string(length: int) -> str: return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

router = APIRouter()


@router.post("/spotify/create-playlist")
def create_spotify_playlist(playlist_name: str):
    try:
        playlist = create_playlist_request(f'{SPOTIFY_BASE_URL}/users/{Config.SPOTIFY_USER_ID}/playlists',playlist_name )
        
        return {"message": "Playlist created successfully", "playlist": playlist ,"status_code": 201}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/spotify/add-tracks")
def add_tracks_to_playlist(playlist_id: str, track_list: list):
    try:
        track_uris = []
        for track in track_list:
            find_track = search_track_request(f'{SPOTIFY_BASE_URL}/search', track)
            if not find_track:
                raise HTTPException(status_code=400, detail="Track not found")
            track_uris.append(find_track.get('tracks', {}).get('items', [])[0].get('uri'))

        add_track = add_track_to_playlist_request(f'{SPOTIFY_BASE_URL}/playlists/{playlist_id}/tracks' , track_uris)    

        return {"message": "Tracks added successfully" , "status_code": add_track["status_code"] , "url": add_track.get('external_urls', {}).get('spotify', '') }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/spotify/access-token")
def get_access_token(client_id: str |None = Config.SPOTIFY_CLIENT_ID, client_secret: str|None = Config.SPOTIFY_CLIENT_SECRET):
   state = generate_random_string(16)
   print(Config.SPOTIFY_CLIENT_ID ,  Config.SPOTIFY_CLIENT_SECRET)
   query_params = { 'response_type': 'code', 'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': "http://127.0.0.1:8000/spotify_callback", 'state': state, 'scope': scope } 
   url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query_params)
   return url


