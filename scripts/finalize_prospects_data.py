import json
import os
import sys

sys.path.append(os.path.abspath("."))
# Import OFFLINE_KNOWLEDGE_BASE from draft_room.py
import draft_room

with open("data/enriched_prospects.json", "r", encoding="utf-8") as f:
    prospects = json.load(f)

# Team badge mapping
BADGE_MAP = {
    "Real Madrid": "assets/teams/real_madrid.svg",
    "Barcelona": "assets/teams/barcelona.svg",
    "SIG Strasbourg": "assets/teams/sig_strasbourg.svg",
    "Cedevita": "assets/teams/cedevita.svg",
    "Nanterre": "assets/teams/nanterre_92.svg",
    "Skyliners Frankfurt": "assets/teams/skyliners_frankfurt.svg",
    "Žalgiris Kaunas": "assets/teams/zalgiris_kaunas.svg",
    "Mega Basket": "assets/teams/mega_basket.svg",
    "FMP Belgrade": "assets/teams/fmp_belgrade.svg",
    "Duke": "assets/teams/duke.svg",
    "Kentucky": "assets/teams/kentucky.svg",
    "UCLA": "assets/teams/ucla.svg",
    "Arizona": "assets/teams/arizona.svg",
    "Villanova": "assets/teams/villanova.svg",
    "North Carolina": "assets/teams/north_carolina.svg",
    "Kansas": "assets/teams/kansas.svg",
    "Texas": "assets/teams/texas.svg",
    "Michigan State": "assets/teams/michigan_state.svg",
    "Oklahoma": "assets/teams/oklahoma.svg",
    "Washington": "assets/teams/washington.svg",
    "Louisville": "assets/teams/louisville.svg",
    "Alabama": "assets/teams/alabama.svg",
    "Gonzaga": "assets/teams/gonzaga.svg",
    "Oregon": "assets/teams/oregon.svg",
    "Chalmette": "assets/teams/chalmette_hs.svg",
    "IMG Academy": "assets/teams/img_academy.svg",
}

FLAG_MAP = {
    "Espanha": "🇪🇸",
    "França": "🇫🇷",
    "Croácia": "🇭🇷",
    "Alemanha": "🇩🇪",
    "Lituânia": "🇱🇹",
    "Sérvia": "🇷🇸",
    "Eslovênia": "🇸🇮",
    "Itália": "🇮🇹",
    "Austrália": "🇦🇺",
    "EUA": "🇺🇸"
}

existing_images = set(os.listdir("assets/players"))

for p in prospects:
    name = p["player"]
    origin = p.get("origin", "")
    
    # Assign team badge
    assigned_badge = None
    for k, bpath in BADGE_MAP.items():
        if k in origin:
            assigned_badge = bpath
            break
    p["team_badge"] = assigned_badge
    
    # Flag emoji
    country = p.get("origin_country", "EUA")
    p["country_flag"] = FLAG_MAP.get(country, "🌐")
    
    # Check if local image file exists
    img_filename = p.get("image_filename", "")
    if img_filename in existing_images:
        p["local_image"] = f"assets/players/{img_filename}"
    else:
        # Check alternative common names
        p["local_image"] = "assets/players/default_player.svg"
    
    # Attach multi-agent offline debate if available
    kb_data = draft_room.OFFLINE_KNOWLEDGE_BASE.get(name)
    if kb_data:
        p["multiagent_debate"] = kb_data
    else:
        # Build simulated agent verdicts based on player profile
        bpm = p.get("stats", {}).get("BPM_est", 6.0)
        ts = p.get("stats", {}).get("TS%", 55.0)
        ft = p.get("stats", {}).get("FT%", 70.0)
        strengths = p.get("scout_reports", {}).get("strengths", [])
        concerns = p.get("scout_reports", {}).get("concerns", [])
        
        p["multiagent_debate"] = {
            "quant": {
                "agent_id": "quant_agent",
                "agent_title": "Head of Advanced Metrics & Biometrics",
                "score": round(max(5.0, min(9.9, bpm * 0.4 + (ts/10.0) - 0.5)), 1),
                "verdict": f"BPM projetado de {bpm:+.1f} com {ts:.1f}% TS% e lance livre em {ft:.1f}%.",
                "metric_highlights": [
                    f"TS% de {ts:.1f}% e USG% de {p['stats'].get('USG%', 20.0):.1f}%.",
                    f"Lance livre ({ft:.1f}%) calibrando a projeção de arremesso.",
                    f"Diferencial de envergadura: {p.get('biometrics', {}).get('wingspan_differential', 'N/D')}."
                ]
            },
            "tactical": {
                "agent_id": "tactical_agent",
                "agent_title": "Director of Scouting & Film Study",
                "score": round(max(5.0, min(9.5, 6.5 + (1.0 if ft > 75 else -0.5))), 1),
                "verdict": f"Scout tático em {origin}: {strengths[0] if strengths else 'Boa presença de quadra'}.",
                "tape_observations": strengths + concerns
            },
            "fit": {
                "agent_id": "fit_agent",
                "agent_title": "VP of Roster Strategy & Modern NBA Fit",
                "score": round(max(5.0, min(9.5, 7.0)), 1),
                "verdict": f"Encaixe funcional no basquete moderno para posição {p.get('position', 'G/F')}.",
                "strategic_arguments": [
                    f"Capacidade de atuar na rotação contemporânea da NBA.",
                    f"Histórico em {origin} ({p.get('origin_league', 'College')})."
                ]
            },
            "gm_consensus": {
                "war_room_chair": "Brad Stevens Archetype (General Manager)",
                "final_score": p.get("war_room", {}).get("gm_score", 7.0),
                "draft_board_tier": p.get("war_room", {}).get("gm_tier", "TIER 3 (Prospecto de Rotação)"),
                "consensus_verdict": p.get("historical_reality", {}).get("historical_verdict", "Avaliação equilibrada"),
                "tension_analysis": "Equilíbrio entre teto de desenvolvimento e eficiência demonstrada.",
                "projection": p.get("historical_reality", {}).get("career_arc", "Projetado para rotação")
            }
        }

with open("data/enriched_prospects.json", "w", encoding="utf-8") as f:
    json.dump(prospects, f, indent=2, ensure_ascii=False)

print("Successfully enriched prospects with badges, flags, and debate data!")
