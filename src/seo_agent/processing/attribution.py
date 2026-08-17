"""Evidence-based normalized channel attribution."""

from __future__ import annotations

from seo_agent.models import Attribution, Channel, NormalizedLead

PAID_MEDIA = {"cpc", "ppc", "paid", "paidsearch", "display"}
MESSENGER_SOURCES = {"telegram", "whatsapp", "viber", "messenger"}


def _text(value: str | None) -> str:
    return (value or "").strip().casefold()


def resolve_attribution(lead: NormalizedLead) -> Attribution:
    """Resolve only explicit source evidence; uncertain records remain unknown."""
    raw = lead.raw
    source = _text(raw.utm_source) or _text(raw.source_type)
    medium = _text(raw.utm_medium)
    evidence: list[str] = []

    if source in {"google", "googleads", "google_ads"} and medium in PAID_MEDIA:
        return Attribution(raw.record_id, Channel.PAID_GOOGLE, 1.0, ("utm_paid_google",))
    if source in {"yandex", "yandex_direct", "yandexdirect"} and medium in PAID_MEDIA:
        return Attribution(raw.record_id, Channel.PAID_YANDEX, 1.0, ("utm_paid_yandex",))
    if source in {"google", "google.com"} and medium in {"", "organic", "seo"}:
        return Attribution(raw.record_id, Channel.ORGANIC_GOOGLE, 0.98, ("explicit_google",))
    if source in {"yandex", "yandex.ru", "ya.ru"} and medium in {"", "organic", "seo"}:
        return Attribution(raw.record_id, Channel.ORGANIC_YANDEX, 0.98, ("explicit_yandex",))
    if medium == "email" or source in {"email", "newsletter"}:
        return Attribution(raw.record_id, Channel.EMAIL, 0.95, ("explicit_email",))
    if source in MESSENGER_SOURCES or medium == "messenger":
        return Attribution(raw.record_id, Channel.MESSENGER, 0.95, ("explicit_messenger",))
    if raw.call_external_id or source == "call":
        return Attribution(raw.record_id, Channel.CALL, 0.95, ("explicit_call",))
    if source in {"partner", "affiliate"}:
        return Attribution(raw.record_id, Channel.PARTNER, 0.95, ("explicit_partner",))
    if source in {"direct", "(direct)"} and medium in {"", "none", "direct"}:
        return Attribution(raw.record_id, Channel.DIRECT, 0.9, ("explicit_direct",))
    if medium == "referral" or source == "referral":
        return Attribution(raw.record_id, Channel.REFERRAL, 0.85, ("explicit_referral",))

    if raw.referrer:
        evidence.append("unmapped_referrer")
    return Attribution(raw.record_id, Channel.UNKNOWN, 0.0, tuple(evidence))
