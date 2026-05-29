---
name: aim-status
description: 'Check AI Memory system status'
trigger: "/aim-status"
---

```python
"""Memory status skill: /aim-status

Check AI Memory Module health, statistics, and system state.

Usage:
    /aim-status                     # Full status report
    /aim-status --section sync      # Sync status only
    /aim-status --section freshness # Freshness summary only
    /aim-status --section decay     # Decay distribution only
    /aim-status --section flags     # System flags only
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_install_dir = os.path.expanduser("~/.ai-memory")
sys.path.insert(0, os.path.join(_install_dir, "src"))

from memory.config import (
    COLLECTION_CODE_PATTERNS,
    COLLECTION_CONVENTIONS,
    COLLECTION_DISCUSSIONS,
    get_config,
)
from memory.qdrant_client import get_qdrant_client
from memory.metrics_push import push_skill_metrics_async


def _time_ago(iso_ts: str) -> str:
    """Return human-readable relative time from ISO 8601 timestamp."""
    try:
        ts = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - ts
        hours = int(delta.total_seconds() / 3600)
        if hours < 1:
            minutes = int(delta.total_seconds() / 60)
            return f"{minutes}m ago"
        elif hours < 48:
            return f"{hours}h ago"
        else:
            return f"{delta.days}d ago"
    except Exception:
        return ""


def _bar(count: int, max_count: int, width: int = 12) -> str:
    """Build ASCII bar proportional to count/max_count."""
    if max_count == 0:
        return ""
    filled = int(round(width * count / max_count))
    return "█" * filled


def section_health(config, client) -> list[str]:
    """Health: service availability."""
    lines = ["Health"]
    services = [
        ("Qdrant", f"{config.qdrant_host}:{config.qdrant_port}"),
        ("Embedding", f"{config.embedding_host}:{config.embedding_port}"),
        ("Monitoring", f"{config.monitoring_host}:{config.monitoring_port}"),
    ]
    for name, endpoint in services:
        try:
            if name == "Qdrant":
                client.get_collections()
                status = "ok"
            else:
                import urllib.request
                urllib.request.urlopen(f"http://{endpoint}/health", timeout=2)
                status = "ok"
        except Exception:
            status = "unavailable"
        lines.append(f"  {name}: {status} ({endpoint})")
    return lines


def section_collections(config, client) -> list[str]:
    """Collections: point counts and disk size."""
    lines = ["Collections"]
    collections = [
        COLLECTION_CODE_PATTERNS,
        COLLECTION_CONVENTIONS,
        COLLECTION_DISCUSSIONS,
    ]
    for coll in collections:
        try:
            info = client.get_collection(coll)
            count = info.points_count or 0
            # Disk size not directly available — estimate from vectors_count
            lines.append(f"  {coll}: {count} points")
        except Exception:
            lines.append(f"  {coll}: unavailable")
    return lines


def section_services(config, client) -> list[str]:
    """Services: detailed service status."""
    lines = ["Services"]
    try:
        health = client.get_collection(COLLECTION_CODE_PATTERNS)
        lines.append(f"  Qdrant:      running | port {config.qdrant_port}")
    except Exception:
        lines.append(f"  Qdrant:      down    | port {config.qdrant_port}")

    lines.append(f"  Embedding:   port {config.embedding_port}")
    lines.append(f"  Monitoring:  port {config.monitoring_port}")
    lines.append(f"  Grafana:     port 23000")
    lines.append(f"  Pushgateway: port 29091")
    return lines


def section_sync(config) -> list[str]:
    """Sync Status: last sync time, items, errors."""
    lines = ["Sync Status"]
    sync_state_path = Path(config.audit_dir) / "state" / "github_sync_state.json"

    if not config.github_sync_enabled:
        lines.append("  GitHub Sync: disabled")
        return lines

    if not sync_state_path.exists():
        lines.append("  No sync history found")
        lines.append("  GitHub Sync: enabled")
        return lines

    try:
        with open(sync_state_path) as f:
            state = json.load(f)

        # State schema: {type_key: {last_synced: ISO, last_count: int}}
        # e.g. {"pull_requests": {"last_synced": "...", "last_count": 5}, ...}
        type_entries = {k: v for k, v in state.items() if isinstance(v, dict)}

        # Most recent last_synced across all types
        last_synced_times = [v.get("last_synced", "") for v in type_entries.values() if v.get("last_synced")]
        last_sync = max(last_synced_times) if last_synced_times else ""

        # Total items and per-type breakdown
        total = sum(v.get("last_count", 0) for v in type_entries.values())
        parts = [f"{v.get('last_count', 0)} {k}" for k, v in type_entries.items() if v.get("last_count")]
        breakdown = f" ({', '.join(parts)})" if parts else ""

        ago = _time_ago(last_sync) if last_sync else ""
        ago_str = f" ({ago})" if ago else ""
        lines.append(f"  Last Sync: {last_sync}{ago_str}")
        lines.append(f"  Items Synced: {total}{breakdown}")
        lines.append(f"  GitHub Sync: enabled")
    except Exception as e:
        lines.append(f"  Sync state unreadable: {e}")

    return lines


def section_freshness(config) -> list[str]:
    """Freshness Summary: fresh/aging/stale/expired counts."""
    lines = ["Freshness Summary"]

    if not config.freshness_enabled:
        lines.append("  Freshness: disabled")
        return lines

    try:
        from memory.freshness import run_freshness_scan
        report = run_freshness_scan(config=config, cwd=os.getcwd())
        lines.append(
            f"  Fresh: {report.fresh_count} | "
            f"Aging: {report.aging_count} | "
            f"Stale: {report.stale_count} | "
            f"Expired: {report.expired_count}"
        )
        lines.append("  Coverage: code-patterns only (conventions/discussions exempt)")
    except Exception as e:
        lines.append(f"  Freshness scan unavailable ({e})")

    return lines


def section_decay(config, client) -> list[str]:
    """Decay Distribution: sample 50 vectors per collection, bucket by 0.2."""
    lines = ["Decay Distribution"]
    collections = [
        (COLLECTION_CODE_PATTERNS, config.decay_half_life_code_patterns),
        (COLLECTION_CONVENTIONS, config.decay_half_life_conventions),
        (COLLECTION_DISCUSSIONS, config.decay_half_life_discussions),
    ]

    # Parse decay_type_overrides for per-type half-lives
    type_overrides: dict[str, int] = {}
    for entry in config.decay_type_overrides.split(","):
        parts = entry.strip().split(":")
        if len(parts) == 2:
            try:
                type_overrides[parts[0]] = int(parts[1])
            except ValueError:
                pass

    buckets = [0] * 5  # [0-0.2), [0.2-0.4), [0.4-0.6), [0.6-0.8), [0.8-1.0]
    total_sampled = 0

    try:
        for coll, default_half_life in collections:
            try:
                points = client.scroll(
                    collection_name=coll,
                    limit=50,
                    with_payload=True,
                    with_vectors=False,
                )[0]
                now = datetime.now(timezone.utc)
                for point in points:
                    payload = point.payload or {}
                    stored_at = payload.get("stored_at") or payload.get("timestamp", "")
                    memory_type = payload.get("type", "")
                    half_life = type_overrides.get(memory_type, default_half_life)
                    if stored_at:
                        try:
                            ts = datetime.fromisoformat(stored_at.replace("Z", "+00:00"))
                            age_days = (now - ts).days
                            temporal_score = 0.5 ** (age_days / half_life)
                        except Exception:
                            temporal_score = 0.5
                    else:
                        temporal_score = 0.5
                    bucket_idx = min(int(temporal_score / 0.2), 4)
                    buckets[bucket_idx] += 1
                    total_sampled += 1
            except Exception:
                continue

        if total_sampled == 0:
            lines.append("  No vectors to sample")
            return lines

        lines.append(f"(sampled {total_sampled} vectors)")
        max_count = max(buckets) if buckets else 1
        labels = [
            ("0.8-1.0 (fresh) ", 4),
            ("0.6-0.8 (recent)", 3),
            ("0.4-0.6 (aging) ", 2),
            ("0.2-0.4 (old)   ", 1),
            ("0.0-0.2 (stale) ", 0),
        ]
        for label, idx in labels:
            bar = _bar(buckets[idx], max_count)
            lines.append(f"  {label}: {bar} {buckets[idx]}")
    except Exception as e:
        lines.append(f"  Decay distribution unavailable ({e})")

    return lines


def section_flags(config) -> list[str]:
    """System Flags: key feature toggles."""
    lines = ["System Flags"]
    flags = [
        ("Auto-update", config.auto_update_enabled),
        ("Freshness", config.freshness_enabled),
        ("GitHub Sync", config.github_sync_enabled),
        ("Parzival", config.parzival_enabled),
    ]
    for name, enabled in flags:
        status = "enabled" if enabled else "disabled"
        lines.append(f"  {name}: {status}")
    return lines


def main() -> None:
    """Entry point for /aim-status skill."""
    import argparse

    start_time = time.perf_counter()
    parser = argparse.ArgumentParser(description="Memory system status")
    parser.add_argument(
        "--section",
        choices=["sync", "freshness", "decay", "flags"],
        help="Show only a specific section",
    )
    args = parser.parse_args()

    config = get_config()

    try:
        client = get_qdrant_client(config)
        qdrant_ok = True
    except Exception:
        client = None
        qdrant_ok = False

    sections_to_show = args.section

    output_lines: list[str] = []

    # Always show header
    output_lines.append("## Memory System Status")
    output_lines.append("")

    if sections_to_show is None or sections_to_show not in ("sync", "freshness", "decay", "flags"):
        # Full report: show all sections
        if qdrant_ok:
            output_lines.extend(section_health(config, client))
            output_lines.append("")
            output_lines.extend(section_collections(config, client))
            output_lines.append("")
            output_lines.extend(section_services(config, client))
            output_lines.append("")
        else:
            output_lines.append("Health")
            output_lines.append("  Qdrant: unavailable")
            output_lines.append("")

    if sections_to_show is None or sections_to_show == "sync":
        output_lines.extend(section_sync(config))
        output_lines.append("")

    if sections_to_show is None or sections_to_show == "freshness":
        output_lines.extend(section_freshness(config))
        output_lines.append("")

    if sections_to_show is None or sections_to_show == "decay":
        if qdrant_ok:
            output_lines.extend(section_decay(config, client))
        else:
            output_lines.append("Decay Distribution")
            output_lines.append("  Decay distribution unavailable (Qdrant offline)")
        output_lines.append("")

    if sections_to_show is None or sections_to_show == "flags":
        output_lines.extend(section_flags(config))
        output_lines.append("")

    # Output budget note
    output_lines.append("─" * 40)
    output_lines.append("Output budget: < 2K tokens")

    print("\n".join(output_lines))

    duration = time.perf_counter() - start_time
    push_skill_metrics_async("memory-status", "success", duration)

    # Skill tracing (PLAN-014 G-06)
    try:
        from memory.trace_buffer import emit_trace_event
        emit_trace_event(
            event_type="skill_execution",
            data={
                "input": f"Skill: aim-status"[:10000],
                "output": f"Result: completed"[:10000],
                "metadata": {"skill_name": "aim-status"},
            },
            session_id=os.environ.get("CLAUDE_SESSION_ID", "unknown"),
            tags=["skill"],
        )
    except Exception:
        pass  # Tracing failures never break skill execution


if __name__ == "__main__":
    main()
```

## Usage

```bash
# Full status report
/aim-status

# Show specific sections only
/aim-status --section sync
/aim-status --section freshness
/aim-status --section decay
/aim-status --section flags
```

## Output Sections

### Health
Shows service availability for Qdrant, Embedding service, and Monitoring API.

### Collections
Point counts per collection:
- **code-patterns** - Project-specific implementation patterns
- **conventions** - Cross-project shared conventions
- **discussions** - Decision context and session summaries

### Services
Detailed service status with port numbers.

### Sync Status
GitHub synchronization state from `.audit/state/github_sync_state.json`:
- Last sync time (with relative time)
- Items synced (with breakdown by type)
- Error count
- GitHub Sync enabled/disabled

Fallback: "No sync history found" if state file doesn't exist.

### Freshness Summary
Code-patterns freshness classification from `run_freshness_scan()`:
- **Fresh** - Content matches, low commit activity
- **Aging** - Some commit activity since stored
- **Stale** - Significant commit activity
- **Expired** - High activity or content changed

Fallback: "Freshness scan unavailable" if no git context.

### Decay Distribution
Temporal decay score distribution from a 50-vector sample per collection.
Decay formula: `temporal_score = 0.5 ^ (age_days / half_life)`
Bucketed into 5 bands: 0.8-1.0 (fresh), 0.6-0.8 (recent), 0.4-0.6 (aging),
0.2-0.4 (old), 0.0-0.2 (stale).

Fallback: "Decay distribution unavailable" if sampling fails.

### System Flags
Key feature toggles from configuration:
- **Auto-update**: `auto_update_enabled`
- **Freshness**: `freshness_enabled`
- **GitHub Sync**: `github_sync_enabled`
- **Parzival**: `parzival_enabled`

## Notes

- Output budget: < 2K tokens total
- Each section handles graceful fallback when data unavailable
- Qdrant connection uses port 26350 with API key authentication
- Metrics pushed via `push_skill_metrics_async` on completion
