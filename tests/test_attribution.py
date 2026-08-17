from datetime import datetime

from seo_agent.models import Channel, RawLead
from seo_agent.processing.attribution import resolve_attribution
from seo_agent.processing.normalize import normalize_lead


def attributed(**kwargs: object):
    raw = RawLead(
        record_id="lead-1",
        source_type="website",
        created_at=datetime(2026, 8, 17),
        **kwargs,
    )
    return resolve_attribution(normalize_lead(raw))


def test_paid_utm_has_priority_over_generic_source() -> None:
    result = attributed(utm_source="google", utm_medium="cpc")

    assert result.channel is Channel.PAID_GOOGLE
    assert result.confidence == 1.0


def test_explicit_search_source_resolves_organic_channel() -> None:
    assert attributed(utm_source="yandex", utm_medium="organic").channel is Channel.ORGANIC_YANDEX


def test_unmapped_evidence_remains_unknown() -> None:
    result = attributed(utm_source="mystery_network", referrer="https://unknown.example")

    assert result.channel is Channel.UNKNOWN
    assert result.confidence == 0.0
