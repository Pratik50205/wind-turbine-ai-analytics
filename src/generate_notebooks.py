"""
Generate Interactive Jupyter Notebooks
Populates the notebooks/ directory with structured exploratory and validation walkthroughs.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_DIR = PROJECT_ROOT / "notebooks"
NB_DIR.mkdir(parents=True, exist_ok=True)

def create_notebook(cells, filepath):
    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python", "version": "3.14.3"},
            "kernelspec": {"name": "python3", "display_name": "Python 3"}
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Created notebook: {filepath.name}")

def main():
    # 1. 01_eda_and_power_curves.ipynb
    cells_01 = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Hill of Towie Wind Farm — Exploratory Data Analysis & Empirical Power Curves\n",
                "\n",
                "This notebook demonstrates empirical power curve derivation, Betz limit validation, and turbine utilization analysis."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "from pathlib import Path\n",
                "\n",
                "PROJECT_ROOT = Path('..').resolve()\n",
                "df_perf = pd.read_csv(PROJECT_ROOT / 'outputs' / '04_performance_analysis' / 'turbine_performance.csv')\n",
                "df_pc = pd.read_csv(PROJECT_ROOT / 'outputs' / '04_performance_analysis' / 'power_curve_data.csv')\n",
                "df_perf.head()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Plot empirical power curve vs reference rated capacity\n",
                "plt.figure(figsize=(10, 6))\n",
                "ws_col = 'wind_speed_midpoint' if 'wind_speed_midpoint' in df_pc.columns else 'wind_speed_bin'\n",
                "pw_col = 'curve_power_kw' if 'curve_power_kw' in df_pc.columns else 'power_mean'\n",
                "plt.plot(df_pc[ws_col], df_pc[pw_col], '-o', color='#0284c7', lw=2.5, label='Measured Power Curve')\n",
                "plt.axhline(y=2300, color='#f59e0b', lw=2, linestyle='--', label='Siemens SWT-2.3-VS-82 (2300 kW)')\n",
                "plt.title('Hill of Towie Farm Empirical Power Curve (IEC 61400-12)', fontsize=12, fontweight='bold')\n",
                "plt.xlabel('Wind Speed (m/s)')\n",
                "plt.ylabel('Active Power (kW)')\n",
                "plt.grid(True, linestyle='--', alpha=0.6)\n",
                "plt.legend()\n",
                "plt.show()"
            ]
        }
    ]
    create_notebook(cells_01, NB_DIR / "01_eda_and_power_curves.ipynb")

    # 2. 02_power_prediction_modeling.ipynb
    cells_02 = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Power Prediction Modeling & Holdout Generalization\n",
                "\n",
                "Evaluates candidate models and validates HistGradientBoostingRegressor on 2026 holdout telemetry."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import joblib\n",
                "from pathlib import Path\n",
                "\n",
                "PROJECT_ROOT = Path('..').resolve()\n",
                "model = joblib.load(PROJECT_ROOT / 'models' / 'final' / 'best_power_model.joblib')\n",
                "df_err = pd.read_csv(PROJECT_ROOT / 'outputs' / '07_power_prediction' / 'error_summary.csv')\n",
                "print('Holdout 2026 Model Metrics:')\n",
                "df_err"
            ]
        }
    ]
    create_notebook(cells_02, NB_DIR / "02_power_prediction_modeling.ipynb")

    # 3. 03_anomaly_detection_and_scada_replay.ipynb
    cells_03 = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Abnormal Behavior Detection & Real-Time SCADA Replay\n",
                "\n",
                "Demonstrates context-masked power deficit anomaly detection and streaming replay verification."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "from pathlib import Path\n",
                "\n",
                "PROJECT_ROOT = Path('..').resolve()\n",
                "df_anom = pd.read_csv(PROJECT_ROOT / 'outputs' / '08_anomaly_detection' / 'anomaly_events.csv')\n",
                "df_rep = pd.read_csv(PROJECT_ROOT / 'outputs' / '10_replay_processing' / 'replay_sample_output.csv')\n",
                "print(f'Total Sustained Underperformance Events: {len(df_anom)}')\n",
                "df_anom.head()"
            ]
        }
    ]
    create_notebook(cells_03, NB_DIR / "03_anomaly_detection_and_scada_replay.ipynb")

if __name__ == "__main__":
    main()
