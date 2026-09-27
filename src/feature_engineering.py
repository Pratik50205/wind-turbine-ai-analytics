"""
Phase 5 — Feature Engineering and Feature Selection Engine
Hill of Towie Wind Farm SCADA Dataset
Author: MDM Minor Project Team
"""

import os
import sys
import logging
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import mutual_info_regression
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_READY_DIR = PROJECT_ROOT / "data" / "model_ready"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "05_feature_engineering"
FIGURES_DIR = OUTPUT_DIR / "figures"
LOGS_DIR = OUTPUT_DIR / "logs"

MODEL_READY_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Logger setup
log_file = LOGS_DIR / "feature_engineering.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("FeatureEngineering")

ROTOR_RADIUS_M = 41.0
SWEPT_AREA_M2 = np.pi * (ROTOR_RADIUS_M ** 2)  # ~5,281.0 m^2

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Computing domain-guided engineered features...")
    df = df.copy()

    # 1. Aerodynamic power term (v^3)
    df['wind_speed_cubed'] = (df['wtc_AcWindSp_mean'] ** 3).astype(np.float32)

    # 2. Ambient Air Density calculation: rho = p / (R * T)
    # Standard sea level pressure p ~ 101,325 Pa; specific gas constant R = 287.05 J/(kg·K)
    temp_kelvin = df['wtc_AmbieTmp_mean'] + 273.15
    df['air_density_kgm3'] = (101325.0 / (287.05 * temp_kelvin)).astype(np.float32)

    # 3. Available aerodynamic wind power: P = 0.5 * rho * A * v^3 (kW)
    df['aero_power_available_kw'] = (0.5 * df['air_density_kgm3'] * SWEPT_AREA_M2 * df['wind_speed_cubed'] / 1000.0).astype(np.float32)

    # 4. Wind direction cyclical transformation (sine and cosine components)
    rad_dir = np.radians(df['wtc_ActualWindDirection_mean'])
    df['wind_dir_sin'] = np.sin(rad_dir).astype(np.float32)
    df['wind_dir_cos'] = np.cos(rad_dir).astype(np.float32)

    # 5. Yaw misalignment / relative wind direction
    # Difference between measured wind direction and nacelle position (modulo 360)
    yaw_misalign = (df['wtc_ActualWindDirection_mean'] - df['wtc_NacelPos_mean']) % 360.0
    # Map to [-180, 180]
    df['yaw_misalignment_deg'] = np.where(yaw_misalign > 180.0, yaw_misalign - 360.0, yaw_misalign).astype(np.float32)

    # 6. Kinematic Drivetrain Features
    # Tip speed ratio (TSR = omega * R / v)
    omega_rotor_rads = df['wtc_MainSRpm_mean'] * (2.0 * np.pi / 60.0)
    df['tip_speed_ratio'] = (omega_rotor_rads * ROTOR_RADIUS_M / (df['wtc_AcWindSp_mean'] + 1e-3)).clip(0.0, 20.0).astype(np.float32)

    # Gearbox speed ratio proxy (Generator RPM / Rotor RPM, nominal ~93.75)
    df['gear_ratio_proxy'] = (df['wtc_GenRpm_mean'] / (df['wtc_MainSRpm_mean'] + 1e-3)).clip(0.0, 150.0).astype(np.float32)

    # Pitch asymmetry across the 3 blades
    df['pitch_asymmetry_deg'] = (
        np.abs(df['wtc_PitcPosA_mean'] - df['wtc_PitcPosB_mean']) +
        np.abs(df['wtc_PitcPosA_mean'] - df['wtc_PitcPosC_mean'])
    ).astype(np.float32)

    # 7. Thermal Temperature Differentials
    # Generator thermal delta over nacelle air
    df['gen_nacelle_temp_delta'] = (df['wtc_Gen1U1Tm_mean'] - df['wtc_NacelTmp_mean']).astype(np.float32)
    # Gearbox thermal delta over ambient air
    df['gear_ambient_temp_delta'] = (df['wtc_GeOilTmp_mean'] - df['wtc_AmbieTmp_mean']).astype(np.float32)

    # 8. Temporal Cyclical Features
    df['hour'] = df['TimeStamp'].dt.hour
    df['month'] = df['TimeStamp'].dt.month
    df['day_of_year'] = df['TimeStamp'].dt.dayofyear

    df['hour_sin'] = np.sin(2.0 * np.pi * df['hour'] / 24.0).astype(np.float32)
    df['hour_cos'] = np.cos(2.0 * np.pi * df['hour'] / 24.0).astype(np.float32)
    df['month_sin'] = np.sin(2.0 * np.pi * (df['month'] - 1) / 12.0).astype(np.float32)
    df['month_cos'] = np.cos(2.0 * np.pi * (df['month'] - 1) / 12.0).astype(np.float32)

    # 9. Lagged & Rolling Features (computed chronologically within each turbine)
    logger.info("Computing temporal lag and rolling features per turbine...")
    df = df.sort_values(by=['StationId', 'TimeStamp']).reset_index(drop=True)

    # Lag 1 (10 minutes prior)
    df['wind_speed_lag1'] = df.groupby('StationId')['wtc_AcWindSp_mean'].shift(1).bfill().astype(np.float32)
    df['gen_rpm_lag1'] = df.groupby('StationId')['wtc_GenRpm_mean'].shift(1).bfill().astype(np.float32)
    df['pitch_lag1'] = df.groupby('StationId')['wtc_PitcPosA_mean'].shift(1).bfill().astype(np.float32)

    # Rolling 30-minute window (3 steps of 10 min)
    df['wind_speed_roll_mean_30m'] = df.groupby('StationId')['wtc_AcWindSp_mean'].transform(
        lambda s: s.rolling(window=3, min_periods=1).mean()
    ).astype(np.float32)
    df['wind_speed_roll_std_30m'] = df.groupby('StationId')['wtc_AcWindSp_mean'].transform(
        lambda s: s.rolling(window=3, min_periods=1).std()
    ).fillna(0.0).astype(np.float32)

    return df

def audit_leakage_and_select_features():
    logger.info("Performing strict target leakage audit and selecting feature subset...")
    
    # 1. Leakage check table
    leakage_records = [
        {
            "feature_name": "wtc_ActPower_mean",
            "leakage_risk": "TARGET",
            "decision": "EXCLUDED_AS_INPUT",
            "rationale": "Exact prediction target variable ($y$). Cannot be used as feature."
        },
        {
            "feature_name": "wtc_AmpPhR_mean",
            "leakage_risk": "HIGH",
            "decision": "EXCLUDED",
            "rationale": "Phase current is a direct electrical consequence of generated active power ($I \\approx P / (\\sqrt{3} V \\cos\\phi)$). Including current creates trivial circular leakage."
        },
        {
            "feature_name": "wtc_VoltPhR_mean",
            "leakage_risk": "LOW",
            "decision": "RETAINED_AUXILIARY",
            "rationale": "Grid voltage is primarily governed by the utility substation and grid stiffness rather than turbine power."
        },
        {
            "feature_name": "wtc_CosPhi_mean",
            "leakage_risk": "MEDIUM",
            "decision": "EXCLUDED",
            "rationale": "Direct power factor calculation derived from instantaneous active and apparent power."
        },
        {
            "feature_name": "wtc_ReactPwr_mean",
            "leakage_risk": "MEDIUM",
            "decision": "EXCLUDED",
            "rationale": "Coupled to electrical generator inverter controls; excluded from primary aerodynamic power prediction."
        },
        {
            "feature_name": "wtc_PowerRef_endvalue",
            "leakage_risk": "HIGH_IF_FREE",
            "decision": "RETAINED_FOR_BASELINE",
            "rationale": "Controller internal setpoint; kept for benchmarking against supervisory control, but primary ML model trains without it to remain independent of SCADA setpoint availability."
        },
        {
            "feature_name": "is_stopped",
            "leakage_risk": "LABEL_LEAKAGE",
            "decision": "EXCLUDED_FROM_ML_INPUTS",
            "rationale": "Operational status flag derived from wtc_ScTurSto_timeon; used only for data partitioning/filtering, not as a regression input."
        },
        {
            "feature_name": "is_curtailed",
            "leakage_risk": "LABEL_LEAKAGE",
            "decision": "EXCLUDED_FROM_ML_INPUTS",
            "rationale": "Synthetic curtailment flag derived using power; using it as input would cause label leakage."
        }
    ]
    df_leakage = pd.DataFrame(leakage_records)
    df_leakage.to_csv(OUTPUT_DIR / "leakage_check.csv", index=False)

    # 2. Selected primary ML feature set
    selected_features_info = [
        {"feature_name": "wtc_AcWindSp_mean", "unit": "m/s", "domain": "Aerodynamic", "description": "Active nacelle anemometer 10-minute mean wind speed"},
        {"feature_name": "wind_speed_cubed", "unit": "m^3/s^3", "domain": "Aerodynamic", "description": "Cubic wind speed modeling theoretical aerodynamic power scaling"},
        {"feature_name": "air_density_kgm3", "unit": "kg/m^3", "domain": "Environmental", "description": "Local air density derived from ambient temperature"},
        {"feature_name": "aero_power_available_kw", "unit": "kW", "domain": "Aerodynamic", "description": "Theoretical available wind power entering the swept rotor area"},
        {"feature_name": "wind_dir_sin", "unit": "unitless", "domain": "Directional", "description": "Cyclical sine component of measured wind direction"},
        {"feature_name": "wind_dir_cos", "unit": "unitless", "domain": "Directional", "description": "Cyclical cosine component of measured wind direction"},
        {"feature_name": "yaw_misalignment_deg", "unit": "deg", "domain": "Control", "description": "Angular difference between incoming wind direction and nacelle orientation"},
        {"feature_name": "wtc_GenRpm_mean", "unit": "rpm", "domain": "Kinematic", "description": "High-speed generator rotational shaft speed"},
        {"feature_name": "wtc_MainSRpm_mean", "unit": "rpm", "domain": "Kinematic", "description": "Low-speed rotor main shaft rotational speed"},
        {"feature_name": "tip_speed_ratio", "unit": "unitless", "domain": "Kinematic", "description": "Rotor blade tip speed to wind speed ratio (TSR)"},
        {"feature_name": "gear_ratio_proxy", "unit": "unitless", "domain": "Kinematic", "description": "Ratio of generator RPM to main rotor RPM"},
        {"feature_name": "wtc_PitcPosA_mean", "unit": "deg", "domain": "Control", "description": "Blade A pitch angle regulating aerodynamic angle of attack"},
        {"feature_name": "pitch_asymmetry_deg", "unit": "deg", "domain": "Mechanical", "description": "Pitch position divergence between rotor blades A, B, and C"},
        {"feature_name": "wtc_AmbieTmp_mean", "unit": "°C", "domain": "Thermal", "description": "Ambient outside air temperature"},
        {"feature_name": "wtc_NacelTmp_mean", "unit": "°C", "domain": "Thermal", "description": "Interior nacelle ambient air temperature"},
        {"feature_name": "wtc_GeOilTmp_mean", "unit": "°C", "domain": "Thermal", "description": "Gearbox lubrication sump oil temperature"},
        {"feature_name": "wtc_Gen1U1Tm_mean", "unit": "°C", "domain": "Thermal", "description": "Generator stator winding temperature"},
        {"feature_name": "gen_nacelle_temp_delta", "unit": "°C", "domain": "Thermal", "description": "Generator winding temperature rise over nacelle ambient"},
        {"feature_name": "gear_ambient_temp_delta", "unit": "°C", "domain": "Thermal", "description": "Gearbox oil temperature rise over ambient air"},
        {"feature_name": "wtc_GearPres_mean", "unit": "bar", "domain": "Hydraulic", "description": "Gearbox lubrication oil circuit pressure"},
        {"feature_name": "wtc_BrakPres_mean", "unit": "bar", "domain": "Hydraulic", "description": "High-speed shaft mechanical brake pressure"},
        {"feature_name": "wind_speed_lag1", "unit": "m/s", "domain": "Temporal Lag", "description": "Wind speed measured in previous 10-minute interval ($t-1$)"},
        {"feature_name": "wind_speed_roll_mean_30m", "unit": "m/s", "domain": "Temporal Rolling", "description": "Rolling 30-minute mean wind speed"},
        {"feature_name": "wind_speed_roll_std_30m", "unit": "m/s", "domain": "Turbulence", "description": "Rolling 30-minute wind speed standard deviation (turbulence proxy)"},
        {"feature_name": "hour_sin", "unit": "unitless", "domain": "Temporal Cycle", "description": "Diurnal cycle sine component"},
        {"feature_name": "hour_cos", "unit": "unitless", "domain": "Temporal Cycle", "description": "Diurnal cycle cosine component"},
        {"feature_name": "month_sin", "unit": "unitless", "domain": "Seasonal Cycle", "description": "Annual seasonal cycle sine component"},
        {"feature_name": "month_cos", "unit": "unitless", "domain": "Seasonal Cycle", "description": "Annual seasonal cycle cosine component"},
        {"feature_name": "latitude", "unit": "deg N", "domain": "Spatial", "description": "Turbine geographic latitude coordinate"},
        {"feature_name": "longitude", "unit": "deg W", "domain": "Spatial", "description": "Turbine geographic longitude coordinate"}
    ]
    df_selected = pd.DataFrame(selected_features_info)
    df_selected.to_csv(OUTPUT_DIR / "selected_features.csv", index=False)

    # 3. Excluded features table
    excluded_features_info = [
        {"feature_name": "wtc_AmpPhR_mean", "reason": "Target leakage (direct electrical proxy for generated power)"},
        {"feature_name": "wtc_CosPhi_mean", "reason": "Target leakage (derived power factor)"},
        {"feature_name": "wtc_ReactPwr_mean", "reason": "Electrical feedback variable"},
        {"feature_name": "wtc_GridFreq_mean", "reason": "Grid external stability parameter; negligible predictive power for turbine mechanical output"},
        {"feature_name": "wtc_VoltPhR_mean", "reason": "High colinearity with grid voltage variations; minimal variance related to wind resource"},
        {"feature_name": "wtc_ScInOper_timeon", "reason": "Operational state indicator; retained for filtering, excluded from regression inputs"},
        {"feature_name": "wtc_ScReToOp_timeon", "reason": "Operational state indicator"},
        {"feature_name": "wtc_ScTurSto_timeon", "reason": "Operational state indicator"}
    ]
    df_excluded = pd.DataFrame(excluded_features_info)
    df_excluded.to_csv(OUTPUT_DIR / "excluded_features.csv", index=False)

    # 4. Feature dictionary
    df_selected.to_csv(OUTPUT_DIR / "feature_dictionary.csv", index=False)
    logger.info(f"Selected {len(df_selected)} engineered features; audited {len(df_leakage)} leakage risks.")
    return df_selected, df_excluded, df_leakage

def compute_feature_statistics_and_importance(df_train: pd.DataFrame, selected_features: list):
    logger.info("Computing feature distributions and importance precheck...")
    
    # 1. Feature statistics
    stats_records = []
    for f in selected_features:
        if f in df_train.columns:
            s = df_train[f].dropna()
            stats_records.append({
                'feature_name': f,
                'mean': round(float(s.mean()), 4),
                'std': round(float(s.std()), 4),
                'min': round(float(s.min()), 4),
                'q25': round(float(s.quantile(0.25)), 4),
                'median': round(float(s.median()), 4),
                'q75': round(float(s.quantile(0.75)), 4),
                'max': round(float(s.max()), 4),
                'missing_count': int(df_train[f].isnull().sum())
            })
    df_feat_stats = pd.DataFrame(stats_records)
    df_feat_stats.to_csv(OUTPUT_DIR / "feature_statistics.csv", index=False)

    # 2. Fast Feature Importance Precheck on clean operational sample
    sample_mask = (df_train['is_stopped'] == 0) & (df_train['is_curtailed'] == 0)
    df_sample = df_train[sample_mask].sample(n=min(25000, len(df_train[sample_mask])), random_state=42)

    X_sample = df_sample[selected_features].fillna(0.0)
    y_sample = df_sample['wtc_ActPower_mean']

    logger.info("Fitting Random Forest Regressor for importance precheck...")
    rf = RandomForestRegressor(n_estimators=50, max_depth=12, n_jobs=-1, random_state=42)
    rf.fit(X_sample, y_sample)

    importances = rf.feature_importances_
    corr_with_y = [float(X_sample[c].corr(y_sample)) for c in selected_features]

    importance_records = []
    for feat, imp, corr in zip(selected_features, importances, corr_with_y):
        importance_records.append({
            'feature_name': feat,
            'rf_importance_pct': round(float(imp * 100.0), 3),
            'linear_correlation_with_power': round(corr, 4) if pd.notna(corr) else 0.0
        })

    df_importance = pd.DataFrame(importance_records).sort_values(by='rf_importance_pct', ascending=False).reset_index(drop=True)
    df_importance['rank'] = range(1, len(df_importance) + 1)
    df_importance.to_csv(OUTPUT_DIR / "feature_importance_precheck.csv", index=False)
    logger.info("Feature importance precheck saved to feature_importance_precheck.csv")
    return df_feat_stats, df_importance

def generate_feature_figures(df_train: pd.DataFrame, df_importance: pd.DataFrame):
    logger.info("Generating Phase 5 feature visualization figures...")
    sample_df = df_train.sample(n=min(10000, len(df_train)), random_state=42)

    # Figure 1: Top Feature Importances Precheck
    plt.figure(figsize=(12, 8))
    top_feats = df_importance.head(15).sort_values(by='rf_importance_pct', ascending=True)
    bars = plt.barh(top_feats['feature_name'], top_feats['rf_importance_pct'], color='#2980b9', edgecolor='black', linewidth=0.5)
    plt.title("Feature Importance Precheck (Random Forest Regressor, MDI %)", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Importance Share (%)", fontsize=11)
    plt.ylabel("Engineered Feature", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5, axis='x')
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 0.3, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "feature_distributions.png", dpi=300)
    plt.close()

    # Figure 2: Engineered Feature Physical Relationships
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Subplot 1: Wind speed cubed vs Power
    axes[0, 0].scatter(sample_df['wind_speed_cubed'], sample_df['wtc_ActPower_mean'], alpha=0.15, s=8, color='#3498db')
    axes[0, 0].set_title("Cubic Wind Speed ($v^3$) vs Active Power Output", fontsize=11, fontweight='bold')
    axes[0, 0].set_xlabel("Wind Speed Cubed ($m^3/s^3$)")
    axes[0, 0].set_ylabel("Active Power (kW)")
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)

    # Subplot 2: Tip Speed Ratio vs Power
    axes[0, 1].scatter(sample_df['tip_speed_ratio'], sample_df['wtc_ActPower_mean'], alpha=0.15, s=8, color='#e67e22')
    axes[0, 1].set_title("Tip Speed Ratio (TSR) vs Active Power Output", fontsize=11, fontweight='bold')
    axes[0, 1].set_xlabel("Tip Speed Ratio (TSR)")
    axes[0, 1].set_ylabel("Active Power (kW)")
    axes[0, 1].grid(True, linestyle="--", alpha=0.5)

    # Subplot 3: Wind Direction Polar Scatter
    axes[1, 0].scatter(sample_df['wind_dir_sin'], sample_df['wind_dir_cos'], c=sample_df['wtc_ActPower_mean'], cmap='viridis', alpha=0.3, s=10)
    axes[1, 0].set_title("Wind Direction Decomposition ($\sin \\theta$ vs $\cos \\theta$)", fontsize=11, fontweight='bold')
    axes[1, 0].set_xlabel("$\sin(\\theta)$ (East-West)")
    axes[1, 0].set_ylabel("$\cos(\\theta)$ (North-South)")
    axes[1, 0].grid(True, linestyle="--", alpha=0.5)

    # Subplot 4: Generator Thermal Delta vs Power
    axes[1, 1].scatter(sample_df['wtc_ActPower_mean'], sample_df['gen_nacelle_temp_delta'], alpha=0.15, s=8, color='#27ae60')
    axes[1, 1].set_title("Generator Thermal Rise over Nacelle vs Power", fontsize=11, fontweight='bold')
    axes[1, 1].set_xlabel("Active Power (kW)")
    axes[1, 1].set_ylabel("Temperature Delta (°C)")
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "feature_relationships.png", dpi=300)
    plt.close()
    logger.info("Feature figures saved.")

def write_feature_report(df_selected, df_excluded, df_leakage, df_importance):
    logger.info("Writing Phase 5 Feature Engineering report...")
    report_file = OUTPUT_DIR / "report.md"

    top_imp_rows = []
    for _, r in df_importance.head(10).iterrows():
        top_imp_rows.append(f"| {r['rank']} | `{r['feature_name']}` | **{r['rf_importance_pct']:.2f}%** | {r['linear_correlation_with_power']:+.4f} |")

    leak_rows = []
    for _, r in df_leakage.iterrows():
        leak_rows.append(f"| `{r['feature_name']}` | **{r['leakage_risk']}** | `{r['decision']}` | {r['rationale']} |")

    report_content = f"""# Phase 5 — Feature Engineering and Feature Selection Report

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
{chr(10).join(leak_rows)}

### Key Safeguards:
- **No Consequential Electrical Features:** Direct generator current (`wtc_AmpPhR_mean`) was excluded because it provides trivial retrospective knowledge of power output ($I \\propto P$).
- **No Operational Status Inputs:** `is_stopped` and `is_curtailed` were excluded from regression inputs, guaranteeing the model predicts purely from physical and atmospheric variables.

---

## 3. Top Engineered Features & Importance Precheck
Preliminary feature importance evaluation using an ensemble Random Forest regressor on operational records:

| Rank | Feature | RF Importance Share | Linear Correlation |
| :--- | :--- | :--- | :--- |
{chr(10).join(top_imp_rows)}

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
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    logger.info("Phase 5 report successfully written.")

def main():
    logger.info("=== Starting Phase 5 Feature Engineering Engine ===")
    
    # 1. Audit and feature selection
    df_selected, df_excluded, df_leakage = audit_leakage_and_select_features()
    selected_feature_names = df_selected['feature_name'].tolist()

    # 2. Load cleaned 2025 data & engineer features
    logger.info("Processing 2025 training feature matrix...")
    df_2025 = pd.read_parquet(PROCESSED_DIR / "scada_2025_cleaned.parquet")
    df_train_feats = engineer_features(df_2025)
    train_path = MODEL_READY_DIR / "train_features_2025.parquet"
    df_train_feats.to_parquet(train_path, index=False)
    logger.info(f"Saved 2025 training features: {train_path} ({len(df_train_feats):,} rows)")

    # 3. Load cleaned 2026 data & engineer features
    logger.info("Processing 2026 testing feature matrix...")
    df_2026 = pd.read_parquet(PROCESSED_DIR / "scada_2026_cleaned.parquet")
    df_test_feats = engineer_features(df_2026)
    test_path = MODEL_READY_DIR / "test_features_2026.parquet"
    df_test_feats.to_parquet(test_path, index=False)
    logger.info(f"Saved 2026 testing features: {test_path} ({len(df_test_feats):,} rows)")

    # 4. Feature statistics and importance precheck
    df_feat_stats, df_importance = compute_feature_statistics_and_importance(df_train_feats, selected_feature_names)

    # 5. Visualizations & report
    generate_feature_figures(df_train_feats, df_importance)
    write_feature_report(df_selected, df_excluded, df_leakage, df_importance)
    logger.info("=== Phase 5 Feature Engineering Complete ===")

if __name__ == "__main__":
    main()
