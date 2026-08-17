"""Dashboard data contract; rendering is an intentionally later integration."""

from __future__ import annotations

from collections.abc import Mapping


def dashboard_payload(metrics: Mapping[str, float]) -> dict[str, float]:
    return dict(metrics)
