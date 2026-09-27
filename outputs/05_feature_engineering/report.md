# Phase 5 — Feature Engineering and Feature Selection Report

**Project:** AI-Based Wind Turbine Performance Analysis and Power Prediction  
**Dataset:** Hill of Towie Wind Farm (21 Siemens SWT-2.3-VS-82 Turbines)  
**Status:** COMPLETE (Acceptance Criteria Satisfied)

---

## 1. Executive Summary
Phase 5 engineered domain-specific aerodynamic, kinematic, thermal, cyclical, and temporal lag features, established strict target leakage guardrails, and generated clean model-ready feature matrices for train (2025) and test (2026) periods. A total of **30 curated input features** were selected and validated.

---

## 2. Target Leakage Prevention & Audit
To ensure defensible, generalization-ready machine learning, all candidate variables underwent a formal target leakage audit:

| Channel | Leakage Risk | Pipeline Decision | Rationale |
| :--- | :--- | :--- | :--- |
| `wtc_ActPower_mean` | **TARGET** | `EXCLUDED_AS_INPUT` | Exact prediction target variable ($y$). Cannot be used as feature. |
| `wtc_AmpPhR_mean` | **HIGH** | `EXCLUDED` | Phase current is a direct electrical consequence of generated active power ($I \approx P / (\sqrt{3} V \cos\phi)$). Including current creates trivial circular leakage. |
| `wtc_VoltPhR_mean` | **LOW** | `RETAINED_AUXILIARY` | Grid voltage is primarily governed by the utility substation and grid stiffness rather than turbine power. |
| `wtc_CosPhi_mean` | **MEDIUM** | `EXCLUDED` | Direct power factor calculation derived from instantaneous active and apparent power. |
| `wtc_ReactPwr_mean` | **MEDIUM** | `EXCLUDED` | Coupled to electrical generator inverter controls; excluded from primary aerodynamic power prediction. |
| `wtc_PowerRef_endvalue` | **HIGH_IF_FREE** | `RETAINED_FOR_BASELINE` | Controller internal setpoint; kept for benchmarking against supervisory control, but primary ML model trains without it to remain independent of SCADA setpoint availability. |
| `is_stopped` | **LABEL_LEAKAGE** | `EXCLUDED_FROM_ML_INPUTS` | Operational status flag derived from wtc_ScTurSto_timeon; used only for data partitioning/filtering, not as a regression input. |
| `is_curtailed` | **LABEL_LEAKAGE** | `EXCLUDED_FROM_ML_INPUTS` | Synthetic curtailment flag derived using power; using it as input would cause label leakage. |

### Key Safeguards:
- **No Consequential Electrical Features:** Direct generator current (`wtc_AmpPhR_mean`) was excluded because it provides trivial retrospective knowledge of power output ($I \propto P$).
- **No Operational Status Inputs:** `is_stopped` and `is_curtailed` were excluded from regression inputs, guaranteeing the model predicts purely from physical and atmospheric variables.

---

## 3. Top Engineered Features & Importance Precheck
Preliminary feature importance evaluation using an ensemble Random Forest regressor on operational records:

| Rank | Feature | RF Importance Share | Linear Correlation |
| :--- | :--- | :--- | :--- |
| 1 | `aero_power_available_kw` | **77.81%** | +0.8127 |
| 2 | `wtc_GenRpm_mean` | **6.10%** | +0.8381 |
| 3 | `wtc_MainSRpm_mean` | **5.55%** | +0.8380 |
| 4 | `wtc_AcWindSp_mean` | **4.22%** | +0.9344 |
| 5 | `wtc_PitcPosA_mean` | **3.06%** | -0.0942 |
| 6 | `wind_speed_cubed` | **1.87%** | +0.8129 |
| 7 | `gen_nacelle_temp_delta` | **0.98%** | +0.9187 |
| 8 | `wtc_Gen1U1Tm_mean` | **0.26%** | +0.8985 |
| 9 | `tip_speed_ratio` | **0.03%** | -0.3422 |
| 10 | `gear_ratio_proxy` | **0.01%** | -0.1514 |

### Physical Domain Significance:
1. **Aerodynamic Scaling (`wind_speed_cubed`, `aero_power_available_kw`):** Accounting for theoretical $v^3$ scaling provides direct physical leverage for non-linear regression models.
2. **Kinematic RPM (`wtc_GenRpm_mean`, `wtc_MainSRpm_mean`):** Operates as the premier mechanical proxy for rotor power capture in Region II.
3. **Blade Pitch Angle (`wtc_PitcPosA_mean`):** Critical for governing power saturation and feathering behavior in Region III.
4. **Air Density (`air_density_kgm3`):** Adjusts expected energy density based on sub-zero winter vs summer temperatures.
5. **Temporal Lag (`wind_speed_lag1`, `wind_speed_roll_mean_30m`):** Incorporates aerodynamic inertia and short-term atmospheric turbulence.

---

## 4. Model-Ready Datasets Generated
Model-ready datasets containing all 30 engineered features, normalized identifiers, and target `wtc_ActPower_mean` have been exported to [`data/model_ready/`](file:///c:/Pratik/MDM/project2/data/model_ready/):
- **`train_features_2025.parquet`**: Full annual 2025 baseline dataset (~1.06M records).
- **`test_features_2026.parquet`**: Holdout 2026 operational dataset (~361k records).

---

## 5. Artifacts Generated
- [`feature_dictionary.csv`](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/feature_dictionary.csv) — 30 selected features with definitions and engineering units.
- [`selected_features.csv`](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/selected_features.csv) — Candidate feature schema.
- [`excluded_features.csv`](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/excluded_features.csv) — Audit of excluded channels.
- [`feature_statistics.csv`](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/feature_statistics.csv) — Distributional statistics of engineered variables.
- [`leakage_check.csv`](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/leakage_check.csv) — Rigorous leakage prevention documentation.
- [`feature_importance_precheck.csv`](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/feature_importance_precheck.csv) — Importance rankings and linear correlations.
- [`figures/feature_distributions.png`](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/figures/feature_distributions.png)
- [`figures/feature_relationships.png`](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/figures/feature_relationships.png)
- [`logs/feature_engineering.log`](file:///c:/Pratik/MDM/project2/outputs/05_feature_engineering/logs/feature_engineering.log)

**Phase 5 Verdict: PASS**
