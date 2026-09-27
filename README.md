# AI-Based Wind Turbine Performance Analysis and Power Prediction

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Dash%20%2B%20Plotly-00f2fe.svg)](http://127.0.0.1:8050)
[![Test Suite](https://img.shields.io/badge/Tests-41%2F41%20Passing-success.svg)](file:///c:/Pratik/MDM/project2/tests)
[![Data Quality](https://img.shields.io/badge/DQI-99.8%2F100-brightgreen.svg)](file:///c:/Pratik/MDM/project2/outputs/02_data_preprocessing)
[![Zero Fabrication](https://img.shields.io/badge/Data%20Audit-Zero%20Fabrication-blue.svg)](file:///c:/Pratik/MDM/project2/outputs/12_final_integration)

An end-to-end, physics-informed data analytics, machine learning, and decision-support system developed for the **Hill of Towie Wind Farm** (Moray, Scotland; 21 Siemens SWT-2.3-VS-82 turbines, 48.3 MW nameplate capacity).

This project integrates high-volume 10-minute SCADA telemetry, physical power curve benchmarking (IEC-61400-12), machine learning power regression, operational anomaly detection, SCADA alarm correlation, a low-latency real-time replay engine, and an interactive **Dash + Plotly Desktop Dashboard**.

---

## ⚡ Quick Navigation

- 🚀 [Startup & Execution Guide](file:///c:/Pratik/MDM/project2/STARTUP_GUIDE.md) — How to set up and run the project
- 📖 [Complete Project Walkthrough](file:///c:/Pratik/MDM/project2/WALKTHROUGH.md) — Step-by-step technical phase guide
- 📑 [Full Technical Report](file:///c:/Pratik/MDM/project2/PROJECT_REPORT.md) — Detailed scientific findings & methodology
- 🎛️ [Dashboard User Guide](file:///c:/Pratik/MDM/project2/docs/DASHBOARD_GUIDE.md) — Guide to the 7 dashboard modules
- 🃏 [Model Card](file:///c:/Pratik/MDM/project2/docs/MODEL_CARD.md) | [Data Card](file:///c:/Pratik/MDM/project2/docs/DATA_CARD.md) | [Limitations](file:///c:/Pratik/MDM/project2/docs/LIMITATIONS.md)

---

## 📊 Key Empirical Project Results

All values reflect empirical calculations from the 16-month Hill of Towie SCADA dataset (January 2025 – April 2026). Zero synthetic or placeholder numbers are used.

| Metric | Empirical Value | Unit / Standard | Status |
| :--- | :--- | :--- | :--- |
| **Fleet Scale** | **21 Turbines** (`T01`–`T21`) | Siemens SWT-2.3-VS-82 (48.3 MW) | Verified |
| **Baseline Generation (2025)** | **96.96 GWh** | Net Grid-Injected Energy | Measured |
| **Fleet Capacity Factor** | **23.88%** | Empirical Range: 16.7% to 32.2% | Verified |
| **Fleet Technical Availability** | **98.42%** | Active Grid Operating Hours | Verified |
| **Aerodynamic Efficiency ($C_p$)**| **0.44** (Peak) | Strictly $\le 0.593$ (Betz Limit) | Validated |
| **Prediction Model** | **HistGradientBoosting** | Physics-Informed Features | Best Model |
| **Holdout Test $R^2$ (2026)** | **0.9962** | 361,504 completely unseen points | Verified |
| **Holdout Test RMSE** | **43.06 kW** | Holdout Power Error | Verified |
| **Normalized RMSE (NRMSE)** | **1.87%** | Relative to 2300 kW Capacity ($< 5\%$) | Exceptional |
| **Holdout Test MAE** | **19.34 kW** | Absolute Residual Expectation | Verified |
| **Target Leakage Quarantine** | **PASSED** | Current $I$ and operational flags isolated | Audited |
| **Sustained Anomaly Events** | **23 Events** | $\ge 30$ min, deficit $\le -250$ kW | Verified |
| **SCADA Alarm Ingestion** | **512,117 Events** | 16-month fleet event log | Cataloged |
| **Root-Cause Anomaly Split** | **65.2% / 34.8%** | 34.8% Silent Aerodynamic Drift | Classified |
| **Replay Streaming Latency** | **1.48 ms / step** | **675 steps/sec** throughput | Benchmarked |
| **Automated Test Suite** | **41 / 41 Passed** | 100% Passing in 2.94s | Verified |

---

## 🖥️ Interactive Decision Support Dashboard

The project features a **7-module Dash + Plotly Desktop Application** designed with a modern dark theme and responsive glassmorphism aesthetic:

1. **Executive Overview:** High-level fleet KPIs (96.96 GWh yield, 23.88% CF, 98.42% availability), fleet power curve tracking, and turbine utilization rankings.
2. **Turbine Performance:** Individual turbine diagnostics (`T01`–`T21`), binned empirical power curve vs. IEC-61400-12 standard, and dynamic wind-power time series.
3. **Power Prediction:** Holdout 2026 test evaluation ($R^2 = 0.9962$, NRMSE $= 1.87\%$), actual vs. predicted parity scatter with $1:1$ ideal diagonal, and physics-informed feature importance breakdown.
4. **Abnormal Behavior:** Sustained underperformance event log (23 events), deficit depth vs. wind speed scatter, and anomaly event records.
5. **Environmental Analysis:** Ambient/nacelle temperature power envelope and Hill of Towie directional wind rose (prevailing South-Southwesterly winds).
6. **Maintenance & Events:** Top SCADA alarm frequencies (512k events), shutdown categories, and root-cause correlation (65.2% coincident, 34.8% silent drift flagged as *"Requires Investigation"*).
7. **Real-Time Replay:** Step streaming engine with **Start**, **Pause**, **Reset**, speed multipliers (1x, 5x, 10x), real-time AI inference, anomaly alert indicators, and 1.48 ms per-step processing latency.

### Visual Preview
![Dashboard Preview](file:///c:/Pratik/MDM/project2/outputs/11_dashboard/preview/final_dashboard_preview.png)

Browser-captured validation screenshots for all 7 tabs are stored in [outputs/11_dashboard/screenshots/](file:///c:/Pratik/MDM/project2/outputs/11_dashboard/screenshots/).

---

## 🏗️ Repository Architecture

```text
c:/Pratik/MDM/project2/
├── config/                     # Configuration files (project.yaml)
├── dashboard/                  # Dashboard root entrypoints and assets
├── data/
│   ├── raw/                    # 215 monthly SCADA CSV files (9.30 GB)
│   ├── processed/              # Cleaned Snappy Parquet datasets
│   └── model_ready/            # Train/Test feature matrices (2025/2026)
├── docs/                       # Technical cards & guides (MODEL_CARD, DATA_CARD, etc.)
├── models/
│   ├── candidates/             # Serialized baseline, ridge, RF candidate models
│   └── final/                  # Serialized best power model (HistGBM)
├── outputs/                    # Complete evidence artifacts (Phases 00 to 13)
│   ├── 00_project_validation/  # Environment reports & manifests
│   ├── 01_data_inventory/      # Schema discovery & dictionary
│   ├── 02_data_preprocessing/   # Cleaning engine & DQI scorecard
│   ├── 03_eda/                 # Exploratory plots & correlation matrices
│   ├── 04_performance_analysis/# Power curves, Cp & turbine rankings
│   ├── 05_feature_engineering/ # Feature importance & leakage audits
│   ├── 06_model_development/   # Model comparison & validation metrics
│   ├── 07_power_prediction/    # 2026 holdout evaluation & error analysis
│   ├── 08_anomaly_detection/   # Sustained underperformance events
│   ├── 09_event_analysis/      # 512k alarm logs & root-cause correlation
│   ├── 10_replay_processing/   # Streaming replay engine benchmarks
│   ├── 11_dashboard/           # Dashboard KPIs, dictionaries, screenshots
│   ├── 12_final_integration/   # Reproducibility manifests & system flow
│   └── 13_final_report/        # FINAL_PROJECT_REPORT.md & .pdf
├── src/                        # Complete pipeline source code
│   ├── pipeline.py             # Unified stage orchestrator
│   ├── preprocessing.py        # Cleaning & physical boundary engine
│   ├── eda.py                  # Exploratory analytics & IEC power curves
│   ├── performance_analysis.py # Yield, capacity factor & Cp calculations
│   ├── feature_engineering.py  # Physics feature derivation & leakage audit
│   ├── power_prediction.py     # ML regression training & holdout evaluation
│   ├── anomaly_detection.py    # Context-masked underperformance detection
│   ├── event_analysis.py       # SCADA alarm & shutdown correlation
│   ├── replay_engine.py        # Low-latency streaming replay engine
│   ├── dashboard_export.py     # Dashboard artifact & preview generator
│   └── dashboard/              # Dash Plotly components, layout, callbacks, app
└── tests/                      # 41 automated pytest unit tests
```

---

## ⚡ Quickstart

### 1. Launch the Decision Dashboard
```bash
python src/dashboard/app.py
```
Open your browser to: **`http://127.0.0.1:8050`**

### 2. Run the Full Automated Test Suite
```bash
python -m pytest -v
```

### 3. Run Pipeline Stages
```bash
# Run complete end-to-end pipeline
python -m src.pipeline --stage all

# Run specific stage
python -m src.pipeline --stage eda
python -m src.pipeline --stage train
python -m src.pipeline --stage anomaly
python -m src.pipeline --stage replay
python -m src.pipeline --stage dashboard
```
