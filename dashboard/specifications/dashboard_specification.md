# Hill of Towie Wind Farm — Dashboard Technical Specification

## 1. System Overview
- **Technology Stack:** Dash 4.0.0, Plotly 6.5.2, Flask WSGI, HTML5/CSS3.
- **Design Paradigm:** Dark Theme Glassmorphism, optimized for desktop 1080p+ widescreen displays.
- **Data Querying Architecture:** Decoupled in-memory caching layer (`src/dashboard/data_service.py`), querying Snappy Parquet tables directly.

---

## 2. Color Palette & Design Tokens
```json
{
  "bg_dark": "#0b0f19",
  "bg_card": "#151e2e",
  "bg_card_secondary": "#1e293b",
  "border": "#2d3748",
  "accent_cyan": "#00f2fe",
  "accent_blue": "#38bdf8",
  "accent_green": "#10b981",
  "accent_amber": "#f59e0b",
  "accent_red": "#ef4444",
  "accent_purple": "#8b5cf6",
  "text_primary": "#f8fafc",
  "text_secondary": "#94a3b8",
  "text_muted": "#64748b"
}
```

---

## 3. Module Specifications

### Module 1: Executive Overview
- **Header:** Live operational status indicator, turbine count (21), total nameplate capacity (48.3 MW).
- **KPI Row:**
  - Fleet Annual Yield: `96.96 GWh`
  - Capacity Factor: `23.88%`
  - Technical Availability: `98.42%`
  - Active Turbines: `21 Units`
  - Model Holdout R²: `0.9962`
  - Sustained Underperformance Events: `23 Events`
- **Charts:**
  - Fleet Generation Profile & AI Power Tracking (150-step window).
  - Turbine Capacity Factor Benchmark (horizontal bar chart ranking T01–T21).

### Module 2: Turbine Performance
- **Controls:** Turbine Dropdown Selector (`T01` to `T21`).
- **Dynamic KPIs:** Selected turbine Annual Yield (GWh), Capacity Factor (%), Mean Power (kW), Availability (%).
- **Charts:**
  - Measured Empirical Power Curve vs. IEC 61400-12 binned reference curve.
  - 10-Minute Wind Speed vs. Active Power dual time-series.

### Module 3: Power Prediction
- **Model KPI Cards:** Holdout Test R² (0.9962), RMSE (43.06 kW), Normalized RMSE (1.87%), MAE (19.34 kW).
- **Charts:**
  - Actual vs. Predicted Power Parity Scatter with 1:1 ideal dashed diagonal.
  - Physics-Informed Feature Importance horizontal bar chart (Top 10 features).

### Module 4: Abnormal Behavior
- **Anomaly KPI Cards:** Sustained Anomalies (23), Average Deficit (-334.2 kW), Average Duration (18.5 hrs), Operational Context.
- **Interactive DataTable:** Sustained anomaly events log with start/end timestamps, duration, deficit, and action status (*"Requires Investigation"*).
- **Chart:** Turbine Anomaly Rate Distribution across the 21 assets.

### Module 5: Environmental Analysis
- **Charts:**
  - Wind Speed vs. Active Power envelope.
  - Prevailing Wind Direction Compass Rose (Hill of Towie site profile).

### Module 6: Maintenance & Events
- **KPI Cards:** Logged Alarms (512,117), Shutdown Records (4,218), Correlated Anomalies (65.2%), Silent Drift (34.8%).
- **Charts:**
  - Top SCADA Alarms by occurrence frequency (fast cut-outs, cut-ins, converter alarms).
  - Anomaly Root-Cause Correlation Donut Chart (Alarmed vs. Silent Drift).

### Module 7: Historical SCADA Replay
- **Controls:** `Start Replay`, `Pause`, `Reset`, Speed Multiplier (`1x`, `5x`, `10x`).
- **Live State Store:** Tracks current streaming step, active turbine, timestamp, and alert status.
- **Streaming Chart:** Rolling 50-step window comparing live SCADA actual power against real-time AI inference.
- **Latency Indicator:** Real-time per-step processing benchmark (**1.48 ms per step**).
