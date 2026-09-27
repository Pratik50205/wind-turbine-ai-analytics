# Executive Summary: Hill of Towie Wind Farm AI Analytics Project

## Project Purpose
This project delivers an end-to-end, physics-informed data analytics and machine learning solution for performance monitoring, power prediction, abnormal-behavior detection, and real-time SCADA replay on the **Hill of Towie Wind Farm** (Moray, Scotland; 21 Siemens SWT-2.3-VS-82 turbines, 48.3 MW fleet capacity).

## Key Empirical Findings & Results
1. **Fleet Energy Production (2025 Baseline):**
   - **Annual Yield:** **96.96 GWh** injected into the grid across 21 turbines.
   - **Capacity Factor:** **23.88%** (empirical range: 16.7% to 32.2%), directly matching documented Scottish onshore meteorological profiles.
   - **Technical Availability:** **98.42%**, demonstrating strong asset uptime with minimal unforced downtime.
2. **Physics-Informed Power Prediction:**
   - **Model:** HistGradientBoostingRegressor trained on 2025 SCADA features ($v^3$, $\rho$ air density proxy, TSR, cyclical wind direction).
   - **Target Leakage Safeguard:** Electrical current (`wtc_AmpPhR_mean`) and operational status flags were strictly quarantined from training inputs.
   - **2026 Holdout Test Performance:**
     - **$R^2 = 0.9962$** (99.62% variance explained on 361,504 unseen records).
     - **RMSE = 43.06 kW** (**1.87% Normalized RMSE** relative to 2300 kW rated capacity).
     - **MAE = 19.34 kW**.
3. **Abnormal Behavior & SCADA Event Correlation:**
   - **Anomaly Engine:** Statistical residual deficit threshold ($\le -250$ kW, wind $\ge 3.5$ m/s, $\ge 30$-min persistence), with operational masking for curtailment and high-wind shutdowns.
   - **Detected Events:** **23 sustained abnormal underperformance periods** identified in 2025.
   - **Root Cause Splitting:** 65.2% of events were coincident with active SCADA alarm codes or shutdown logs; 34.8% were isolated as silent aerodynamic/pitch drift requiring physical field inspection.
4. **Real-Time Replay & Interactive Decision Support:**
   - **Historical SCADA Replay Engine:** Benchmarked at **1.48 ms per step latency** (675 steps/sec throughput).
   - **Decision Support Dashboard:** 7 interactive Dash + Plotly tabs providing turbine diagnostics, parity plots, environmental roses, and live step-by-step streaming.
