"""WIP guard for human-approved work items."""

from __future__ import annotations

from collections.abc import Iterable

from seo_agent.models import GrowthTask, TaskSize


def can_start_task(
    active_tasks: Iterable[GrowthTask],
    candidate: GrowthTask,
    large_limit: int = 1,
    small_limit: int = 2,
) -> bool:
    active = [task for task in active_tasks if task.status == "active"]
    same_size = sum(task.size is candidate.size for task in active)
    limit = large_limit if candidate.size is TaskSize.LARGE else small_limit
    return same_size < limit
