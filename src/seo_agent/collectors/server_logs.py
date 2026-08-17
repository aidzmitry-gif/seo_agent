"""Server-log collector contract; path and retention policy are external inputs."""

from __future__ import annotations

from typing import Any

from seo_agent.models import CollectionResult


class ServerLogsCollector:
    name = "server_logs"

    def collect_delta(self, watermark: dict[str, Any]) -> CollectionResult:
        return CollectionResult(
            source=self.name,
            next_watermark=watermark,
            detail="stub: configure an approved read-only log source before collection",
        )
