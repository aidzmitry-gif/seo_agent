# Operations and safety

Use `python workflows/daily_0900.py --dry-run` for a no-network, no-state-write
orchestration preview. A real adapter must be explicitly configured with credentials
and tested against a limited delta. State writes are opt-in and are restricted to
local watermark/report/task files.

No collector deploys SEO changes, sends Bitrix tasks, or changes production. Those
operations require staging evidence, QA and human approval at the time of action.
