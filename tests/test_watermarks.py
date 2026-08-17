from datetime import date

from seo_agent.state.watermarks import WatermarkStore


def test_claim_prevents_replay_and_complete_marks_success(tmp_path) -> None:
    store = WatermarkStore(tmp_path / "watermarks.json")
    run_date = date(2026, 8, 17)

    assert store.claim_run(run_date)
    assert not store.claim_run(run_date)
    assert not store.has_completed_run(run_date)

    store.complete_run(run_date)

    assert store.has_completed_run(run_date)


def test_source_watermark_is_persisted(tmp_path) -> None:
    store = WatermarkStore(tmp_path / "watermarks.json")

    store.update_source("bitrix24", {"last_id": "100", "last_success": "2026-08-17T09:01:00Z"})

    assert store.load()["bitrix24"]["last_id"] == "100"
