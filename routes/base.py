from fastapi import FastAPI, Request ,APIRouter ,Form ,HTTPException
from fastapi.templating import Jinja2Templates
from services.youtube import youtube_title_fetch
from services.spotify import create_playlist_request, search_track_request, add_track_to_playlist_request
from config import Config
templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/")
def render_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/")
async def playlist_convert(request: Request, playlist_url: str = Form(...) , playlist_name: str = Form(...)):
    if playlist_name and playlist_url is None:
        raise HTTPException(status_code=400, detail="Please fill in all fields")
    
    retrive_title = await youtube_title_fetch(playlist_url)
    if len(retrive_title) < 1:
        raise HTTPException(status_code=400, detail="Failed to fetch playlist items")
    
    spotify_playlist = create_playlist_request(f"https://api.spotify.com/v1/users/{Config.SPOTIFY_USER_ID}/playlists", playlist_name) 

    if "error" in spotify_playlist:
        raise HTTPException(status_code=400, detail="Failed to create playlist")
    
    track_uris = []
    for title in retrive_title:
        track = search_track_request(f'{Config.SPOTIFY_BASE_URL}/search', title )
        if "error" in track:
            continue
        
        track_uris.append(track["tracks"]["items"][0]["uri"])

    add_track = add_track_to_playlist_request(f'{Config.SPOTIFY_BASE_URL}/playlists/{spotify_playlist.get("id")}/tracks', track_uris)
    
    if "error" in add_track:
        raise HTTPException(status_code=400, detail="Failed to add track to playlist")
    
    return templates.TemplateResponse("index.html", {"request": request, "success": True , "playlist_url": spotify_playlist["external_urls"]["spotify"]})



    