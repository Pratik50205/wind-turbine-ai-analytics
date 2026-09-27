# Dash Plotly Desktop Application

This directory provides the launcher and configuration for the **Dash + Plotly Desktop Application**.

## Quick Start
```bash
python dashboard/dash_plotly/run_dashboard.py
```
Open: `http://127.0.0.1:8050`

The core modular UI implementation is maintained under:
- `src/dashboard/app.py`: Application entrypoint & Flask WSGI server
- `src/dashboard/layout.py`: 7-module tab definitions
- `src/dashboard/callbacks.py`: Interactive callback registrations
- `src/dashboard/components.py`: Reusable dark-mode UI cards and banners
- `src/dashboard/styles.py`: Glassmorphism dark design tokens
- `src/dashboard/data_service.py`: Cached, fast in-memory analytical query service
