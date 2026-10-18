import json
import re
import sys

with open("war_room_verdicts.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

verdicts_by_player = {}

for line in lines:
    line_clean = line.strip()
    if not line_clean.startswith("|") or ":---" in line_clean or "Jogador" in line_clean:
        continue
    cols = [c.strip() for c in line_clean.split("|")[1:-1]]
    if len(cols) >= 7:
        player_raw = cols[0].replace("**", "").strip()
        try:
            year = int(cols[1])
            quant = float(cols[2])
            tactical = float(cols[3])
            fit = float(cols[4])
            gm_col = cols[5]
            reality = cols[6]
            
            # gm_col format: **7.3** (TIER 3 (Starter Competente / Armadilha na Pick #1))
            score_match = re.search(r'\*\*([\d\.]+)\*\*', gm_col)
            gm_score = float(score_match.group(1)) if score_match else 0.0
            tier_match = re.search(r'\((.+)\)', gm_col)
            gm_tier = tier_match.group(1) if tier_match else "Prospecto"
            
            verdicts_by_player[player_raw] = {
                "quant_score": quant,
                "tactical_score": tactical,
                "fit_score": fit,
                "gm_score": gm_score,
                "gm_tier": gm_tier,
                "reality": reality
            }
        except Exception:
            pass

print(f"Parsed {len(verdicts_by_player)} player verdicts from tables.")

# Dossiers parsing
with open("war_room_verdicts.md", "r", encoding="utf-8") as f:
    full_text = f.read()

dossier_sections = re.split(r'###\s*🏀\s*', full_text)[1:]
dossiers_by_player = {}
for sec in dossier_sections:
    first_line = sec.split("\n")[0].strip()
    name = re.sub(r'\(.*?\)', '', first_line).strip()
    dossiers_by_player[name] = sec.strip()

print(f"Parsed {len(dossiers_by_player)} player dossiers.")

# Load enriched prospects
with open("data/enriched_prospects.json", "r", encoding="utf-8") as f:
    prospects = json.load(f)

for p in prospects:
    name = p["player"]
    # Look up in verdicts
    v = verdicts_by_player.get(name)
    if not v:
        for k, val in verdicts_by_player.items():
            if k.lower() == name.lower() or name.lower() in k.lower():
                v = val
                break
    if v:
        p["war_room"] = v
    else:
        # Default tier and score based on draft pick and BPM
        bpm = p.get("stats", {}).get("BPM_est", 5.0)
        p["war_room"] = {
            "quant_score": round(max(5.0, min(9.9, bpm * 0.4 + 4.5)), 1),
            "tactical_score": 6.8,
            "fit_score": 6.8,
            "gm_score": round(max(5.0, min(9.9, bpm * 0.35 + 5.2)), 1),
            "gm_tier": "TIER 3 (Rotação Sólida)",
            "reality": p.get("historical_reality", {}).get("career_arc", "")
        }

    # Look up dossier text
    d = dossiers_by_player.get(name)
    if not d:
        for k, val in dossiers_by_player.items():
            if k.lower() in name.lower() or name.lower() in k.lower():
                d = val
                break
    p["has_detailed_dossier"] = bool(d)

with open("data/enriched_prospects.json", "w", encoding="utf-8") as f:
    json.dump(prospects, f, indent=2, ensure_ascii=False)

print("Saved enriched_prospects.json with complete war room data.")
