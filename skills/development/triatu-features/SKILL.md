---
name: triatu-features
description: "Feature module organization for Triatu (features/*). Use when creating or migrating a feature, adding components/hooks/logic, or writing feature-level docs."
---

# Triatu Features

## Quick start

- Each feature lives in `features/<feature>/`.
- Keep feature code local unless it is truly shared across multiple features.
- Provide `README.md` per feature with entry points, key flows, and tests.

## Expected structure

- `features/<feature>/components`
- `features/<feature>/hooks`
- `features/<feature>/logic`
- `features/<feature>/__tests__`
- `features/<feature>/index.ts`
- `features/<feature>/README.md`

## Workflow

1) Inventory existing UI in `components/` and move feature-specific parts under the feature.
2) Export public surface from `features/<feature>/index.ts`.
3) Add `data-testid` hooks for e2e flows when needed.
4) Write or migrate tests into `features/<feature>/__tests__`.
5) Update feature `README.md` and link from main docs if needed.

## References

- `docs/DEVELOPMENT.md`
- `tests/README.md`
- `features/*/README.md`
