"""Provider-neutral competitor observation contract."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CompetitorObservation:
    competitor_domain: str
    query: str
    source: str
