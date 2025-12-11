# WAIQ_Knuckle

**W**eb **A**pplication **I**nterview **Q**uestions Portal — “Hack the Planet” training edition.

Deliberately vulnerable web app for practicing AppSec interview-style vulns.

## ⚠️ WARNING
This app is intentionally vulnerable. See [SECURITY.md](SECURITY.md). Do **not** use real creds or expose to the internet.

## Stack
- Python (Flask), SQLite
- (Optional later) Go sidecar for extra vuln demos
- Simple server-rendered Jinja templates

## Current branches
- `main` (release), `dev` (staging), `build` (active work)

## Quickstart (local, dev only)
```bash
cd WAIQ_Knuckle
python -m venv venv && source venv/bin/activate   # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
python app/app.py
# browse http://localhost:5000
```

## Seeded creds / data (intentionally weak)
- Users: `admin/admin123`, `alice/password`, `zer0_c00l/hacktheplanet`, `acidburn/crashoverride`
- Guestbook has stored XSS samples (“Hack the Planet” refs)

## Implemented modules (mapped from AppSec_Questions_Modules_Ideas)
- XSS Guestbook (reflected/stored) — Q4, Q8, Q19, Q41, Q44, Q65
- SQLi Login (string-built query) — Q5, Q28, Q50, Q64
- IDOR Profile Viewer — Q10, Q31
- Coming soon: File Upload (no validation), CSRF (no token)

## Roadmap
- Add more modules from the 91-question guide (Upload, CSRF, SSTI, SSRF, Open Redirect, etc.)
- Add optional Go service for SSRF/IDOR demos
- Add CI (pytest + bandit; go test + gosec)
- Add a simple module “shop” UI and lab instructions per module