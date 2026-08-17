"""Stable cohort keys for delta analysis."""

from __future__ import annotations

from datetime import date

from seo_agent.models import Channel


def cohort_key(observed_on: date, channel: Channel, landing_url: str | None) -> str:
    landing = landing_url or "unknown"
    return f"{observed_on.isoformat()}|{channel.value}|{landing}"
