---
name: triatu-testing
description: "Testing workflow for Triatu (TDD, Vitest, Playwright). Use when adding tests, fixing failing suites, or setting up e2e flows."
---

# Triatu Testing

## Quick start

- TDD required: write test first, then code.
- Unit/integration: Vitest.
- E2E: Playwright under `tests/e2e`.

## Commands

- `pnpm test` (Vitest)
- `pnpm test:e2e` (Playwright)
- `pnpm exec playwright test --ui` (interactive)
- `pnpm exec playwright test --headed` (visible browser)

## Workflow

1) Add stable `data-testid` in UI for any e2e interaction.
2) Keep Vitest tests under `tests/`, `features/`, or `lib/`.
3) Keep Playwright tests under `tests/e2e/` only.
4) For e2e that touches Supabase, require:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `NEXT_PUBLIC_E2E=true` (if used)
5) Clean up seeded data at the end of each e2e run.

## References

- `docs/DEVELOPMENT.md`
- `tests/README.md`
