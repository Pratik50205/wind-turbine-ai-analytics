"""
Vercel Serverless Function Entrypoint
Exposes the Hill of Towie Wind Farm Dash Application
"""

import os
import sys
from pathlib import Path

# Ensure project root is at the head of sys.path
_cwd = Path(os.getcwd())
if str(_cwd) not in sys.path:
    sys.path.insert(0, str(_cwd))

_file_root = Path(__file__).resolve().parent.parent
if str(_file_root) not in sys.path:
    sys.path.insert(0, str(_file_root))

from src.dashboard.app import app as dash_app, server

# Expose Flask WSGI instance to Vercel runtime
app = server
application = server
