# WAIQ_Knuckle

**W**eb **A**pplication **I**nterview **Q**uestions Portal — "Hack the Planet" training edition.

Deliberately vulnerable web app for practicing AppSec interview-style vulns. Built with **Python (Flask)**, **TypeScript**, and **Go**. Hands-on labs inspired by real AppSec interview questions.

## ⚠️ WARNING

This app is **intentionally vulnerable**. See [SECURITY.md](SECURITY.md). Do **not** use real credentials or expose to the internet.

---

## Quick Start — Setup Menu

Run the setup menu to choose how to run:

```bash
python setup.py
# Or:  setup.bat  (Windows)  |  ./setup.sh  (Linux/macOS; chmod +x setup.sh if needed)
```

**Default port: 5000.** Setup checks if the port is free before running. If port 5000 is in use, you’ll be prompted to enter a different port.

| Option | Mode | Description |
|--------|------|-------------|
| 1 | **Web (local)** | Flask in terminal, open browser manually |
| 2 | **GUI (local)** | Desktop launcher — start Flask, Go proxy, open browser |
| 3 | **Web (Docker)** | `docker-compose up` — full stack containerized |
| 4 | **GUI (Docker)** | Docker + auto-open browser |
| 5 | **Setup only** | Create venv, install dependencies |

---

## Run Options

| | Web (browser) | GUI (desktop launcher) |
|---|---|---|
| **Local (venv)** | `python setup.py` → 1, or `run.bat` / `run.sh` | `python setup.py` → 2, or `python launcher_gui.py` |
| **Containerized** | `python setup.py` → 3, or `docker-compose up` | `python setup.py` → 4 |

**Prerequisites:**
- **Local:** Python 3.11+, Node.js (optional), Go 1.21+ (optional, for SSRF)
- **Docker:** Docker and Docker Compose

---

## Manual Run (no menu)

**Local Web** (checks port, prompts if 5000 is busy):
```bash
python -m venv venv && venv\Scripts\activate   # Windows
pip install -r requirements.txt
python run_web.py   # or: run.bat / run.sh
```

**Local GUI:**
```bash
python launcher_gui.py   # (after venv + pip install; prompts if port busy)
```

**Docker:**
```bash
docker-compose up --build
```

Open **http://localhost:5000** (or the port you chose if 5000 was in use).

---

## Stack

| Component | Purpose |
|-----------|---------|
| **Python (Flask)** | Backend, routes, SQLite, Jinja2 |
| **TypeScript** | Client-side logic (SSRF form, API calls) |
| **Go** | SSRF-vulnerable proxy sidecar |

---

## Ports

| Port | Service |
|------|---------|
| **5000** (default) | Flask (main app). Setup checks availability; prompts for a new port if busy. |
| 9000 | Go SSRF proxy (optional) |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_PORT` | `5000` | Flask port. Setup checks if free; prompts for new port if in use. |
| `APP_SECRET_KEY` | `insecure-training-key` | Flask session signing |
| `APP_DB_PATH` | `data/app.db` | SQLite database path |
| `GO_PROXY_HOST` | `127.0.0.1` | Go proxy host (use `go-proxy` in Docker) |
| `GO_PROXY_PORT` | `9000` | Go proxy port |

Copy [.env.example](.env.example) to `.env` to override.

---

## Seeded Credentials (intentionally weak)

| Username | Password |
|----------|----------|
| admin | admin123 |
| alice | password |
| zer0_c00l | hacktheplanet |
| acidburn | crashoverride |

---

## Labs

33 modules with interactive mock sites. Each has an objective, walkthrough, hints, and solution. Examples:

- **XSS Guestbook** — Reflected/Stored XSS
- **SQLi Login** — String-built query injection
- **IDOR Profile** — Direct object reference, no auth check
- **SSRF Proxy** — Go sidecar fetches arbitrary URLs
- **SSTI, Open Redirect, JWT, API Security, XXE** — and more

---

## Scripts

| Command | Description |
|---------|-------------|
| `python setup.py` | Interactive setup & run menu (checks port before run) |
| `python launcher_gui.py` | GUI launcher (checks port, starts Flask, opens browser) |
| `python run_web.py` | Start Flask with port check (used by run.bat / run.sh) |
| `python app/app.py` | Start Flask directly (set APP_PORT if 5000 is busy) |
| `go run ./go/cmd/proxy` | Start Go SSRF proxy |
| `run.bat` / `run.sh` | Quick local Web run |
| `npm run build` | Compile TypeScript |
| `python exploit_test.py` | Run PoC vuln tests (local only) |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Publishing to GitHub

**Before pushing**, ensure:
- No `.env` file is committed (use `.env.example` as template)
- No `data/` or `*.db` files
- No `venv/` or `node_modules/`
- Run `git status` and review untracked files

```bash
# Create repo on GitHub (do not initialize with README)
git remote add origin https://github.com/HCKNKnuckle/WAIQ_Knuckle.git
git push -u origin main
```
