#!/usr/bin/env python3
"""Run Flask after checking port. Prompts for new port if default is in use."""
import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from port_utils import prompt_for_port, DEFAULT_PORT

def main():
    port = prompt_for_port(DEFAULT_PORT)
    python = sys.executable
    if (PROJECT_ROOT / "venv" / "Scripts" / "python.exe").exists():
        python = str(PROJECT_ROOT / "venv" / "Scripts" / "python.exe")
    elif (PROJECT_ROOT / "venv" / "bin" / "python").exists():
        python = str(PROJECT_ROOT / "venv" / "bin" / "python")
    env = {**os.environ, "APP_PORT": str(port)}
    print(f"\n[*] Starting at http://localhost:{port} (default: {DEFAULT_PORT})")
    print("[*] For SSRF: run 'go run ./go/cmd/proxy' in another terminal\n")
    subprocess.run([python, "app/app.py"], cwd=PROJECT_ROOT, env=env)

if __name__ == "__main__":
    main()
