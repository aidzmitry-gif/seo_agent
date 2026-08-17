"""Small, explicit KPI calculations over qualified site leads."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from seo_agent.models import Qualification, RawLead


@dataclass(frozen=True, slots=True)
class KpiSnapshot:
    start: date
    end: date
    raw_site_leads: int
    qualified_site_leads: int
    qualification_rate: float


def _is_site_lead(lead: RawLead) -> bool:
    return bool(lead.landing_url) or lead.source_type.casefold() in {"site", "website", "form"}


def calculate_kpis(
    records: list[RawLead], qualifications: list[Qualification], start: date, end: date
) -> KpiSnapshot:
    if end < start:
        raise ValueError("end must not precede start")
    qualified_ids = {item.record_id for item in qualifications if item.qualified}
    selected = [
        record
        for record in records
        if start <= record.created_at.date() <= end and _is_site_lead(record)
    ]
    raw_count = len(selected)
    qualified_count = sum(record.record_id in qualified_ids for record in selected)
    rate = qualified_count / raw_count if raw_count else 0.0
    return KpiSnapshot(start, end, raw_count, qualified_count, rate)


def change_ratio(current: float, previous: float) -> float | None:
    """Return relative change; ``None`` means no defensible percentage baseline."""
    return (current - previous) / previous if previous else None
