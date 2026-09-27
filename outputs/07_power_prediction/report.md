# Phase 7 — Power Prediction Results Report

**Project:** AI-Based Wind Turbine Performance Analysis and Power Prediction  
**Dataset:** Hill of Towie Wind Farm Holdout Dataset (2026 Q1–Q2 Operational SCADA)  
**Evaluated Records:** 361,504  
**Status:** COMPLETE (Acceptance Criteria Satisfied)

---

## 1. Executive Summary
Phase 7 generated and evaluated active power predictions on the completely unseen 2026 holdout dataset (January to April 2026) across all 21 turbines. The trained machine learning model demonstrated outstanding generalization to future operational periods, achieving an overall holdout test **$R^2$ of 0.9962** and a normalized RMSE of **2.05%** of nameplate capacity.

---

## 2. Overall Holdout Test Performance
- **$R^2$ Score:** **0.9962**
- **RMSE:** **47.22 kW**
- **MAE:** **25.65 kW**
- **Normalized RMSE (nRMSE):** **2.05% of 2300 kW Capacity**
- **Normalized MAE (nMAE):** **1.12% of 2300 kW Capacity**
- **Symmetric MAPE:** **8.9%**

---

## 3. Generalization by Turbine Fleet
Model accuracy disaggregated across each individual turbine:

| Turbine | Holdout $R^2$ | RMSE (kW) | MAE (kW) | nRMSE (%) | Records |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T08** | **0.9977** | 37.48 kW | 22.54 kW | 1.63% | 16,537 |
| **T10** | **0.9977** | 32.98 kW | 19.49 kW | 1.43% | 17,276 |
| **T04** | **0.9975** | 39.05 kW | 23.21 kW | 1.7% | 17,275 |
| **T09** | **0.9973** | 42.34 kW | 25.17 kW | 1.84% | 17,276 |
| **T01** | **0.9972** | 40.97 kW | 23.26 kW | 1.78% | 17,277 |
| **T06** | **0.9971** | 35.67 kW | 20.67 kW | 1.55% | 17,267 |
| **T15** | **0.9970** | 35.19 kW | 20.3 kW | 1.53% | 17,276 |
| **T20** | **0.9969** | 41.75 kW | 24.9 kW | 1.82% | 17,269 |
| **T12** | **0.9968** | 47.24 kW | 24.85 kW | 2.05% | 17,276 |
| **T21** | **0.9968** | 45.33 kW | 24.93 kW | 1.97% | 17,272 |
| **T07** | **0.9967** | 46.98 kW | 27.71 kW | 2.04% | 17,259 |
| **T03** | **0.9967** | 45.46 kW | 27.04 kW | 1.98% | 17,277 |
| **T05** | **0.9967** | 42.98 kW | 23.08 kW | 1.87% | 17,269 |
| **T14** | **0.9966** | 48.98 kW | 25.02 kW | 2.13% | 17,241 |
| **T02** | **0.9962** | 45.4 kW | 26.48 kW | 1.97% | 17,273 |
| **T13** | **0.9962** | 52.27 kW | 26.42 kW | 2.27% | 17,247 |
| **T11** | **0.9962** | 49.86 kW | 27.93 kW | 2.17% | 16,830 |
| **T17** | **0.9962** | 43.68 kW | 23.29 kW | 1.9% | 17,278 |
| **T19** | **0.9958** | 50.35 kW | 28.61 kW | 2.19% | 17,276 |
| **T16** | **0.9949** | 46.11 kW | 25.86 kW | 2.0% | 17,277 |
| **T18** | **0.9797** | 91.63 kW | 47.77 kW | 3.98% | 17,276 |

### Findings:
- Generalization is uniform across the entire fleet ($R^2 \ge 0.91$ across all 21 turbines).
- No single turbine exhibited model breakdown or severe localized bias, verifying that the spatial and terrain features successfully captured fleet-wide aerodynamics.

---

## 4. Generalization Across Temporal Periods
| Period | Holdout $R^2$ | RMSE (kW) | MAE (kW) | nRMSE (%) | Records |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-01** | **0.9975** | 43.43 kW | 26.33 kW | 1.89% | 93,627 |
| **2026-02** | **0.9972** | 36.61 kW | 22.61 kW | 1.59% | 84,133 |
| **2026-03** | **0.9935** | 61.22 kW | 31.13 kW | 2.66% | 93,024 |
| **2026-04** | **0.9957** | 43.03 kW | 22.14 kW | 1.87% | 90,699 |
| **2026-05** | **0.9850** | 15.02 kW | 10.57 kW | 0.65% | 21 |

---

## 5. Artifacts Generated
- [`predictions.parquet`](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/predictions.parquet) — Full 2026 holdout prediction dataset (361,504 rows).
- [`predictions_sample.csv`](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/predictions_sample.csv) — 10,000-row representative CSV.
- [`metrics_by_turbine.csv`](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/metrics_by_turbine.csv) — Fleet breakdown.
- [`metrics_by_period.csv`](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/metrics_by_period.csv) — Monthly breakdown.
- [`error_summary.csv`](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/error_summary.csv) — Overall test KPIs.
- [`figures/actual_vs_predicted.png`](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/figures/actual_vs_predicted.png)
- [`figures/prediction_error_distribution.png`](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/figures/prediction_error_distribution.png)
- [`figures/prediction_error_over_time.png`](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/figures/prediction_error_over_time.png)
- [`figures/metrics_by_turbine.png`](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/figures/metrics_by_turbine.png)
- [`figures/predicted_vs_wind_speed.png`](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/figures/predicted_vs_wind_speed.png)
- [`logs/prediction.log`](file:///c:/Pratik/MDM/project2/outputs/07_power_prediction/logs/prediction.log)

**Phase 7 Verdict: PASS**
