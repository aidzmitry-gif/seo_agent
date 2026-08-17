"""Internal-link proposals remain recommendations until human-approved."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InternalLinkProposal:
    source_url: str
    target_url: str
    anchor: str
    rationale: str
