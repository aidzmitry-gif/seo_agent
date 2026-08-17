"""Form-friction observation contract."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FormObservation:
    form_id: str
    event: str
    count: int
