import urllib.request
import urllib.parse
import json
import os
import sys

# Ensure UTF-8 output
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

os.makedirs("assets/players", exist_ok=True)
os.makedirs("assets/teams", exist_ok=True)

HEADERS = {"User-Agent": "NBAWarRoomScout/1.0 (contact: student@draft.org)"}

def search_wikimedia(query):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrlimit=3&prop=imageinfo&iiprop=url&iiurlwidth=500&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        res = urllib.request.urlopen(req, timeout=8)
        data = json.loads(res.read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        results = []
        for pid, p in pages.items():
            info = p.get("imageinfo", [{}])[0]
            thumb = info.get("thumburl")
            orig = info.get("url")
            results.append({"title": p.get("title"), "thumb": thumb, "url": orig})
        return results
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return []

if __name__ == "__main__":
    queries = [
        "Trae Young Oklahoma",
        "Jayson Tatum Duke",
        "Markelle Fultz Washington",
        "Lonzo Ball UCLA",
        "Donovan Mitchell Louisville",
        "Deandre Ayton Arizona",
        "Frank Ntilikina Strasbourg",
        "Shai Gilgeous-Alexander Kentucky",
        "Marvin Bagley Duke",
        "Mikal Bridges Villanova",
        "Bam Adebayo Kentucky",
        "De'Aaron Fox Kentucky"
    ]
    for q in queries:
        res = search_wikimedia(q)
        print(f"\nQuery: {q}")
        for r in res[:2]:
            print(f"  {r['title']} -> {r['thumb'][:90] if r['thumb'] else 'None'}")
