---
name: aim-parzival-constraints
description: Load Parzival behavioral constraints as context reminder
allowed-tools: Bash
---

# Parzival Constraints — Active Reminder

Load Parzival's behavioral constraints from `_ai-memory/pov/constraints/`. Used during session activation, after compaction, or when Parzival seems to be drifting.

## Steps

1. Run the following Python script to load constraints:

```python
import sys
import os
import time

# Set up import path for ai-memory source
_install_dir = os.path.expanduser("~/.ai-memory")
sys.path.insert(0, os.path.join(_install_dir, "src"))

start_ms = time.perf_counter()

try:
    from memory.injection import load_parzival_constraints
except ImportError as e:
    print("## Parzival Constraints (Active Reminder)\n")
    print(f"**Unavailable**: AI Memory module not installed ({e})")
    sys.exit(0)

# Optional: Prometheus metrics (best-effort)
try:
    from memory.metrics_push import push_skill_metrics_async
except ImportError:
    push_skill_metrics_async = None

project_root = os.getcwd()

# Check for --phase argument
phase = None
for i, arg in enumerate(sys.argv):
    if arg == "--phase" and i + 1 < len(sys.argv):
        phase = sys.argv[i + 1]

# Load constraints
constraints = load_parzival_constraints(project_root, phase=phase)
elapsed_ms = int((time.perf_counter() - start_ms) * 1000)

print("## Parzival Constraints (Active Reminder)\n")

if not constraints:
    print("No constraint files found at `_ai-memory/pov/constraints/`.\n")
    print("Ensure Parzival v2 is installed with constraint files.")
    print(f"\n---\nConstraints: 0 loaded | {elapsed_ms}ms")
    if push_skill_metrics_async:
        try:
            push_skill_metrics_async("aim-parzival-constraints", "empty", time.perf_counter() - start_ms)
        except Exception:
            pass
else:
    print(constraints)
    if push_skill_metrics_async:
        try:
            push_skill_metrics_async("aim-parzival-constraints", "success", time.perf_counter() - start_ms)
        except Exception:
            pass

# Skill tracing (PLAN-014 G-06)
try:
    from memory.trace_buffer import emit_trace_event
    emit_trace_event(
        event_type="skill_execution",
        data={
            "input": f"Skill: aim-parzival-constraints"[:10000],
            "output": f"Result: completed"[:10000],
            "metadata": {"skill_name": "aim-parzival-constraints"},
        },
        session_id=os.environ.get("CLAUDE_SESSION_ID", "unknown"),
        tags=["skill"],
    )
except Exception:
    pass  # Tracing failures never break skill execution
```

2. Internalize the constraints as active behavioral rules for the remainder of this session.

3. If no constraints are found, continue without — file-based context (MEMORY.md, oversight/) provides sufficient guidance.
