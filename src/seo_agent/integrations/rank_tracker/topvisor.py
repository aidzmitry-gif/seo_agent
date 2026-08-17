"""Topvisor placeholder adapter."""

from __future__ import annotations


class TopvisorAdapter:
    provider = "topvisor"

    def collect_positions(self, queries: list[str], region: str) -> list[dict[str, object]]:
        raise NotImplementedError("Configure the Topvisor adapter after provider selection.")
