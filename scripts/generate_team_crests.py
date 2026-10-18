import os
import sys

os.makedirs("assets/teams", exist_ok=True)

def create_svg(filename, svg_content):
    path = os.path.join("assets/teams", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"Created {filename}")

# Team SVGs with authentic brand palettes and clean vector geometry
TEAMS = {
    "real_madrid.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <defs>
    <radialGradient id="rmGold" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFE885"/>
      <stop offset="100%" stop-color="#E1B846"/>
    </radialGradient>
    <linearGradient id="rmPurple" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#7B2CBF"/>
      <stop offset="100%" stop-color="#4A0E8F"/>
    </linearGradient>
  </defs>
  <!-- Outer Gold Ring -->
  <circle cx="60" cy="65" r="46" fill="#FFFFFF" stroke="url(#rmGold)" stroke-width="7"/>
  <!-- Diagonal Purple Stripe -->
  <clipPath id="circleClip">
    <circle cx="60" cy="65" r="42"/>
  </clipPath>
  <g clip-path="url(#circleClip)">
    <polygon points="18,105 102,25 115,38 31,118" fill="url(#rmPurple)"/>
  </g>
  <!-- Royal Crown -->
  <path d="M38,28 L43,15 L60,24 L77,15 L82,28 Z" fill="url(#rmGold)" stroke="#9E7616" stroke-width="1.5"/>
  <circle cx="43" cy="14" r="3" fill="#D90429"/>
  <circle cx="60" cy="11" r="3.5" fill="#FFE885"/>
  <circle cx="77" cy="14" r="3" fill="#D90429"/>
  <path d="M57,7 L63,7 M60,4 L60,10" stroke="#FFE885" stroke-width="2"/>
  <!-- Monogram RMCF -->
  <text x="60" y="73" font-family="'Arial Black', sans-serif" font-size="24" font-weight="900" fill="#E1B846" text-anchor="middle" letter-spacing="-1">RM</text>
  <text x="60" y="88" font-family="'Arial', sans-serif" font-size="8" font-weight="bold" fill="#1E293B" text-anchor="middle" letter-spacing="1.5">REAL MADRID</text>
  <text x="60" y="98" font-family="'Arial', sans-serif" font-size="6.5" font-weight="bold" fill="#7B2CBF" text-anchor="middle">EUROLEAGUE</text>
</svg>''',

    "barcelona.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <defs>
    <clipPath id="fcbShield">
      <path d="M20,20 L100,20 Q100,75 60,110 Q20,75 20,20 Z"/>
    </clipPath>
  </defs>
  <!-- Shield Outline -->
  <path d="M18,18 L102,18 Q102,77 60,113 Q18,77 18,18 Z" fill="#EAB308" stroke="#A16207" stroke-width="2"/>
  <g clip-path="url(#fcbShield)">
    <!-- Top Left St George Cross -->
    <rect x="20" y="20" width="40" height="30" fill="#FFFFFF"/>
    <rect x="36" y="20" width="8" height="30" fill="#DC2626"/>
    <rect x="20" y="31" width="40" height="8" fill="#DC2626"/>
    <!-- Top Right Catalan Senyera -->
    <rect x="60" y="20" width="40" height="30" fill="#EAB308"/>
    <rect x="68" y="20" width="5" height="30" fill="#DC2626"/>
    <rect x="78" y="20" width="5" height="30" fill="#DC2626"/>
    <rect x="88" y="20" width="5" height="30" fill="#DC2626"/>
    <!-- Middle Gold Divider -->
    <rect x="20" y="50" width="80" height="8" fill="#EAB308"/>
    <text x="60" y="57" font-family="'Arial Black', sans-serif" font-size="7" font-weight="bold" fill="#1E1B4B" text-anchor="middle">FCB BASKET</text>
    <!-- Bottom Blaugrana Stripes -->
    <rect x="20" y="58" width="80" height="55" fill="#1E3A8A"/>
    <rect x="33" y="58" width="13" height="55" fill="#991B1B"/>
    <rect x="60" y="58" width="13" height="55" fill="#991B1B"/>
    <rect x="87" y="58" width="13" height="55" fill="#991B1B"/>
    <!-- Central Basketball -->
    <circle cx="60" cy="85" r="14" fill="#F97316" stroke="#9A3412" stroke-width="1.5"/>
    <path d="M46,85 Q60,80 74,85 M60,71 L60,99" stroke="#9A3412" stroke-width="1.2" fill="none"/>
  </g>
</svg>''',

    "sig_strasbourg.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <defs>
    <linearGradient id="sigRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EF4444"/>
      <stop offset="100%" stop-color="#991B1B"/>
    </linearGradient>
  </defs>
  <path d="M20,15 L100,15 Q100,75 60,110 Q20,75 20,15 Z" fill="url(#sigRed)" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="60" cy="55" r="28" fill="#FFFFFF"/>
  <circle cx="60" cy="55" r="24" fill="#F97316" stroke="#C2410C" stroke-width="1.5"/>
  <path d="M36,55 Q60,45 84,55 M60,31 L60,79" stroke="#C2410C" stroke-width="1.5" fill="none"/>
  <text x="60" y="52" font-family="'Arial Black', sans-serif" font-size="16" font-weight="900" fill="#FFFFFF" text-anchor="middle" stroke="#000000" stroke-width="0.8">SIG</text>
  <text x="60" y="65" font-family="'Arial Black', sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">STRASBOURG</text>
  <text x="60" y="95" font-family="'Arial', sans-serif" font-size="8" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">FRANCE (LNB)</text>
</svg>''',

    "cedevita.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <circle cx="60" cy="60" r="50" fill="#EA580C" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="60" cy="60" r="44" fill="#18181B"/>
  <circle cx="60" cy="60" r="28" fill="#EA580C"/>
  <path d="M32,60 Q60,45 88,60 M60,32 L60,88" stroke="#FFFFFF" stroke-width="2" fill="none"/>
  <text x="60" y="55" font-family="'Arial Black', sans-serif" font-size="14" font-weight="900" fill="#FFFFFF" text-anchor="middle">CEDEVITA</text>
  <text x="60" y="70" font-family="'Arial', sans-serif" font-size="8" font-weight="bold" fill="#FDBA74" text-anchor="middle">ZAGREB</text>
  <text x="60" y="95" font-family="'Arial', sans-serif" font-size="7" font-weight="bold" fill="#FFFFFF" text-anchor="middle">CROATIA</text>
</svg>''',

    "nanterre_92.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="15" y="15" width="90" height="90" rx="20" fill="#15803D" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="60" cy="50" r="24" fill="#FFFFFF"/>
  <text x="60" y="59" font-family="'Arial Black', sans-serif" font-size="26" font-weight="900" fill="#15803D" text-anchor="middle">92</text>
  <text x="60" y="86" font-family="'Arial Black', sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">NANTERRE</text>
  <text x="60" y="97" font-family="'Arial', sans-serif" font-size="7" font-weight="bold" fill="#BBF7D0" text-anchor="middle">FRANCE</text>
</svg>''',

    "skyliners_frankfurt.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <path d="M20,20 L100,20 L85,105 L35,105 Z" fill="#0284C7" stroke="#38BDF8" stroke-width="3"/>
  <polygon points="60,25 90,85 30,85" fill="#0369A1"/>
  <text x="60" y="55" font-family="'Arial Black', sans-serif" font-size="12" font-weight="900" fill="#FFFFFF" text-anchor="middle">SKYLINERS</text>
  <text x="60" y="72" font-family="'Arial Black', sans-serif" font-size="9" font-weight="bold" fill="#BAE6FD" text-anchor="middle">FRANKFURT</text>
  <text x="60" y="95" font-family="'Arial', sans-serif" font-size="7" font-weight="bold" fill="#FFFFFF" text-anchor="middle">GERMANY BBL</text>
</svg>''',

    "zalgiris_kaunas.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <path d="M20,15 L100,15 Q100,75 60,110 Q20,75 20,15 Z" fill="#166534" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="60" cy="52" r="26" fill="#FFFFFF"/>
  <circle cx="60" cy="52" r="22" fill="#15803D"/>
  <text x="60" y="60" font-family="'Arial Black', sans-serif" font-size="24" font-weight="900" fill="#FFFFFF" text-anchor="middle">Ž</text>
  <text x="60" y="90" font-family="'Arial Black', sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">ŽALGIRIS</text>
  <text x="60" y="101" font-family="'Arial', sans-serif" font-size="6.5" font-weight="bold" fill="#86EFAC" text-anchor="middle">KAUNAS • LITUÂNIA</text>
</svg>''',

    "mega_basket.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="15" y="15" width="90" height="90" rx="22" fill="#EC4899" stroke="#FDE047" stroke-width="4"/>
  <circle cx="60" cy="52" r="24" fill="#FACC15"/>
  <text x="60" y="59" font-family="'Arial Black', sans-serif" font-size="14" font-weight="900" fill="#BE185D" text-anchor="middle">MEGA</text>
  <text x="60" y="86" font-family="'Arial Black', sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">BASKET</text>
  <text x="60" y="97" font-family="'Arial', sans-serif" font-size="7" font-weight="bold" fill="#FDE047" text-anchor="middle">SÉRVIA (ABA)</text>
</svg>''',

    "fmp_belgrade.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <path d="M20,15 L100,15 Q100,80 60,110 Q20,80 20,15 Z" fill="#DC2626" stroke="#FFFFFF" stroke-width="3"/>
  <text x="60" y="55" font-family="'Arial Black', sans-serif" font-size="22" font-weight="900" fill="#FFFFFF" text-anchor="middle">FMP</text>
  <text x="60" y="75" font-family="'Arial Black', sans-serif" font-size="9" font-weight="bold" fill="#FEF08A" text-anchor="middle">BELGRADE</text>
  <text x="60" y="95" font-family="'Arial', sans-serif" font-size="7" font-weight="bold" fill="#FFFFFF" text-anchor="middle">SERBIA</text>
</svg>''',

    "duke.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#003087" stroke="#FFFFFF" stroke-width="3"/>
  <text x="60" y="76" font-family="'Times New Roman', serif" font-size="64" font-weight="900" fill="#FFFFFF" text-anchor="middle" font-style="italic">D</text>
  <text x="60" y="98" font-family="'Arial Black', sans-serif" font-size="9" font-weight="bold" fill="#93C5FD" text-anchor="middle" letter-spacing="1">BLUE DEVILS</text>
</svg>''',

    "kentucky.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#0033A0" stroke="#FFFFFF" stroke-width="3"/>
  <text x="48" y="72" font-family="'Arial Black', sans-serif" font-size="44" font-weight="900" fill="#FFFFFF" text-anchor="middle">U</text>
  <text x="74" y="80" font-family="'Arial Black', sans-serif" font-size="44" font-weight="900" fill="#FFFFFF" text-anchor="middle">K</text>
  <text x="60" y="100" font-family="'Arial Black', sans-serif" font-size="8.5" font-weight="bold" fill="#93C5FD" text-anchor="middle" letter-spacing="1">WILDCATS</text>
</svg>''',

    "ucla.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#2D68C4" stroke="#F2A900" stroke-width="4"/>
  <text x="60" y="68" font-family="'Brush Script MT', 'Arial', cursive" font-size="36" font-weight="bold" fill="#F2A900" text-anchor="middle">Ucla</text>
  <text x="60" y="92" font-family="'Arial Black', sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="1.5">BRUINS</text>
</svg>''',

    "arizona.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#0C2340" stroke="#AB0520" stroke-width="4"/>
  <text x="60" y="74" font-family="'Impact', 'Arial Black', sans-serif" font-size="56" fill="#AB0520" text-anchor="middle" stroke="#FFFFFF" stroke-width="1.5">A</text>
  <text x="60" y="96" font-family="'Arial Black', sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">WILDCATS</text>
</svg>''',

    "villanova.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#00205B" stroke="#13B5EA" stroke-width="4"/>
  <text x="60" y="74" font-family="'Arial Black', sans-serif" font-size="54" font-weight="900" fill="#FFFFFF" text-anchor="middle" stroke="#13B5EA" stroke-width="1.5">V</text>
  <text x="60" y="96" font-family="'Arial Black', sans-serif" font-size="9" font-weight="bold" fill="#13B5EA" text-anchor="middle">WILDCATS</text>
</svg>''',

    "north_carolina.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#7BAFD4" stroke="#FFFFFF" stroke-width="3"/>
  <text x="48" y="70" font-family="'Arial Black', sans-serif" font-size="42" font-weight="900" fill="#FFFFFF" text-anchor="middle">N</text>
  <text x="72" y="76" font-family="'Arial Black', sans-serif" font-size="42" font-weight="900" fill="#FFFFFF" text-anchor="middle">C</text>
  <text x="60" y="98" font-family="'Arial Black', sans-serif" font-size="8.5" font-weight="bold" fill="#00205B" text-anchor="middle">TAR HEELS</text>
</svg>''',

    "kansas.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#0051BA" stroke="#E8000D" stroke-width="4"/>
  <text x="60" y="70" font-family="'Arial Black', sans-serif" font-size="38" font-weight="900" fill="#E8000D" text-anchor="middle" stroke="#FFFFFF" stroke-width="1.5">KU</text>
  <text x="60" y="95" font-family="'Arial Black', sans-serif" font-size="9" font-weight="bold" fill="#FFC82D" text-anchor="middle">JAYHAWKS</text>
</svg>''',

    "texas.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#BF5700" stroke="#FFFFFF" stroke-width="3"/>
  <!-- Longhorn silhouette -->
  <path d="M22,46 Q40,38 50,56 L60,65 L70,56 Q80,38 98,46 Q86,58 76,66 L74,76 L46,76 L44,66 Q34,58 22,46 Z" fill="#FFFFFF"/>
  <text x="60" y="98" font-family="'Arial Black', sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">LONGHORNS</text>
</svg>''',

    "michigan_state.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#18453B" stroke="#FFFFFF" stroke-width="3"/>
  <!-- Spartan Helmet -->
  <path d="M60,26 Q76,26 76,46 L76,60 L68,60 L68,48 Q68,40 60,40 Q52,40 52,48 L52,60 L44,60 L44,46 Q44,26 60,26 Z" fill="#FFFFFF"/>
  <path d="M50,60 L70,60 L66,78 L54,78 Z" fill="#FFFFFF"/>
  <text x="60" y="98" font-family="'Arial Black', sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">SPARTANS</text>
</svg>''',

    "oklahoma.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#841617" stroke="#FDF6EE" stroke-width="4"/>
  <text x="48" y="70" font-family="'Impact', 'Arial Black', sans-serif" font-size="44" fill="#FDF6EE" text-anchor="middle">O</text>
  <text x="72" y="76" font-family="'Impact', 'Arial Black', sans-serif" font-size="44" fill="#FDF6EE" text-anchor="middle">U</text>
  <text x="60" y="98" font-family="'Arial Black', sans-serif" font-size="8.5" font-weight="bold" fill="#FDF6EE" text-anchor="middle">SOONERS</text>
</svg>''',

    "washington.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#4B2E83" stroke="#B7A57A" stroke-width="4"/>
  <text x="60" y="76" font-family="'Impact', 'Arial Black', sans-serif" font-size="54" fill="#B7A57A" text-anchor="middle" stroke="#FFFFFF" stroke-width="1">W</text>
  <text x="60" y="98" font-family="'Arial Black', sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">HUSKIES</text>
</svg>''',

    "louisville.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#AD0000" stroke="#000000" stroke-width="4"/>
  <circle cx="60" cy="52" r="24" fill="#000000"/>
  <text x="60" y="60" font-family="'Impact', sans-serif" font-size="32" fill="#AD0000" text-anchor="middle" stroke="#FFFFFF" stroke-width="1">L</text>
  <text x="60" y="95" font-family="'Arial Black', sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">CARDINALS</text>
</svg>''',

    "alabama.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#9E1B32" stroke="#FFFFFF" stroke-width="3"/>
  <text x="60" y="76" font-family="'Times New Roman', serif" font-size="58" font-weight="bold" fill="#FFFFFF" text-anchor="middle" font-style="italic">A</text>
  <text x="60" y="98" font-family="'Arial Black', sans-serif" font-size="8" font-weight="bold" fill="#FFFFFF" text-anchor="middle">CRIMSON TIDE</text>
</svg>''',

    "gonzaga.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#041E42" stroke="#C1C6C8" stroke-width="3"/>
  <text x="60" y="74" font-family="'Arial Black', sans-serif" font-size="48" font-weight="900" fill="#BA0C2F" text-anchor="middle" stroke="#FFFFFF" stroke-width="1.5">G</text>
  <text x="60" y="98" font-family="'Arial Black', sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">BULLDOGS</text>
</svg>''',

    "oregon.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#154734" stroke="#FEE123" stroke-width="4"/>
  <ellipse cx="60" cy="56" rx="26" ry="20" fill="none" stroke="#FEE123" stroke-width="10"/>
  <text x="60" y="98" font-family="'Arial Black', sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">DUCKS</text>
</svg>''',

    "chalmette_hs.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#1E293B" stroke="#E11D48" stroke-width="4"/>
  <circle cx="60" cy="50" r="22" fill="#E11D48"/>
  <text x="60" y="58" font-family="'Impact', sans-serif" font-size="24" fill="#FFFFFF" text-anchor="middle">CHS</text>
  <text x="60" y="86" font-family="'Arial Black', sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">CHALMETTE</text>
  <text x="60" y="98" font-family="'Arial', sans-serif" font-size="7" font-weight="bold" fill="#FDA4AF" text-anchor="middle">HIGH SCHOOL</text>
</svg>''',

    "img_academy.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="10" y="10" width="100" height="100" rx="16" fill="#0F172A" stroke="#0284C7" stroke-width="4"/>
  <polygon points="60,25 85,55 35,55" fill="#0284C7"/>
  <text x="60" y="74" font-family="'Arial Black', sans-serif" font-size="16" font-weight="900" fill="#FFFFFF" text-anchor="middle">IMG</text>
  <text x="60" y="90" font-family="'Arial Black', sans-serif" font-size="8" font-weight="bold" fill="#38BDF8" text-anchor="middle">ACADEMY</text>
  <text x="60" y="100" font-family="'Arial', sans-serif" font-size="6.5" font-weight="bold" fill="#94A3B8" text-anchor="middle">PREP HIGH SCHOOL</text>
</svg>'''
}

for fname, code in TEAMS.items():
    create_svg(fname, code)

print(f"Generated {len(TEAMS)} vector team badges.")
