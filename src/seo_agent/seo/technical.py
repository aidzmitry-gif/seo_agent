"""Technical issue candidate contract for a crawler or log adapter."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TechnicalIssue:
    url: str
    issue_type: str
    severity: str
    evidence: str
