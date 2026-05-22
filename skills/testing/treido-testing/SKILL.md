```skill
---
name: treido-testing
description: |
  Testing expert for Treido marketplace covering Playwright E2E and Vitest unit tests.
  Triggers: test, testing, e2e, playwright, vitest, unit test, spec, fixture, mock,
  assertion, coverage, CI, smoke test, regression, selector, data-testid, getByRole,
  getByTestId, test isolation, flaky test, test timeout, jsdom, chromium, webkit.
  NOT for: i18n parity tests (treido-i18n), auth logic (treido-backend), UI styling (treido-design).
---

# treido-testing

> Testing orchestrator for Treido's Playwright E2E and Vitest unit test suites.

## Quick Reference

| Setting | Value |
|---------|-------|
| E2E Framework | Playwright |
| Unit Framework | Vitest + @testing-library |
| E2E Projects | chromium, firefox, webkit, mobile-chrome, mobile-safari, accessibility |
| Unit Environment | jsdom |
| Base Fixture | `e2e/fixtures/base.ts` |
| Test Setup | `test/setup.ts` |
| Coverage Target | 80% lines |
| Test Timeout | 60s (E2E), default (unit) |

---

## Test Scripts

| Script | Purpose |
|--------|---------|
| `pnpm test:unit` | Run all unit tests |
| `pnpm test:unit:watch` | Watch mode |
| `pnpm test:unit:coverage` | With coverage report |
| `pnpm test:e2e` | Chromium E2E (no a11y) |
| `pnpm test:e2e:smoke` | Smoke tests only |
| `pnpm test:e2e:headed` | Browser UI visible |
| `pnpm test:a11y` | Accessibility tests |
| `pnpm test:ci` | CI pipeline (unit + build + E2E) |

---

## Rule ID Reference

### CRITICAL Rules

| Rule ID | Summary | Details |
|---------|---------|---------|
| `test-e2e-fixture` | Use `app` fixture from base.ts | [playwright.md](references/playwright.md) |
| `test-e2e-selector` | Prefer getByRole over CSS | [playwright.md](references/playwright.md) |
| `test-isolation` | No shared state between tests | [patterns.md](references/patterns.md) |
| `test-no-hardcoded-wait` | Never use hardcoded timeouts | [patterns.md](references/patterns.md) |

### HIGH Rules

| Rule ID | Summary | Details |
|---------|---------|---------|
| `test-e2e-auth` | Use auth fixtures, not login flow | [playwright.md](references/playwright.md) |
| `test-unit-mock` | Use vi.mock() for module mocking | [vitest.md](references/vitest.md) |
| `test-unit-async` | Always await async operations | [vitest.md](references/vitest.md) |
| `test-naming` | Descriptive test names with context | [patterns.md](references/patterns.md) |

### MEDIUM Rules

| Rule ID | Summary | Details |
|---------|---------|---------|
| `test-e2e-hydration` | Wait for hydration before interactions | [playwright.md](references/playwright.md) |
| `test-unit-cleanup` | Tests auto-cleanup via vitest config | [vitest.md](references/vitest.md) |
| `test-ci-parallel` | Workers=1 on CI for stability | [ci.md](references/ci.md) |
| `test-reuse-server` | Use existing server for faster local runs | [ci.md](references/ci.md) |

---

## Forbidden Patterns

| Pattern | Why Forbidden | Correct Approach |
|---------|---------------|------------------|
| `page.waitForTimeout(5000)` | Flaky, arbitrary delay | `waitForHydration()` or `expect().toBeVisible()` |
| `page.locator('.my-class')` | Brittle CSS selector | `page.getByRole('button', { name: /submit/i })` |
| Login flow in each test | Slow, brittle | Auth fixtures (`loginWithPassword` once) |
| `test.only` left in code | Skips other tests | Remove before commit (enforced on CI) |
| Shared mutable state | Test pollution | Fresh setup per test |
| `vi.mock()` without reset | Mock leaks | `vi.resetAllMocks()` in beforeEach |
| Hardcoded URLs | Environment-specific | Use `baseURL` from config |
| `setTimeout` in tests | Flaky timing | `vi.useFakeTimers()` or await events |

---

## Pause Conditions

**STOP and request approval before:**

- Adding new E2E test file (ensure it has proper project targeting)
- Modifying global test setup files (`test/setup.ts`, `e2e/global-setup.ts`)
- Changing coverage thresholds in `vitest.config.ts`
- Adding new Playwright projects

---

## Review Checklist

- [ ] E2E tests use `app` fixture from `e2e/fixtures/base.ts`
- [ ] Selectors use accessibility-first approach (getByRole, getByLabel)
- [ ] No hardcoded waits (`waitForTimeout` with arbitrary values)
- [ ] Test isolation verified (can run in any order)
- [ ] Auth tests use fixtures, not login flow
- [ ] Unit tests mock external dependencies
- [ ] Coverage threshold maintained (80% lines)
- [ ] Test names describe behavior, not implementation

---

## Reference Documents

| Reference | Content |
|-----------|---------|
| [playwright.md](references/playwright.md) | E2E tests, fixtures, selectors, auth |
| [vitest.md](references/vitest.md) | Unit tests, mocking, test utilities |
| [patterns.md](references/patterns.md) | What to test where, naming, isolation |
| [ci.md](references/ci.md) | CI config, tasks, parallelization |

---

## SSOT Documents

| Topic | Location |
|-------|----------|
| Playwright config | `playwright.config.ts` |
| Vitest config | `vitest.config.ts` |
| Test setup | `test/setup.ts` |
| E2E fixtures | `e2e/fixtures/` |

---

## Handoffs

| To Agent | When |
|----------|------|
| **treido-i18n** | i18n parity test (`i18n-messages-parity.test.ts`) |
| **treido-backend** | Auth logic, Supabase queries in tests |
| **treido-frontend** | Component structure, RSC patterns |
| **treido-design** | Accessibility violations, UI patterns |

---

## Verification Commands

```bash
# Run unit tests
pnpm test:unit

# Run E2E smoke (reuse existing dev server)
REUSE_EXISTING_SERVER=true pnpm test:e2e:smoke

# Run with coverage
pnpm test:unit:coverage

# Run accessibility tests
pnpm test:a11y
```
```
