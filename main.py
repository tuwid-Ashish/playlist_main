from fastapi import FastAPI, Request ,APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from routes.base import router as base_router
from routes.youtube import router as youtube_router
from routes.spotify import router as spotify_router

app = FastAPI()

app.include_router(router=base_router , tags=["home"])
app.include_router(router=youtube_router , tags=["youtube"])
app.include_router(router=spotify_router , tags=["spotify"])