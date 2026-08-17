# KPI contract

`qualified_site_leads` counts leads whose source is the website and whose flags
meet every configured qualification requirement. `raw_site_leads`, deals, won
deals, revenue, conversion rates, revenue per lead and first response time are
reported as supporting business KPI.

Daily comparisons use yesterday, 7 vs previous 7 days, 28 vs previous 28 days,
and the 90-day baseline. Results must be segmentable by the dimensions in
`config/kpi.yaml`; unavailable dimensions are reported as missing, not invented.
