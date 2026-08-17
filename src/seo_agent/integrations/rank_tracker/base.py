"""Rank-tracker adapter protocol."""

from __future__ import annotations

from typing import Protocol


class RankTracker(Protocol):
    provider: str

    def collect_positions(self, queries: list[str], region: str) -> list[dict[str, object]]:
        """Return provider data without shaping core SEO logic around the vendor."""
