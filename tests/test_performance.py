"""
Unit Tests for Phase 4 Turbine Performance Analysis
"""

from pathlib import Path
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_phase4_artifacts_exist():
    out4 = PROJECT_ROOT / "outputs" / "04_performance_analysis"
    assert out4.exists(), "Phase 4 output directory missing"

    required_files = [
        "report.md",
        "performance_metrics.csv",
        "turbine_performance.csv",
        "wind_bin_performance.csv",
        "power_curve_data.csv",
        "deviation_analysis.csv",
        "downtime_summary.csv",
        "figures/empirical_power_curve.png",
        "figures/actual_vs_reference.png",
        "figures/turbine_performance_comparison.png",
        "figures/performance_by_wind_bin.png",
        "figures/performance_deviation_time_series.png",
        "logs/performance_analysis.log"
    ]
    for rf in required_files:
        p = out4 / rf
        assert p.exists() and p.stat().st_size > 0, f"Phase 4 artifact {rf} is missing or empty"

def test_farm_performance_metrics():
    metrics_f = PROJECT_ROOT / "outputs" / "04_performance_analysis" / "performance_metrics.csv"
    df = pd.read_csv(metrics_f)
    assert not df.empty
    row = df.iloc[0]
    assert row["turbines_count"] == 21
    assert row["total_annual_generation_gwh"] > 80.0  # Actual measured ~96.96 GWh
    assert row["farm_capacity_factor_pct"] > 20.0

def test_turbine_performance_ranking():
    turb_f = PROJECT_ROOT / "outputs" / "04_performance_analysis" / "turbine_performance.csv"
    df = pd.read_csv(turb_f)
    assert len(df) == 21
    assert "farm_rank" in df.columns
    assert df["farm_rank"].tolist() == list(range(1, 22))
    assert (df["technical_availability_pct"] >= 95.0).all()

def test_power_curve_cp():
    pc_f = PROJECT_ROOT / "outputs" / "04_performance_analysis" / "power_curve_data.csv"
    df = pd.read_csv(pc_f)
    assert not df.empty
    assert (df["power_coefficient_cp"] <= 0.593).all(), "Cp cannot exceed Betz limit"
    assert (df["power_coefficient_cp"] >= 0.0).all()
