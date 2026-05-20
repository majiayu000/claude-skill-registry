---
name: parzival-save-handoff
description: "Save Parzival session handoff document to Qdrant for cross-session memory"
---

"""Save Parzival handoff to Qdrant: /parzival-save-handoff

Called by parzival-closeout command after creating the handoff file.
Stores the handoff content to Qdrant discussions collection with
type=agent_handoff, agent_id=parzival.

Usage:
    /parzival-save-handoff "PM #54: Phase 1d scoping complete..."
    /parzival-save-handoff --file oversight/session-logs/SESSION_HANDOFF_2026-02-16_PM54.md
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

_install_dir = os.path.expanduser("~/.ai-memory")
sys.path.insert(0, os.path.join(_install_dir, "src"))

from memory.config import get_config
from memory.storage import MemoryStorage
from memory.metrics_push import push_skill_metrics_async


def main():
    start_time = time.perf_counter()
    config = get_config()

    if not config.parzival_enabled:
        print("Parzival is not enabled. Set PARZIVAL_ENABLED=true in .env.")
        return

    # Accept content as argument or --file path
    content = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "--file" and len(sys.argv) > 2:
            file_path = Path(sys.argv[2])
            if not file_path.is_absolute():
                file_path = Path.cwd() / file_path
            if file_path.exists():
                content = file_path.read_text(encoding="utf-8")
            else:
                print(f"Error: File not found: {file_path}")
                sys.exit(1)
        else:
            content = " ".join(sys.argv[1:])

    if not content:
        print("Error: No content provided. Pass text or --file <path>.")
        sys.exit(1)

    storage = MemoryStorage(config)
    try:
        result = storage.store_agent_memory(
            content=content,
            memory_type="agent_handoff",
            agent_id="parzival",
            cwd=os.getcwd(),
        )
    except Exception as e:
        print(f"Warning: Failed to save handoff to Qdrant: {e}")
        print("Closeout continues — file write is the primary record.")
        push_skill_metrics_async("parzival-save-handoff", "error", time.perf_counter() - start_time)
        return

    status = result.get("status", "unknown")
    if status == "stored":
        print(f"Handoff saved to Qdrant (id: {result.get('memory_id', 'unknown')[:8]}...)")
    elif status == "duplicate":
        print("Handoff already exists in Qdrant (duplicate detected).")
    else:
        print(f"Handoff storage result: {status}")

    metric_status = "success" if status in ("stored", "duplicate") else "error"
    push_skill_metrics_async("parzival-save-handoff", metric_status, time.perf_counter() - start_time)

    # Skill tracing (PLAN-014 G-06)
    try:
        from memory.trace_buffer import emit_trace_event
        emit_trace_event(
            event_type="skill_execution",
            data={
                "input": f"Skill: parzival-save-handoff"[:10000],
                "output": f"Result: completed"[:10000],
                "metadata": {"skill_name": "parzival-save-handoff"},
            },
            session_id=os.environ.get("CLAUDE_SESSION_ID", "unknown"),
            tags=["skill"],
        )
    except Exception:
        pass  # Tracing failures never break skill execution


if __name__ == "__main__":
    main()
