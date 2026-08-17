"""Bitrix24 CRM delta adapter placeholder using universal CRM endpoints later."""

from __future__ import annotations

from typing import Any

from seo_agent.models import CollectionResult


class Bitrix24Collector:
    name = "bitrix24"

    def collect_delta(self, watermark: dict[str, Any]) -> CollectionResult:
        return CollectionResult(
            source=self.name,
            next_watermark=watermark,
            detail="stub: configure universal Bitrix24 CRM credentials before collection",
        )
