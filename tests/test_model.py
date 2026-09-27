"""
Unit Tests for Phase 6 and 7 Power Prediction Models and Holdout Results
"""

from pathlib import Path
import joblib
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_serialized_models_exist():
    models_dir = PROJECT_ROOT / "models"
    assert (models_dir / "final" / "best_power_model.joblib").exists()
    assert (models_dir / "candidates" / "hist_gradient_boosting.joblib").exists()
    assert (models_dir / "candidates" / "random_forest.joblib").exists()
    assert (models_dir / "candidates" / "ridge_linear.joblib").exists()

def test_phase6_artifacts_exist():
    out6 = PROJECT_ROOT / "outputs" / "06_model_development"
    assert out6.exists()

    required_files = [
        "report.md",
        "model_comparison.csv",
        "train_validation_test_split.csv",
        "hyperparameters.csv",
        "final_model_metrics.csv",
        "figures/model_comparison.png",
        "figures/actual_vs_predicted_test.png",
        "figures/residual_distribution.png",
        "figures/residual_time_series.png",
        "figures/feature_importance.png",
        "logs/model_training.log"
    ]
    for rf in required_files:
        p = out6 / rf
        assert p.exists() and p.stat().st_size > 0, f"Phase 6 artifact {rf} is missing or empty"

def test_phase7_artifacts_exist():
    out7 = PROJECT_ROOT / "outputs" / "07_power_prediction"
    assert out7.exists()

    required_files = [
        "report.md",
        "predictions.parquet",
        "predictions_sample.csv",
        "metrics_by_turbine.csv",
        "metrics_by_period.csv",
        "error_summary.csv",
        "figures/actual_vs_predicted.png",
        "figures/prediction_error_distribution.png",
        "figures/prediction_error_over_time.png",
        "figures/metrics_by_turbine.png",
        "figures/predicted_vs_wind_speed.png",
        "logs/prediction.log"
    ]
    for rf in required_files:
        p = out7 / rf
        assert p.exists() and p.stat().st_size > 0, f"Phase 7 artifact {rf} is missing or empty"

def test_holdout_prediction_performance():
    metrics_f = PROJECT_ROOT / "outputs" / "07_power_prediction" / "error_summary.csv"
    df = pd.read_csv(metrics_f)
    assert not df.empty
    row = df.iloc[0]
    assert row["R2_Score"] >= 0.85, f"R2 score should be >= 0.85, got {row['R2_Score']}"
    assert row["Normalized_RMSE_pct"] <= 15.0, f"nRMSE should be <= 15%, got {row['Normalized_RMSE_pct']}"

def test_predictions_dataset_structure():
    pred_sample_f = PROJECT_ROOT / "outputs" / "07_power_prediction" / "predictions_sample.csv"
    df = pd.read_csv(pred_sample_f)
    assert len(df) >= 5000
    assert "actual_power_kw" in df.columns
    assert "predicted_power_kw" in df.columns
    assert "prediction_error_kw" in df.columns
    assert "turbine_id" in df.columns

    # Bounds on predictions
    assert df["predicted_power_kw"].min() >= 0.0
    assert df["predicted_power_kw"].max() <= 2450.0
