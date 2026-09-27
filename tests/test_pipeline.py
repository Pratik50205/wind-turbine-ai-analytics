"""
Unit Tests for Phase 12 & 13 — Integration & Final Reporting
"""

from pathlib import Path
import pandas as pd
import json
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_integration_outputs():
    p12_dir = PROJECT_ROOT / "outputs" / "12_final_integration"
    assert (p12_dir / "phase_status.csv").exists(), "Missing phase_status.csv"
    assert (p12_dir / "final_dataset_manifest.csv").exists(), "Missing final_dataset_manifest.csv"
    assert (p12_dir / "artifact_manifest.csv").exists(), "Missing artifact_manifest.csv"
    assert (p12_dir / "pipeline_execution_summary.json").exists(), "Missing pipeline_execution_summary.json"
    assert (p12_dir / "figures" / "final_system_flow.png").exists(), "Missing final_system_flow.png"

def test_phase_status_all_completed():
    p12_dir = PROJECT_ROOT / "outputs" / "12_final_integration"
    df = pd.read_csv(p12_dir / "phase_status.csv")
    assert len(df) >= 12, f"Expected at least 12 phases, found {len(df)}"
    assert (df["status"] == "COMPLETED").all(), "Not all phases are marked COMPLETED"

def test_final_report_artifacts():
    p13_dir = PROJECT_ROOT / "outputs" / "13_final_report"
    assert (p13_dir / "FINAL_PROJECT_REPORT.md").exists(), "Missing FINAL_PROJECT_REPORT.md"
    assert (p13_dir / "FINAL_PROJECT_REPORT.pdf").exists(), "Missing FINAL_PROJECT_REPORT.pdf"
    assert (p13_dir / "executive_summary.md").exists(), "Missing executive_summary.md"
    assert (p13_dir / "final_metrics.csv").exists(), "Missing final_metrics.csv"
    assert (p13_dir / "model_card.md").exists(), "Missing model_card.md"
    assert (p13_dir / "data_card.md").exists(), "Missing data_card.md"
    assert (p13_dir / "limitations.md").exists(), "Missing limitations.md"
    assert (p13_dir / "reproducibility_check.md").exists(), "Missing reproducibility_check.md"

def test_documentation_cards():
    docs_dir = PROJECT_ROOT / "docs"
    assert (docs_dir / "MODEL_CARD.md").exists(), "Missing docs/MODEL_CARD.md"
    assert (docs_dir / "DATA_CARD.md").exists(), "Missing docs/DATA_CARD.md"
    assert (docs_dir / "DATA_DICTIONARY.md").exists(), "Missing docs/DATA_DICTIONARY.md"
    assert (docs_dir / "LIMITATIONS.md").exists(), "Missing docs/LIMITATIONS.md"
    assert (docs_dir / "DASHBOARD_GUIDE.md").exists(), "Missing docs/DASHBOARD_GUIDE.md"
    assert (docs_dir / "REPRODUCIBILITY.md").exists(), "Missing docs/REPRODUCIBILITY.md"
