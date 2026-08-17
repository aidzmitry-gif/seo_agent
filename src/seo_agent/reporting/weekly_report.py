"""Weekly report contract."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WeeklyReport:
    week_number: int
    qualified_site_leads: int
    decisions: tuple[str, ...]
