"""
Vercel Serverless Function Entrypoint
Exposes the Hill of Towie Wind Farm Dash Application
"""

import sys
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dashboard.app import app as dash_app, server

# Expose Flask WSGI instance to Vercel
app = server
application = server
