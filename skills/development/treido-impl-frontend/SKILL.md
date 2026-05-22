---
name: treido-impl-frontend
description: "Frontend implementer for Treido (patches code). Executes audit findings/tasks with Tailwind v4 + shadcn + next-intl rails. Trigger: FE-IMPL"
---

# Treido Frontend Implementer (Writes Code)

You **do patch files**. Only proceed if you are the designated **single writer** for this batch.

## Workflow (Execute a Planned Task)

1. Read the source of truth for work:
   - `TASKS.md` (active tasks + acceptance checks)
   - linked audit artifact under `audit/`
2. Pick a **1–3 file batch**; avoid unrelated refactors.
3. Implement with Treido rails:
   - Server Components by default; add `"use client"` only when required
   - All user-facing strings via `next-intl` (`messages/en.json`, `messages/bg.json`)
   - Tailwind v4 only: **no gradients**, **no arbitrary values**, **no palette colors**
   - Keep `components/ui/*` as primitives only; compose in `components/shared/*` or route-private `_components/*`
4. Do not edit `TASKS.md`. Report back: task ID(s), files changed, and verification results.
5. Verify.

## Verification (Always)

```bash
pnpm -s typecheck
pnpm -s lint
pnpm -s styles:gate
```

## Helpful Commands (Optional)

```bash
rg -n "\"use client\"" app components
rg -n "\\[[^\\]]+\\]" app components
```

## Handoff Signal

- `OPUS: review?` when cross-boundary/risky
- `DONE (no review needed)` otherwise
