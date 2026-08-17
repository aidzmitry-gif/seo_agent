"""Deterministic bottleneck ordering from the operating policy."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class BottleneckType(StrEnum):
    DATA_QUALITY = "data_quality"
    LEAD_DROP = "lead_drop"
    CONVERSION = "conversion"
    VISIBILITY = "visibility"
    LEAD_QUALITY = "lead_quality"
    TECHNICAL_SEO = "technical_seo"
    BACKLOG = "backlog"


@dataclass(frozen=True, slots=True)
class Bottleneck:
    kind: BottleneckType
    rationale: str


def detect_bottleneck(
    *,
    quality_passed: bool,
    lead_drop: bool = False,
    conversion_weak: bool = False,
    visibility_weak: bool = False,
    lead_quality_weak: bool = False,
    technical_issue: bool = False,
) -> Bottleneck:
    """Select exactly one problem in the approved order of operations."""
    choices = (
        (not quality_passed, BottleneckType.DATA_QUALITY, "Data quality gate did not pass."),
        (lead_drop, BottleneckType.LEAD_DROP, "Qualified lead volume dropped."),
        (conversion_weak, BottleneckType.CONVERSION, "Traffic exists but conversion is weak."),
        (
            visibility_weak,
            BottleneckType.VISIBILITY,
            "Search demand exists but visibility is weak.",
        ),
        (lead_quality_weak, BottleneckType.LEAD_QUALITY, "Lead quality is weak."),
        (technical_issue, BottleneckType.TECHNICAL_SEO, "Technical SEO issue detected."),
    )
    for applies, kind, rationale in choices:
        if applies:
            return Bottleneck(kind, rationale)
    return Bottleneck(BottleneckType.BACKLOG, "Select the highest Lead Impact Score backlog task.")
