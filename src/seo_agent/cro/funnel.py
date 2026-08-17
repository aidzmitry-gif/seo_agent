"""Funnel measurement record."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FunnelStep:
    name: str
    visitors: int
    qualified_leads: int
