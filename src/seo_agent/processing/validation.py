"""Quality gate and controlled lead qualification rules."""

from __future__ import annotations

from seo_agent.models import (
    Attribution,
    Channel,
    DataQualityResult,
    DuplicateLink,
    Qualification,
    RawLead,
)

DISQUALIFICATION_REASONS = {
    "spam",
    "test",
    "duplicate",
    "irrelevant_request",
    "cannot_be_processed",
}


def assess_qualification(raw: RawLead, is_duplicate: bool = False) -> Qualification:
    """Apply the configured required flags without inferring sales eligibility."""
    reason: str | None = None
    if raw.is_spam:
        reason = "spam"
    elif raw.is_test:
        reason = "test"
    elif is_duplicate:
        reason = "duplicate"
    elif raw.is_relevant is not True:
        reason = "irrelevant_request"
    elif raw.sales_processable is not True:
        reason = "cannot_be_processed"
    return Qualification(raw.record_id, reason is None, reason)


def run_data_quality_gate(
    records: list[RawLead],
    attributions: list[Attribution],
    duplicate_links: list[DuplicateLink],
    attribution_min: float = 0.95,
    duplicate_rate_max: float = 0.02,
    api_errors: tuple[str, ...] = (),
    incomplete_sources: tuple[str, ...] = (),
) -> DataQualityResult:
    """Block analysis when data cannot safely support a growth decision."""
    if not 0 <= attribution_min <= 1 or not 0 <= duplicate_rate_max <= 1:
        raise ValueError("quality thresholds must be between 0 and 1")
    eligible_ids = {item.record_id for item in records if not item.is_spam and not item.is_test}
    attributed_ids = {
        item.record_id
        for item in attributions
        if item.record_id in eligible_ids and item.channel is not Channel.UNKNOWN
    }
    completeness = len(attributed_ids) / len(eligible_ids) if eligible_ids else 0.0
    duplicate_count = len({link.duplicate_record_id for link in duplicate_links})
    duplicate_rate = duplicate_count / len(records) if records else 0.0
    issues: list[str] = []
    if not records:
        issues.append("no_records")
    if completeness < attribution_min:
        issues.append("attribution_below_threshold")
    if duplicate_rate > duplicate_rate_max:
        issues.append("duplicate_rate_above_threshold")
    issues.extend(f"api_error:{error}" for error in api_errors)
    issues.extend(f"incomplete_source:{source}" for source in incomplete_sources)
    return DataQualityResult(not issues, completeness, duplicate_rate, tuple(issues))
