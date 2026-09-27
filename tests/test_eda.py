"""
Unit Tests for Phase 3 Exploratory Data Analysis (EDA)
"""

from pathlib import Path
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_phase3_artifacts_exist():
    out3 = PROJECT_ROOT / "outputs" / "03_eda"
    assert out3.exists(), "Phase 3 output directory missing"

    required_files = [
        "report.md",
        "descriptive_statistics.csv",
        "correlation_matrix.csv",
        "turbine_summary.csv",
        "operating_state_summary.csv",
        "power_distribution.csv",
        "relationship_summary.csv",
        "figures/power_distribution.png",
        "figures/wind_speed_distribution.png",
        "figures/correlation_heatmap.png",
        "figures/wind_speed_vs_power.png",
        "figures/power_time_series.png",
        "figures/turbine_comparison.png",
        "figures/additional_relationships/pitch_vs_wind.png",
        "figures/additional_relationships/gen_rpm_vs_power.png",
        "figures/additional_relationships/temperature_vs_power.png",
        "figures/additional_relationships/gear_oil_temp_vs_power.png",
        "logs/eda.log"
    ]
    for rf in required_files:
        p = out3 / rf
        assert p.exists() and p.stat().st_size > 0, f"Phase 3 artifact {rf} is missing or empty"

def test_descriptive_statistics_content():
    stats_f = PROJECT_ROOT / "outputs" / "03_eda" / "descriptive_statistics.csv"
    df = pd.read_csv(stats_f)
    assert not df.empty
    vars_present = set(df["variable"])
    assert "wtc_ActPower_mean" in vars_present
    assert "wtc_AcWindSp_mean" in vars_present
    assert "wtc_GenRpm_mean" in vars_present

    power_row = df[df["variable"] == "wtc_ActPower_mean"].iloc[0]
    assert power_row["max"] <= 2450.0
    assert power_row["min"] >= -50.0

def test_turbine_summary_content():
    turb_f = PROJECT_ROOT / "outputs" / "03_eda" / "turbine_summary.csv"
    df = pd.read_csv(turb_f)
    assert len(df) == 21, f"Expected 21 turbines, found {len(df)}"
    assert (df["capacity_factor_pct"] >= 15.0).all(), "All turbines should have CF >= 15%"
    assert (df["capacity_factor_pct"] <= 35.0).all(), "All turbines should have CF <= 35%"

def test_power_curve_monotonicity():
    pc_f = PROJECT_ROOT / "outputs" / "03_eda" / "power_distribution.csv"
    df = pd.read_csv(pc_f).dropna(subset=["mean_power_kw"])
    # In Region II (4 to 10 m/s), power should increase with wind speed
    region_2 = df[(df["wind_speed_midpoint"] >= 4.0) & (df["wind_speed_midpoint"] <= 10.0)]
    assert region_2["mean_power_kw"].is_monotonic_increasing, "Power curve should be increasing in Region II"
