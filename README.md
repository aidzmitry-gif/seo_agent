# microchips.by SEO Growth Agent

Safety-first foundation for an SEO/CRO/GEO growth operating system whose North Star
is **qualified site leads correctly registered in Bitrix24**. It connects search
demand, website behaviour and changes to qualified leads, deals and revenue; it is
not an autonomous production deployer.

## Included in this iteration

- typed domain models, normalisation, non-destructive deduplication and formal
  attribution taxonomy;
- data-quality gate, KPI aggregation, bottleneck order and Lead Impact Score;
- per-source watermarks, change/experiment/task registries and replay protection;
- credential-free delta collector adapters, rank-tracker adapter interfaces and a
  safe 09:00 workflow skeleton;
- configuration, operating documentation and executable tests.

The Bitrix24 collector now has an injectable universal-CRM delta contract. Configure
tenant-specific contact, UTM and qualification fields under
`config/sources.yaml` → `sources.bitrix24.field_mapping`; blank values remain
unknown rather than being inferred. It still requires an explicitly approved
transport and credentials before it can call the API.

## Layout

- `config/`: policy and threshold contracts.
- `src/seo_agent/`: core processing, analysis, collectors and local state.
- `workflows/`: safe orchestration entrypoints.
- `state/`: committed empty/default local operating registers.
- `docs/`: process, KPI and governance documentation.

## Local setup and verification

Requires Python 3.11+.

```powershell
py -3 -m pip install -e ".[dev]"
py -3 -m pytest
ruff check .
python workflows/daily_0900.py --dry-run
```

Copy `.env.example` to `.env` and provide only the integrations you deliberately
enable. Never commit `.env`, exports or real credentials.

## Data-quality gate

The gate blocks SEO/CRO analysis when attribution completeness is below 95%,
duplicate rate exceeds 2%, API errors exist, or expected source data is incomplete.
It returns a P0 data-quality task instead of proposing marketing work.

## Logs and human approval

`state/change_log.json` stores significant website changes and
`state/experiments.json` stores controlled experiments. The current workflow can
collect, analyse and recommend only. Production actions require a separately
recorded human approval after staging and QA.
