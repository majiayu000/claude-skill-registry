---
name: frontend-quality-bar
description: Enforce a high-quality, production-ready standard for changes in this Next.js + Chakra UI frontend repo. Use for UX polish, accessibility, performance, error/loading states, code hygiene, and “ready to merge” checks (lint/format/build).
---

# Frontend Quality Bar (Stacked Poker)

## Always start here

1. Read `.cursor/rules/frontend-guidelines.mdc` (project expectations).
2. Identify the user-facing surface (page/component) and list required states:
   - loading, empty, error, success
3. Prefer small, incremental changes; avoid broad refactors unless requested.

## Definition of done (minimum)

- UI has loading/error handling for async work that affects UX.
- No console errors in normal flows; logs are purposeful for debugging only.
- Accessibility basics: labels, keyboard access, focus visibility.
- Responsive: works in both portrait/landscape where applicable.
- Styling uses theme tokens/semantic tokens (no random hexes).

## Commands

- `npm run lint`
- `npm run build`
- `npm run format` (when touching many files)

For convenience, run `scripts/quality.sh` from this skill.

## What to load next

- For a detailed PR checklist: read `references/checklist.md`.
- For perf/a11y patterns that match this repo: read `references/perf-a11y.md`.

