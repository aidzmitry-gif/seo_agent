"""Search-demand records supplied by replaceable data adapters."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SearchDemand:
    query: str
    region: str
    volume: int | None
    source: str
