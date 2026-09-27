"""
Configuration Loader Module
Provides unified access to YAML configurations across the pipeline and dashboard.
"""

from pathlib import Path
from typing import Any, Dict
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"

def load_yaml(filename: str) -> Dict[str, Any]:
    file_path = CONFIG_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_project_config() -> Dict[str, Any]:
    return load_yaml("project.yaml")

def get_data_config() -> Dict[str, Any]:
    return load_yaml("data.yaml")

def get_model_config() -> Dict[str, Any]:
    return load_yaml("model.yaml")

def get_dashboard_config() -> Dict[str, Any]:
    return load_yaml("dashboard.yaml")

def get_paths() -> Dict[str, Path]:
    cfg = get_project_config()
    raw_paths = cfg.get("paths", {})
    return {
        k: (PROJECT_ROOT / v).resolve()
        for k, v in raw_paths.items()
    }
