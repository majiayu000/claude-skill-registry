---
name: refactor-dictionaries
license: MIT
description: |
  Audit dictionary usage against the Dictionary Usage Doctrine.
  Produces a severity-grouped report with minimal refactor suggestions.
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
    - dictionary
    - dict
    - typing
    - public API
    - type safety
    - dataclass
    - TypedDict
---

# Instructions

Read all references in `references/` before using this skill.

## Signals

- Reviewing public APIs for improper dict usage
- Detecting dynamic-vs-known structure violations
- Dictionaries crossing module boundaries or encoding state
- The user asks to "audit dictionaries" or "check dict usage"

## References

**Directory:** `references/`

- `01_GOAL.md`
- `02_DEFINITIONS.md`
- `03_INVARIANTS.md`
- `04_SCOPE.md`
- `05_CHECKS.md`
- `06_OUTPUT.md`
