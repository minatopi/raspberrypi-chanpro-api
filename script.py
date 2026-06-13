import json
import requests
from datetime import datetime, timedelta, timezone

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

now = datetime.now(timezone.utc)

state = load_local("state.json")
old_map = {p["title"]: p for p in state.get("posts", [])}

output_posts = []

for p in remote["posts"]:
    title = p["title"]
    like = p["like"]
    views = p["views"]

    old = old_map.get(title)

    if not old:
        status = "new"
        first_seen = now
    else:
        first_seen = datetime.fromisoformat(old["first_seen"])

        if old["like"] == like and old["views"] == views:
            status = "old"
        else:
            status = "updated"

    output_posts.append({
        "title": title,
        "like": like,
        "views": views,
        "status": status,
        "first_seen": first_seen.isoformat()
    })

# 7日以上削除
one_week_ago = now - timedelta(days=7)
output_posts = [
    p for p in output_posts
    if datetime.fromisoformat(p["first_seen"]) > one_week_ago
]

output = {
    "last_updated": now.isoformat(),
    "posts": output_posts
}

save("output.json", output)
save("state.json", output)
