#!/usr/bin/env python3
"""
WAIQ Knuckle - GUI Launcher
Desktop launcher: start Flask, Go proxy, open in browser.
"""

import os
import sys
import threading
import webbrowser
import subprocess
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog
except ImportError:
    print("Tkinter not available. Run: python setup.py and choose option 1 (Web local).")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_PORT = 5000
flask_proc = None
go_proc = None
_app_port = None


def get_port():
    """Get port to use: from env, or check default and prompt if busy."""
    global _app_port
    if _app_port is not None:
        return _app_port
    from port_utils import is_port_available, DEFAULT_PORT
    port = int(os.environ.get("APP_PORT", str(DEFAULT_PORT)))
    if is_port_available(port):
        _app_port = port
        return port
    # Port busy - prompt via dialog
    root = tk.Tk()
    root.withdraw()
    new_port = simpledialog.askinteger(
        "Port in use",
        f"Port {port} is already in use.\nEnter a different port (1-65535):",
        initialvalue=port + 1,
        minvalue=1,
        maxvalue=65535,
    )
    root.destroy()
    if new_port is None:
        return None
    if is_port_available(new_port):
        _app_port = new_port
        return new_port
    messagebox.showerror("Port busy", f"Port {new_port} is also in use.")
    return None


def get_url():
    return f"http://localhost:{get_port() or DEFAULT_PORT}"


def run_flask():
    global flask_proc
    if flask_proc and flask_proc.poll() is None:
        return True
    port = get_port()
    if port is None:
        return False
    venv_python = PROJECT_ROOT / "venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        venv_python = PROJECT_ROOT / "venv" / "bin" / "python"
    if not venv_python.exists():
        messagebox.showerror("Error", "Run setup first (python setup.py, option 5)")
        return False
    flask_proc = subprocess.Popen(
        [str(venv_python), "app/app.py"],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env={**os.environ, "FLASK_DEBUG": "0", "APP_PORT": str(port)},
    )
    threading.Thread(target=lambda: _read_output(flask_proc, "flask"), daemon=True).start()
    return True


def run_go_proxy():
    global go_proc
    if go_proc and go_proc.poll() is None:
        return
    go_exe = Path("go")
    if not (PROJECT_ROOT / "go" / "cmd" / "proxy" / "main.go").exists():
        messagebox.showwarning("Go proxy", "Go source not found. SSRF module will not work.")
        return
    try:
        go_proc = subprocess.Popen(
            ["go", "run", "./cmd/proxy"],
            cwd=str(PROJECT_ROOT / "go"),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        threading.Thread(target=lambda: _read_output(go_proc, "go"), daemon=True).start()
    except FileNotFoundError:
        messagebox.showwarning("Go proxy", "Go not installed. SSRF module will return 502.")


def _read_output(proc, name):
    if proc and proc.stdout:
        for line in proc.stdout:
            pass  # Consume to avoid blocking


def open_browser():
    webbrowser.open(get_url())


def create_gui():
    root = tk.Tk()
    root.title("WAIQ Knuckle — Launcher")
    root.geometry("420x320")
    root.configure(bg="#0a0a0a")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#0a0a0a")
    style.configure("TLabel", background="#0a0a0a", foreground="#00ff00", font=("Consolas", 10))
    style.configure("TButton", font=("Consolas", 10), padding=8)
    style.map("TButton", background=[("active", "#003300")])

    main = ttk.Frame(root, padding=20)
    main.pack(fill=tk.BOTH, expand=True)

    ttk.Label(main, text="WAIQ Knuckle", font=("Consolas", 16, "bold")).pack(pady=(0, 5))
    ttk.Label(main, text="Hack the Planet.", foreground="#00ffff").pack(pady=(0, 2))
    ttk.Label(main, text=f"Default port: {DEFAULT_PORT}", font=("Consolas", 8), foreground="#666").pack(pady=(0, 15))

    ttk.Label(main, text="Local (venv):").pack(anchor="w")
    btn_frame = ttk.Frame(main)
    btn_frame.pack(fill="x", pady=5)
    ttk.Button(btn_frame, text="Start Web", command=lambda: (run_flask() and open_browser())).pack(side="left", padx=(0, 8))
    ttk.Button(btn_frame, text="Start Go Proxy", command=run_go_proxy).pack(side="left", padx=(0, 8))
    ttk.Button(btn_frame, text="Open Browser", command=open_browser).pack(side="left")

    ttk.Label(main, text="").pack(pady=8)
    ttk.Label(main, text="Or use: python setup.py (options 3–4 for Docker)").pack(anchor="w", pady=(10, 0))

    ttk.Label(main, text="", font=("", 4)).pack()
    ttk.Button(main, text="Exit", command=root.quit).pack(pady=10)

    def on_closing():
        global flask_proc, go_proc
        if flask_proc and flask_proc.poll() is None:
            flask_proc.terminate()
        if go_proc and go_proc.poll() is None:
            go_proc.terminate()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    os.chdir(PROJECT_ROOT)
    create_gui()
