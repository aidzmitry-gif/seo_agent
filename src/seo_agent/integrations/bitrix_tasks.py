"""Draft Bitrix task payloads only; sending is intentionally not implemented."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BitrixTaskDraft:
    title: str
    description: str
    priority: str = "P0"


def draft_data_quality_task(issues: tuple[str, ...]) -> BitrixTaskDraft:
    return BitrixTaskDraft(
        title="Restore data quality before SEO/CRO analysis",
        description="Blocking issues: " + ", ".join(issues),
    )
