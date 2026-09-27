"""
Unit Tests for Phase 2 Data Preprocessing and Quality Engine
"""

from pathlib import Path
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_phase2_artifacts_exist():
    out2 = PROJECT_ROOT / "outputs" / "02_data_preprocessing"
    assert out2.exists(), "Phase 2 output directory missing"

    required_files = [
        "report.md",
        "preprocessing_summary.json",
        "row_counts_before_after.csv",
        "missing_values_before.csv",
        "missing_values_after.csv",
        "duplicates_report.csv",
        "invalid_values_report.csv",
        "outlier_review.csv",
        "transformations.csv",
        "cleaned_sample.csv",
        "data_quality_scorecard.csv",
        "figures/missingness_before.png",
        "figures/missingness_after.png",
        "figures/distributions_before.png",
        "figures/distributions_after.png",
        "figures/cleaning_impact.png",
        "logs/preprocessing.log"
    ]
    for rf in required_files:
        p = out2 / rf
        assert p.exists() and p.stat().st_size > 0, f"Phase 2 artifact {rf} is missing or empty"

def test_processed_parquet_files_exist():
    proc_dir = PROJECT_ROOT / "data" / "processed"
    assert (proc_dir / "scada_2025_cleaned.parquet").exists()
    assert (proc_dir / "scada_2026_cleaned.parquet").exists()
    assert (proc_dir / "alarms_cleaned.parquet").exists()

def test_processed_data_integrity():
    df_sample = pd.read_csv(PROJECT_ROOT / "outputs" / "02_data_preprocessing" / "cleaned_sample.csv")
    assert len(df_sample) >= 5000, "Cleaned sample should have at least 5000 rows"

    # Check key columns exist
    assert "wtc_ActPower_mean" in df_sample.columns
    assert "wtc_AcWindSp_mean" in df_sample.columns
    assert "wtc_GenRpm_mean" in df_sample.columns
    assert "turbine_name" in df_sample.columns
    assert "is_curtailed" in df_sample.columns
    assert "is_aux_consumption" in df_sample.columns

    # Check physical constraints
    assert df_sample["wtc_ActPower_mean"].min() >= -50.0
    assert df_sample["wtc_ActPower_mean"].max() <= 2450.0
    assert df_sample["wtc_AcWindSp_mean"].min() >= 0.0
    assert df_sample["wtc_AcWindSp_mean"].max() <= 35.0

    # No nulls in key predictors
    assert df_sample["wtc_ActPower_mean"].isnull().sum() == 0
    assert df_sample["wtc_AcWindSp_mean"].isnull().sum() == 0

def test_data_quality_scorecard():
    score_f = PROJECT_ROOT / "outputs" / "02_data_preprocessing" / "data_quality_scorecard.csv"
    df = pd.read_csv(score_f)
    assert not df.empty
    assert "metric" in df.columns
    assert "score" in df.columns
    assert "status" in df.columns
