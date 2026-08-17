from datetime import UTC, datetime
from typing import Any

from seo_agent.collectors.bitrix24 import (
    Bitrix24Collector,
    Bitrix24FieldMap,
    build_delta_params,
    map_bitrix24_item,
)


def mapping() -> Bitrix24FieldMap:
    return Bitrix24FieldMap.from_config(
        {
            "created_at": "createdTime",
            "updated_at": "updatedTime",
            "source_type": "sourceId",
            "phone": "ufPhone",
            "email": "ufEmail",
            "utm_source": "ufUtmSource",
            "utm_medium": "ufUtmMedium",
            "is_relevant": "ufRelevant",
            "sales_processable": "ufSalesProcessable",
        }
    )


def item(identifier: int, updated_at: str) -> dict[str, Any]:
    return {
        "id": identifier,
        "createdTime": "2026-08-18T09:00:00+03:00",
        "updatedTime": updated_at,
        "sourceId": "WEB",
        "originId": "form-9",
        "ufPhone": "8 (029) 123-45-67",
        "ufEmail": "Lead@Example.by",
        "ufUtmSource": "google",
        "ufUtmMedium": "cpc",
        "ufRelevant": "Y",
        "ufSalesProcessable": "1",
    }


def test_builds_inclusive_delta_request_from_watermark() -> None:
    params = build_delta_params(
        1,
        mapping(),
        {"last_updated_time": "2026-08-17T09:00:00+03:00"},
    )

    assert params["entityTypeId"] == 1
    assert params["filter"] == {">=updatedTime": "2026-08-17T09:00:00+03:00"}
    assert params["order"] == {"updatedTime": "ASC", "id": "ASC"}
    assert params["select"] == [
        "id",
        "createdTime",
        "updatedTime",
        "sourceId",
        "originId",
        "ufPhone",
        "ufEmail",
        "ufUtmSource",
        "ufUtmMedium",
        "ufRelevant",
        "ufSalesProcessable",
    ]


def test_maps_configured_bitrix24_fields_without_guessing() -> None:
    lead = map_bitrix24_item(item(100, "2026-08-18T10:00:00+03:00"), mapping())

    assert lead.record_id == "bitrix24:100"
    assert lead.crm_id == "100"
    assert lead.source_type == "WEB"
    assert lead.phone == "8 (029) 123-45-67"
    assert lead.email == "Lead@Example.by"
    assert lead.is_relevant is True
    assert lead.sales_processable is True
    assert lead.metadata["ufUtmSource"] == "google"


def test_collects_all_pages_and_advances_watermark() -> None:
    calls: list[tuple[str, dict[str, Any]]] = []
    pages = [
        {"result": {"items": [item(100, "2026-08-18T10:00:00+03:00")]}, "next": 50},
        {"result": {"items": [item(101, "2026-08-18T11:00:00+03:00")] }},
    ]

    def transport(method: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((method, params))
        return pages.pop(0)

    collector = Bitrix24Collector(
        transport,
        field_map=mapping(),
        now=lambda: datetime(2026, 8, 18, 9, 30, tzinfo=UTC),
    )

    result = collector.collect_delta({"last_updated_time": "2026-08-17T09:00:00+03:00"})

    assert result.complete
    assert len(result.records) == 2
    assert [lead.record_id for lead in result.leads] == ["bitrix24:100", "bitrix24:101"]
    assert result.next_watermark == {
        "last_success": "2026-08-18T09:30:00+00:00",
        "last_updated_time": "2026-08-18T11:00:00+03:00",
        "last_id": "101",
    }
    assert [params["start"] for _, params in calls] == [0, 50]
    assert all(method == "crm.item.list" for method, _ in calls)


def test_stub_makes_no_transport_call_without_injection() -> None:
    result = Bitrix24Collector().collect_delta({"last_id": "100"})

    assert not result.complete
    assert result.records == ()
    assert result.leads == ()
