import json
import requests
from datetime import datetime, timedelta

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
now = datetime.utcnow()

state = load_local("state.json")
old_map = {p["title"]: p for p in state.get("posts", [])}

output = []
new_state = []

for p in remote["posts"]:
    title = p["title"]
    like = p["like"]
    views = p["views"]

    old = old_map.get(title)

    status = "new"
    if old:
        if old["like"] == like and old["views"] == views:
            status = "old"
        else:
            status = "updated"

    p["status"] = status
    p["checked_at"] = now.isoformat()

    # 7日ルール用（初登場時間がなければ付与）
    if old and "first_seen" in old:
        p["first_seen"] = old["first_seen"]
    else:
        p["first_seen"] = now.isoformat()

    output.append(p)

# 7日以上前を削除
one_week_ago = now - timedelta(days=7)
output = [
    p for p in output
    if datetime.fromisoformat(p["first_seen"].replace("Z","")) > one_week_ago
]

save("output.json", {"posts": output})
save("state.json", {"posts": output})
