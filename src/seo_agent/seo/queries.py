"""Query clustering contract."""

from __future__ import annotations


def normalize_query(query: str) -> str:
    return " ".join(query.casefold().split())
