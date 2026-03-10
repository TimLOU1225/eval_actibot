#!/bin/bash
# Install requirements if missing and run the Actibot Eval UI.

echo "Checking dependencies..."
python3 -m pip install -r requirements.txt --quiet

echo "Starting Actibot Evaluation UI on http://127.0.0.1:8001/static/index.html ..."
python3 -m uvicorn app:app --host 127.0.0.1 --port 8001 --reload
