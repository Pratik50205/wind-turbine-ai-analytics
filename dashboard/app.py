"""
Hill of Towie Wind Farm - Dashboard Entrypoint
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dashboard.app import app, server

if __name__ == "__main__":
    print("Starting Hill of Towie Wind Farm Dash Application on http://127.0.0.1:8050 ...")
    app.run(host="127.0.0.1", port=8050, debug=False)
