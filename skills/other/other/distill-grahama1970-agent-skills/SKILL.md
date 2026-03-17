---
name: distill
description: >
  Compatibility shim for legacy distill callers. Forwards to /doc2qra
  while preserving the historical CLI interface.
triggers:
  - distill
  - legacy distill
  - memory acquire content
metadata:
  short-description: Legacy distill compatibility wrapper
  status: compatibility

provides:
  - distill
composes:
  - doc2qra
  - task-monitor
---

# distill (compatibility)

This skill exists for backward compatibility. Forwards to `/doc2qra`.

- Legacy callers (for example `memory acquire content`) still invoke `distill`.
- The shim forwards all arguments directly to `/doc2qra`.

Supported flags (passed through to doc2qra):

- `--file` — PDF, markdown, or text file
- `--url` — URL to fetch and distill
- `--text` — Raw text to distill
- `--scope` — Memory scope
- `--persona` — Persona for quality gating
- `--json` — JSON output
- `--dry-run` — Preview without storing
- `--context` — Domain focus
