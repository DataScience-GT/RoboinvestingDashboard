#!/usr/bin/env python3
"""
Simple script to start the backend server.
This will use the same Python that has your packages installed.
"""

import subprocess
import sys
import os

# Change to the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Try to find the Python that has streamlit (and thus all packages)
python_candidates = [
    '/Library/Frameworks/Python.framework/Versions/3.12/bin/python3',
    '/Library/Frameworks/Python.framework/Versions/3.12/bin/python',
    sys.executable,  # Current Python
    'python3',
    'python'
]

python_cmd = None
for candidate in python_candidates:
    try:
        result = subprocess.run(
            [candidate, '-c', 'import flask, flask_cors, openai; print("OK")'],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            python_cmd = candidate
            print(f"✅ Using Python: {candidate}")
            break
    except:
        continue

if not python_cmd:
    print("❌ Could not find Python with required packages (flask, flask_cors, openai)")
    print("Please install them: pip install flask flask-cors openai")
    sys.exit(1)

# Start the backend server
print("\n🚀 Starting backend server on http://localhost:8080")
print("Press Ctrl+C to stop\n")
try:
    subprocess.run([python_cmd, 'backend_server.py'])
except KeyboardInterrupt:
    print("\n\n👋 Server stopped")

