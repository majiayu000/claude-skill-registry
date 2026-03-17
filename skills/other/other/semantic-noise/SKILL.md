---
name: refactor-semantic-noise
license: MIT
description: |
  Audit semantic noise and namespace integrity.
  Produces a severity-grouped report with namespace/rename suggestions.
metadata:
  author: Jordan Godau
  references:
    - 01_GOAL.md
    - 02_DEFINITIONS.md
    - 03_INVARIANTS.md
    - 04_SCOPE.md
    - 05_CHECKS.md
    - 06_OUTPUT.md
  keywords:
    - semantic
    - noise
    - namespace
    - prefix
    - suffix
    - redundant
    - taxonomy
    - boundary
---

# Instructions

Read all references in `references/` before using this skill.

## Signals

- Reviewing naming for redundant prefixes/suffixes
- Import stutter or taxonomy crammed into identifiers
- Missing structural boundaries indicated by naming clusters
- The user asks to "audit naming" or "check namespace integrity"

## References

**Directory:** `references/`

- `01_GOAL.md`
- `02_DEFINITIONS.md`
- `03_INVARIANTS.md`
- `04_SCOPE.md`
- `05_CHECKS.md`
- `06_OUTPUT.md`
