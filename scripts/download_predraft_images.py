import urllib.request
import urllib.parse
import json
import os
import sys
import time

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

os.makedirs("assets/players", exist_ok=True)
HEADERS = {"User-Agent": "NBAWarRoomScout/1.0 (contact: test@nbascouting.org)"}

def download_file_by_title(title, dest_filename, width=500):
    dest_path = os.path.join("assets/players", dest_filename)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        print(f"Already exists: {dest_filename}")
        return True

    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&iiurlwidth={width}&format=json"
    req = urllib.request.Request(api_url, headers=HEADERS)
    try:
        res = urllib.request.urlopen(req, timeout=10)
        data = json.loads(res.read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        page = list(pages.values())[0]
        imageinfo = page.get("imageinfo", [{}])[0]
        thumb_url = imageinfo.get("thumburl") or imageinfo.get("url")
        if not thumb_url:
            print(f"No thumburl for {title}")
            return False

        time.sleep(0.5)
        img_req = urllib.request.Request(thumb_url, headers=HEADERS)
        content = urllib.request.urlopen(img_req, timeout=15).read()
        with open(dest_path, "wb") as f:
            f.write(content)
        print(f"Downloaded {dest_filename} ({len(content)} bytes)")
        return True
    except Exception as e:
        print(f"Error downloading {title} as {dest_filename}: {e}")
        return False

# Mapping of players to verified pre-draft / early-career files on Wikimedia Commons
PREDRAFT_COMMONS_FILES = {
    # 2018
    "luka_doncic.jpg": "File:Luka Dončić 7 Real Madrid Baloncesto Euroleague 20171012.jpg",
    "trae_young.jpg": "File:20170329 MCDAAG Trae Young dribbling.jpg",
    "deandre_ayton.jpg": "File:20170329 MCDAAG Deandre Ayton on the wing.jpg",
    "marvin_bagley_iii.jpg": "File:DUKEvUNC 2018-03-03 - Marvin Bagley III.jpg",
    "jaren_jackson_jr.jpg": "File:20170329 MCDAAG Jaren Jackson Jr. inbounds.jpg",
    "grayson_allen.jpg": "File:DUKEvUNC 2018-03-03 - Grayson Allen, Kenny Williams, Marvin Bagley III.jpg",
    "shai_gilgeous-alexander.jpg": "File:2023-08-09 Deutschland gegen Kanada (Basketball-Länderspiel) by Sandro Halank–109.jpg",
    "mikal_bridges.jpg": "File:Mikal Bridges, April 2024.jpg",
    "miles_bridges.jpg": "File:Miles Bridges 2019.jpg",
    "collin_sexton.jpg": "File:Collin Sexton (51658041101) (cropped2).jpg",
    "michael_porter_jr.jpg": "File:Michael Porter Nuggets (cropped).jpg",
    "robert_williams_iii.jpg": "File:Robert Williams (51687558126) (cropped).jpg",
    "dzanan_musa.jpg": "File:Džanan Musa 13 Real Madrid Baloncesto Euroleague 20241017.jpg",
    "isaac_bonga.jpg": "File:Isaac Bonga 17 KK Partizan Euroleague 20260225 (3) (cropped).jpg",
    "rodions_kurucs.jpg": "File:Rodions Kurucs 7 Saski Baskonia Euroleague 20260115 (4).jpg",
    "mitchell_robinson.jpg": "File:Mitchell Robinson - 52976499477 (cropped).jpg",
    "anfernee_simons.jpg": "File:AnferneeSimons (cropped).jpg",
    "jalen_brunson.jpg": "File:Jalen Brunson 2023 (cropped).jpg",
    "donte_divincenzo.jpg": "File:Donte DiVincenzo (White House visit).jpg",

    # 2017
    "markelle_fultz.jpg": "File:20160330 MCDAAG Markelle Fultz dribbling.jpg",
    "lonzo_ball.jpg": "File:20160330 MCDAAG Lonzo Ball receives ball.jpg",
    "jayson_tatum.jpg": "File:2016 Jordan Brand Classic (26391615216).jpg",
    "donovan_mitchell.jpg": "File:Donovan Mitchell Utah 2018 (cropped).jpg",
    "deaaron_fox.jpg": "File:20160330 MCDAAG De'Aaron Fox at the top of the key.jpg",
    "bam_adebayo.jpg": "File:20160330 MCDAAG Bam Adebayo with the ball.jpg",
    "lauri_markkanen.jpg": "File:Lauri Markkanen, Cavaliers vs Rockets on December 15, 2021 (cropped).jpg",
    "frank_ntilikina.jpg": "File:Frank Ntilikina (cropped).jpg",
    "josh_hart.jpg": "File:Josh Hart - 52977163784 (cropped).jpg",
    "kyle_kuzma.jpg": "File:Kyle Kuzma (51815879993) (cropped).jpg",
    "derrick_white.jpg": "File:Boston Celtics player Derrick White on November 21, 2024 at the White House (cropped).jpg",
    "og_anunoby.jpg": "File:OG Anunoby (41708749222) (cropped).jpg",
    "jarrett_allen.jpg": "File:Jarrett Allen (51657225262) (cropped).jpg",
    "john_collins.jpg": "File:John Collins (5397460) (cropped).jpg",
    "zach_collins.jpg": "File:Zach Collins crop.jpg",
    "luke_kennard.jpg": "File:Wizards vs. Clippers - 51848728899 (cropped).jpg",
    "malik_monk.jpg": "File:Malik Monk - 51960020214 (cropped2).jpg",
    "isaiah_hartenstein.jpg": "File:Isaiah Hartenstein OKC Thunder 2025 NBA Cup (cropped).jpg",
}

if __name__ == "__main__":
    for filename, title in PREDRAFT_COMMONS_FILES.items():
        download_file_by_title(title, filename)
        time.sleep(0.3)
