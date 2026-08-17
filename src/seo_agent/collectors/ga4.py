"""Optional GA4 delta adapter placeholder."""

from __future__ import annotations

from typing import Any

from seo_agent.models import CollectionResult


class GA4Collector:
    name = "ga4"

    def collect_delta(self, watermark: dict[str, Any]) -> CollectionResult:
        return CollectionResult(
            source=self.name,
            next_watermark=watermark,
            detail="stub: configure GA4 property and credentials before collection",
        )
