"""Explicit opportunity evidence records."""

from __future__ import annotations

from dataclasses import dataclass

from seo_agent.analysis.prioritization import Opportunity


@dataclass(frozen=True, slots=True)
class EvidencedOpportunity:
    opportunity: Opportunity
    hypothesis: str
    evidence_refs: tuple[str, ...]

    @property
    def eligible(self) -> bool:
        return bool(self.hypothesis and self.evidence_refs and self.opportunity.score > 0)
