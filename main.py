from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from utils import encode_base62, decode_base62
from database import save_url, get_url, increment_click, get_all_urls
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

app = FastAPI(title="URL Shortener")

# Base URL — reads from env var for GCloud, falls back to localhost
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


class ShortenRequest(BaseModel):
    long_url: str


@app.get("/", response_class=HTMLResponse)
def index():
    with open(BASE_DIR / "templates" / "index.html") as f:
        return f.read()


@app.post("/shorten")
def shorten_url(req: ShortenRequest):
    url = req.long_url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    short_id = save_url(url)
    short_code = encode_base62(short_id)
    short_url = f"{BASE_URL}/{short_code}"
    return {"short_url": short_url, "short_code": short_code}


@app.get("/api/stats")
def stats():
    return get_all_urls()


@app.get("/{short_code}")
def redirect(short_code: str):
    try:
        short_id = decode_base62(short_code)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid short code")

    data = get_url(short_id)
    if not data:
        raise HTTPException(status_code=404, detail="URL not found")

    increment_click(short_id)
    return RedirectResponse(url=data["url"], status_code=302)