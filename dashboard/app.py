"""
Hill of Towie Wind Farm - Dashboard Entrypoint
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dashboard.app import app as dash_app, server

# For Vercel Serverless WSGI execution:
# Vercel requires the underlying Flask WSGI instance (with `wsgi_app`).
# Exposing `app` and `application` as `server` ensures Vercel discovers a valid WSGI callable.
app = server
application = server

if __name__ == "__main__":
    print("Starting Hill of Towie Wind Farm Dash Application on http://127.0.0.1:8050 ...")
    dash_app.run(host="127.0.0.1", port=8050, debug=False)

