# Vercel Deployment Guide

This project is configured for single-command and automated Git deployments on [Vercel](https://vercel.com).

---

## 🚀 Quick Deployment (Vercel Git Integration)

1. **Push your code to GitHub**:
   ```bash
   git push origin main
   ```
2. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**.
3. Click **"Add New..."** $\rightarrow$ **"Project"**.
4. Select your GitHub repository (`wind-turbine-ai-analytics`).
5. Leave all build settings at their defaults:
   - **Framework Preset**: `Other`
   - **Root Directory**: `./` (default)
   - **Build Command**: empty
   - **Output Directory**: empty
6. Click **Deploy**.

Vercel will install dependencies from `requirements.txt`, compile `api/index.py`, and launch the live Dash application.

---

## 🛠️ Architecture & Configuration Files

| File | Purpose |
| :--- | :--- |
| [`api/index.py`](api/index.py) | Serverless WSGI entrypoint. Discovers and exposes the underlying Flask server (`app.server`). |
| [`vercel.json`](vercel.json) | Wildcard route rewrites (`/(.*)` $\rightarrow$ `/api/index`) so the Dash frontend and callbacks work on any route. |
| [`.python-version`](.python-version) | Locks Python runtime to `3.12` for pre-compiled Linux wheels and fast cold-starts. |
| [`requirements.txt`](requirements.txt) | Streamlined runtime packages (`dash`, `plotly`, `pandas`, `numpy`) kept strictly under Vercel's 250MB lambda limit. |
| [`requirements-full.txt`](requirements-full.txt) | Full offline pipeline/training dependencies (`scikit-learn`, `scipy`, etc.). |
| [`.vercelignore`](.vercelignore) | Prevents heavy local telemetry datasets (`data/`) and test caches from uploading. |

---

## 💻 Local Testing

You can run the dashboard locally at any time using:

```bash
# Option 1: Standard entrypoint
python dashboard/app.py

# Option 2: Serverless entrypoint
python api/index.py
```
Open [http://127.0.0.1:8050](http://127.0.0.1:8050) in your browser.
