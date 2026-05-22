---
name: simplify
description: ruthlessly simplify systems (delete first, DRY, SSOT, leverage libraries)
---

Our code should be as simple as possible. Default to **deleting** and **centralizing**.

## Core Moves

- Question requirements first: what can we remove or narrow?
- Delete unused code, obsolete flags, dead paths, and premature abstractions.
- Enforce SSOT: business rules, validation, enums, constants live in one place.
- DRY duplicated logic: extract shared helpers/components only when it genuinely reduces complexity.
- Prefer established libraries over custom boilerplate.

## Practical Commands (When Useful)

- `scc . --include-ext ts,tsx --by-file` (hotspots by size/complexity)
- `codefetch` (if installed; convert code into markdown for review)
- `knip` (dead code / unused exports)
- `jscpd` (duplication; scope with `--pattern` to avoid noise, e.g. `components/**/*.tsx`)
- `rg` (fast, precise code search)

## Recurring Pain Points (Watch For)

- `useEffect` that’s doing non-external sync work (often removable)
  - See `~/.config/docs/React/ReactEffectsGuide.md`

## Output Format

- What to delete (highest leverage first)
- What to consolidate into SSOT
- What to replace with a library (if any)
- Minimal migration steps
