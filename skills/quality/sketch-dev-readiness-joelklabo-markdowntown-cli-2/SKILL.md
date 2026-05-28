---
name: sketch-dev-readiness
description: Enforce Sketch Magic dev-readiness gates. Use when asked “are you done?”, when dev server errors appear, when proof video is required, or when verifying compile/lint/test/dev-smoke status.
---

# Sketch Dev Readiness

## Overview
Define the exact steps required before claiming work is complete: dev server health, log review, DevTools checks, proof video, and quality gates.

## Workflow (do not skip)
1. **Dev server starts cleanly**: run `pnpm dev` and confirm no build errors.
2. **Log review**: tail server output or use `pnpm dev:logs`.
3. **Dev-smoke gate**: run `pnpm dev:smoke` and confirm success.
4. **DevTools QA**: follow the DevTools QA checklist (see references).
5. **Proof video**: run `pnpm proof:video` and confirm a `.webm` artifact.
6. **Quality gates**: `pnpm compile`, `pnpm lint`, `pnpm test:unit` must be green.

## Failure rule
If any step fails or logs show errors, **do not claim done**. Create a follow-up task and fix the issue first.

## References
- `references/dev-readiness.md` — detailed gate list and log locations.
