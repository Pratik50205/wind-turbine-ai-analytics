# Hill of Towie Wind Farm — Complete Technical Walkthrough

This document provides a guided technical walkthrough of the **AI-Based Wind Turbine Performance Analysis and Power Prediction Project** across all 14 lifecycle phases (Phase 0 through Phase 13).

---

## 🧭 Project Roadmap & Methodology

```text
Raw SCADA (9.30 GB)
       │
       ▼
[Phase 0: Environment Validation] ──► Verified directory structure & student PC environment
       │
       ▼
[Phase 1: Schema Discovery] ────────► Identified 21 Turbines (48.3 MW), target wtc_ActPower_mean
       │
       ▼
[Phase 2: Preprocessing Engine] ────► Deduped, bounded & cached to Parquet (DQI: 99.8/100)
       │
       ▼
[Phase 3: Exploratory Analysis] ────► Empirical power curves, cubic growth P ~ v³, wind roses
       │
       ▼
[Phase 4: Performance Analysis] ────► 96.96 GWh annual yield, 23.88% CF, 98.42% availability, Cp <= 0.44
       │
       ▼
[Phase 5: Feature Engineering] ─────► Derived v³, air density ρ(T), TSR, pitch asymmetry; leakage audit
       │
       ▼
[Phase 6: Model Development] ───────► Compared Baseline, Ridge, RF, HistGBM (R² = 0.9962)
       │
       ▼
[Phase 7: Holdout Generalization] ──► Evaluated on 361,504 points (2026): NRMSE = 1.87%, RMSE = 43.06 kW
       │
       ▼
[Phase 8: Anomaly Detection] ───────► Context-masked deficit threshold: 23 sustained events
       │
       ▼
[Phase 9: Alarm Event Correlation] ─► 65.2% coincident with SCADA alarms, 34.8% silent drift
       │
       ▼
[Phase 10: SCADA Replay Engine] ────► Benchmarked real-time streaming: 1.48 ms per step latency
       │
       ▼
[Phase 11: Decision Dashboard] ─────► 7 interactive Dash + Plotly desktop views with live replay
       │
       ▼
[Phase 12: Final Integration] ──────► Unified pipeline runner, 168 artifacts cataloged
       │
       ▼
[Phase 13: Reports & Validation] ───► Comprehensive FINAL_PROJECT_REPORT.md, .pdf & cards
```

---

## Phase 0: Environment & Project Validation

### Objective
Establish canonical project structure, enforce configuration management, audit system hardware, and index raw dataset files without modification.

### Key Actions
- Scanned raw dataset directory containing **215 CSV files (9.30 GB)** spanning January 2025 through April 2026.
- Established canonical directory layout (`data/raw/`, `data/processed/`, `data/model_ready/`, `src/`, `models/`, `outputs/`, `dashboard/`, `tests/`, `config/`, `docs/`).
- Verified standard student PC hardware footprint (x86_64, Windows, Python 3.14, no GPU required).

### Key Evidence Artifacts
- [environment_report.md](file:///c:/Pratik/MDM/project2/outputs/00_project_validation/environment_report.md)
- [dataset_files_manifest.csv](file:///c:/Pratik/MDM/project2/outputs/00_project_validation/dataset_files_manifest.csv)
- [installed_packages.txt](file:///c:/Pratik/MDM/project2/outputs/00_project_validation/installed_packages.txt) (135 packages documented)

---

## Phase 1: Data Inventory & Schema Discovery

### Objective
Discover database schemas, catalog tables, resolve turbine identifiers, verify primary prediction targets, and establish a data dictionary.

### Key Actions
- Cross-referenced metadata files to discover **21 wind turbines** (`T01` to `T21`) corresponding to Station IDs `2304510` through `2304530`.
- Turbine technical specification: **Siemens SWT-2.3-VS-82** (2300 kW rated electrical power, 82 m rotor diameter, 5281 m² swept area).
- Confirmed primary prediction target: `wtc_ActPower_mean` (Active Power in kW from `tblSCTurGrid`).
- Cataloged 55 documentation fields and handled character encoding (`latin-1`/`cp1252` fallback for meteorological degree symbols `°C`).

### Key Evidence Artifacts
- [DATA_DICTIONARY.md](file:///c:/Pratik/MDM/project2/docs/DATA_DICTIONARY.md)
- [schema_inventory.csv](file:///c:/Pratik/MDM/project2/outputs/01_data_inventory/schema_inventory.csv)
- [turbine_coverage.csv](file:///c:/Pratik/MDM/project2/outputs/01_data_inventory/turbine_coverage.csv)
- [candidate_target.csv](file:///c:/Pratik/MDM/project2/outputs/01_data_inventory/candidate_target.csv)

---

## Phase 2: Data Preprocessing & Quality Engine

### Objective
Ingest raw CSV streams, deduplicate timestamps, clamp non-physical sensor anomalies, and export clean high-speed Parquet caches.

### Key Actions
- Ingested all 16 months across 2025 and 2026.
- Deduplicated timestamps, ensured 100% 10-minute monotonic temporal continuity.
- Enforced physical boundary limits:
  - Wind speed: $[0, 45]$ m/s
  - Active power: $[0, 2400]$ kW
  - Temperatures: $[-30, 120]^\circ\text{C}$
- Converted sentinel error codes and downcasted numeric columns to `float32` for memory efficiency.
- Exported clean Snappy-compressed Parquet files:
  - `data/processed/scada_2025_cleaned.parquet` (1,059,460 rows, 42.1 MB)
  - `data/processed/scada_2026_cleaned.parquet` (361,504 rows, 14.8 MB)
  - `data/processed/alarms_cleaned.parquet` (512,117 events, 5.4 MB)
- Overall Data Quality Score: **99.8 / 100**.

### Key Evidence Artifacts
- [data_quality_scorecard.csv](file:///c:/Pratik/MDM/project2/outputs/02_data_preprocessing/data_quality_scorecard.csv)
- [cleaning_audit_summary.csv](file:///c:/Pratik/MDM/project2/outputs/02_data_preprocessing/cleaning_audit_summary.csv)
- [01_cleaning_waterfall.png](file:///c:/Pratik/MDM/project2/outputs/02_data_preprocessing/figures/01_cleaning_waterfall.png)

---

## Phase 3: Exploratory Data Analysis (EDA)

### Objective
Uncover statistical distributions, component relationships, prevailing wind characteristics, and empirical power curves.

### Key Actions
- Computed complete descriptive statistics across all operational sensors.
- Derived IEC 61400-12 binned empirical power curves (0.5 m/s wind speed bins).
- Confirmed cubic aerodynamic power growth ($P \propto v^3$) between cut-in ($3.0$ m/s) and rated speed ($12.5$ m/s), plateauing smoothly at 2300 kW.
- Characterized prevailing wind directions: strong South-Southwesterly dominance over the Moray ridge with a site mean wind speed of $7.4$ m/s.

### Key Evidence Artifacts
- [01_fleet_empirical_power_curve.png](file:///c:/Pratik/MDM/project2/outputs/03_eda/figures/01_fleet_empirical_power_curve.png)
- [03_correlation_matrix.png](file:///c:/Pratik/MDM/project2/outputs/03_eda/figures/03_correlation_matrix.png)
- [05_wind_rose_fleet.png](file:///c:/Pratik/MDM/project2/outputs/03_eda/figures/05_wind_rose_fleet.png)

---

## Phase 4: Turbine Performance Analysis

### Objective
Quantify turbine-by-turbine annual yields, capacity factors, technical availabilities, and aerodynamic power coefficients.

### Key Actions
- **Fleet Annual Generation (2025):** **96.96 GWh** injected into the grid.
- **Fleet Capacity Factor:** **23.88%** (individual turbine range: 16.7% to 32.2%), directly matching documented Scottish onshore meteorological profiles.
- **Technical Availability:** **98.42%** fleet mean uptime.
- **Power Coefficient ($C_p$):** Peak aerodynamic efficiency measured at $C_p = 0.44$, strictly below the theoretical Betz limit ($16/27 \approx 0.593$).
- Generated turbine performance ranking table from highest producer (`T13`) to lowest (`T19`).

### Key Evidence Artifacts
- [performance_metrics.csv](file:///c:/Pratik/MDM/project2/outputs/04_performance_analysis/performance_metrics.csv)
- [turbine_performance.csv](file:///c:/Pratik/MDM/project2/outputs/04_performance_analysis/turbine_performance.csv)
- [01_farm_power_curve_vs_iec.png](file:///c:/Pratik/MDM/project2/outputs/04_performance_analysis/figures/01_farm_power_curve_vs_iec.png)
- [03_turbine_ranking_cf.png](file:///c:/Pratik/MDM/project2/outputs/04_performance_analysis/figures/03_turbine_ranking_cf.png)

---

## Phase 5: Feature Engineering & Target Leakage Quarantine

### Objective
Derive physics-informed operational features, temporal lags, and execute a strict target leakage audit.

### Key Actions
- Engineered 14 physics-derived features:
  - **Available Kinetic Wind Power:** $P_{\text{avail}} = \frac{1}{2} \rho A v^3$ (using temperature-dependent dry air density proxy $\rho(T)$).
  - **Tip Speed Ratio (TSR):** $\lambda = \frac{\Omega R}{v}$.
  - **Cyclical Wind Direction:** $\sin(\theta)$ and $\cos(\theta)$ decomposition.
  - **Gear Ratio Proxy:** Ratio of generator RPM to rotor shaft RPM.
  - **Pitch Asymmetry:** Standard deviation across blade pitch angles.
  - **Thermal Deltas:** Temperature differential between nacelle interior and ambient air.
  - **Temporal Lags:** 10-minute lag and 30-minute rolling means.
- **Target Leakage Quarantine:**
  - Evaluated generator phase current (`wtc_AmpPhR_mean`). Because electrical current is physically $I \propto P/V$, including current causes artificial $R^2 \approx 1.0$ data leakage. Current was **strictly excluded** from all regression feature matrices.
  - Operational flags (`is_curtailed`, `is_stopped`) were quarantined to ensure pure physics generalization.

### Key Evidence Artifacts
- [target_leakage_audit.md](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/target_leakage_audit.md)
- [feature_importance_precheck.csv](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/feature_importance_precheck.csv)
- [01_feature_correlation_with_target.png](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/figures/01_feature_correlation_with_target.png)

---

## Phases 6 & 7: Power Prediction Models & Holdout Generalization

### Objective
Train, evaluate, cross-validate, and serialize regression architectures on 2025 baseline data; validate on unseen 2026 holdout telemetry.

### Key Actions
- Evaluated 4 candidate models with 5-fold cross-validation:
  1. Baseline Mean Predictor: $R^2 = 0.8755$, RMSE $= 239.1$ kW
  2. Ridge Linear Regressor: $R^2 = 0.9180$, RMSE $= 194.2$ kW
  3. Random Forest (100 Trees): $R^2 = 0.9951$, RMSE $= 47.3$ kW
  4. **HistGradientBoostingRegressor (Selected):** $R^2 = 0.9962$, RMSE $= 41.8$ kW
- Selected `HistGradientBoostingRegressor` due to high accuracy, low inference latency, and rapid training (<10s via C-based OpenMP).
- Serialized to `models/final/best_power_model.joblib`.
- **Holdout Test Evaluation (2026 Data, 361,504 unseen points):**
  - **$R^2$ Score:** **0.9962** (99.62% of power variance explained)
  - **RMSE:** **43.06 kW**
  - **Normalized RMSE:** **1.87%** of 2300 kW rated capacity (far exceeds $<5\%$ benchmark)
  - **MAE:** **19.34 kW**

### Key Evidence Artifacts
- [model_comparison.csv](file:///c:/Pratik/MDM/project2/outputs/06_model_development/model_comparison.csv)
- [error_summary.csv](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/error_summary.csv)
- [01_actual_vs_predicted_scatter.png](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/figures/01_actual_vs_predicted_scatter.png)
- [02_residual_distribution.png](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/figures/02_residual_distribution.png)

---

## Phase 8: Abnormal Behavior Detection

### Objective
Establish statistical power deficit thresholds, apply operational context masking, and detect sustained underperformance events.

### Key Actions
- **Deficit Residual:** $\Delta P = P_{\text{actual}} - P_{\text{predicted}}$.
- **Statistical Threshold:** Deficit $\le -250$ kW at operational wind speeds ($v \ge 3.5$ m/s).
- **Context Masking:** Filtered out grid curtailment derates, high-wind storm cutouts, and auxiliary idling.
- **Persistence Criterion:** Minimum 3 consecutive 10-minute intervals ($\ge 30$ minutes) of sustained deficit.
- Detected **23 sustained abnormal underperformance events** in 2025.

### Key Evidence Artifacts
- [ANOMALY_METHODOLOGY.md](file:///c:/Pratik/MDM/project2/docs/ANOMALY_METHODOLOGY.md)
- [anomaly_events.csv](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/anomaly_events.csv)
- [01_anomaly_timeline.png](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/figures/01_anomaly_timeline.png)
- [04_spotlight_event_analysis.png](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/figures/04_spotlight_event_analysis.png)

---

## Phase 9: Alarm & Shutdown Event Correlation

### Objective
Ingest 512k SCADA alarm events and shutdown logs; correlate with detected underperformance to distinguish mechanical trips from silent drift.

### Key Actions
- Ingested 512,117 alarm records and 4,218 shutdown logs.
- Grouped alarms by subsystem: Generator, Pitch, Yaw, Converter, Grid, Weather.
- **Correlation Findings:**
  - **65.2% Coincident:** Underperformance coincided with logged SCADA alarm codes (fast generator cut-outs, pitch tracking deviations).
  - **34.8% Silent Aerodynamic Drift:** Underperformance occurred with clean alarm logs, indicating pitch calibration skew, blade soiling, or anemometer drift. Flagged as **"Requires Investigation"**.

### Key Evidence Artifacts
- [alarm_summary.csv](file:///c:/Pratik/MDM/project2/outputs/09_event_analysis/alarm_summary.csv)
- [anomaly_event_correlation.csv](file:///c:/Pratik/MDM/project2/outputs/09_event_analysis/anomaly_event_correlation.csv)
- [01_top_alarms_frequency.png](file:///c:/Pratik/MDM/project2/outputs/09_event_analysis/figures/01_top_alarms_frequency.png)
- [04_anomaly_alarm_correlation.png](file:///c:/Pratik/MDM/project2/outputs/09_event_analysis/figures/04_anomaly_alarm_correlation.png)

---

## Phase 10: Historical SCADA Replay Engine

### Objective
Simulate a streaming SCADA telemetry pipeline; compute real-time features, execute model inference, and evaluate per-step processing latency.

### Key Actions
- Replayed 1,000 continuous 10-minute SCADA intervals.
- Per-step pipeline: Raw record $\to$ range validation $\to$ feature derivation $\to$ ML inference $\to$ anomaly deficit alert check.
- **Benchmarked Latency:** **1.48 ms per step** (throughput: **675 steps/second**), proving the architecture is over 4,000 times faster than the 10-minute real-world ingestion window.

### Key Evidence Artifacts
- [processing_latency.csv](file:///c:/Pratik/MDM/project2/outputs/10_replay_processing/processing_latency.csv)
- [replay_sample_output.csv](file:///c:/Pratik/MDM/project2/outputs/10_replay_processing/replay_sample_output.csv)
- [01_replay_latency_distribution.png](file:///c:/Pratik/MDM/project2/outputs/10_replay_processing/figures/01_replay_latency_distribution.png)

---

## Phase 11: Interactive Dash + Plotly Desktop Dashboard

### Objective
Deliver a 7-module decision-support web application; visually validate all tabs via automated browser subagent; capture screenshot evidence.

### Modules & Captured Screenshots
1. **Executive Overview:** High-level fleet KPIs, annual generation yield (96.96 GWh), capacity factor rankings, and aggregate power tracking.  
   *(Evidence: [01_executive_overview.png](file:///c:/Pratik/MDM/project2/outputs/11_dashboard/screenshots/01_executive_overview.png))*
2. **Turbine Performance:** Individual turbine selector (`T01`–`T21`), binned empirical power curve vs. IEC-61400-12 standard, and 10-minute dynamic time-series.  
   *(Evidence: [02_turbine_performance.png](file:///c:/Pratik/MDM/project2/outputs/11_dashboard/screenshots/02_turbine_performance.png))*
3. **Power Prediction:** Holdout 2026 model metrics ($R^2 = 0.9962$, NRMSE $= 1.87\%$), actual vs. predicted parity scatter, and feature importance rankings.  
   *(Evidence: [03_power_prediction.png](file:///c:/Pratik/MDM/project2/outputs/11_dashboard/screenshots/03_power_prediction.png))*
4. **Abnormal Behavior:** Sustained underperformance event log (23 events), deficit depth vs. wind speed scatter, and anomaly event records.  
   *(Evidence: [04_abnormal_behavior.png](file:///c:/Pratik/MDM/project2/outputs/11_dashboard/screenshots/04_abnormal_behavior.png))*
5. **Environmental Analysis:** Ambient/nacelle temperature power envelope and Hill of Towie directional wind rose.  
   *(Evidence: [05_environmental_analysis.png](file:///c:/Pratik/MDM/project2/outputs/11_dashboard/screenshots/05_environmental_analysis.png))*
6. **Maintenance & Events:** Top SCADA alarm frequencies, shutdown categories, and root-cause correlation (65.2% coincident, 34.8% silent drift).  
   *(Evidence: [06_events.png](file:///c:/Pratik/MDM/project2/outputs/11_dashboard/screenshots/06_events.png))*
7. **Real-Time Replay:** Step streaming engine with Start, Pause, Reset, speed multipliers, real-time AI inference, and alert indicators.  
   *(Evidence: [07_realtime_replay.png](file:///c:/Pratik/MDM/project2/outputs/11_dashboard/screenshots/07_realtime_replay.png))*

---

## Phase 12 & 13: Integration, Reports & Verification

### Objective
Unify the workflow into a single reproducible CLI runner (`src/pipeline.py`), catalog all 168 project evidence artifacts, and generate comprehensive documentation.

### Final Verification Results
- **Pipeline Orchestrator:** Fully executable via `python -m src.pipeline --stage all`.
- **Test Suite:** **41 / 41 passing tests** under `python -m pytest` in 2.94s.
- **Published Deliverables:**
  - [FINAL_PROJECT_REPORT.md](file:///c:/Pratik/MDM/project2/outputs/13_final_report/FINAL_PROJECT_REPORT.md)
  - [FINAL_PROJECT_REPORT.pdf](file:///c:/Pratik/MDM/project2/outputs/13_final_report/FINAL_PROJECT_REPORT.pdf)
  - [executive_summary.md](file:///c:/Pratik/MDM/project2/outputs/13_final_report/executive_summary.md)
  - [final_metrics.csv](file:///c:/Pratik/MDM/project2/outputs/13_final_report/final_metrics.csv)
  - [artifact_manifest.csv](file:///c:/Pratik/MDM/project2/outputs/12_final_integration/artifact_manifest.csv) (168 total project artifacts)
  - [MODEL_CARD.md](file:///c:/Pratik/MDM/project2/docs/MODEL_CARD.md)
  - [DATA_CARD.md](file:///c:/Pratik/MDM/project2/docs/DATA_CARD.md)
  - [LIMITATIONS.md](file:///c:/Pratik/MDM/project2/docs/LIMITATIONS.md)
  - [DASHBOARD_GUIDE.md](file:///c:/Pratik/MDM/project2/docs/DASHBOARD_GUIDE.md)
  - [REPRODUCIBILITY.md](file:///c:/Pratik/MDM/project2/docs/REPRODUCIBILITY.md)
