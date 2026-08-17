"""Validated local change-log persistence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_CHANGE_FIELDS = {
    "change_id",
    "date",
    "url",
    "type",
    "before",
    "after",
    "hypothesis",
    "primary_metric",
    "baseline",
    "review_date",
    "status",
}


def append_change(path: Path, change: dict[str, Any]) -> None:
    missing = REQUIRED_CHANGE_FIELDS - set(change)
    if missing:
        raise ValueError(f"Change record is missing fields: {sorted(missing)}")
    items = _load_list(path)
    if any(item["change_id"] == change["change_id"] for item in items):
        raise ValueError(f"Duplicate change_id: {change['change_id']}")
    items.append(change)
    _write_list(path, items)


def _load_list(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Registry must be a list: {path}")
    return data


def _write_list(path: Path, items: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(items, indent=2), encoding="utf-8")
