---
name: refactor-squatters
license: MIT
description: |
  Detect squatters: modules and packages that occupy namespace positions
  they do not semantically own. Identifies utility dumps, stuttery siblings,
  axis violations, layer bleeding, and semantic diffusion — common structural
  smells introduced by agentic programming.
metadata:
  author: Jordan Godau
  references:
    - 01_GOAL.md
    - 02_DEFINITIONS.md
    - 03_INVARIANTS.md
    - 04_HEURISTICS.md
    - 05_PROCEDURE.md
    - 06_REMEDIATION.md
    - 07_OUTPUT.md
  scripts:
    - detect.sh
    - detect.ps1
  keywords:
    - squatters
    - namespace
    - integrity
    - wrong home
    - misplaced
    - utility dump
    - common
    - helpers
    - utils
    - stutter
    - sibling
    - axis violation
    - layer bleeding
    - semantic diffusion
    - homeless concept
---

# Instructions

Read all references in `references/` before using this skill.

## What is a Squatter?

A **squatter** is a module or package that occupies a namespace position it does not semantically own.

In real estate, squatters occupy property without legal claim. In codebases, squatters occupy import paths without conceptual legitimacy. They exist because:

1. **Agentic programming** prioritizes "make it work" over "make it belong"
2. **Domain modeling was deferred** — the code landed somewhere expedient
3. **Compensatory naming** masked the misplacement (e.g., `las_fields.py` instead of `las/fields.py`)

Squatters degrade navigability. A developer (or agent) cannot guess where code lives because the filesystem lies about ownership.

## Central Invariant

> Every module should be importable from a path that a domain expert would guess correctly.

If a module name compensates for weak structure, or sits beside a package it should be inside, the filesystem is lying about the domain model.

## Signals

- Reviewing package structure after significant growth
- Noticing `common/`, `utils/`, or `helpers/` packages
- Seeing modules with underscore prefixes matching sibling package names (e.g., `las_fields.py` beside `las/`)
- Finding single-function modules that only wrap a foreign dependency
- Observing imports that cross architectural layers upward

## References

**Directory:** `references/`

- `01_GOAL.md` — What this skill accomplishes
- `02_DEFINITIONS.md` — Vocabulary for squatters and namespace violations
- `03_INVARIANTS.md` — Rules that determine violations
- `04_HEURISTICS.md` — Detection patterns and signals
- `05_PROCEDURE.md` — Step-by-step audit process
- `06_REMEDIATION.md` — Refactoring directions (hypotheses, not mandates)
- `07_OUTPUT.md` — Report format and severity classification

## Scripts

**Directory:** `scripts/`

- `detect.sh`: Scan for structural smells (macOS/Linux/WSL)
- `detect.ps1`: Scan for structural smells (Windows)

## Usage

```bash
# Scan a package for squatters
.codex/skills/refactor/squatters/scripts/detect.sh pulsar/api

# Scan with specific pattern focus
.codex/skills/refactor/squatters/scripts/detect.sh pulsar/api --pattern utility-dump
.codex/skills/refactor/squatters/scripts/detect.sh pulsar/api --pattern stuttery-sibling
```
