# Model Card: Hill of Towie Wind Power Prediction Model

## Model Details
- **Model Name:** Hill of Towie Wind Turbine Power Regressor
- **Architecture:** HistGradientBoostingRegressor (scikit-learn)
- **Version:** 1.0.0
- **Target Variable:** `wtc_ActPower_mean` (Active Power in kW)
- **Rated Capacity:** 2300 kW per turbine
- **Model Artifact:** `models/final/best_power_model.joblib`

## Training & Evaluation Data
- **Training Period:** January 1, 2025 – December 31, 2025 (1,059,460 10-minute records).
- **Validation:** 5-fold cross-validation on 2025 dataset.
- **Holdout Test Period:** January 1, 2026 – April 30, 2026 (361,504 completely unseen records).
- **Turbines Evaluated:** 21 turbines (`T01` through `T21`).

## Input Features (Physics-Informed)
- `wtc_AcWindSp_mean` (Wind Speed, m/s)
- `wind_speed_cubed` ($v^3$, cubic aerodynamic energy proxy)
- `air_density_proxy` (Temperature-dependent dry air density)
- `aero_power_available_kw` (Available kinetic wind power)
- `wtc_GenRpm_mean` (Generator RPM)
- `wtc_MainSRpm_mean` (Main Rotor Shaft RPM)
- `tip_speed_ratio` (TSR $\lambda$)
- `gear_ratio_proxy`
- `pitch_asymmetry_deg`
- `wind_direction_sin`, `wind_direction_cos`
- `temp_delta_nacelle_ambient`
- 10-minute lags and 30-minute rolling means

## Target Leakage Audit
- **Generator Current (`wtc_AmpPhR_mean`):** Strictly excluded ($I \propto P/V$).
- **Operational Status Flags:** Quarantined from ML regression features.

## Metrics on Holdout Test Set (2026)
- **$R^2$ Score:** 0.9962
- **Root Mean Squared Error (RMSE):** 43.06 kW
- **Normalized RMSE:** 1.87% of 2300 kW rated capacity
- **Mean Absolute Error (MAE):** 19.34 kW

## Intended & Non-Intended Uses
- **Intended Use:** Asset health monitoring, operational performance benchmarking, baseline underperformance anomaly detection.
- **Non-Intended Use:** NOT for automated safety-critical pitch/brake control or sub-second grid synchronization.
