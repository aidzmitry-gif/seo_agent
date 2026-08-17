"""Lead-impact scoring used to rank evidence-backed opportunities."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


def calculate_lead_impact_score(
    potential_qualified_leads: float,
    confidence: float,
    effort_hours: float,
    time_to_impact_factor: float,
) -> float:
    """Return a bounded, safe score or zero when inputs cannot support ranking.

    Invalid or zero denominators do not create an infinite priority. Confidence is
    deliberately constrained to the evidence range [0, 1].
    """
    values = (potential_qualified_leads, confidence, effort_hours, time_to_impact_factor)
    if not all(isfinite(value) for value in values):
        return 0.0
    if potential_qualified_leads <= 0 or not 0 <= confidence <= 1:
        return 0.0
    if effort_hours <= 0 or time_to_impact_factor <= 0:
        return 0.0
    return potential_qualified_leads * confidence / effort_hours / time_to_impact_factor


@dataclass(frozen=True, slots=True)
class Opportunity:
    opportunity_id: str
    potential_qualified_leads: float
    confidence: float
    effort_hours: float
    time_to_impact_factor: float

    @property
    def score(self) -> float:
        return calculate_lead_impact_score(
            self.potential_qualified_leads,
            self.confidence,
            self.effort_hours,
            self.time_to_impact_factor,
        )


def rank_opportunities(opportunities: list[Opportunity]) -> list[Opportunity]:
    return sorted(opportunities, key=lambda opportunity: opportunity.score, reverse=True)
