---
name: refactor-import-hygiene
license: MIT
description: |
  Audit Python imports to preserve semantic context and prevent shadowing after refactors.
  Prefer namespace-first imports over direct symbol imports for generic identifiers.
metadata:
  author: Jordan Godau
  references:
    - 01_GOAL.md
    - 02_DEFINITION.md
    - 03_RULES.md
    - 04_PROCEDURE.md
    - 05_OUTPUT.md
    - 06_EXAMPLES.md
  keywords:
    - import
    - imports
    - namespace
    - shadowing
    - collision
    - from import
    - symbol
---

# Instructions

Read all references in `references/` before using this skill.

## Signals

- Module-stutter was removed and symbols became intentionally generic (Metadata, Spec, File, Header, Payload)
- A refactor moved code into new namespaces and callsites were updated
- The diff introduces many `from X import Y` imports
- There are repeated name collisions or ambiguous identifiers in local scopes

## References

**Directory:** `references/`

- `01_GOAL.md`
- `02_DEFINITION.md`
- `03_RULES.md`
- `04_PROCEDURE.md`
- `05_OUTPUT.md`
- `06_EXAMPLES.md`
