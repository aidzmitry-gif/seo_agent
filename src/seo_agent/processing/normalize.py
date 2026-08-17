"""Pure normalization functions for contacts and provider-neutral lead records."""

from __future__ import annotations

import re

from seo_agent.models import NormalizedLead, RawLead


def normalize_phone(value: str | None) -> str | None:
    """Return a stable E.164-like number where evidence is sufficient.

    Belarusian domestic 8-0XX numbers become +375XX. Short or non-phone values
    return ``None`` instead of being guessed.
    """
    if not value:
        return None
    digits = re.sub(r"\D", "", value)
    if len(digits) == 11 and digits.startswith("80"):
        digits = f"375{digits[2:]}"
    if len(digits) < 10 or len(digits) > 15:
        return None
    return f"+{digits}"


def normalize_email(value: str | None) -> str | None:
    """Lowercase and validate a minimally usable email address."""
    if not value:
        return None
    candidate = value.strip().casefold()
    if candidate.count("@") != 1:
        return None
    local, domain = candidate.split("@")
    if not local or not domain or "." not in domain or " " in candidate:
        return None
    try:
        domain = domain.encode("idna").decode("ascii")
    except UnicodeError:
        return None
    return f"{local}@{domain}"


def normalize_lead(raw: RawLead) -> NormalizedLead:
    return NormalizedLead(
        raw=raw,
        normalized_phone=normalize_phone(raw.phone),
        normalized_email=normalize_email(raw.email),
    )
