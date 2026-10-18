import json
import os
import sys
import time
import unicodedata
import urllib.request
import urllib.parse

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

os.makedirs("assets/players", exist_ok=True)
HEADERS = {"User-Agent": "NBAWarRoomScout/1.0 (contact: test@nbascouting.org)"}

def slugify(name):
    n = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("utf-8")
    for ch in [" ", "-", ".", "'", "/", "(", ")"]:
        n = n.replace(ch, "_")
    while "__" in n:
        n = n.replace("__", "_")
    return n.strip("_").lower() + ".jpg"

d17 = json.load(open("data/draft_2017.json", encoding="utf-8"))
d18 = json.load(open("data/draft_2018.json", encoding="utf-8"))
all_players = d17 + d18

print(f"Total prospects: {len(all_players)}")

# Query Wikipedia pageimages for players
def fetch_wiki_thumbnail(player_name, filename):
    dest = os.path.join("assets/players", filename)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return True

    # Try Wikipedia titles
    candidate_titles = [
        player_name,
        player_name.replace(" ", "_"),
        f"{player_name} (basketball)",
        f"{player_name.replace(' ', '_')} (basketball)"
    ]

    for title in candidate_titles:
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&pithumbsize=600&format=json"
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            res = urllib.request.urlopen(req, timeout=8)
            data = json.loads(res.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for pid, p in pages.items():
                if pid == "-1":
                    continue
                thumb = p.get("thumbnail", {}).get("source")
                if thumb:
                    time.sleep(0.3)
                    img_req = urllib.request.Request(thumb, headers=HEADERS)
                    content = urllib.request.urlopen(img_req, timeout=12).read()
                    with open(dest, "wb") as f:
                        f.write(content)
                    print(f"Fetched {filename} from {title} ({len(content)} bytes)")
                    return True
        except Exception as e:
            # print(f"Error {title}: {e}")
            pass
        time.sleep(0.2)
    return False

# Also build a comprehensive players_catalog.json with image paths and enriched metadata
enriched_players = []
for p in all_players:
    p_copy = dict(p)
    slug = slugify(p["player"])
    p_copy["image_filename"] = slug
    
    # Classify origin type
    origin = p.get("origin", "")
    if any(k in origin for k in ["Espanha", "EuroLeague", "França", "Alemanha", "Sérvia", "Croácia", "Lituânia", "Itália", "Eslovênia", "Austrália"]):
        origin_type = "International"
    elif "High School" in origin or "HS" in origin:
        origin_type = "High School"
    else:
        origin_type = "NCAA"
    
    p_copy["origin_type"] = origin_type
    
    # Extract country / league tag
    if "Real Madrid" in origin:
        country = "Espanha"
        league = "Liga ACB / EuroLeague"
        club = "Real Madrid Baloncesto"
    elif "Barcelona" in origin:
        country = "Espanha"
        league = "Liga ACB / EuroLeague"
        club = "FC Barcelona"
    elif "SIG Strasbourg" in origin:
        country = "França"
        league = "LNB Pro A"
        club = "SIG Strasbourg"
    elif "Nanterre" in origin:
        country = "França"
        league = "LNB Pro A"
        club = "Nanterre 92"
    elif "Élan Béarnais" in origin:
        country = "França"
        league = "LNB Pro A"
        club = "Élan Béarnais Pau-Lacq-Orthez"
    elif "Cedevita" in origin:
        country = "Croácia"
        league = "Liga Croata / EuroCup"
        club = "KK Cedevita Zagreb"
    elif "Skyliners Frankfurt" in origin:
        country = "Alemanha"
        league = "Basketball Bundesliga (BBL)"
        club = "Fraport Skyliners"
    elif "Mega Basket" in origin:
        country = "Sérvia"
        league = "KLS / Liga ABA"
        club = "KK Mega Basket"
    elif "FMP Belgrade" in origin:
        country = "Sérvia"
        league = "KLS / Liga ABA"
        club = "KK FMP Belgrado"
    elif "Žalgiris Kaunas" in origin:
        country = "Lituânia"
        league = "LKL / EuroLeague"
        club = "BC Žalgiris Kaunas"
    elif "Olimpija" in origin:
        country = "Eslovênia"
        league = "Liga Eslovena / ABA"
        club = "KK Olimpija Ljubljana"
    elif "Capo d'Orlando" in origin:
        country = "Itália"
        league = "Lega Basket Serie A"
        club = "Orlandina Basket"
    elif "Gran Canaria" in origin:
        country = "Espanha"
        league = "Liga ACB / EuroCup"
        club = "CB Gran Canaria"
    elif "Adelaide 36ers" in origin:
        country = "Austrália"
        league = "NBL (Austrália)"
        club = "Adelaide 36ers"
    elif "Chalmette" in origin:
        country = "EUA"
        league = "High School (Louisiana)"
        club = "Chalmette High School Owls"
    elif "IMG Academy" in origin:
        country = "EUA"
        league = "High School Prep (Flórida)"
        club = "IMG Academy Ascenders"
    else:
        country = "EUA"
        league = "NCAA Division I"
        club = f"{origin} Basketball"

    p_copy["origin_country"] = country
    p_copy["origin_league"] = league
    p_copy["origin_club_full"] = club

    enriched_players.append(p_copy)

if __name__ == "__main__":
    count_downloaded = 0
    for p in enriched_players:
        img_file = p["image_filename"]
        if not os.path.exists(os.path.join("assets/players", img_file)):
            success = fetch_wiki_thumbnail(p["player"], img_file)
            if success:
                count_downloaded += 1
    
    print(f"Downloaded {count_downloaded} additional player photos.")
    
    # Save enriched players to json for the web interface
    with open("data/enriched_prospects.json", "w", encoding="utf-8") as f:
        json.dump(enriched_players, f, indent=2, ensure_ascii=False)
    print("Saved data/enriched_prospects.json")
