# Hill of Towie Wind Farm — Project Startup & Execution Guide

This document provides step-by-step instructions to set up, execute, verify, and interact with the **AI-Based Wind Turbine Performance Analysis and Power Prediction System**.

---

## 1. System Requirements

The pipeline is engineered to run on a **standard student PC footprint** without requiring cloud compute or GPUs.

- **Operating System:** Windows 10/11, Linux (Ubuntu 20.04+), or macOS.
- **Python Version:** Python 3.10, 3.11, 3.12, 3.13, or 3.14.
- **Hardware Footprint:**
  - **CPU:** 4+ physical cores recommended (OpenMP multi-threaded in C).
  - **RAM:** 8 GB minimum (16 GB recommended for raw CSV streaming).
  - **Disk Space:** ~12 GB free (9.3 GB raw CSVs + 200 MB Parquet cache + outputs).
  - **GPU:** **None required** (HistGradientBoostingRegressor trains in <10 seconds on CPU).

---

## 2. Environment Setup

### Step 1: Clone or Navigate to the Repository
```bash
cd c:\Pratik\MDM\project2
```

### Step 2: Install Core Dependencies
Ensure all project dependencies are installed in your active Python environment:
```bash
pip install -r requirements.txt
```

Core libraries utilized:
- `pandas` & `pyarrow` (High-speed columnar Parquet caching)
- `scikit-learn` & `joblib` (Model training, CV evaluation, serialization)
- `plotly` & `dash` (Interactive dark-themed desktop dashboard)
- `matplotlib` & `seaborn` (Static reporting & multi-page PDF generation)
- `pytest` (Automated regression testing)
- `pyyaml` (Unified configuration loader)

---

## 3. Data Directory Verification

The project expects raw SCADA CSV files under `data/raw/`. The repository maintains clean separation between:
1. `data/raw/`: Read-only source CSV files (215 files, 9.30 GB).
2. `data/processed/`: Deduplicated, validated, compressed Snappy Parquet files.
3. `data/model_ready/`: Physics-engineered train/test matrices with target leakage quarantine.

Verify that the raw directories exist:
```text
data/raw/
├── 2025/ (Monthly SCADA CSVs from Jan to Dec 2025)
├── 2026/ (Monthly SCADA CSVs from Jan to Apr 2026)
├── Hill_of_Towie_ShutdownDuration/
├── Hill_of_Towie_turbine_metadata.csv
└── documentation/
```

*(Note: Once processed into `data/processed/*.parquet`, the pipeline runs 100% offline without re-reading the 9.3 GB CSV files.)*

---

## 4. Launching the Interactive Dashboard

The primary presentation and decision-support interface is a native **Dash + Plotly Desktop Application**.

### Start the Dashboard
```bash
python src/dashboard/app.py
```
*Or alternatively:*
```bash
python dashboard/app.py
```

### Accessing the Interface
Open your web browser and navigate to:
```text
http://127.0.0.1:8050
```

### Dashboard Features:
- **Tab 1 — Executive Overview:** High-level fleet KPIs, annual generation yield (96.96 GWh), capacity factor rankings, and aggregate power tracking.
- **Tab 2 — Turbine Performance:** Individual turbine selector (`T01`–`T21`), binned empirical power curve vs. IEC-61400-12 standard, and 10-minute dynamic time-series.
- **Tab 3 — Power Prediction:** Holdout 2026 model metrics ($R^2 = 0.9962$, NRMSE $= 1.87\%$), actual vs. predicted parity scatter with $1:1$ diagonal, and top feature importance rankings.
- **Tab 4 — Abnormal Behavior:** Sustained underperformance event log (23 events), deficit depth vs. wind speed scatter, and anomaly event records.
- **Tab 5 — Environmental Analysis:** Ambient/nacelle temperature power envelope and Hill of Towie directional wind rose (prevailing South-Southwesterly winds).
- **Tab 6 — Maintenance & Events:** Top SCADA alarm frequencies (512k events), shutdown categories, and root-cause correlation (65.2% coincident, 34.8% silent drift flagged as *"Requires Investigation"*).
- **Tab 7 — Real-Time Replay:** Step streaming engine with **Start**, **Pause**, **Reset**, speed multipliers (1x, 5x, 10x), real-time AI inference, anomaly alert indicators, and 1.48 ms per-step processing latency.

---

## 5. Running the Automated Test Suite

A comprehensive test suite with 41 unit tests validates every stage from raw schema ingestion to dashboard callbacks.

Run all tests:
```bash
python -m pytest -v
```

Expected output:
```text
======================== 41 passed in 2.94s ========================
```

Test coverage includes:
- `test_data_inventory.py`: Schema discovery, turbine IDs, candidate targets and features.
- `test_preprocessing.py`: Data cleaning, deduplication, physical range clamping, DQI score.
- `test_eda.py`: Descriptive statistics, power curve monotonicity, correlation matrix.
- `test_performance.py`: Annual energy yields, capacity factor, availability, Betz limit ($C_p \le 0.44$).
- `test_features.py`: Physics feature derivations, TSR, air density proxy, **target leakage audit**.
- `test_model.py`: Model candidates, serialization, holdout test metrics ($R^2 > 0.99$, NRMSE $< 5\%$).
- `test_anomaly.py`: Deficit threshold (-250 kW), operational masking, 30-min persistence rule.
- `test_replay.py`: Streaming latency (< 50 ms), throughput (> 20 steps/s), sample structure.
- `test_dashboard.py`: Data service KPIs, all 7 tab layouts, screenshot completeness.
- `test_pipeline.py`: Stage completion statuses, reproducibility manifests, documentation cards.

---

## 6. Running Pipeline Stages

The pipeline can be executed end-to-end or stage-by-stage via [src/pipeline.py](file:///c:/Pratik/MDM/project2/src/pipeline.py).

### Run Entire Pipeline (End-to-End)
```bash
python -m src.pipeline --stage all
```

### Run Individual Stages
```bash
# Phase 1: Data Inventory & Schema Discovery
python -m src.pipeline --stage inventory

# Phase 2: Data Preprocessing & Parquet Caching
python -m src.pipeline --stage preprocessing

# Phase 3: Exploratory Data Analysis & Power Curves
python -m src.pipeline --stage eda

# Phase 4: Turbine Performance Analysis & Farm Yield
python -m src.pipeline --stage performance

# Phase 5: Feature Engineering & Target Leakage Audit
python -m src.pipeline --stage features

# Phase 6 & 7: Power Prediction Model Training & Holdout
python -m src.pipeline --stage train

# Phase 8: Abnormal Behavior Detection
python -m src.pipeline --stage anomaly

# Phase 9: Alarm & Shutdown Event Correlation
python -m src.pipeline --stage events

# Phase 10: SCADA Replay Engine Simulation
python -m src.pipeline --stage replay

# Phase 11: Dashboard Artifacts Export & Previews
python -m src.pipeline --stage dashboard

# Phase 12: Final Integration & Manifest Generation
python -m src.pipeline --stage integration
```

---

## 7. Generating Final Reports & Documentation

To recompile the final project report, executive summary, metrics tables, and multi-page PDF:
```bash
python src/final_validation_report.py
```

Generated report artifacts in `outputs/13_final_report/`:
- [FINAL_PROJECT_REPORT.md](file:///c:/Pratik/MDM/project2/outputs/13_final_report/FINAL_PROJECT_REPORT.md)
- [FINAL_PROJECT_REPORT.pdf](file:///c:/Pratik/MDM/project2/outputs/13_final_report/FINAL_PROJECT_REPORT.pdf)
- [executive_summary.md](file:///c:/Pratik/MDM/project2/outputs/13_final_report/executive_summary.md)
- [final_metrics.csv](file:///c:/Pratik/MDM/project2/outputs/13_final_report/final_metrics.csv)
- [model_card.md](file:///c:/Pratik/MDM/project2/outputs/13_final_report/model_card.md)
- [data_card.md](file:///c:/Pratik/MDM/project2/outputs/13_final_report/data_card.md)
- [limitations.md](file:///c:/Pratik/MDM/project2/outputs/13_final_report/limitations.md)
- [reproducibility_check.md](file:///c:/Pratik/MDM/project2/outputs/13_final_report/reproducibility_check.md)

---

## 8. Troubleshooting & FAQs

### Q1: The browser shows "Site can't be reached" on `http://127.0.0.1:8050`
- **Cause:** The Dash server is not running.
- **Solution:** In your terminal, run `python src/dashboard/app.py` and verify the terminal displays: `Dash is running on http://127.0.0.1:8050/`. Keep the terminal open while browsing.

### Q2: Port 8050 is already in use
- **Cause:** A previous instance of Dash is still running in the background.
- **Solution:** Change the port in `src/dashboard/app.py` to `port=8055` or terminate existing Python processes:
  ```powershell
  Get-Process python | Stop-Process
  ```

### Q3: Why does `pytest` complain when running `pytest` directly on Windows?
- **Cause:** Python environment path differences on Windows PowerShell.
- **Solution:** Always invoke pytest as a module: `python -m pytest -v`.

### Q4: Was any data synthetic or fabricated?
- **Answer:** **No.** Zero synthetic numbers, dummy values, or fabricated model scores were used. Every metric, power curve, capacity factor (23.88%), anomaly count (23), and model score ($R^2 = 0.9962$) was computed directly from the Hill of Towie open SCADA telemetry.
