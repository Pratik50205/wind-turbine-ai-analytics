"""
Hill of Towie Wind Farm - AI-Based Decision Support Dashboard
Native Dash + Plotly Desktop Application
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import dash
from src.dashboard.layout import build_main_layout
from src.dashboard.callbacks import register_callbacks

# Create Dash application instance
app = dash.Dash(
    __name__,
    title="Hill of Towie - Wind Farm AI Dashboard",
    update_title="Computing Analytics...",
    suppress_callback_exceptions=True
)

# Assign main layout
app.layout = build_main_layout()

# Register interactive callbacks
register_callbacks(app)

# Expose WSGI server
server = app.server

if __name__ == "__main__":
    print("Starting Hill of Towie Wind Farm Dash Application on http://127.0.0.1:8050 ...")
    app.run(host="127.0.0.1", port=8050, debug=False)
