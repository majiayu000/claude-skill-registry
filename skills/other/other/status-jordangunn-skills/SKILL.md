---
name: plan-status
license: MIT
description: >
  Display the execution status of a plan by parsing frontmatter metadata.
  Shows progress at-a-glance without requiring manual inspection of each file.
metadata:
  author: Jordan Godau
  references:
    - 01_INTENT.md
    - 02_PROCEDURE.md
  scripts:
    - status.sh
    - status.ps1
  keywords:
    - plan
    - status
    - progress
    - tracking
---

# Instructions

Read all references in `references/` before using this skill.

## Signals

- User asks "what's the status of the plan?"
- User wants to see progress on a phase
- User asks "what's done?" or "what's left?"
- Before resuming work on an existing plan

## References

**Directory:** `references/`

- `01_INTENT.md`
- `02_PROCEDURE.md`

## Scripts

**Directory:** `scripts/`

- `status.sh`: Parses frontmatter and displays plan status (macOS/Linux/WSL)
- `status.ps1`: Parses frontmatter and displays plan status (Windows)
