"""Weekly-review planning skeleton; it makes recommendations only."""

from __future__ import annotations


def build_weekly_review() -> dict[str, str]:
    return {
        "mode": "recommendation_only",
        "required_inputs": "validated KPI deltas, change log, experiment log, active tasks",
        "output": "winner/loser decisions and next measurement dates",
    }
