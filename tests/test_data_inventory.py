"""
Unit Tests for Phase 0 and Phase 1 Validation and Data Inventory
"""

from pathlib import Path
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_phase0_artifacts_exist():
    out0 = PROJECT_ROOT / "outputs" / "00_project_validation"
    assert out0.exists(), "Phase 0 output directory missing"
    
    required_files = [
        "environment_report.md",
        "environment.json",
        "installed_packages.txt",
        "dataset_files_manifest.csv",
        "configuration_snapshot.yaml",
        "validation_log.txt"
    ]
    for rf in required_files:
        p = out0 / rf
        assert p.exists() and p.stat().st_size > 0, f"Phase 0 artifact {rf} is missing or empty"

def test_phase0_manifest_content():
    manifest_f = PROJECT_ROOT / "outputs" / "00_project_validation" / "dataset_files_manifest.csv"
    df = pd.read_csv(manifest_f)
    assert len(df) >= 200, f"Expected at least 200 dataset files, found {len(df)}"
    assert "relative_path" in df.columns
    assert "size_mb" in df.columns
    assert df["size_mb"].sum() > 5000, "Dataset manifest volume should be > 5 GB"

def test_phase1_artifacts_exist():
    out1 = PROJECT_ROOT / "outputs" / "01_data_inventory"
    assert out1.exists(), "Phase 1 output directory missing"

    required_files = [
        "report.md",
        "schema_inventory.csv",
        "table_inventory.csv",
        "field_inventory.csv",
        "timestamp_coverage.csv",
        "turbine_coverage.csv",
        "missingness_overview.csv",
        "candidate_features.csv",
        "candidate_target.csv",
        "source_document_crosscheck.csv",
        "figures/data_coverage.png",
        "figures/missingness_overview.png",
        "logs/inventory.log"
    ]
    for rf in required_files:
        p = out1 / rf
        assert p.exists() and p.stat().st_size > 0, f"Phase 1 artifact {rf} is missing or empty"

    # Also check docs/DATA_DICTIONARY.md
    dict_f = PROJECT_ROOT / "docs" / "DATA_DICTIONARY.md"
    assert dict_f.exists() and dict_f.stat().st_size > 0, "DATA_DICTIONARY.md missing or empty"

def test_candidate_target_validity():
    target_f = PROJECT_ROOT / "outputs" / "01_data_inventory" / "candidate_target.csv"
    df = pd.read_csv(target_f)
    assert not df.empty
    row = df.iloc[0]
    assert row["candidate_target"] == "wtc_ActPower_mean"
    assert row["engineering_unit"] == "kW"
    assert row["rated_turbine_power_kw"] == 2300.0
    assert row["selection_verdict"] == "CONFIRMED_PRIMARY_TARGET"

def test_turbine_coverage_count():
    cov_f = PROJECT_ROOT / "outputs" / "01_data_inventory" / "turbine_coverage.csv"
    df = pd.read_csv(cov_f)
    assert len(df) == 21, f"Expected 21 turbines, found {len(df)}"
    assert set(df["turbine_name"]) == {f"T{i:02d}" for i in range(1, 22)}
    assert df["rated_power_kw"].iloc[0] == 2300.0

def test_candidate_features():
    feat_f = PROJECT_ROOT / "outputs" / "01_data_inventory" / "candidate_features.csv"
    df = pd.read_csv(feat_f)
    assert not df.empty
    feature_names = set(df["feature_name"])
    assert "wtc_AcWindSp_mean" in feature_names
    assert "wtc_GenRpm_mean" in feature_names
    assert "wtc_PitcPosA_mean" in feature_names
    assert "wtc_AmbieTmp_mean" in feature_names
