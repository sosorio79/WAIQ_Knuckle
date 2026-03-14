#!/usr/bin/env python3
"""Generate SVG icons for each WAIQ Knuckle module."""
from pathlib import Path

# Fallout Terminal (phosphor green on dark)
ACCENT = "#39ff14"   # phosphor green
DARK = "#33ee33"    # text/strokes on dark
LIGHT = "#228b22"   # muted strokes
BG = "#0d100d"      # card/dark

OUT = Path(__file__).resolve().parent.parent / "app" / "static" / "images" / "modules"
OUT.mkdir(parents=True, exist_ok=True)

# Each module: (slug, SVG path/content as string - use {accent}, {dark}, {light})
# Using simplified inline SVG paths for each icon concept
ICONS = {
    "xss-guestbook": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <text x="64" y="45" font-family="monospace" font-size="28" fill="{DARK}" text-anchor="middle">&lt;/&gt;</text>
  <path d="M30 75 L50 55 L70 75 L98 55" stroke="{ACCENT}" stroke-width="3" fill="none"/>
  <circle cx="64" cy="90" r="8" fill="{ACCENT}" opacity="0.8"/>
</svg>''',
    "sqli-login": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <ellipse cx="64" cy="50" rx="30" ry="18" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M34 50 L34 95 L94 95 L94 50" fill="none" stroke="{DARK}" stroke-width="2"/>
  <line x1="64" y1="50" x2="64" y2="95" stroke="{DARK}" stroke-width="2"/>
  <path d="M52 75 L64 65 L76 75" stroke="{ACCENT}" stroke-width="2" fill="none"/>
  <rect x="50" y="85" width="28" height="4" rx="1" fill="{ACCENT}"/>
</svg>''',
    "idor-profile": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <circle cx="64" cy="42" r="18" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M40 95 Q40 70 64 70 Q88 70 88 95" fill="none" stroke="{DARK}" stroke-width="2"/>
  <rect x="20" y="35" width="28" height="28" rx="4" fill="{ACCENT}" opacity="0.6"/>
  <text x="34" y="55" font-size="16" fill="#39ff14" text-anchor="middle">ID</text>
</svg>''',
    "ssrf-proxy": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <circle cx="35" cy="64" r="16" fill="none" stroke="{DARK}" stroke-width="2"/>
  <circle cx="93" cy="64" r="16" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M51 64 L77 64" stroke="{ACCENT}" stroke-width="3"/>
  <path d="M70 54 L80 64 L70 74" stroke="{ACCENT}" stroke-width="2" fill="none"/>
  <circle cx="64" cy="100" r="8" fill="{ACCENT}"/>
</svg>''',
    "csrf-no-token": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <path d="M30 64 L50 44 L50 54 L78 54 L78 74 L50 74 L50 84 Z" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M98 64 L78 84 L78 74 L50 74 L50 54 L78 54 L78 44 Z" fill="none" stroke="{ACCENT}" stroke-width="2"/>
</svg>''',
    "upload-no-validation": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <rect x="44" y="55" width="40" height="50" rx="4" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M64 55 L64 25 M54 35 L64 25 L74 35" stroke="{ACCENT}" stroke-width="2" fill="none"/>
  <path d="M30 100 L98 100" stroke="{LIGHT}" stroke-width="1"/>
</svg>''',
    "web-cache": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <rect x="24" y="40" width="80" height="50" rx="4" fill="none" stroke="{DARK}" stroke-width="2"/>
  <line x1="24" y1="55" x2="104" y2="55" stroke="{LIGHT}"/>
  <line x1="24" y1="70" x2="104" y2="70" stroke="{LIGHT}"/>
  <path d="M44 95 L64 75 L84 95" stroke="{ACCENT}" stroke-width="2" fill="none"/>
</svg>''',
    "session-management": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <rect x="32" y="35" width="64" height="45" rx="6" fill="none" stroke="{DARK}" stroke-width="2"/>
  <circle cx="48" cy="55" r="6" fill="{ACCENT}"/>
  <circle cx="64" cy="55" r="6" fill="{ACCENT}"/>
  <circle cx="80" cy="55" r="6" fill="{ACCENT}"/>
  <path d="M48 75 L64 85 L80 75" stroke="{DARK}" stroke-width="2" fill="none"/>
</svg>''',
    "jwt-auth": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <rect x="24" y="40" width="80" height="18" rx="2" fill="none" stroke="{DARK}" stroke-width="2"/>
  <rect x="24" y="62" width="80" height="18" rx="2" fill="none" stroke="{DARK}" stroke-width="2"/>
  <rect x="24" y="84" width="80" height="18" rx="2" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M64 20 L64 38 M64 58 L64 80 M64 102 L64 108" stroke="{ACCENT}" stroke-width="2"/>
</svg>''',
    "encoding-crypto": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <path d="M64 30 L80 50 L80 78 L64 98 L48 78 L48 50 Z" fill="none" stroke="{DARK}" stroke-width="2"/>
  <rect x="56" y="55" width="16" height="22" rx="2" fill="{ACCENT}"/>
</svg>''',
    "request-smuggling": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <rect x="20" y="35" width="35" height="20" rx="2" fill="none" stroke="{DARK}" stroke-width="2"/>
  <rect x="73" y="35" width="35" height="20" rx="2" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M55 45 L73 45" stroke="{ACCENT}" stroke-width="2"/>
  <path d="M64 55 L64 73 M58 67 L64 73 L70 67" stroke="{ACCENT}" stroke-width="2" fill="none"/>
</svg>''',
    "hpp-waf": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <rect x="30" y="40" width="68" height="48" rx="4" fill="none" stroke="{DARK}" stroke-width="2"/>
  <line x1="40" y1="55" x2="88" y2="55" stroke="{LIGHT}"/>
  <line x1="40" y1="70" x2="88" y2="70" stroke="{LIGHT}"/>
  <line x1="40" y1="85" x2="88" y2="85" stroke="{LIGHT}"/>
  <circle cx="55" cy="55" r="4" fill="{ACCENT}"/>
  <circle cx="55" cy="70" r="4" fill="{ACCENT}"/>
</svg>''',
    "same-origin-cors": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <circle cx="45" cy="55" r="22" fill="none" stroke="{DARK}" stroke-width="2"/>
  <circle cx="83" cy="55" r="22" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M67 55 L77 55" stroke="{ACCENT}" stroke-width="3"/>
  <path d="M61 55 L51 55" stroke="{ACCENT}" stroke-width="3"/>
  <path d="M64 40 L64 70" stroke="{LIGHT}" stroke-dasharray="4 2"/>
</svg>''',
    "websockets": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <path d="M35 55 L50 75 L65 45 L80 75 L93 55" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M35 80 L50 60 L65 90 L80 60 L93 80" fill="none" stroke="{ACCENT}" stroke-width="2"/>
</svg>''',
    "csp": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <path d="M64 25 L95 45 L95 83 L64 103 L33 83 L33 45 Z" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M64 45 L85 58 L85 90 L64 103 L43 90 L43 58 Z" fill="{ACCENT}" opacity="0.5"/>
</svg>''',
    "business-logic": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <circle cx="40" cy="45" r="12" fill="none" stroke="{DARK}" stroke-width="2"/>
  <circle cx="88" cy="45" r="12" fill="none" stroke="{DARK}" stroke-width="2"/>
  <circle cx="64" cy="95" r="12" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M48 52 L58 80" stroke="{ACCENT}" stroke-width="2"/>
  <path d="M80 52 L70 80" stroke="{ACCENT}" stroke-width="2"/>
</svg>''',
    "ssti": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <text x="64" y="50" font-family="monospace" font-size="24" fill="{DARK}" text-anchor="middle">{{{{ }}}}</text>
  <path d="M40 70 L64 90 L88 70" stroke="{ACCENT}" stroke-width="2" fill="none"/>
</svg>''',
    "deserialization": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <rect x="35" y="45" width="58" height="40" rx="4" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M45 55 L75 55 M45 65 L75 65 M45 75 L65 75" stroke="{LIGHT}"/>
  <path d="M93 65 L105 65 M93 75 L105 75" stroke="{ACCENT}" stroke-width="2"/>
</svg>''',
    "command-injection": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <rect x="24" y="30" width="80" height="68" rx="4" fill="#1e1e1e"/>
  <line x1="35" y1="50" x2="75" y2="50" stroke="#4ec9b0"/>
  <line x1="35" y1="65" x2="65" y2="65" stroke="#4ec9b0"/>
  <line x1="35" y1="80" x2="85" y2="80" stroke="{ACCENT}"/>
  <rect x="35" y="88" width="20" height="4" fill="{ACCENT}"/>
</svg>''',
    "prototype-pollution": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <circle cx="64" cy="40" r="15" fill="none" stroke="{DARK}" stroke-width="2"/>
  <circle cx="40" cy="85" r="12" fill="none" stroke="{DARK}" stroke-width="2"/>
  <circle cx="88" cy="85" r="12" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M55 52 L45 78 M73 52 L83 78" stroke="{ACCENT}" stroke-width="2"/>
</svg>''',
    "api-security": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <path d="M40 45 L55 60 L40 75 L55 60 L88 60" fill="none" stroke="{DARK}" stroke-width="2"/>
  <rect x="30" y="85" width="68" height="18" rx="4" fill="none" stroke="{ACCENT}" stroke-width="2"/>
  <line x1="38" y1="94" x2="90" y2="94" stroke="{ACCENT}"/>
</svg>''',
    "xxe": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <text x="64" y="50" font-family="monospace" font-size="20" fill="{DARK}" text-anchor="middle">&lt;?xml&gt;</text>
  <path d="M35 65 L50 80 L65 65 L80 80 L93 65" stroke="{ACCENT}" stroke-width="2" fill="none"/>
</svg>''',
    "information-disclosure": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <rect x="35" y="35" width="58" height="58" rx="4" fill="none" stroke="{DARK}" stroke-width="2"/>
  <line x1="45" y1="55" x2="83" y2="55" stroke="{LIGHT}"/>
  <line x1="45" y1="70" x2="75" y2="70" stroke="{LIGHT}"/>
  <circle cx="50" cy="90" r="8" fill="{ACCENT}"/>
  <path d="M50 82 L50 86 M48 90 L52 90" stroke="white" stroke-width="1.5"/>
</svg>''',
    "sensitive-data-url": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <text x="64" y="55" font-family="monospace" font-size="14" fill="{DARK}" text-anchor="middle">https://...</text>
  <rect x="28" y="65" width="72" height="4" rx="1" fill="{LIGHT}"/>
  <circle cx="64" cy="95" r="10" fill="{ACCENT}"/>
  <path d="M64 88 L64 92 M61 95 L67 95" stroke="white" stroke-width="2"/>
</svg>''',
    "open-redirect": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <circle cx="45" cy="64" r="14" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M59 64 L85 64 L85 44 L105 64 L85 84 L85 64" stroke="{ACCENT}" stroke-width="2" fill="none"/>
</svg>''',
    "captcha": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <rect x="24" y="40" width="80" height="48" rx="6" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M40 65 Q50 55 64 65 Q78 75 88 65" stroke="{LIGHT}" stroke-width="2" fill="none"/>
  <circle cx="52" cy="58" r="3" fill="{ACCENT}"/>
  <circle cx="76" cy="58" r="3" fill="{ACCENT}"/>
</svg>''',
    "formula-injection": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <rect x="28" y="35" width="72" height="58" rx="2" fill="none" stroke="{DARK}" stroke-width="2"/>
  <line x1="28" y1="55" x2="100" y2="55" stroke="{LIGHT}"/>
  <line x1="28" y1="75" x2="100" y2="75" stroke="{LIGHT}"/>
  <line x1="48" y1="35" x2="48" y2="93" stroke="{LIGHT}"/>
  <text x="38" y="68" font-size="16" fill="{ACCENT}" text-anchor="middle">=</text>
</svg>''',
    "html-injection": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <text x="64" y="55" font-family="monospace" font-size="24" fill="{DARK}" text-anchor="middle">&lt;h1&gt;</text>
  <path d="M40 75 L64 95 L88 75" stroke="{ACCENT}" stroke-width="2" fill="none"/>
</svg>''',
    "crlf-injection": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <line x1="30" y1="45" x2="98" y2="45" stroke="{DARK}"/>
  <line x1="30" y1="65" x2="98" y2="65" stroke="{DARK}"/>
  <line x1="30" y1="85" x2="98" y2="85" stroke="{DARK}"/>
  <path d="M50 55 L60 65 L50 75 M55 65 L95 65" stroke="{ACCENT}" stroke-width="2" fill="none"/>
</svg>''',
    "network-tls": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <path d="M64 25 L95 45 L95 75 L64 95 L33 75 L33 45 Z" fill="none" stroke="{DARK}" stroke-width="2"/>
  <rect x="52" y="55" width="24" height="22" rx="2" fill="{ACCENT}"/>
  <circle cx="64" cy="68" r="3" fill="white"/>
</svg>''',
    "scoping": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <circle cx="64" cy="64" r="35" fill="none" stroke="{DARK}" stroke-width="2"/>
  <circle cx="64" cy="64" r="20" fill="none" stroke="{ACCENT}" stroke-width="2"/>
  <circle cx="64" cy="64" r="6" fill="{ACCENT}"/>
</svg>''',
    "general-web-security": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <circle cx="64" cy="55" r="25" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M64 30 L75 45 L92 48 L80 60 L83 78 L64 70 L45 78 L48 60 L36 48 L53 45 Z" fill="none" stroke="{ACCENT}" stroke-width="2"/>
</svg>''',
    "behavioral": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="12" fill="{BG}"/>
  <circle cx="64" cy="48" r="20" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M40 95 Q40 75 64 75 Q88 75 88 95" fill="none" stroke="{DARK}" stroke-width="2"/>
  <path d="M52 48 L60 56 L76 40" stroke="{ACCENT}" stroke-width="2" fill="none"/>
</svg>''',
}


def main():
    for slug, svg in ICONS.items():
        path = OUT / f"{slug}.svg"
        path.write_text(svg, encoding="utf-8")
        print(f"Wrote {path}")
    print(f"\nGenerated {len(ICONS)} icons in {OUT}")


if __name__ == "__main__":
    main()
