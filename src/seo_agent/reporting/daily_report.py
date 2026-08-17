"""Daily report rendering without any external publication side effect."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from seo_agent.models import DataQualityResult


@dataclass(frozen=True, slots=True)
class DailyReport:
    run_date: date
    quality: DataQualityResult
    recommendation: str
    source_statuses: tuple[str, ...]


def render_daily_report(report: DailyReport) -> str:
    quality_status = "passed" if report.quality.passed else "blocked"
    issues = ", ".join(report.quality.issues) or "none"
    sources = "\n".join(f"- {status}" for status in report.source_statuses)
    return (
        f"# Daily growth report — {report.run_date.isoformat()}\n\n"
        f"Data-quality gate: **{quality_status}**\n\n"
        f"- Attribution completeness: {report.quality.attribution_completeness:.1%}\n"
        f"- Duplicate rate: {report.quality.duplicate_rate:.1%}\n"
        f"- Blocking issues: {issues}\n\n"
        f"## Source status\n{sources}\n\n"
        f"## Decision\n{report.recommendation}\n"
    )


def write_daily_report(report: DailyReport, directory: Path) -> Path:
    """Write only to a caller-selected local directory."""
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / f"daily-{report.run_date.isoformat()}.md"
    destination.write_text(render_daily_report(report), encoding="utf-8")
    return destination
