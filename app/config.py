from pathlib import Path
import os


def get_settings():
    base_dir = Path(__file__).resolve().parent
    return {
        "SECRET_KEY": os.environ.get("APP_SECRET_KEY", "insecure-training-key"),
        "DB_PATH": os.environ.get(
            "APP_DB_PATH", str(base_dir.parent / "data" / "app.db")
        ),
    }

