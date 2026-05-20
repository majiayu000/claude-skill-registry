---
name: pymc-bayesian-modeling
description: Compatibility alias for the descriptive PyMC skill name. Delegate to the canonical local `pymc` payload while preserving route and README compatibility.
---

# pymc-bayesian-modeling (Compatibility Alias)

## Purpose

Provide a stable descriptive alias for Bayesian modeling workflows that are
canonically maintained under the sibling `pymc` skill directory.

This preserves:

- README-facing descriptive naming
- existing `skills-lock` and catalog entries
- route compatibility for callers that still ask for `pymc-bayesian-modeling`

## Resolution Order

1. Use the canonical local `pymc` skill payload first.
2. Reuse its assets, references, and scripts:
   - `../pymc/SKILL.md`
   - `../pymc/assets/**`
   - `../pymc/references/**`
   - `../pymc/scripts/**`
3. Keep this alias thin and free of its own duplicated heavy payload.

## Minimal Workflow

1. Read `../pymc/SKILL.md` for the full PyMC workflow.
2. Use the canonical templates and diagnostic scripts from `../pymc/`.
3. Report results under the requested alias name only for user-facing continuity.
