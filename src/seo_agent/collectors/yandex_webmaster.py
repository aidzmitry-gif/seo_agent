"""Yandex Webmaster delta adapter placeholder."""

from __future__ import annotations

from typing import Any

from seo_agent.models import CollectionResult


class YandexWebmasterCollector:
    name = "yandex_webmaster"

    def collect_delta(self, watermark: dict[str, Any]) -> CollectionResult:
        return CollectionResult(
            source=self.name,
            next_watermark=watermark,
            detail="stub: configure Webmaster host and OAuth token before collection",
        )
