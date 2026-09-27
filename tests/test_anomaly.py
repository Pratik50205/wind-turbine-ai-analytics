"""
Unit Tests for Phase 8 Abnormal Behavior and Anomaly Detection
"""

from pathlib import Path
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_phase8_artifacts_exist():
    out8 = PROJECT_ROOT / "outputs" / "08_anomaly_detection"
    assert out8.exists()

    required_files = [
        "report.md",
        "anomaly_methodology.md",
        "threshold_analysis.csv",
        "anomaly_results.parquet",
        "anomaly_summary.csv",
        "anomaly_by_turbine.csv",
        "anomaly_events.csv",
        "residual_statistics.csv",
        "figures/residual_distribution.png",
        "figures/residual_threshold.png",
        "figures/anomaly_timeline.png",
        "figures/anomaly_frequency_by_turbine.png",
        "figures/representative_events/spotlight_event.png",
        "logs/anomaly_detection.log"
    ]
    for rf in required_files:
        p = out8 / rf
        assert p.exists() and p.stat().st_size > 0, f"Phase 8 artifact {rf} is missing or empty"

    assert (PROJECT_ROOT / "docs" / "ANOMALY_METHODOLOGY.md").exists()

def test_anomaly_classification_structure():
    summary_f = PROJECT_ROOT / "outputs" / "08_anomaly_detection" / "anomaly_summary.csv"
    df = pd.read_csv(summary_f)
    assert not df.empty
    statuses = set(df["operational_status"])
    assert "normal" in statuses
    assert "abnormal_behavior" in statuses
    assert "curtailed_operation" in statuses
    assert "shutdown_associated" in statuses

    # Normal should be majority (> 80%)
    normal_share = df[df["operational_status"] == "normal"]["percentage"].iloc[0]
    assert normal_share > 80.0

def test_anomaly_event_persistence_rule():
    events_f = PROJECT_ROOT / "outputs" / "08_anomaly_detection" / "anomaly_events.csv"
    df = pd.read_csv(events_f)
    if not df.empty:
        assert (df["duration_minutes"] >= 30).all(), "All persistent events must be >= 30 minutes"
        assert (df["observations_count"] >= 3).all()
