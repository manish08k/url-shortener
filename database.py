db = {}
counter = 1

def save_url(long_url):
    global counter
    short_id = counter
    db[short_id] = {"url": long_url, "clicks": 0}
    counter += 1
    return short_id

def get_url(short_id):
    return db.get(short_id)

def increment_click(short_id):
    if short_id in db:
        db[short_id]["clicks"] += 1