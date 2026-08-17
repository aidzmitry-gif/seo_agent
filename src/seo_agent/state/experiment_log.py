"""Validated local experiment-log persistence."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from seo_agent.state.change_log import _load_list, _write_list

REQUIRED_EXPERIMENT_FIELDS = {
    "experiment_id",
    "hypothesis",
    "segment",
    "variant_a",
    "variant_b",
    "primary_metric",
    "guardrail",
    "start_date",
    "review_date",
    "decision",
}


def append_experiment(path: Path, experiment: dict[str, Any]) -> None:
    missing = REQUIRED_EXPERIMENT_FIELDS - set(experiment)
    if missing:
        raise ValueError(f"Experiment record is missing fields: {sorted(missing)}")
    if experiment["variant_a"] == experiment["variant_b"]:
        raise ValueError("Experiment variants must differ")
    items = _load_list(path)
    if any(item["experiment_id"] == experiment["experiment_id"] for item in items):
        raise ValueError(f"Duplicate experiment_id: {experiment['experiment_id']}")
    items.append(experiment)
    _write_list(path, items)
