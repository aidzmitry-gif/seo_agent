"""Interface shared by source adapters."""

from __future__ import annotations

from typing import Any, Protocol

from seo_agent.models import CollectionResult


class DeltaCollector(Protocol):
    name: str

    def collect_delta(self, watermark: dict[str, Any]) -> CollectionResult:
        """Fetch only changed records and return the next watermark on success."""
