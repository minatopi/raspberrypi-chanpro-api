import json
import requests
from datetime import datetime, timezone

URL = "https://minatopi.github.io/chanpro-api/data.json"

def load_json(url):
    return requests.get(url).json()

def load_local(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

remote = load_json(URL)
now = datetime.now(timezone.utc).isoformat()

state = load_local("state.json")
old_map = {p["title"]: p for p in state.get("posts", [])}

output_posts = []
new_state_posts = []

for p in remote["posts"]:
    title = p["title"]
    like = p["like"]
    views = p["views"]

    old = old_map.get(title)

    if not old:
        status = "new"
    elif old["like"] == like and old["views"] == views:
        status = "old"
    else:
        status = "updated"

    item = {
        "title": title,
        "like": like,
        "views": views,
        "status": status
    }

    output_posts.append(item)
    new_state_posts.append(item)

output = {
    "last_updated": now,
    "posts": output_posts
}

save("output.json", output)
save("state.json", {"posts": new_state_posts})
