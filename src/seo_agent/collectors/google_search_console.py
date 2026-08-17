"""Google Search Console delta adapter placeholder with freshness guard later."""

from __future__ import annotations

from typing import Any

from seo_agent.models import CollectionResult


class GoogleSearchConsoleCollector:
    name = "google_search_console"

    def collect_delta(self, watermark: dict[str, Any]) -> CollectionResult:
        return CollectionResult(
            source=self.name,
            next_watermark=watermark,
            detail="stub: configure GSC site and service account before collection",
        )
