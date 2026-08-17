"""Configuration loading with no implicit environment or network side effects."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

CONFIG_FILES = (
    "project.yaml",
    "kpi.yaml",
    "sources.yaml",
    "qualification.yaml",
    "regions.yaml",
    "thresholds.yaml",
)


def load_config(config_dir: Path) -> dict[str, dict[str, Any]]:
    """Load all mandatory YAML configuration files keyed by their stem."""
    loaded: dict[str, dict[str, Any]] = {}
    for name in CONFIG_FILES:
        path = config_dir / name
        if not path.is_file():
            raise FileNotFoundError(f"Required configuration is missing: {path}")
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Configuration must be a mapping: {path}")
        loaded[path.stem] = data
    return loaded
