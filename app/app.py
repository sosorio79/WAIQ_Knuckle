from flask import Flask, render_template, render_template_string, request, redirect, url_for, flash, jsonify, Response
from pathlib import Path
import sqlite3
import urllib.request
import urllib.error
import urllib.parse
import os
import sys
import base64
import hashlib
import json
import secrets
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from config import get_settings
from modules.catalog import MODULES
from modules.lab_content import get_lab_content


def get_db_path():
    settings = get_settings()
    db_path = Path(settings["DB_PATH"])
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def seed_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            content TEXT
        );
        """
    )

    # Intentionally weak/seeds
    cur.execute(
        "INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO users (id, username, password) VALUES (2, 'alice', 'password')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO users (id, username, password) VALUES (3, 'zer0_c00l', 'hacktheplanet')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO users (id, username, password) VALUES (4, 'acidburn', 'crashoverride')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO messages (id, author, content) VALUES (1, 'alice', '<script>alert(1)</script>')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO messages (id, author, content) VALUES (2, 'zer0_c00l', 'Hack the Planet! <b>Crash Override</b> was here.')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO messages (id, author, content) VALUES (3, 'acidburn', 'Mess with the best, die like the rest.')"
    )

    conn.commit()
    conn.close()


def create_app():
    app = Flask(__name__)
    settings = get_settings()
    app.config["SECRET_KEY"] = settings["SECRET_KEY"]

    seed_db()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/modules")
    def list_modules():
        return render_template("modules.html", modules=MODULES)

    # API proxy to Go SSRF service (Python forwards to Go sidecar)
    @app.route("/api/proxy")
    def api_proxy():
        target = request.args.get("url", "")
        if not target:
            return jsonify({"error": "missing url parameter"}), 400
        go_host = os.environ.get("GO_PROXY_HOST", "127.0.0.1")
        go_port = os.environ.get("GO_PROXY_PORT", "9000")
        go_url = f"http://{go_host}:{go_port}/fetch?url={urllib.parse.quote(target)}"
        try:
            req = urllib.request.Request(go_url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return body, resp.status, {"Content-Type": "text/plain; charset=utf-8"}
        except Exception:
            pass
        # Python fallback when Go proxy not running
        try:
            req = urllib.request.Request(target, headers={"User-Agent": "WAIQ-SSRF-Demo/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return body, resp.status, {"Content-Type": "text/plain; charset=utf-8"}
        except urllib.error.HTTPError as e:
            return e.read().decode("utf-8", errors="replace"), e.code, {"Content-Type": "text/plain"}
        except Exception as e:
            return str(e), 502, {"Content-Type": "text/plain"}

    def _module_view(slug, template):
        """Shared handler for module lab and frame. Returns Flask response."""
        module = next((m for m in MODULES if m["slug"] == slug), None)
        if not module:
            return "Module not found", 404

        # Demo vulnerable behaviors (intentionally weak)
        if module["slug"] == "xss-guestbook":
            conn = get_db()
            cur = conn.cursor()
            if request.method == "POST":
                author = request.form.get("author", "anon")
                content = request.form.get("content", "")
                cur.execute(
                    "INSERT INTO messages (author, content) VALUES (?, ?)",
                    (author, content),
                )
                conn.commit()
                flash("Message posted (unsanitized).", "info")
                return redirect(request.url)

            cur.execute("SELECT author, content FROM messages ORDER BY id DESC")
            messages = cur.fetchall()
            conn.close()
            return render_template(
                template, module=module, lab=get_lab_content(module["slug"]), messages=messages
            )

        if module["slug"] == "sqli-login":
            error = None
            user = None
            if request.method == "POST":
                username = request.form.get("username", "")
                password = request.form.get("password", "")
                # Intentional SQL injection vulnerability: unparameterized query
                conn = get_db()
                cur = conn.cursor()
                query = f"SELECT id, username FROM users WHERE username = '{username}' AND password = '{password}'"
                try:
                    cur.execute(query)
                    user = cur.fetchone()
                except sqlite3.Error as exc:
                    error = f"DB error: {exc}"
                conn.close()
                if user:
                    flash(f"Welcome, {user['username']}! (query: {query})", "success")
                else:
                    error = error or "Invalid credentials (query was vulnerable)."
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), error=error)

        if module["slug"] == "idor-profile":
            target_id = request.args.get("id", "1")
            conn = get_db()
            cur = conn.cursor()
            # Intentional IDOR: no ownership check
            cur.execute("SELECT id, username, password FROM users WHERE id = ?", (target_id,))
            row = cur.fetchone()
            conn.close()
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), record=row, target_id=target_id)

        if module["slug"] == "ssrf-proxy":
            return render_template(template, module=module, lab=get_lab_content(module["slug"]))

        if module["slug"] == "open-redirect":
            # Vulnerable: redirect param used without validation (phishing scenario)
            redirect_to = (
                request.values.get("redirect")
                or request.values.get("next")
                or request.values.get("return")
                or "/"
            )
            if request.method == "POST":
                return redirect(redirect_to)
            return render_template(
                template,
                module=module,
                lab=get_lab_content(module["slug"]),
                redirect_preview=redirect_to,
            )

        if module["slug"] == "ssti":
            # Vulnerable: user input passed to render_template_string (intentionally weak)
            result = None
            if request.method == "POST":
                user_input = request.form.get("template", "")
                try:
                    result = render_template_string("Hello, " + user_input + "!")
                except Exception as e:
                    result = f"Error: {e}"
            return render_template(
                template,
                module=module,
                lab=get_lab_content(module["slug"]),
                ssti_result=result,
            )

        # ─── Mock demos for remaining modules ───
        if module["slug"] == "upload-no-validation":
            if request.method == "POST" and "file" in request.files:
                f = request.files["file"]
                if f.filename:
                    # Intentionally no validation
                    name = f.filename.replace("..", "")  # weak attempt, still vulnerable
                    path = Path(tempfile.gettempdir()) / "waiq_uploads"
                    path.mkdir(exist_ok=True)
                    dest = path / name
                    f.save(str(dest))
                    flash(f"File saved to {dest}. No validation performed.", "info")
            return render_template(template, module=module, lab=get_lab_content(module["slug"]))

        if module["slug"] == "session-management":
            sid = request.args.get("sessid") or request.cookies.get("demo_sessid") or secrets.token_hex(8)
            resp = render_template(template, module=module, lab=get_lab_content(module["slug"]), sessid=sid)
            r = app.make_response(resp)
            r.set_cookie("demo_sessid", sid)
            return r

        if module["slug"] == "jwt-auth":
            header = '{"alg":"none","typ":"JWT"}'
            payload = '{"user":"guest","admin":false}'
            custom = request.form.get("payload", payload) if request.method == "POST" else payload
            if request.method == "POST":
                try:
                    p = json.loads(custom)
                    if p.get("admin"):
                        return render_template(template, module=module, lab=get_lab_content(module["slug"]), jwt_result="Admin access granted!", jwt_payload=custom)
                except json.JSONDecodeError:
                    pass
            b64h = base64.urlsafe_b64encode(header.encode()).decode().rstrip("=")
            b64p = base64.urlsafe_b64encode(custom.encode()).decode().rstrip("=")
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), jwt_token=f"{b64h}.{b64p}.", jwt_payload=custom)

        if module["slug"] == "encoding-crypto":
            result = None
            if request.method == "POST":
                action = request.form.get("action", "encode")
                val = request.form.get("value", "")
                if action == "encode":
                    result = base64.b64encode(val.encode()).decode()
                elif action == "decode":
                    try:
                        result = base64.b64decode(val.encode()).decode()
                    except Exception as e:
                        result = str(e)
                elif action == "hash":
                    result = hashlib.md5(val.encode()).hexdigest()
                elif action == "verify":
                    h = request.form.get("hash", "")
                    result = "Match!" if hashlib.md5(val.encode()).hexdigest() == h else "No match"
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), enc_result=result)

        if module["slug"] == "hpp-waf":
            # Server uses LAST value (like some PHP)
            ids = request.values.getlist("id")
            chosen = ids[-1] if ids else None
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), hpp_chosen=chosen, hpp_all=ids)

        if module["slug"] == "command-injection":
            result = None
            if request.method == "POST":
                host = request.form.get("host", "127.0.0.1")
                # Intentional vuln: concatenates into command (whitelisted to ping only)
                cmd = f"ping -n 1 {host}" if os.name == "nt" else f"ping -c 1 {host}"
                result = f"Executing: {cmd}\n"
                try:
                    out = subprocess.run(cmd, shell=True, capture_output=True, timeout=5, text=True)
                    result += out.stdout or out.stderr or "(no output)"
                except Exception as e:
                    result += str(e)
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), cmd_result=result)

        if module["slug"] == "api-security":
            api_result = None
            if request.method == "POST":
                data = request.get_json(silent=True) or dict(request.form)
                user = data.get("username", "guest")
                is_admin = data.get("isAdmin", data.get("admin")) in (True, "true", "1", 1)
                if is_admin:
                    api_result = {"success": True, "user": user, "role": "admin", "message": "Mass assignment worked!"}
                else:
                    api_result = {"success": True, "user": user, "role": "user"}
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), api_result=api_result)

        if module["slug"] == "xxe":
            result = None
            if request.method == "POST":
                xml_data = request.form.get("xml", "")
                try:
                    # Vulnerable: parse XML with external entities
                    root = ET.fromstring(xml_data)
                    result = ET.tostring(root, encoding="unicode")
                except ET.ParseError as e:
                    result = f"Parse error: {e}"
                except Exception as e:
                    result = str(e)
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), xxe_result=result)

        if module["slug"] == "information-disclosure":
            # Use generic mock paths to avoid leaking local filesystem structure
            return render_template(
                template,
                module=module,
                lab=get_lab_content(module["slug"]),
                debug_info={"flask": "2.x", "python": sys.version.split()[0], "db_path": "/app/data/app.db"},
            )

        if module["slug"] == "sensitive-data-url":
            token = request.args.get("token", secrets.token_hex(8))
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), url_token=token)

        if module["slug"] == "captcha":
            ans = 5 + 3  # Simple math
            correct = False
            if request.method == "POST":
                guess = request.form.get("answer", "")
                correct = str(guess) == str(ans)
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), captcha_correct=correct)

        if module["slug"] == "formula-injection":
            if request.method == "POST":
                cell = request.form.get("cell", "hello")
                csv = f"Name,Value\nuser_input,{cell}\n"
                return Response(csv, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=export.csv"})
            return render_template(template, module=module, lab=get_lab_content(module["slug"]))

        if module["slug"] == "crlf-injection":
            loc = request.values.get("url", "/")
            header_val = request.values.get("header", "")
            crlf_preview = f"Location: {loc}\r\n" + (f"X-Injected: {header_val}\r\n" if header_val else "")
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), crlf_preview=crlf_preview, crlf_url=loc)

        if module["slug"] == "web-cache":
            fwd = request.headers.get("X-Forwarded-Host", "none")
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), cache_host=fwd)

        if module["slug"] == "business-logic":
            balance = 100
            if request.method == "POST":
                amt = int(request.form.get("amount", 0))
                balance = 100 - amt  # No check for negative or overdraft
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), balance=balance)

        if module["slug"] == "deserialization":
            result = None
            if request.method == "POST":
                # Show concept: JSON with __reduce__-like would be pickle; we mock with JSON
                data = request.form.get("json", "{}")
                try:
                    obj = json.loads(data)
                    if "__proto__" in str(obj) or "admin" in str(obj).lower():
                        result = "Dangerous deserialization pattern detected in production!"
                    else:
                        result = f"Parsed: {obj}"
                except Exception as e:
                    result = str(e)
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), deser_result=result)

        if module["slug"] == "request-smuggling":
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), req_te=request.headers.get("Transfer-Encoding", ""), req_cl=request.headers.get("Content-Length", ""))

        if module["slug"] == "same-origin-cors":
            resp = app.make_response(render_template(template, module=module, lab=get_lab_content(module["slug"])))
            resp.headers["Access-Control-Allow-Origin"] = "*"  # Misconfigured: allows any origin
            return resp

        if module["slug"] == "csp":
            resp = app.make_response(render_template(template, module=module, lab=get_lab_content(module["slug"])))
            resp.headers["Content-Security-Policy"] = "script-src 'unsafe-inline' 'self'"  # Weak: allows inline scripts
            return resp

        if module["slug"] == "websockets":
            return render_template(template, module=module, lab=get_lab_content(module["slug"]))

        if module["slug"] == "prototype-pollution":
            result = None
            if request.method == "POST":
                data = request.form.get("json", "{}")
                try:
                    obj = json.loads(data)
                    if "__proto__" in obj or "constructor" in str(obj):
                        result = "Prototype pollution pattern! Object would be merged unsafely."
                    else:
                        result = f"Merged: {obj}"
                except Exception as e:
                    result = str(e)
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), proto_result=result)

        if module["slug"] == "html-injection":
            # Reflect user input in HTML (same as XSS but for non-script injection)
            reflected = request.args.get("name", "")
            return render_template(template, module=module, lab=get_lab_content(module["slug"]), html_reflected=reflected)

        if module["slug"] == "network-tls":
            return render_template(template, module=module, lab=get_lab_content(module["slug"]))

        if module["slug"] == "scoping":
            return render_template(template, module=module, lab=get_lab_content(module["slug"]))

        if module["slug"] == "general-web-security":
            return render_template(template, module=module, lab=get_lab_content(module["slug"]))

        if module["slug"] == "behavioral":
            return render_template(template, module=module, lab=get_lab_content(module["slug"]))

        # Default: lab layout with description + walkthrough
        return render_template(template, module=module, lab=get_lab_content(module["slug"]))

    @app.route("/modules/<slug>", methods=["GET", "POST"])
    def module_detail(slug):
        return _module_view(slug, "module_lab.html")

    @app.route("/modules/<slug>/frame", methods=["GET", "POST"])
    def module_frame(slug):
        return _module_view(slug, "module_frame.html")

    return app


if __name__ == "__main__":
    app = create_app()
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    port = int(os.environ.get("APP_PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=debug)

