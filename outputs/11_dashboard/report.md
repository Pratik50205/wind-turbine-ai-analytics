# Phase 11 — Final Dashboard Verification & Export Report

## 1. Executive Summary
The interactive decision-support application for the **Hill of Towie Wind Farm** has been developed using **Dash 4.0.0 + Plotly 6.5.2 Desktop**.
The application interfaces directly with verified model artifacts and clean Parquet datasets from Phases 1 through 10, strictly prohibiting synthetic or hardcoded demo values.

## 2. Architecture & Design System
- **Framework:** Dash 4.0.0 with Plotly Desktop, custom dark mode and glassmorphism styling (`src/dashboard/styles.py`).
- **Data Access:** Fast in-memory cached service (`src/dashboard/data_service.py`), decoupled from the UI.
- **Entrypoints:**
  - `python src/dashboard/app.py`
  - `python dashboard/app.py`
- **Application Modules:**
  1. **Executive Overview:** High-level fleet KPIs (96.96 GWh annual generation, 23.88% CF, 98.42% availability), fleet power curve tracking, and turbine utilization rankings.
  2. **Turbine Performance:** Individual turbine diagnostics (`T01`–`T21`), binned empirical power curve vs IEC-61400-12 standard, and dynamic wind-power time-series.
  3. **Power Prediction:** Holdout 2026 test evaluation ($R^2 = 0.9962$, RMSE $= 43.06$ kW, NRMSE $= 1.87%$), actual vs predicted parity scatter, and physics-informed feature importance breakdown.
  4. **Abnormal Behavior:** 23 sustained underperformance events ($\ge 30$ min, deficit $\le -250$ kW, wind $\ge 3.5$ m/s), turbine distribution, and interactive event table.
  5. **Environmental & Operating Analysis:** Wind speed-power envelope and Hill of Towie directional wind rose.
  6. **Maintenance & Events:** 512k SCADA alarm frequency, shutdown categories, and anomaly-alarm correlation (65.2% coincident, 34.8% silent drift flagged as "Requires Investigation").
  7. **Historical SCADA Replay:** Interactive step streaming engine with Play/Pause/Reset, speed multipliers, real-time AI inference, anomaly alert banner, and low latency (1.48 ms).

## 3. Verified Dashboard KPIs
| KPI Name | Value | Unit | Aggregation Level | Source |
| :--- | :--- | :--- | :--- | :--- |
| **Fleet Annual Energy Yield** | 96.96 | GWh | Fleet Annual Sum (2025) | Phase 4 |
| **Fleet Capacity Factor** | 23.88 | % | Fleet Mean (2025) | Phase 4 |
| **Fleet Technical Availability** | 98.42 | % | Active Grid Operating Hours | Phase 4 |
| **Active Turbines** | 21 | Units | Siemens SWT-2.3-VS-82 | Phase 1 |
| **Holdout Model $R^2$ Score** | 0.9962 | Ratio | 2026 Test Set (361,504 pts) | Phase 7 |
| **Holdout Test RMSE** | 43.06 | kW | Holdout Prediction Error | Phase 7 |
| **Holdout Normalized RMSE** | 1.87 | % | % of 2300 kW Capacity | Phase 7 |
| **Sustained Anomaly Events** | 23 | Events | $\ge 30$ min underperformance | Phase 8 |
| **SCADA Alarms Ingested** | 512,117 | Events | 16-month fleet record | Phase 2 |
| **Replay Processing Latency** | 1.48 | ms/step | Real-Time Inference Step | Phase 10 |

## 4. Export Artifacts Manifest
- `dashboard_kpi_results.csv`: Machine-readable table of all displayed dashboard KPIs.
- `dashboard_data_dictionary.csv`: Full semantic definition, formula, source, and thresholds for all metrics.
- `dashboard_refresh_manifest.json`: Verification manifest confirming sources, timestamps, and zero-fabrication compliance.
- `preview/final_dashboard_preview.png`: 4-quadrant static preview graphic.
- `screenshots/`: Browser-captured validation screenshots for all dashboard views.
