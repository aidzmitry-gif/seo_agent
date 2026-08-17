"""Non-destructive duplicate candidate detection."""

from __future__ import annotations

from datetime import timedelta

from seo_agent.models import DuplicateLink, NormalizedLead

STRONG_IDENTIFIERS = ("crm_id", "origin_id", "call_external_id", "form_request_id")


def _strong_match(left: NormalizedLead, right: NormalizedLead) -> tuple[str, ...]:
    matches: list[str] = []
    for field in STRONG_IDENTIFIERS:
        left_value = getattr(left.raw, field)
        if left_value and left_value == getattr(right.raw, field):
            matches.append(field)
    return tuple(matches)


def _contact_match(
    earlier: NormalizedLead,
    current: NormalizedLead,
    temporal_window_days: int,
) -> tuple[str, ...]:
    if earlier.raw.source_type != current.raw.source_type:
        return ()
    if current.raw.created_at - earlier.raw.created_at > timedelta(days=temporal_window_days):
        return ()
    reasons: list[str] = []
    if earlier.normalized_phone and earlier.normalized_phone == current.normalized_phone:
        reasons.append("normalized_phone")
    if earlier.normalized_email and earlier.normalized_email == current.normalized_email:
        reasons.append("normalized_email")
    return tuple(reasons)


def find_duplicate_links(
    records: list[NormalizedLead], temporal_window_days: int = 7
) -> list[DuplicateLink]:
    """Link each candidate to the earliest matching master without removing data."""
    if temporal_window_days < 0:
        raise ValueError("temporal_window_days must be non-negative")

    links: list[DuplicateLink] = []
    master_by_record_id: dict[str, str] = {}
    ordered = sorted(records, key=lambda item: (item.raw.created_at, item.raw.record_id))
    for index, current in enumerate(ordered):
        for earlier in ordered[:index]:
            # A duplicate cannot start a new temporal window for later records.
            if earlier.raw.record_id in master_by_record_id:
                continue
            reasons = _strong_match(earlier, current) or _contact_match(
                earlier, current, temporal_window_days
            )
            if reasons:
                master_id = master_by_record_id.get(earlier.raw.record_id, earlier.raw.record_id)
                links.append(DuplicateLink(current.raw.record_id, master_id, reasons))
                master_by_record_id[current.raw.record_id] = master_id
                break
    return links
