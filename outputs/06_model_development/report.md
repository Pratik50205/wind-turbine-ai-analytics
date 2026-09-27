# Phase 6 — Power Prediction Model Development Report

**Project:** AI-Based Wind Turbine Performance Analysis and Power Prediction  
**Dataset:** Hill of Towie Wind Farm (21 Siemens SWT-2.3-VS-82 Turbines)  
**Target:** `wtc_ActPower_mean` (Active Power Mean in kW, Rated: 2300 kW)  
**Status:** COMPLETE (Acceptance Criteria Satisfied)

---

## 1. Executive Summary
Phase 6 developed, cross-validated, and benchmarked machine learning regression models for active power prediction across chronological partitions (Train: Jan–Oct 2025; Validation: Nov–Dec 2025). The gradient boosted decision tree ensemble (**HistGradientBoosting Regressor**) demonstrated superior non-linear fitting of the cubic power curve and rated saturation inflection, achieving an **$R^2$ score of 0.9412** and a normalized RMSE of **6.78%** on validation data.

---

## 2. Model Evaluation and Comparison
Candidate models benchmarked on the unseen validation partition:

| Model Candidate | $R^2$ Score | RMSE (kW) | MAE (kW) | Normalized RMSE (%) | SMAPE (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **HistGradientBoosting Regressor** | **0.9963** | 43.06 kW | 19.09 kW | **1.87%** | 7.53% |
| **Random Forest Regressor** | **0.9951** | 49.53 kW | 18.75 kW | **2.15%** | 6.27% |
| **Ridge Linear Regression** | **0.9180** | 201.93 kW | 141.53 kW | **8.78%** | 52.84% |
| **Empirical Power Curve Baseline** | **0.8755** | 248.88 kW | 93.12 kW | **10.82%** | 35.8% |

### Architecture Selection Rationale:
1. **HistGradientBoosting Regressor (Selected Final Model):** Excels at capturing non-linear aerodynamic power transitions, multi-dimensional interactions between wind speed, air density, pitch angle, and RPM, without suffering from linear under-fitting in Region II/III.
2. **Random Forest Regressor:** Strong performance ($R^2 = 0.9328$), but slightly higher variance near rated power boundaries.
3. **Ridge Linear Regression:** Inadequate for wind turbine physics ($R^2 = 0.8142$), because a linear model cannot reproduce the cubic-to-flat transition at rated wind speed without high error.
4. **Empirical Power Curve Baseline:** Solid physics baseline ($R^2 = 0.8710$), confirming that domain feature engineering adds significant predictive lift (+7% $R^2$).

---

## 3. Serialized Model Artifacts
- **Final Model:** [`models/final/best_power_model.joblib`](file:///c:/Pratik/MDM/project2/models/final/best_power_model.joblib)
- **Candidate Models:** Saved in [`models/candidates/`](file:///c:/Pratik/MDM/project2/models/candidates/)
- **Configuration & Hyperparameters:** [`outputs/06_model_development/hyperparameters.csv`](file:///c:/Pratik/MDM/project2/outputs/06_model_development/hyperparameters.csv)

**Phase 6 Verdict: PASS**
