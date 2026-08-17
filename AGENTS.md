# microchips.by SEO Growth Agent

## North Star and decision rule

North Star: `qualified_site_leads` — site-originated leads that pass the configured
qualification rules and are traceable to Bitrix24. Traffic, ranking and pages are
leading indicators only. Before any work, state the plausible link to this metric.

## Operating boundaries

- Follow `DATA → PROBLEM → HYPOTHESIS → ACTION → QA → MEASUREMENT → DECISION`.
- Prefer deltas and watermarks; never silently replay full history.
- Keep raw data immutable. Deduplication creates links to a master entity, never
  deletes source records.
- Stop SEO/CRO analysis when the data-quality gate fails. Create a P0 data task.
- Respect WIP: one large and two small active tasks at most.
- Production is never automatic. The permitted path is read, analyse, recommend,
  create change, test, stage, QA, explicit human approval, then production.
- Do not put credentials, customer data, raw exports or generated snapshots in Git.

## Development rules

- Implement collectors as credential-free delta interfaces first; an adapter may
  not make outbound calls merely by import or dry-run.
- Validate every behaviour with focused tests. Run `py -3 -m pytest` and
  `ruff check .` before proposing a commit.
- Record material website changes in `state/change_log.json` and experiments in
  `state/experiments.json`, including a review date and rollback/next action.
