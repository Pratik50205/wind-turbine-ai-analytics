"""
Unit Tests for Phase 10 — Historical SCADA Replay Engine
"""

from pathlib import Path
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_replay_outputs_exist():
    p10_dir = PROJECT_ROOT / "outputs" / "10_replay_processing"
    assert (p10_dir / "processing_latency.csv").exists() or (p10_dir / "replay_performance_metrics.csv").exists(), "Missing latency csv"
    assert (p10_dir / "replay_sample_output.csv").exists(), "Missing replay_sample_output.csv"

def test_replay_performance_metrics():
    p10_dir = PROJECT_ROOT / "outputs" / "10_replay_processing"
    csv_file = (p10_dir / "processing_latency.csv") if (p10_dir / "processing_latency.csv").exists() else (p10_dir / "replay_performance_metrics.csv")
    df = pd.read_csv(csv_file)
    assert not df.empty, "Latency metric csv is empty"

    mean_latency = df.iloc[0]["mean_latency_ms"]
    throughput_col = "throughput_steps_per_second" if "throughput_steps_per_second" in df.columns else "throughput_steps_per_sec"
    throughput = df.iloc[0][throughput_col]

    assert mean_latency < 100.0, f"Replay mean latency too high: {mean_latency} ms"
    assert throughput > 20.0, f"Replay throughput too low: {throughput} steps/s"

def test_replay_sample_records():
    p10_dir = PROJECT_ROOT / "outputs" / "10_replay_processing"
    df = pd.read_csv(p10_dir / "replay_sample_output.csv")
    assert len(df) >= 100, f"Expected at least 100 sample records, found {len(df)}"

    required_cols = ["timestamp", "turbine_id", "wind_speed_ms", "actual_power_kw", "predicted_power_kw", "realtime_alert"]
    for col in required_cols:
        assert col in df.columns, f"Missing required column in replay sample: {col}"
