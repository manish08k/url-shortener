from datetime import datetime

db = {}
counter = 1


def save_url(long_url: str) -> int:
    global counter
    short_id = counter
    db[short_id] = {
        "url": long_url,
        "clicks": 0,
        "created_at": datetime.utcnow().isoformat(),
    }
    counter += 1
    return short_id


def get_url(short_id: int) -> dict | None:
    return db.get(short_id)


def increment_click(short_id: int):
    if short_id in db:
        db[short_id]["clicks"] += 1


def get_all_urls() -> list:
    from utils import encode_base62
    import os
    base = os.getenv("BASE_URL", "http://localhost:8000")
    return [
        {
            "short_url": f"{base}/{encode_base62(sid)}",
            "original_url": data["url"],
            "clicks": data["clicks"],
            "created_at": data["created_at"],
        }
        for sid, data in db.items()
    ]