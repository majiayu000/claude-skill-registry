---
name: refactor-module-stutter
license: MIT
description: |
  Detect module/package name stutter in Python public APIs.
  Produces a Markdown report and optional CI gate.
metadata:
  author: Jordan Godau
  references:
    - 01_GOAL.md
    - 02_DEFINITION.md
    - 03_RULES.md
    - 04_ENFORCEMENT.md
    - 05_CONFIGURATIONS.md
    - 06_OUTPUT.md
    - 07_SUGGESTIONS.md
    - 08_EXAMPLES.md
  scripts:
    - checker.py
    - pylint.py
  keywords:
    - stutter
    - naming
    - module
    - package
    - redundant
    - prefix
    - public API
---

# Instructions

Read all references in `references/` before using this skill.

## Signals

- Reviewing new modules or public symbols
- Auditing naming conventions before a release
- The user asks to "check for stutter" or "audit naming"

## References

**Directory:** `references/`

- `01_GOAL.md`
- `02_DEFINITION.md`
- `03_RULES.md`
- `04_ENFORCEMENT.md`
- `05_CONFIGURATIONS.md`
- `06_OUTPUT.md`
- `07_SUGGESTIONS.md`
- `08_EXAMPLES.md`

## Scripts

**Directory:** `scripts/`

- `checker.py`: AST-based checker + report
- `pylint.py`: Pylint plugin that provides lint-level enforcement.
