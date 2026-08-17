from datetime import datetime, timedelta

from seo_agent.models import RawLead
from seo_agent.processing.deduplicate import find_duplicate_links
from seo_agent.processing.normalize import normalize_email, normalize_lead, normalize_phone

NOW = datetime(2026, 8, 17, 9, 0)


def lead(record_id: str, **kwargs: object) -> RawLead:
    return RawLead(record_id=record_id, source_type="form", created_at=NOW, **kwargs)


def test_normalizes_belarusian_phone_and_email() -> None:
    assert normalize_phone("8 (029) 123-45-67") == "+375291234567"
    assert normalize_phone("not a phone") is None
    assert normalize_email("  Sales@Example.BY ") == "sales@example.by"
    assert normalize_email("invalid") is None


def test_links_duplicate_by_strong_crm_id_without_deleting_raw_records() -> None:
    records = [
        normalize_lead(lead("a", crm_id="42")),
        normalize_lead(lead("b", crm_id="42", phone="+375291234567")),
    ]

    links = find_duplicate_links(records)

    assert links[0].duplicate_record_id == "b"
    assert links[0].master_record_id == "a"
    assert links[0].reasons == ("crm_id",)
    assert len(records) == 2


def test_links_same_contact_only_inside_source_and_time_window() -> None:
    first = normalize_lead(lead("a", phone="+375291234567"))
    second = normalize_lead(
        RawLead(
            record_id="b",
            source_type="form",
            created_at=NOW + timedelta(days=2),
            phone="8 029 123 45 67",
        )
    )
    outside = normalize_lead(
        RawLead(
            record_id="c",
            source_type="form",
            created_at=NOW + timedelta(days=9),
            phone="8 029 123 45 67",
        )
    )

    links = find_duplicate_links([first, second, outside], temporal_window_days=7)

    assert [(item.duplicate_record_id, item.master_record_id) for item in links] == [("b", "a")]
