---
name: aim-parzival-bootstrap
description: Load Parzival cross-session memory from Qdrant
allowed-tools: Bash
---

# Parzival Bootstrap — Cross-Session Memory

Load cross-session context from previous Parzival sessions stored in Qdrant. This replaces the automatic startup injection with an on-demand skill invocation.

## Steps

1. Run the following Python script to retrieve cross-session context:

```python
import sys
import os
import time
from datetime import datetime, timezone

# Set up import path for ai-memory source
_install_dir = os.path.expanduser("~/.ai-memory")
sys.path.insert(0, os.path.join(_install_dir, "src"))

start_ms = time.perf_counter()
_trace_start = datetime.now(tz=timezone.utc)

try:
    from memory.config import MemoryConfig
    from memory.search import MemorySearch
    from memory.injection import (
        retrieve_bootstrap_context,
        select_results_greedy,
        format_injection_output,
        init_session_state,
        log_injection_event,
    )
    from memory.project import detect_project
    from memory.qdrant_client import QdrantUnavailable
except ImportError as e:
    print(f"## Cross-Session Memory (Parzival Bootstrap)\n")
    print(f"**Unavailable**: AI Memory module not installed ({e})")
    print(f"\nBootstrap: import error | Qdrant: unknown")
    sys.exit(0)

# Optional: Prometheus metrics (best-effort, never blocks)
try:
    from memory.metrics_push import push_skill_metrics_async
except ImportError:
    push_skill_metrics_async = None

# Optional: Langfuse trace events (best-effort, never blocks)
# LANGFUSE: V3 ONLY. See LANGFUSE-INTEGRATION-SPEC.md
try:
    from memory.trace_buffer import emit_trace_event
except ImportError:
    emit_trace_event = None

TRACE_CONTENT_MAX = 10000

try:
    config = MemoryConfig()
except Exception as e:
    print(f"## Cross-Session Memory (Parzival Bootstrap)\n")
    print(f"**Unavailable**: Failed to load configuration ({e})")
    print(f"\nBootstrap: config error | Qdrant: unknown")
    sys.exit(0)

if not config.parzival_enabled:
    print("## Cross-Session Memory (Parzival Bootstrap)\n")
    print("Parzival is not enabled. Set `PARZIVAL_ENABLED=true` in .env to activate.")
    sys.exit(0)

try:
    project_name = detect_project(os.getcwd())
    search_client = MemorySearch(config)
    session_id = os.environ.get("CLAUDE_SESSION_ID", "unknown")

    # Retrieve bootstrap context from Qdrant
    results = retrieve_bootstrap_context(search_client, project_name, config)

    # Greedy-fill within token budget
    selected, tokens_used = select_results_greedy(results, config.bootstrap_token_budget)

    # Format as markdown with attribution
    formatted = format_injection_output(selected, tier=1)

    elapsed_ms = int((time.perf_counter() - start_ms) * 1000)
    duration_seconds = time.perf_counter() - start_ms

    # Initialize session state for Tier 2 deduplication (HIGH)
    injected_ids = [str(r.get("id", "")) for r in selected if r.get("id")]
    init_session_state(session_id, injected_ids)

    # Audit log (HIGH)
    from pathlib import Path
    audit_dir = Path(os.getcwd()) / ".audit"
    log_injection_event(
        tier=1,
        trigger="skill:aim-parzival-bootstrap",
        project=project_name,
        session_id=session_id,
        results_considered=len(results),
        results_selected=len(selected),
        tokens_used=tokens_used,
        budget=config.bootstrap_token_budget,
        audit_dir=audit_dir,
    )

    # Build output
    print("## Cross-Session Memory (Parzival Bootstrap)\n")

    if not selected:
        print("No cross-session memories found for this project.\n")
    else:
        # Group results by type for organized display
        handoffs = [r for r in selected if r.get("type") == "agent_handoff"]
        decisions = [r for r in selected if r.get("type") in ("decision", "agent_memory")]
        insights = [r for r in selected if r.get("type") == "agent_insight"]
        github = [r for r in selected if r.get("type", "").startswith("github_")]
        other = [r for r in selected if r not in handoffs + decisions + insights + github]

        if handoffs:
            print("### Last Handoff\n")
            for h in handoffs:
                print(h.get("content", "").strip())
                print()

        if decisions:
            print("### Recent Decisions\n")
            for d in decisions:
                score_pct = int(d.get("score", 0) * 100)
                print(f"- **[{score_pct}%]** {d.get('content', '').strip()[:200]}")
            print()

        if insights:
            print("### Insights\n")
            for i in insights:
                score_pct = int(i.get("score", 0) * 100)
                print(f"- **[{score_pct}%]** {i.get('content', '').strip()[:200]}")
            print()

        if github:
            print("### GitHub Activity (since last session)\n")
            for g in github:
                score_pct = int(g.get("score", 0) * 100)
                print(f"- **[{g.get('type', 'github')}|{score_pct}%]** {g.get('content', '').strip()[:200]}")
            print()

        if other:
            print("### Other Context\n")
            for o in other:
                score_pct = int(o.get("score", 0) * 100)
                print(f"- **[{o.get('type', 'unknown')}|{score_pct}%]** {o.get('content', '').strip()[:200]}")
            print()

        # Include raw formatted output for full context
        print("<details><summary>Raw retrieved context</summary>\n")
        print(formatted)
        print("\n</details>\n")

    print("---")
    print(f"Bootstrap: {len(selected)} results | {tokens_used} tokens | {elapsed_ms}ms | Qdrant: available")

    # Prometheus metrics (CRITICAL — best-effort, never blocks)
    if push_skill_metrics_async:
        try:
            push_skill_metrics_async(
                "aim-parzival-bootstrap",
                "success" if selected else "empty",
                duration_seconds,
            )
        except Exception:
            pass

    # Top-level Langfuse trace (MEDIUM — best-effort, never blocks)
    # LANGFUSE: V3 trace buffer pattern. See LANGFUSE-INTEGRATION-SPEC.md §3.1
    if emit_trace_event:
        try:
            emit_trace_event(
                event_type="skill_bootstrap",
                data={
                    "input": f"Parzival bootstrap skill for project: {project_name}",
                    "output": f"Selected {len(selected)} results, {tokens_used} tokens, {elapsed_ms}ms"[:TRACE_CONTENT_MAX],
                    "metadata": {
                        "skill_name": "aim-parzival-bootstrap",
                        "project_name": project_name,
                        "results_considered": len(results),
                        "results_selected": len(selected),
                        "tokens_used": tokens_used,
                        "elapsed_ms": elapsed_ms,
                        "agent_name": os.environ.get("CLAUDE_AGENT_NAME", "main"),
                        "agent_role": os.environ.get("CLAUDE_AGENT_ROLE", "user"),
                    },
                },
                project_id=project_name,
                session_id=session_id,
                start_time=_trace_start,
                end_time=datetime.now(tz=timezone.utc),
                tags=["skill", "bootstrap"],
            )
        except Exception:
            pass

except (QdrantUnavailable, ConnectionError, TimeoutError) as e:
    elapsed_ms = int((time.perf_counter() - start_ms) * 1000)
    print("## Cross-Session Memory (Parzival Bootstrap)\n")
    print(f"**Qdrant unavailable**: {e}\n")
    print("Continuing with file-based context only.\n")
    print("---")
    print(f"Bootstrap: 0 results | 0 tokens | {elapsed_ms}ms | Qdrant: unavailable")
    if push_skill_metrics_async:
        try:
            push_skill_metrics_async("aim-parzival-bootstrap", "failed", time.perf_counter() - start_ms)
        except Exception:
            pass

except Exception as e:
    elapsed_ms = int((time.perf_counter() - start_ms) * 1000)
    error_type = type(e).__name__
    print("## Cross-Session Memory (Parzival Bootstrap)\n")
    print(f"**Error retrieving context**: {error_type}: {e}\n")
    print("Continuing with file-based context only.\n")
    print("---")
    print(f"Bootstrap: 0 results | 0 tokens | {elapsed_ms}ms | Qdrant: error")
    if push_skill_metrics_async:
        try:
            push_skill_metrics_async("aim-parzival-bootstrap", "failed", time.perf_counter() - start_ms)
        except Exception:
            pass
```

2. Include the script output in your current context as cross-session memory from previous Parzival sessions.

3. If the script reports Qdrant unavailable or an error, note this and continue with file-based context only (MEMORY.md, oversight/ files).
