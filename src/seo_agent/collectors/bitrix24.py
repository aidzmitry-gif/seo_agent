"""Safe universal-CRM delta collector and explicit Bitrix24 field mapping."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, fields
from datetime import UTC, datetime
from typing import Any

from seo_agent.models import CollectionResult, RawLead

Bitrix24Transport = Callable[[str, Mapping[str, Any]], Mapping[str, Any]]
_MAPPABLE_FIELDS = {
    "created_at",
    "updated_at",
    "source_type",
    "origin_id",
    "phone",
    "email",
    "call_external_id",
    "form_request_id",
    "utm_source",
    "utm_medium",
    "referrer",
    "landing_url",
    "is_spam",
    "is_test",
    "is_relevant",
    "sales_processable",
}


@dataclass(frozen=True, slots=True)
class Bitrix24FieldMap:
    """Maps tenant-specific universal CRM fields to the stable lead contract."""

    created_at: str = "createdTime"
    updated_at: str = "updatedTime"
    source_type: str = "sourceId"
    origin_id: str | None = "originId"
    phone: str | None = None
    email: str | None = None
    call_external_id: str | None = None
    form_request_id: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    referrer: str | None = None
    landing_url: str | None = None
    is_spam: str | None = None
    is_test: str | None = None
    is_relevant: str | None = None
    sales_processable: str | None = None

    @classmethod
    def from_config(cls, values: Mapping[str, Any] | None) -> Bitrix24FieldMap:
        if values is None:
            return cls()
        unknown = set(values) - _MAPPABLE_FIELDS
        if unknown:
            raise ValueError(f"Unknown Bitrix24 field mappings: {sorted(unknown)}")
        normalized = {
            key: value.strip() if isinstance(value, str) and value.strip() else None
            for key, value in values.items()
        }
        for required in ("created_at", "updated_at", "source_type"):
            if required in normalized and normalized[required] is None:
                raise ValueError(f"Bitrix24 mapping is required: {required}")
        return cls(**normalized)

    def selected_fields(self) -> list[str]:
        selected = ["id"]
        for field in fields(self):
            value = getattr(self, field.name)
            if value and value not in selected:
                selected.append(value)
        return selected


def build_delta_params(
    entity_type_id: int,
    field_map: Bitrix24FieldMap,
    watermark: Mapping[str, Any],
    start: int = 0,
) -> dict[str, Any]:
    """Build one `crm.item.list` page request without sending it."""
    if entity_type_id <= 0:
        raise ValueError("entity_type_id must be positive")
    params: dict[str, Any] = {
        "entityTypeId": entity_type_id,
        "select": field_map.selected_fields(),
        "order": {field_map.updated_at: "ASC", "id": "ASC"},
        "start": start,
    }
    last_updated = watermark.get("last_updated_time")
    if isinstance(last_updated, str) and last_updated:
        params["filter"] = {f">={field_map.updated_at}": last_updated}
    return params


def map_bitrix24_item(item: Mapping[str, Any], field_map: Bitrix24FieldMap) -> RawLead:
    """Map one raw CRM item without guessing absent custom fields."""
    crm_id = _required_text(item.get("id"), "id")
    created_at = _parse_iso_datetime(item.get(field_map.created_at), field_map.created_at)
    source_type = _text(item.get(field_map.source_type)) or "unknown"
    return RawLead(
        record_id=f"bitrix24:{crm_id}",
        crm_id=crm_id,
        source_type=source_type,
        created_at=created_at,
        origin_id=_mapped_text(item, field_map.origin_id),
        phone=_mapped_text(item, field_map.phone),
        email=_mapped_text(item, field_map.email),
        call_external_id=_mapped_text(item, field_map.call_external_id),
        form_request_id=_mapped_text(item, field_map.form_request_id),
        utm_source=_mapped_text(item, field_map.utm_source),
        utm_medium=_mapped_text(item, field_map.utm_medium),
        referrer=_mapped_text(item, field_map.referrer),
        landing_url=_mapped_text(item, field_map.landing_url),
        is_spam=_mapped_bool(item, field_map.is_spam) is True,
        is_test=_mapped_bool(item, field_map.is_test) is True,
        is_relevant=_mapped_bool(item, field_map.is_relevant),
        sales_processable=_mapped_bool(item, field_map.sales_processable),
        metadata=dict(item),
    )


class Bitrix24Collector:
    """Collects universal CRM deltas only when an explicit transport is injected."""

    name = "bitrix24"

    def __init__(
        self,
        transport: Bitrix24Transport | None = None,
        *,
        entity_type_id: int = 1,
        field_map: Bitrix24FieldMap | None = None,
        max_pages: int = 1000,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        if max_pages <= 0:
            raise ValueError("max_pages must be positive")
        self._transport = transport
        self.entity_type_id = entity_type_id
        self.field_map = field_map or Bitrix24FieldMap()
        self.max_pages = max_pages
        self._now = now or (lambda: datetime.now(UTC))

    def collect_delta(self, watermark: dict[str, Any]) -> CollectionResult:
        if self._transport is None:
            return CollectionResult(
                source=self.name,
                next_watermark=watermark,
                detail="stub: inject an approved Bitrix24 universal-CRM transport",
            )
        try:
            records = self._collect_pages(watermark)
            leads = tuple(map_bitrix24_item(record, self.field_map) for record in records)
            next_watermark = self._next_watermark(records, watermark)
            return CollectionResult(
                source=self.name,
                records=tuple(records),
                leads=leads,
                next_watermark=next_watermark,
                complete=True,
                detail="universal CRM delta collected",
            )
        except Exception:
            return CollectionResult(
                source=self.name,
                next_watermark=watermark,
                errors=("bitrix24_delta_contract_error",),
                detail="Bitrix24 delta rejected; inspect field mapping and response contract",
            )

    def _collect_pages(self, watermark: Mapping[str, Any]) -> list[Mapping[str, Any]]:
        records: list[Mapping[str, Any]] = []
        start = 0
        for _ in range(self.max_pages):
            response = self._transport(
                "crm.item.list",
                build_delta_params(self.entity_type_id, self.field_map, watermark, start),
            )
            page = _extract_items(response)
            records.extend(page)
            next_start = _extract_next(response)
            if next_start is None:
                return records
            if next_start <= start:
                raise ValueError("Bitrix24 pagination did not advance")
            start = next_start
        raise ValueError("Bitrix24 pagination limit reached")

    def _next_watermark(
        self, records: list[Mapping[str, Any]], previous: Mapping[str, Any]
    ) -> dict[str, Any]:
        if not records:
            return dict(previous)
        newest = max(
            records,
            key=lambda item: (
                _parse_iso_datetime(item.get(self.field_map.updated_at), self.field_map.updated_at),
                _id_sort_key(item.get("id")),
            ),
        )
        return {
            "last_success": self._now().astimezone(UTC).isoformat(),
            "last_updated_time": _required_text(
                newest.get(self.field_map.updated_at), self.field_map.updated_at
            ),
            "last_id": _required_text(newest.get("id"), "id"),
        }


def _extract_items(response: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    result = response.get("result", response)
    if not isinstance(result, Mapping):
        raise ValueError("Bitrix24 response result must be a mapping")
    items = result.get("items", ())
    if not isinstance(items, list) or not all(isinstance(item, Mapping) for item in items):
        raise ValueError("Bitrix24 response items must be a list of mappings")
    return items


def _extract_next(response: Mapping[str, Any]) -> int | None:
    next_value = response.get("next")
    if next_value is None and isinstance(response.get("result"), Mapping):
        next_value = response["result"].get("next")
    if next_value is None:
        return None
    try:
        return int(next_value)
    except (TypeError, ValueError) as error:
        raise ValueError("Bitrix24 response next must be an integer") from error


def _required_text(value: Any, field_name: str) -> str:
    text = _text(value)
    if text is None:
        raise ValueError(f"Bitrix24 field is required: {field_name}")
    return text


def _mapped_text(item: Mapping[str, Any], field_name: str | None) -> str | None:
    return _text(item.get(field_name)) if field_name else None


def _text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (str, int, float)):
        text = str(value).strip()
        return text or None
    return None


def _mapped_bool(item: Mapping[str, Any], field_name: str | None) -> bool | None:
    if not field_name:
        return None
    value = item.get(field_name)
    if isinstance(value, bool):
        return value
    text = _text(value)
    if text is None:
        return None
    if text.casefold() in {"y", "yes", "true", "1"}:
        return True
    if text.casefold() in {"n", "no", "false", "0"}:
        return False
    raise ValueError(f"Bitrix24 boolean field has unsupported value: {field_name}")


def _parse_iso_datetime(value: Any, field_name: str) -> datetime:
    text = _required_text(value, field_name)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"Bitrix24 datetime field is invalid: {field_name}") from error
    if parsed.tzinfo is None:
        raise ValueError(f"Bitrix24 datetime field requires timezone: {field_name}")
    return parsed


def _id_sort_key(value: Any) -> tuple[int, int | str]:
    text = _required_text(value, "id")
    return (0, int(text)) if text.isdecimal() else (1, text)
