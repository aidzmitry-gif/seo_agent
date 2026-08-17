"""Single-factor experiment proposal; no traffic allocation occurs here."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExperimentProposal:
    hypothesis: str
    segment: str
    variant_a: str
    variant_b: str
    primary_metric: str = "qualified_lead_cvr"
    guardrail: str = "qualification_rate"
