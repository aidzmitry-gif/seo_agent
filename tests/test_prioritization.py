from seo_agent.analysis.prioritization import (
    Opportunity,
    calculate_lead_impact_score,
    rank_opportunities,
)


def test_calculates_lead_impact_score() -> None:
    assert calculate_lead_impact_score(12, 0.5, 3, 2) == 1.0


def test_zero_or_invalid_inputs_are_not_prioritized() -> None:
    assert calculate_lead_impact_score(12, 1.2, 3, 2) == 0.0
    assert calculate_lead_impact_score(12, 0.5, 0, 2) == 0.0
    assert calculate_lead_impact_score(-1, 0.5, 3, 2) == 0.0


def test_ranks_highest_score_first() -> None:
    high = Opportunity("high", 12, 0.5, 3, 2)
    low = Opportunity("low", 2, 0.5, 3, 2)

    assert [item.opportunity_id for item in rank_opportunities([low, high])] == ["high", "low"]
