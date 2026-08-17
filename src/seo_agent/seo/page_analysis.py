"""Page-analysis evidence record."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PageObservation:
    url: str
    metric: str
    value: float
    evidence_date: str
