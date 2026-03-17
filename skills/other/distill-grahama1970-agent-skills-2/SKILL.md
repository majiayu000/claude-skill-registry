---
name: distill
description: >
  Compatibility shim for legacy distill callers. Forwards to doc2qra entrypoint
  while preserving historical CLI flags used by memory acquire workflows.
triggers:
  - distill
  - legacy distill
  - memory acquire content
metadata:
  short-description: Legacy distill compatibility wrapper
  status: compatibility
---

# distill (compatibility)

This skill exists for backward compatibility.

- Legacy callers (for example `memory acquire content`) still invoke `distill`.
- The shim forwards arguments to:
  - `/home/graham/workspace/experiments/pi-mono/.pi/skills/doc2qra/__main__.py`

Recommended migration target:

- `/extractor --learn`

Current supported legacy flags (pass-through):

- `--file`
- `--url`
- `--text`
- `--scope`
- `--context`
- `--dry-run`
- `--json`
- `--sections-only`
- `--summary-only`
