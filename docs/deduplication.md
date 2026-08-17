# Deduplication

Raw records are immutable. The pipeline produces normalized records, duplicate
candidates and a master-entity link. Exact CRM ID, `ORIGIN_ID`, call external ID
and form request ID are strong evidence. Normalized phone or email may link records
only when source type matches and timestamps are inside the configured temporal
window. Every duplicate stores the reason and the master record ID.
