"""
Dash Plotly Desktop Application Launcher
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dashboard.app import app

if __name__ == "__main__":
    print("Launching Hill of Towie Wind Farm Dash Application from dashboard/dash_plotly...")
    app.run(host="127.0.0.1", port=8050, debug=False)
