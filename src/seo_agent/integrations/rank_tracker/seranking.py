"""SE Ranking placeholder adapter."""

from __future__ import annotations


class SERankingAdapter:
    provider = "seranking"

    def collect_positions(self, queries: list[str], region: str) -> list[dict[str, object]]:
        raise NotImplementedError("Configure the SE Ranking adapter after provider selection.")
