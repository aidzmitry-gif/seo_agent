from datetime import date, datetime

from seo_agent.analysis.kpi import calculate_kpis, change_ratio
from seo_agent.models import Qualification, RawLead


def test_calculates_qualified_site_lead_rate() -> None:
    records = [
        RawLead("a", "website", datetime(2026, 8, 17), landing_url="https://microchips.by/a"),
        RawLead("b", "phone", datetime(2026, 8, 17)),
    ]
    qualifications = [Qualification("a", True, None), Qualification("b", True, None)]

    snapshot = calculate_kpis(records, qualifications, date(2026, 8, 17), date(2026, 8, 17))

    assert snapshot.raw_site_leads == 1
    assert snapshot.qualified_site_leads == 1
    assert snapshot.qualification_rate == 1.0
    assert change_ratio(12, 10) == 0.2
    assert change_ratio(1, 0) is None
