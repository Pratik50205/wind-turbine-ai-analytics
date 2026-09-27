# Hill of Towie Wind Farm — Dashboard User Guide

## Running the Application
```bash
# Option 1: Run via source module
python src/dashboard/app.py

# Option 2: Run via dashboard entrypoint
python dashboard/app.py
```
Open your browser to: `http://127.0.0.1:8050`

## Dashboard Modules
1. **Executive Overview:** High-level fleet KPIs, annual energy production, and turbine rankings.
2. **Turbine Performance:** Individual turbine selector (`T01`–`T21`), power curve comparison, and 10-minute dynamic time-series.
3. **Power Prediction:** Model performance metrics, actual vs predicted parity scatter, and feature importances.
4. **Abnormal Behavior:** Sustained underperformance anomaly table and turbine anomaly distributions.
5. **Environmental Analysis:** Wind speed-power envelope and directional wind rose.
6. **Maintenance & Events:** Top SCADA alarms and root-cause correlation breakdown.
7. **Real-Time Replay:** Interactive step streaming engine with Play, Pause, Reset, and speed controls.
