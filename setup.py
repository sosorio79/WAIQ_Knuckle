#!/usr/bin/env python3
"""
WAIQ Knuckle - Setup & Run Menu
Choose: Web or GUI | Local (venv) or Containerized (Docker)
Default port: 5000. Checks port before run; prompts for new port if in use.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

from port_utils import prompt_for_port, DEFAULT_PORT

PROJECT_ROOT = Path(__file__).resolve().parent


def ensure_venv():
    """Create venv and install deps if needed."""
    venv = PROJECT_ROOT / "venv"
    if not (venv / "Scripts" / "python.exe").exists() and not (venv / "bin" / "python").exists():
        print("[*] Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True, cwd=PROJECT_ROOT)
    pip = venv / "Scripts" / "pip.exe" if (venv / "Scripts").exists() else venv / "bin" / "pip"
    python = venv / "Scripts" / "python.exe" if (venv / "Scripts").exists() else venv / "bin" / "python"
    if not (PROJECT_ROOT / "app" / "app.py").exists():
        print("[!] Run setup from project root.")
        sys.exit(1)
    print("[*] Installing dependencies...")
    subprocess.run([str(pip), "install", "-q", "-r", "requirements.txt"], check=True, cwd=PROJECT_ROOT)
    return str(python)


def run_web_local():
    """Start Flask in foreground (local venv)."""
    port = prompt_for_port(DEFAULT_PORT)
    python = ensure_venv()
    url = f"http://localhost:{port}"
    print(f"\n[*] Starting Flask at {url} (default port: {DEFAULT_PORT})")
    print("[*] For SSRF module: run 'go run ./go/cmd/proxy' in another terminal\n")
    env = {**os.environ, "APP_PORT": str(port)}
    subprocess.run([python, "app/app.py"], cwd=PROJECT_ROOT, env=env)


def run_gui_local():
    """Launch GUI launcher (tkinter) which starts Flask + opens browser."""
    port = prompt_for_port(DEFAULT_PORT)
    python = ensure_venv()
    env = {**os.environ, "APP_PORT": str(port)}
    subprocess.run([python, "launcher_gui.py"], cwd=PROJECT_ROOT, env=env)


def run_web_docker():
    """Start via Docker Compose."""
    port = prompt_for_port(DEFAULT_PORT)
    url = f"http://localhost:{port}"
    print(f"\n[*] Starting Docker Compose (Flask + Go proxy) on port {port}...")
    print(f"[*] Open {url} when ready (default port: {DEFAULT_PORT})\n")
    env = {**os.environ, "APP_PORT": str(port)}
    subprocess.run(["docker-compose", "up", "--build"], cwd=PROJECT_ROOT, env=env)


def run_gui_docker():
    """Start Docker, open browser, then attach to logs."""
    port = prompt_for_port(DEFAULT_PORT)
    url = f"http://localhost:{port}"
    print(f"\n[*] Starting Docker Compose on port {port}...")
    env = {**os.environ, "APP_PORT": str(port)}
    proc = subprocess.Popen(
        ["docker-compose", "up", "--build"],
        cwd=PROJECT_ROOT,
        env=env,
    )
    import time
    time.sleep(5)  # Give containers time to start
    print(f"[*] Opening browser at {url} (default port: {DEFAULT_PORT})")
    webbrowser.open(url)
    proc.wait()


def main():
    os.chdir(PROJECT_ROOT)
    print("\n" + "=" * 50)
    print("  WAIQ Knuckle — Setup & Run")
    print("=" * 50)
    print(f"\n  Default port: {DEFAULT_PORT} (checks availability before run)")
    print("\n  1. Web  (local venv)  — Flask in terminal, open browser manually")
    print("  2. GUI  (local venv)  — Desktop launcher, auto-open browser")
    print("  3. Web  (Docker)      — Containerized, full stack")
    print("  4. GUI  (Docker)      — Containerized + auto-open browser")
    print("  5. Setup only         — Create venv, install deps")
    print("  6. Exit")
    print()
    choice = input("Choose (1–6): ").strip()
    print()

    if choice == "1":
        run_web_local()
    elif choice == "2":
        run_gui_local()
    elif choice == "3":
        run_web_docker()
    elif choice == "4":
        run_gui_docker()
    elif choice == "5":
        ensure_venv()
        print("[+] Setup complete.")
    elif choice == "6":
        print("Hack the Planet.")
    else:
        print("[!] Invalid choice. Run again.")


if __name__ == "__main__":
    main()
