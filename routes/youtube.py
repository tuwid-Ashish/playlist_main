from fastapi import APIRouter, HTTPException, Request, Form 
from services.youtube import youtube_title_fetch
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse, tags=["home"])
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/youtube/playlist", response_class=HTMLResponse)
async def get_playlist_videos(request: Request, playlist_url: str = Form(...), playlist_name: str = Form(...)):
    try:
        if not playlist_url and not playlist_name:
            raise HTTPException(status_code=400, detail="Please provide a valid playlist URL")
        
        videos = await youtube_title_fetch(playlist_url)
        return {"videos_title": videos}
    except Exception as e:
        print(f'Error: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))


