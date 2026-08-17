# Data model

The core entity is a raw lead record with immutable source payload and normalized
contact/attribution fields. Deduplication emits a link from duplicate to master;
qualification emits a boolean and a controlled disqualification code. KPI snapshots
aggregate qualified and raw leads without overwriting source facts. Watermarks are
per source and daily-run claims prevent accidental replay.
