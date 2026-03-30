from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
import os

from src.database.database import save_url, get_url


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://url-shorter-99x1.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://url-shorter-99x1.onrender.com"


class ShortenRequest(BaseModel):
    url: str


@app.post("/shorten")
async def shorten_url(request: ShortenRequest):
    try:
        short_id = await save_url(request.url)
        return {"short_url": f"{BASE_URL}/{short_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Servir archivos estáticos (CSS, JS, etc.) bajo /static
app.mount("/static", StaticFiles(directory="src/public"), name="static")


@app.get("/")
async def serve_index():
    """Sirve el index.html en la raíz."""
    index_path = os.path.join("src", "public", "index.html")
    with open(index_path, "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/{short_id}")
async def redirect_url(short_id: str):
    """Redirige a la URL original dado un short_id."""
    original_url = await get_url(short_id)
    if not original_url:
        raise HTTPException(status_code=404, detail="URL no encontrada")
    return RedirectResponse(url=original_url)