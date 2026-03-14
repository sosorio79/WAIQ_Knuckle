#!/bin/bash
# WAIQ Knuckle - Local launcher (Linux/macOS). Default port: 5000
cd "$(dirname "$0")"

if [ ! -d venv ]; then
    echo "Creating venv..."
    python3 -m venv venv
fi
source venv/bin/activate

pip install -q -r requirements.txt
python run_web.py
