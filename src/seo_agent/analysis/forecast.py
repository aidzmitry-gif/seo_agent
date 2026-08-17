"""Provisional target recalculation after a validated baseline exists."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TargetForecast:
    baseline_qualified_leads: float
    growth_rate: float
    target_qualified_leads: float
    provisional: bool


def forecast_target(
    baseline_qualified_leads: float, growth_rate: float, validated_days: int
) -> TargetForecast:
    if baseline_qualified_leads < 0 or growth_rate < 0:
        raise ValueError("baseline and growth rate must be non-negative")
    return TargetForecast(
        baseline_qualified_leads,
        growth_rate,
        baseline_qualified_leads * (1 + growth_rate),
        validated_days < 14,
    )
