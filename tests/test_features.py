"""
Unit Tests for Phase 5 Feature Engineering and Selection
"""

from pathlib import Path
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_phase5_artifacts_exist():
    out5 = PROJECT_ROOT / "outputs" / "05_feature_engineering"
    assert out5.exists(), "Phase 5 output directory missing"

    required_files = [
        "report.md",
        "feature_dictionary.csv",
        "selected_features.csv",
        "excluded_features.csv",
        "feature_statistics.csv",
        "leakage_check.csv",
        "feature_importance_precheck.csv",
        "figures/feature_distributions.png",
        "figures/feature_relationships.png",
        "logs/feature_engineering.log"
    ]
    for rf in required_files:
        p = out5 / rf
        assert p.exists() and p.stat().st_size > 0, f"Phase 5 artifact {rf} is missing or empty"

def test_model_ready_data_exists():
    mr_dir = PROJECT_ROOT / "data" / "model_ready"
    assert (mr_dir / "train_features_2025.parquet").exists()
    assert (mr_dir / "test_features_2026.parquet").exists()

def test_leakage_audit_rigor():
    leak_f = PROJECT_ROOT / "outputs" / "05_feature_engineering" / "leakage_check.csv"
    df_leak = pd.read_csv(leak_f)
    assert not df_leak.empty

    # Phase current must be excluded
    current_check = df_leak[df_leak["feature_name"] == "wtc_AmpPhR_mean"].iloc[0]
    assert current_check["decision"] == "EXCLUDED"
    assert current_check["leakage_risk"] == "HIGH"

    # Selected features cannot include target or current
    sel_f = PROJECT_ROOT / "outputs" / "05_feature_engineering" / "selected_features.csv"
    df_sel = pd.read_csv(sel_f)
    selected_names = set(df_sel["feature_name"])
    assert "wtc_ActPower_mean" not in selected_names
    assert "wtc_AmpPhR_mean" not in selected_names

def test_engineered_feature_values():
    stat_f = PROJECT_ROOT / "outputs" / "05_feature_engineering" / "feature_statistics.csv"
    df_stat = pd.read_csv(stat_f).set_index("feature_name")

    # Air density must be physically realistic (~1.2 kg/m^3)
    assert 1.15 <= df_stat.loc["air_density_kgm3", "mean"] <= 1.30

    # Wind speed cubed must be positive
    assert df_stat.loc["wind_speed_cubed", "min"] >= 0.0

    # Wind direction sine and cosine must be within [-1, 1]
    assert -1.0 <= df_stat.loc["wind_dir_sin", "min"] <= 1.0
    assert -1.0 <= df_stat.loc["wind_dir_cos", "max"] <= 1.0
