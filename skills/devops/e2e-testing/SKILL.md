---
name: e2e-testing
description: "Playwright-based end-to-end testing workflow."
user-invocable: false
agent: testing-automation-engineer
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
  - Skill
adr: adr/ADR-107-e2e-testing.md
routing:
  category: testing
  triggers:
    - playwright
    - E2E test
    - end-to-end
    - browser test
    - page object model
    - POM
    - test flakiness
  pairs_with:
    - testing-automation-engineer
    - typescript-frontend-engineer
    - test-driven-development
---

# E2E Testing Skill (Playwright)

Playwright-based E2E testing across four phases: Scaffold, Build, Run, Validate. Each phase produces a saved artifact and must pass its gate before the next phase begins.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| async, Promise.all, race condition, waitForTimeout, fixture teardown | `async.md` | Routes to the matching deep reference |
| auth, login, storageState, OAuth, SSO, JWT, RBAC, multi-role, session expiry | `auth.md` | Routes to the matching deep reference |
| config, playwright.config.ts, POM, data-testid, CI/CD workflow | `templates.md` | Routes to the matching deep reference |
| error, timeout, tsc fail, locator, fill, missing JSON | `errors.md` | Routes to the matching deep reference |
| POM examples, waiting, multi-browser, shared auth session | `playwright-patterns.md` | Routes to the matching deep reference |
| Web3, MetaMask, wallet, addInitScript | `wallet-testing.md` | Routes to the matching deep reference |
| payment, financial, production skip, blockchain | `financial-flows.md` | Routes to the matching deep reference |
| flaky, intermittent, repeat-each, retries, quarantine | `flakiness-triage.md` | Routes to the matching deep reference |

## Instructions

### PHASE 1: SCAFFOLD

**Goal:** Verify Playwright is installed, create the directory structure, and generate `playwright.config.ts`.

**Actions:**
1. Check if `@playwright/test` is installed: `npx playwright --version`. If not, run `npm install -D @playwright/test` and `npx playwright install`.
2. Create directory structure:
   ```
   tests/
     e2e/
       auth/
       features/
       api/
   pages/          <- POM classes live here
   artifacts/
     screenshots/
     traces/
     videos/
   ```
3. Write `playwright.config.ts` using the template in `references/templates.md`. The config bakes in failure diagnostics by default: `screenshot: 'only-on-failure'`, `trace: 'on-first-retry'`, and `video: 'retain-on-failure'` so that every failure produces actionable artifacts without manual setup. CI retries (`retries: process.env.CI ? 2 : 0`) absorb transient infrastructure flakiness without masking real bugs.
4. Confirm `playwright.config.ts` is valid TypeScript: `npx tsc --noEmit`. Run this deterministic check before any subjective assessment of the config -- compiler errors are facts, opinions are not.

**Artifact:** `playwright.config.ts` + `tests/e2e/` directory structure.

**Gate:** `playwright.config.ts` exists AND `tests/e2e/` directory exists. If either is missing, do not proceed to Phase 2 -- diagnose and fix.

See `references/templates.md` for the full `playwright.config.ts` template and multi-browser matrix rationale.

---

### PHASE 2: BUILD

**Goal:** Write POM classes for target feature areas, then write spec files that use those POMs.

Every page or feature area gets a typed Page Object class. Spec files never contain inline locators -- all selectors live in the POM. This separation means a selector change is a one-line POM edit, not a grep-and-replace across dozens of specs.

**Actions:**
1. Identify the feature areas under test (auth, checkout, dashboard, etc.).
2. For each area, create a POM class in `pages/` (see POM Pattern in `references/templates.md`). All locators must use `data-testid` attributes via `page.getByTestId()`. CSS selectors (`page.locator('.btn-primary')`) break silently when styles change. XPath breaks on DOM restructuring. Text matching (`page.locator('text=Submit')`) breaks on copy changes. `data-testid` is a testing contract that survives all three.
3. Write spec files in `tests/e2e/<area>/` using the POMs.
4. Run `npx tsc --noEmit` to verify all files compile.
5. Fix any TypeScript errors before proceeding.

**Artifact:** `tests/e2e/**/*.spec.ts` files + `pages/*.ts` POM classes, all compiling cleanly.

**Gate:** At least one `.spec.ts` exists under `tests/e2e/` AND `npx tsc --noEmit` exits 0. If compile fails, fix errors -- do not proceed to Phase 3 with broken TypeScript.

See `references/templates.md` for the POM Pattern, data-testid convention, and waiting/timing rules.

---

### PHASE 3: RUN

**Goal:** Execute the test suite, capture the results JSON, and identify any failing or flaky tests.

**Actions:**
1. Ensure the application under test is running (or document the `BASE_URL` required).
2. Run the full suite with JSON reporter configured in `playwright.config.ts`:
   ```bash
   npx playwright test
   ```
3. If any tests fail, run them in isolation with `--repeat-each=5` to distinguish flaky from consistently failing:
   ```bash
   npx playwright test tests/e2e/auth/login.spec.ts --repeat-each=5
   ```
4. Quarantine confirmed flaky tests with `test.fixme()`. Never delete a failing test -- deleted tests leave silent coverage gaps. Quarantined tests are visible debt with tracking references:
   ```typescript
   test.fixme('flaky: login redirects intermittently', async ({ page }) => {
     // TODO: #123 -- investigate race condition with auth cookie
     ...
   });
   ```
5. Use `test.skip()` only for conditional environment guards (e.g., "skip on WebKit"), not for sweeping failures under the rug.

**Artifact:** `playwright-results.json` (presence is the gate -- pass rate is not).

**Gate:** `playwright-results.json` exists at the project root. The file must contain valid JSON. Pass rate does not block Phase 4 -- reporting on failures is Phase 4's job.

See `references/templates.md` for the full Flaky Test Quarantine Protocol.

---

### PHASE 4: VALIDATE

**Goal:** Deterministic checks on test output, then structured report generation.

**Actions:**
1. **Deterministic checks first** -- run these before any LLM summary because compiler output and JSON parsing are facts, not opinions:
   - `playwright-results.json` exists and parses as valid JSON.
   - Extract counts: `python3 -c "import json,sys; d=json.load(open('playwright-results.json')); print(d.get('stats', d))"`
   - Identify all `unexpected` (failed) and `flaky` result entries.
2. **LLM triage** (only after deterministic checks pass):
   - For each failed test, identify whether it is: (a) a broken assertion, (b) a selector mismatch, (c) a timing/async issue, or (d) an application bug.
   - Categorize flaky tests for quarantine vs. fix.
3. Write `e2e-report.md` using the report template in `references/templates.md`.

**Artifact:** `e2e-report.md`.

**Gate:** `e2e-report.md` exists. Skill is complete only when this file is written.

See `references/templates.md` for the e2e-report.md template and the GitHub Actions CI/CD workflow template.

---

## Error Handling

See `references/errors.md` for the symptom/cause/fix matrix covering tsc failures, CI-only flakes, missing results JSON, locator timeouts, fill-vs-clear bugs, and DOM ordering issues.

---

## References

| Signal / Task Type | Load This Reference |
|--------------------|---------------------|
| async, Promise.all, race condition, waitForTimeout, fixture teardown | [async.md](references/async.md) |
| auth, login, storageState, OAuth, SSO, JWT, RBAC, multi-role, session expiry | [auth.md](references/auth.md) |
| config, playwright.config.ts, POM, data-testid, CI/CD workflow | [templates.md](references/templates.md) |
| error, timeout, tsc fail, locator, fill, missing JSON | [errors.md](references/errors.md) |
| POM examples, waiting, multi-browser, shared auth session | [playwright-patterns.md](references/playwright-patterns.md) |
| Web3, MetaMask, wallet, addInitScript | [wallet-testing.md](references/wallet-testing.md) |
| payment, financial, production skip, blockchain | [financial-flows.md](references/financial-flows.md) |
| flaky, intermittent, repeat-each, retries, quarantine | [flakiness-triage.md](references/flakiness-triage.md) |

- [ADR-107](../../adr/ADR-107-e2e-testing.md) -- Decision record for this skill
- [Playwright docs](https://playwright.dev/docs/intro) -- Official API reference
