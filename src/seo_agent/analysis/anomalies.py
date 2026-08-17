"""Conservative anomaly flags; diagnosis remains a human-reviewed step."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Anomaly:
    metric: str
    current: float
    previous: float
    change_ratio: float | None
    flagged: bool


def compare_metric(metric: str, current: float, previous: float, threshold: float = 0.2) -> Anomaly:
    if previous <= 0:
        return Anomaly(metric, current, previous, None, False)
    ratio = (current - previous) / previous
    return Anomaly(metric, current, previous, ratio, abs(ratio) >= threshold)
