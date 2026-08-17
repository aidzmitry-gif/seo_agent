"""Typed, provider-neutral records used across the growth operating system."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any


class Channel(StrEnum):
    ORGANIC_GOOGLE = "organic_google"
    ORGANIC_YANDEX = "organic_yandex"
    PAID_GOOGLE = "paid_google"
    PAID_YANDEX = "paid_yandex"
    DIRECT = "direct"
    REFERRAL = "referral"
    EMAIL = "email"
    MESSENGER = "messenger"
    CALL = "call"
    PARTNER = "partner"
    UNKNOWN = "unknown"


class TaskSize(StrEnum):
    LARGE = "large"
    SMALL = "small"


@dataclass(frozen=True, slots=True)
class RawLead:
    """Immutable source record. Its payload is never altered or deleted."""

    record_id: str
    source_type: str
    created_at: datetime
    crm_id: str | None = None
    phone: str | None = None
    email: str | None = None
    origin_id: str | None = None
    call_external_id: str | None = None
    form_request_id: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    referrer: str | None = None
    landing_url: str | None = None
    is_spam: bool = False
    is_test: bool = False
    is_relevant: bool | None = None
    sales_processable: bool | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class NormalizedLead:
    raw: RawLead
    normalized_phone: str | None
    normalized_email: str | None


@dataclass(frozen=True, slots=True)
class DuplicateLink:
    duplicate_record_id: str
    master_record_id: str
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Attribution:
    record_id: str
    channel: Channel
    confidence: float
    evidence: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Qualification:
    record_id: str
    qualified: bool
    disqual_reason: str | None


@dataclass(frozen=True, slots=True)
class DataQualityResult:
    passed: bool
    attribution_completeness: float
    duplicate_rate: float
    issues: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CollectionResult:
    source: str
    records: tuple[Mapping[str, Any], ...] = ()
    leads: tuple[RawLead, ...] = ()
    next_watermark: Mapping[str, Any] = field(default_factory=dict)
    complete: bool = False
    errors: tuple[str, ...] = ()
    detail: str = "not configured"


@dataclass(frozen=True, slots=True)
class GrowthTask:
    task_id: str
    title: str
    size: TaskSize
    priority: str
    lead_impact_score: float
    status: str = "proposed"
