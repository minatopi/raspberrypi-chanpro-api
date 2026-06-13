import json
import requests
from datetime import datetime, timezone

URL = "https://minatopi.github.io/chanpro-api/data.json"


def load_json(url):
    return requests.get(url, timeout=10).json()


def load_local(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# --- fetch ---
remote = load_json(URL)
now = datetime.now(timezone.utc).isoformat()

# --- state ---
state = load_local("state.json")
old_map = state.get("posts", {})  # dict前提

new_state = {}
output_posts = []

for p in remote.get("posts", []):
    title = p["title"]
    like = p["like"]
    views = p["views"]

    old = old_map.get(title)

    if old is None:
        status = "new"
    elif old["like"] == like and old["views"] == views:
        status = "old"
    else:
        status = "updated"

    output_posts.append({
        "title": title,
        "like": like,
        "views": views,
        "status": status
    })

    # state更新
    new_state[title] = {
        "like": like,
        "views": views
    }


output = {
    "last_updated": now,
    "count": len(output_posts),
    "posts": output_posts
}


save("output.json", output)
save("state.json", {"posts": new_state})
