"""Per-source watermark and daily-run replay protection."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


class WatermarkStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"runs": {}}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Watermark state must be an object: {self.path}")
        data.setdefault("runs", {})
        return data

    def has_completed_run(self, run_date: date) -> bool:
        run = self.load()["runs"].get(run_date.isoformat(), {})
        return run.get("status") == "complete"

    def claim_run(self, run_date: date) -> bool:
        state = self.load()
        runs = state["runs"]
        key = run_date.isoformat()
        if key in runs:
            return False
        runs[key] = {"status": "running"}
        self._write(state)
        return True

    def complete_run(self, run_date: date) -> None:
        state = self.load()
        state["runs"][run_date.isoformat()] = {"status": "complete"}
        self._write(state)

    def update_source(self, source: str, watermark: dict[str, Any]) -> None:
        state = self.load()
        state[source] = watermark
        self._write(state)

    def _write(self, state: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(f"{self.path.suffix}.tmp")
        temporary.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
        temporary.replace(self.path)
