"""
Unit Tests for Phase 11 — Decision Support Dashboard
"""

from pathlib import Path
import pandas as pd
import pytest

from src.dashboard.data_service import data_service
from src.dashboard.layout import (
    build_executive_tab,
    build_turbine_tab,
    build_prediction_tab,
    build_anomaly_tab,
    build_environmental_tab,
    build_events_tab,
    build_replay_tab
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_data_service_kpis():
    kpis = data_service.get_kpis()
    assert kpis["total_generation_gwh"] > 50.0, "Total generation should be > 50 GWh"
    assert 15.0 < kpis["fleet_capacity_factor"] < 40.0, "Capacity factor should be realistic (15-40%)"
    assert kpis["fleet_availability"] > 90.0, "Technical availability should be > 90%"
    assert kpis["turbines_count"] == 21, "Turbines count must be 21"
    assert kpis["model_r2_score"] > 0.95, "Model R2 score must exceed 0.95"
    assert kpis["model_nrmse_pct"] < 5.0, "Normalized RMSE must be below 5%"

def test_all_seven_tab_layouts():
    t1 = build_executive_tab()
    t2 = build_turbine_tab()
    t3 = build_prediction_tab()
    t4 = build_anomaly_tab()
    t5 = build_environmental_tab()
    t6 = build_events_tab()
    t7 = build_replay_tab()

    assert t1 is not None
    assert t2 is not None
    assert t3 is not None
    assert t4 is not None
    assert t5 is not None
    assert t6 is not None
    assert t7 is not None

def test_dashboard_artifacts_exist():
    p11_dir = PROJECT_ROOT / "outputs" / "11_dashboard"
    assert (p11_dir / "dashboard_kpi_results.csv").exists(), "Missing dashboard_kpi_results.csv"
    assert (p11_dir / "dashboard_data_dictionary.csv").exists(), "Missing dashboard_data_dictionary.csv"
    assert (p11_dir / "dashboard_refresh_manifest.json").exists(), "Missing dashboard_refresh_manifest.json"
    assert (p11_dir / "preview" / "final_dashboard_preview.png").exists(), "Missing final_dashboard_preview.png"

def test_dashboard_screenshots_complete():
    screen_dir = PROJECT_ROOT / "outputs" / "11_dashboard" / "screenshots"
    expected = [
        "01_executive_overview.png",
        "02_turbine_performance.png",
        "03_power_prediction.png",
        "04_abnormal_behavior.png",
        "05_environmental_analysis.png",
        "06_events.png",
        "07_realtime_replay.png"
    ]
    for s in expected:
        f = screen_dir / s
        assert f.exists(), f"Missing screenshot {s}"
        assert f.stat().st_size > 10000, f"Screenshot {s} is suspiciously small ({f.stat().st_size} bytes)"
