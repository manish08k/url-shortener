from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from utils import encode_base62
from database import save_url, get_url, increment_click

app = FastAPI()

@app.post("/shorten")
def shorten_url(long_url: str):
    short_id = save_url(long_url)
    short_code = encode_base62(short_id)
    return {"short_url": f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
def redirect(short_code: str):
    try:
        short_id = decode_base62(short_code)
    except:
        raise HTTPException(status_code=404, detail="Invalid URL")

    data = get_url(short_id)
    if not data:
        raise HTTPException(status_code=404, detail="URL not found")

    increment_click(short_id)
    return RedirectResponse(url=data["url"])


# decode function
import string
BASE62 = string.ascii_letters + string.digits

def decode_base62(code):
    base = len(BASE62)
    num = 0
    for char in code:
        num = num * base + BASE62.index(char)
    return num