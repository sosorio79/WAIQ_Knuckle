from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path
import sqlite3

from config import get_settings
from modules.catalog import MODULES


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

    @app.route("/modules/<slug>", methods=["GET", "POST"])
    def module_detail(slug):
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
                "module_detail.html", module=module, messages=messages
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
            return render_template("module_detail.html", module=module, error=error)

        if module["slug"] == "idor-profile":
            target_id = request.args.get("id", "1")
            conn = get_db()
            cur = conn.cursor()
            # Intentional IDOR: no ownership check
            cur.execute("SELECT id, username, password FROM users WHERE id = ?", (target_id,))
            row = cur.fetchone()
            conn.close()
            return render_template("module_detail.html", module=module, record=row, target_id=target_id)

        # Default: just show info
        return render_template("module_detail.html", module=module)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

