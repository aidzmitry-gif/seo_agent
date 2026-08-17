"""End-of-cycle review skeleton; no production action occurs here."""

from __future__ import annotations


def build_quarterly_review() -> dict[str, str]:
    return {
        "mode": "recommendation_only",
        "required_inputs": "13-week qualified-lead, deal and revenue evidence",
        "output": "next-cycle baseline, target and prioritised backlog",
    }
