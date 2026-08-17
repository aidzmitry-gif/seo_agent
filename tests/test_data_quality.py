from datetime import datetime

from seo_agent.models import Attribution, Channel, RawLead
from seo_agent.processing.validation import run_data_quality_gate


def raw(record_id: str) -> RawLead:
    return RawLead(record_id, "website", datetime(2026, 8, 17))


def test_gate_passes_at_exact_attribution_threshold() -> None:
    records = [raw(str(index)) for index in range(20)]
    attributions = [
        Attribution(str(index), Channel.DIRECT, 1.0, ("test",)) for index in range(19)
    ] + [Attribution("19", Channel.UNKNOWN, 0.0, ())]

    result = run_data_quality_gate(records, attributions, [], attribution_min=0.95)

    assert result.passed
    assert result.attribution_completeness == 0.95


def test_gate_blocks_empty_or_incomplete_data() -> None:
    result = run_data_quality_gate([], [], [], incomplete_sources=("bitrix24",))

    assert not result.passed
    assert "no_records" in result.issues
    assert "incomplete_source:bitrix24" in result.issues


def test_gate_blocks_duplicate_rate_above_threshold() -> None:
    from seo_agent.models import DuplicateLink

    records = [raw(str(index)) for index in range(10)]
    attributions = [Attribution(str(index), Channel.DIRECT, 1.0, ()) for index in range(10)]
    links = [DuplicateLink("1", "0", ("crm_id",))]

    result = run_data_quality_gate(
        records,
        attributions,
        links,
        duplicate_rate_max=0.02,
    )

    assert not result.passed
    assert "duplicate_rate_above_threshold" in result.issues
