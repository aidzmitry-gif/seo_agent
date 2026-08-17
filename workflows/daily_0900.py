"""Safe daily 09:00 orchestration skeleton; it never deploys production changes."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from seo_agent.analysis.bottlenecks import detect_bottleneck  # noqa: E402
from seo_agent.analysis.kpi import calculate_kpis  # noqa: E402
from seo_agent.collectors import (  # noqa: E402
    Bitrix24Collector,
    GA4Collector,
    GoogleSearchConsoleCollector,
    YandexMetricaCollector,
    YandexWebmasterCollector,
)
from seo_agent.integrations.bitrix_tasks import draft_data_quality_task  # noqa: E402
from seo_agent.models import CollectionResult, RawLead  # noqa: E402
from seo_agent.processing.attribution import resolve_attribution  # noqa: E402
from seo_agent.processing.deduplicate import find_duplicate_links  # noqa: E402
from seo_agent.processing.normalize import normalize_lead  # noqa: E402
from seo_agent.processing.validation import (  # noqa: E402
    assess_qualification,
    run_data_quality_gate,
)
from seo_agent.reporting.daily_report import (  # noqa: E402
    DailyReport,
    render_daily_report,
    write_daily_report,
)
from seo_agent.settings import load_config  # noqa: E402
from seo_agent.state.watermarks import WatermarkStore  # noqa: E402


@dataclass(frozen=True, slots=True)
class DailyRunResult:
    run_date: date
    blocked: bool
    recommendation: str
    report: str
    sources: tuple[CollectionResult, ...]


def _source_watermark(state: dict[str, object], source: str) -> dict[str, object]:
    aliases = {"google_search_console": "gsc"}
    stored = state.get(aliases.get(source, source), {})
    return dict(stored) if isinstance(stored, dict) else {}


def run_daily(
    repository_root: Path = REPOSITORY_ROOT,
    run_date: date | None = None,
    *,
    write_state: bool = False,
    write_report_file: bool = False,
) -> DailyRunResult:
    """Run the safe data-quality-first path with adapters that make no network calls."""
    run_date = run_date or date.today()
    config = load_config(repository_root / "config")
    thresholds = config["thresholds"]["data_quality"]
    store = WatermarkStore(repository_root / "state" / "watermarks.json")

    if write_state and not store.claim_run(run_date):
        raise RuntimeError(f"Daily run has already been claimed: {run_date.isoformat()}")

    state = store.load()
    collectors = (
        Bitrix24Collector(),
        YandexMetricaCollector(),
        GoogleSearchConsoleCollector(),
        YandexWebmasterCollector(),
        GA4Collector(),
    )
    results = tuple(
        collector.collect_delta(_source_watermark(state, collector.name))
        for collector in collectors
    )
    # Provider-specific raw-to-domain mapping is a deliberate next integration.
    # The first-stage stubs return no records, but the full safety sequence is kept.
    raw_records: list[RawLead] = []
    normalized_records = [normalize_lead(record) for record in raw_records]
    duplicate_links = find_duplicate_links(normalized_records)
    attributions = [resolve_attribution(record) for record in normalized_records]
    incomplete_sources = tuple(result.source for result in results if not result.complete)
    quality = run_data_quality_gate(
        records=raw_records,
        attributions=attributions,
        duplicate_links=duplicate_links,
        attribution_min=float(thresholds["attribution_min"]),
        duplicate_rate_max=float(thresholds["duplicate_rate_max"]),
        api_errors=tuple(error for result in results for error in result.errors),
        incomplete_sources=incomplete_sources,
    )

    if not quality.passed:
        task = draft_data_quality_task(quality.issues)
        recommendation = f"{task.priority}: {task.title}. {task.description}"
    else:  # Kept for real configured adapters; it still recommends rather than changes production.
        duplicate_ids = {link.duplicate_record_id for link in duplicate_links}
        qualifications = [
            assess_qualification(record, record.record_id in duplicate_ids)
            for record in raw_records
        ]
        calculate_kpis(raw_records, qualifications, run_date, run_date)
        bottleneck = detect_bottleneck(quality_passed=True)
        recommendation = f"{bottleneck.rationale} Check WIP before selecting a scored task."

    report_model = DailyReport(
        run_date=run_date,
        quality=quality,
        recommendation=recommendation,
        source_statuses=tuple(f"{item.source}: {item.detail}" for item in results),
    )
    rendered_report = render_daily_report(report_model)
    if write_report_file:
        write_daily_report(report_model, repository_root / "data" / "snapshots")
    if write_state:
        for result in results:
            if result.complete:
                store.update_source(result.source, dict(result.next_watermark))
        store.complete_run(run_date)
    return DailyRunResult(run_date, not quality.passed, recommendation, rendered_report, results)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run safe 09:00 SEO Growth Agent orchestration."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Display a no-write orchestration result."
    )
    parser.add_argument(
        "--write-state", action="store_true", help="Opt in to local watermark run state."
    )
    parser.add_argument(
        "--write-report", action="store_true", help="Opt in to a local snapshot report."
    )
    arguments = parser.parse_args()
    if arguments.write_state and arguments.dry_run:
        parser.error("--dry-run cannot be combined with --write-state")
    result = run_daily(write_state=arguments.write_state, write_report_file=arguments.write_report)
    print(result.report)


if __name__ == "__main__":
    main()
