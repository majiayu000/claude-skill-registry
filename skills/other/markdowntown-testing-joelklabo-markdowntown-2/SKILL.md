---
name: markdowntown-testing
description: Use this when running or adding tests (compile/lint/unit/E2E), updating test utilities, or working with Playwright/visual testing in markdowntown.
---

# Testing + Playwright E2E

## When to use
- Adding or updating unit/integration tests.
- Running the required CI checks before commit.
- Designing or debugging Playwright/E2E flows.

## Required checks (default workflow)
1. `npm run compile`
2. `npm run lint`
3. `npm run test:unit`

## E2E + visual tests
- `npm run test:e2e` runs Vitest E2E with `vitest.e2e.config.ts`.
- `npm run test:visual` runs Playwright visual tests (`playwright-visual.config.ts`).
- Set `E2E_BASE_URL` if you need a non-default host.

## Workflow guidance
- Prefer **small, focused** unit tests in `__tests__` for components and lib helpers.
- When adding a new user flow, update the E2E narratives so behavior stays aligned.
- If a test fails due to output changes, update snapshots/fixtures and document why.

## References
- codex/skills/markdowntown-testing/references/tests.md
- codex/skills/markdowntown-testing/references/playwright.md

## Guardrails
- Keep tests deterministic; avoid time-based flakiness where possible.
- Always record refactors/bugs discovered as follow-up bd tasks.
