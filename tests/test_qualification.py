from datetime import datetime

from seo_agent.models import RawLead
from seo_agent.processing.validation import assess_qualification


def lead(**kwargs: object) -> RawLead:
    return RawLead("lead-1", "website", datetime(2026, 8, 17), **kwargs)


def test_qualification_requires_all_explicit_flags() -> None:
    qualified = assess_qualification(lead(is_relevant=True, sales_processable=True))
    incomplete = assess_qualification(lead(is_relevant=True))

    assert qualified.qualified
    assert qualified.disqual_reason is None
    assert not incomplete.qualified
    assert incomplete.disqual_reason == "cannot_be_processed"


def test_qualification_uses_controlled_duplicate_reason() -> None:
    result = assess_qualification(lead(is_relevant=True, sales_processable=True), is_duplicate=True)

    assert result.disqual_reason == "duplicate"
