---
name: aim-purge
description: "Purge old memories from Qdrant collections with safety guards"
trigger: "/aim-purge"
---

```python
"""Memory purge skill: /aim-purge

Purge old memories from Qdrant collections with safety guards.

Usage:
    /aim-purge --older-than 30d              # Dry-run (preview)
    /aim-purge --older-than 30d --confirm    # Execute purge
    /aim-purge --older-than 90d --collection code-patterns
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

_install_dir = os.path.expanduser("~/.ai-memory")
sys.path.insert(0, os.path.join(_install_dir, "src"))

from memory.config import (
    COLLECTION_CODE_PATTERNS,
    COLLECTION_CONVENTIONS,
    COLLECTION_DISCUSSIONS,
    COLLECTION_JIRA_DATA,
    get_config,
)
from memory.qdrant_client import get_qdrant_client
from memory.metrics_push import push_skill_metrics_async

from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue,
    Range,
)

ALL_COLLECTIONS = [
    COLLECTION_CODE_PATTERNS,
    COLLECTION_CONVENTIONS,
    COLLECTION_DISCUSSIONS,
    COLLECTION_JIRA_DATA,
]


def parse_duration(duration_str: str) -> timedelta:
    """Parse duration string like '30d', '2w', '3m', '1y' to timedelta.

    Args:
        duration_str: Duration in format <number><unit>.

    Returns:
        timedelta representing the duration.

    Raises:
        ValueError: If format is invalid.
    """
    match = re.match(r"^(\d+)([dwmy])$", duration_str.strip())
    if not match:
        raise ValueError(
            f"Invalid duration: '{duration_str}'. "
            f"Use format: <number><unit> where unit = d/w/m/y"
        )
    value = int(match.group(1))
    unit = match.group(2)
    if unit == "d":
        return timedelta(days=value)
    elif unit == "w":
        return timedelta(weeks=value)
    elif unit == "m":
        return timedelta(days=value * 30)  # Approximate
    elif unit == "y":
        return timedelta(days=value * 365)  # Approximate
    raise ValueError(f"Unknown unit: {unit}")


def scan_purgeable(client, collections, group_id, cutoff_iso):
    """Scroll collections and return point IDs older than cutoff.

    Args:
        client: QdrantClient instance.
        collections: List of collection names to scan.
        group_id: Project group_id filter (None = all projects).
        cutoff_iso: ISO 8601 cutoff timestamp string.

    Returns:
        Dict mapping collection -> list of (point_id, type, timestamp).
    """
    results = {}
    for collection in collections:
        points_to_purge = []
        must_conditions = [
            FieldCondition(
                key="timestamp",
                range=Range(lt=cutoff_iso),
            ),
        ]
        if group_id:
            must_conditions.append(
                FieldCondition(
                    key="group_id",
                    match=MatchValue(value=group_id),
                )
            )

        offset = None
        while True:
            points, next_offset = client.scroll(
                collection_name=collection,
                scroll_filter=Filter(must=must_conditions),
                limit=100,
                offset=offset,
                with_payload=["type", "timestamp"],
            )
            for point in points:
                payload = point.payload or {}
                points_to_purge.append((
                    point.id,
                    payload.get("type", "unknown"),
                    payload.get("timestamp", "unknown"),
                ))
            if next_offset is None:
                break
            offset = next_offset

        if points_to_purge:
            results[collection] = points_to_purge
    return results


def format_dry_run(purgeable, cutoff_dt):
    """Format dry-run preview output."""
    lines = ["## Memory Purge — Dry Run", ""]
    lines.append(f"**Cutoff**: Memories stored before {cutoff_dt.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")

    total = 0
    for collection, points in purgeable.items():
        lines.append(f"### {collection}: {len(points)} memories")
        # Type breakdown
        type_counts = {}
        for _, mtype, _ in points:
            type_counts[mtype] = type_counts.get(mtype, 0) + 1
        for mtype, count in sorted(type_counts.items()):
            lines.append(f"  - {mtype}: {count}")
        total += len(points)

    lines.append("")
    lines.append(f"**Total**: {total} memories would be purged")
    lines.append("")
    lines.append("Re-run with `--confirm` to execute purge.")
    return "\n".join(lines)


def execute_purge(client, purgeable):
    """Delete purgeable points from Qdrant.

    Returns:
        Dict mapping collection -> count deleted.
    """
    deleted = {}
    for collection, points in purgeable.items():
        point_ids = [pid for pid, _, _ in points]
        # Delete in batches of 100
        for i in range(0, len(point_ids), 100):
            batch = point_ids[i : i + 100]
            client.delete(
                collection_name=collection,
                points_selector=batch,
            )
        deleted[collection] = len(point_ids)
    return deleted


def log_purge(purgeable, deleted, cutoff_iso, cwd):
    """Append purge record to audit log."""
    log_path = Path(cwd) / ".audit" / "logs" / "purge-log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cutoff": cutoff_iso,
        "collections": {
            col: len(pts) for col, pts in purgeable.items()
        },
        "deleted": deleted,
    }
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    """Entry point for /aim-purge skill."""
    parser = argparse.ArgumentParser(description="Purge old memories")
    parser.add_argument("--older-than", required=True, help="Duration (e.g., 30d, 2w, 3m, 1y)")
    parser.add_argument("--collection", help="Limit to one collection")
    parser.add_argument("--confirm", action="store_true", help="Execute purge (default is dry-run)")
    args = parser.parse_args()

    start_time = time.perf_counter()
    config = get_config()

    try:
        duration = parse_duration(args.older_than)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if duration == timedelta(0):
        print("Warning: --older-than 0d targets ALL memories in scope. Use with extreme caution.")

    cutoff_dt = datetime.now(timezone.utc) - duration
    cutoff_iso = cutoff_dt.isoformat()

    collections = ALL_COLLECTIONS
    if args.collection:
        if args.collection not in ALL_COLLECTIONS:
            print(f"Error: Unknown collection '{args.collection}'. Valid: {ALL_COLLECTIONS}")
            sys.exit(1)
        collections = [args.collection]

    # Resolve group_id for project scoping
    import os
    group_id = os.environ.get("AI_MEMORY_GROUP_ID") or Path.cwd().name

    try:
        client = get_qdrant_client(config)
    except Exception as e:
        print(f"Error: Cannot connect to Qdrant: {e}")
        sys.exit(1)

    purgeable = scan_purgeable(client, collections, group_id, cutoff_iso)

    if not purgeable:
        print(f"No memories found older than {args.older_than} for project '{group_id}'.")
        push_skill_metrics_async("memory-purge", "empty", time.perf_counter() - start_time)
        return

    if not args.confirm:
        print(format_dry_run(purgeable, cutoff_dt))
        push_skill_metrics_async("memory-purge", "success", time.perf_counter() - start_time)
        return

    # Execute purge
    deleted = execute_purge(client, purgeable)
    log_purge(purgeable, deleted, cutoff_iso, os.getcwd())

    # Summary
    total = sum(deleted.values())
    print(f"## Memory Purge Complete")
    print(f"")
    print(f"**Purged {total} memories** older than {args.older_than}")
    for col, count in deleted.items():
        print(f"  - {col}: {count}")
    print(f"")
    print(f"Audit log: `.audit/logs/purge-log.jsonl`")

    push_skill_metrics_async("memory-purge", "success", time.perf_counter() - start_time)

    # Skill tracing (PLAN-014 G-06)
    try:
        from memory.trace_buffer import emit_trace_event
        emit_trace_event(
            event_type="skill_execution",
            data={
                "input": f"Skill: aim-purge"[:10000],
                "output": f"Result: completed"[:10000],
                "metadata": {"skill_name": "aim-purge"},
            },
            session_id=os.environ.get("CLAUDE_SESSION_ID", "unknown"),
            tags=["skill"],
        )
    except Exception:
        pass  # Tracing failures never break skill execution


if __name__ == "__main__":
    main()
```
