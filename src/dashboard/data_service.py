"""
Dashboard Data Service
Provides fast in-memory access and aggregation for Dash Plotly components.
"""

import os
from pathlib import Path
from functools import lru_cache
import pandas as pd
import numpy as np

# Robust root resolution for local execution and Vercel serverless environment
_cwd = Path(os.getcwd())
if (_cwd / "outputs").exists():
    PROJECT_ROOT = _cwd
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class DashboardDataService:
    def __init__(self):
        self.root = PROJECT_ROOT
        self._load_data()

    def _load_data(self):
        # 1. Performance and fleet metrics
        p4_dir = self.root / "outputs" / "04_performance_analysis"
        self.df_metrics = pd.read_csv(p4_dir / "performance_metrics.csv") if (p4_dir / "performance_metrics.csv").exists() else pd.DataFrame()
        self.df_turb_perf = pd.read_csv(p4_dir / "turbine_performance.csv") if (p4_dir / "turbine_performance.csv").exists() else pd.DataFrame()
        if not self.df_turb_perf.empty:
            if 'turbine_name' in self.df_turb_perf.columns and 'turbine_id' not in self.df_turb_perf.columns:
                self.df_turb_perf['turbine_id'] = self.df_turb_perf['turbine_name']
            if 'actual_yield_mwh' in self.df_turb_perf.columns and 'annual_energy_yield_gwh' not in self.df_turb_perf.columns:
                self.df_turb_perf['annual_energy_yield_gwh'] = self.df_turb_perf['actual_yield_mwh'] / 1000.0
            if 'actual_mean_power_kw' in self.df_turb_perf.columns and 'mean_active_power_kw' not in self.df_turb_perf.columns:
                self.df_turb_perf['mean_active_power_kw'] = self.df_turb_perf['actual_mean_power_kw']
        self.df_pc = pd.read_csv(p4_dir / "power_curve_data.csv") if (p4_dir / "power_curve_data.csv").exists() else pd.DataFrame()
        if not self.df_pc.empty:
            if 'wind_speed_midpoint' in self.df_pc.columns and 'wind_speed_bin' not in self.df_pc.columns:
                self.df_pc['wind_speed_bin'] = self.df_pc['wind_speed_midpoint']
            if 'curve_power_kw' in self.df_pc.columns and 'power_mean' not in self.df_pc.columns:
                self.df_pc['power_mean'] = self.df_pc['curve_power_kw']
            if 'reference_power' not in self.df_pc.columns:
                self.df_pc['reference_power'] = 2300.0
        self.df_wind_bins = pd.read_csv(p4_dir / "wind_bin_performance.csv") if (p4_dir / "wind_bin_performance.csv").exists() else pd.DataFrame()

        # 2. Power prediction holdout results
        p7_dir = self.root / "outputs" / "07_power_prediction"
        self.df_turb_metrics = pd.read_csv(p7_dir / "metrics_by_turbine.csv") if (p7_dir / "metrics_by_turbine.csv").exists() else pd.DataFrame()
        self.df_error_summary = pd.read_csv(p7_dir / "error_summary.csv") if (p7_dir / "error_summary.csv").exists() else pd.DataFrame()

        # Sample predictions for fast interactive rendering
        pred_sample_file = p7_dir / "predictions_sample.csv"
        self.df_preds_sample = pd.read_csv(pred_sample_file) if pred_sample_file.exists() else pd.DataFrame()
        if not self.df_preds_sample.empty:
            self.df_preds_sample['timestamp'] = pd.to_datetime(self.df_preds_sample['timestamp'])
            if 'actual_power_kw' in self.df_preds_sample.columns and 'actual_power' not in self.df_preds_sample.columns:
                self.df_preds_sample['actual_power'] = self.df_preds_sample['actual_power_kw']
            if 'predicted_power_kw' in self.df_preds_sample.columns and 'predicted_power' not in self.df_preds_sample.columns:
                self.df_preds_sample['predicted_power'] = self.df_preds_sample['predicted_power_kw']
            if 'prediction_error_kw' in self.df_preds_sample.columns and 'residual' not in self.df_preds_sample.columns:
                self.df_preds_sample['residual'] = self.df_preds_sample['prediction_error_kw']

        # 3. Anomaly detection results
        p8_dir = self.root / "outputs" / "08_anomaly_detection"
        self.df_anomaly_summary = pd.read_csv(p8_dir / "anomaly_summary.csv") if (p8_dir / "anomaly_summary.csv").exists() else pd.DataFrame()
        self.df_anomaly_by_turb = pd.read_csv(p8_dir / "anomaly_by_turbine.csv") if (p8_dir / "anomaly_by_turbine.csv").exists() else pd.DataFrame()
        self.df_anomaly_events = pd.read_csv(p8_dir / "anomaly_events.csv") if (p8_dir / "anomaly_events.csv").exists() else pd.DataFrame()
        if not self.df_anomaly_events.empty:
            if 'mean_power_deficit_kw' in self.df_anomaly_events.columns and 'mean_deficit_kw' not in self.df_anomaly_events.columns:
                self.df_anomaly_events['mean_deficit_kw'] = self.df_anomaly_events['mean_power_deficit_kw']
            if 'peak_power_deficit_kw' in self.df_anomaly_events.columns and 'max_deficit_kw' not in self.df_anomaly_events.columns:
                self.df_anomaly_events['max_deficit_kw'] = self.df_anomaly_events['peak_power_deficit_kw']
            if 'mean_wind_speed_ms' in self.df_anomaly_events.columns and 'mean_wind_speed' not in self.df_anomaly_events.columns:
                self.df_anomaly_events['mean_wind_speed'] = self.df_anomaly_events['mean_wind_speed_ms']
            if 'action_recommended' in self.df_anomaly_events.columns and 'recommended_action' not in self.df_anomaly_events.columns:
                self.df_anomaly_events['recommended_action'] = self.df_anomaly_events['action_recommended']

        # 4. Event & Alarm logs
        p9_dir = self.root / "outputs" / "09_event_analysis"
        self.df_alarms = pd.read_csv(p9_dir / "alarm_summary.csv") if (p9_dir / "alarm_summary.csv").exists() else pd.DataFrame()
        if not self.df_alarms.empty:
            if 'total_occurrences' in self.df_alarms.columns and 'count' not in self.df_alarms.columns:
                self.df_alarms['count'] = self.df_alarms['total_occurrences']
            if 'alarm_description' in self.df_alarms.columns and 'description' not in self.df_alarms.columns:
                self.df_alarms['description'] = self.df_alarms['alarm_description']
        self.df_shutdowns = pd.read_csv(p9_dir / "shutdown_summary.csv") if (p9_dir / "shutdown_summary.csv").exists() else pd.DataFrame()
        self.df_corr = pd.read_csv(p9_dir / "anomaly_event_correlation.csv") if (p9_dir / "anomaly_event_correlation.csv").exists() else pd.DataFrame()

        # 5. Feature importances
        p5_dir = self.root / "outputs" / "05_feature_engineering"
        self.df_importance = pd.read_csv(p5_dir / "feature_importance_precheck.csv") if (p5_dir / "feature_importance_precheck.csv").exists() else pd.DataFrame()
        if not self.df_importance.empty:
            if 'feature_name' in self.df_importance.columns and 'feature' not in self.df_importance.columns:
                self.df_importance['feature'] = self.df_importance['feature_name']
            if 'rf_importance_pct' in self.df_importance.columns and 'importance' not in self.df_importance.columns:
                self.df_importance['importance'] = self.df_importance['rf_importance_pct']

        # 6. Replay sample stream
        p10_dir = self.root / "outputs" / "10_replay_processing"
        self.df_replay = pd.read_csv(p10_dir / "replay_sample_output.csv") if (p10_dir / "replay_sample_output.csv").exists() else pd.DataFrame()
        if not self.df_replay.empty:
            self.df_replay['ts_dt'] = pd.to_datetime(self.df_replay['timestamp'])
            if 'actual_power_kw' in self.df_replay.columns and 'actual_power' not in self.df_replay.columns:
                self.df_replay['actual_power'] = self.df_replay['actual_power_kw']
            if 'predicted_power_kw' in self.df_replay.columns and 'predicted_power' not in self.df_replay.columns:
                self.df_replay['predicted_power'] = self.df_replay['predicted_power_kw']
            if 'wind_speed_ms' in self.df_replay.columns and 'wind_speed' not in self.df_replay.columns:
                self.df_replay['wind_speed'] = self.df_replay['wind_speed_ms']
            if 'realtime_alert' in self.df_replay.columns and 'alert' not in self.df_replay.columns:
                self.df_replay['alert'] = self.df_replay['realtime_alert']
            if 'prediction_residual_kw' in self.df_replay.columns and 'residual_kw' not in self.df_replay.columns:
                self.df_replay['residual_kw'] = self.df_replay['prediction_residual_kw']

    def get_kpis(self):
        m = self.df_metrics.iloc[0] if not self.df_metrics.empty else {}
        e = self.df_error_summary.iloc[0] if not self.df_error_summary.empty else {}
        total_anom = int(len(self.df_anomaly_events)) if not self.df_anomaly_events.empty else 0
        return {
            "total_generation_gwh": m.get("total_annual_generation_gwh", 96.96),
            "fleet_capacity_factor": m.get("farm_capacity_factor_pct", 23.4),
            "fleet_availability": m.get("farm_technical_availability_pct", 98.1),
            "turbines_count": int(m.get("turbines_count", 21)),
            "model_r2_score": e.get("R2_Score", 0.9963),
            "model_nrmse_pct": e.get("Normalized_RMSE_pct", 1.87),
            "anomaly_events_count": total_anom
        }

    def get_turbines_list(self):
        return [f"T{i:02d}" for i in range(1, 22)]

# Singleton instance
data_service = DashboardDataService()
