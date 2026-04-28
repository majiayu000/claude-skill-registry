---
name: review-test
description: Comprehensive test suite review across five phases. Fills unit coverage gaps, surveys integration coverage, surveys E2E (browser) coverage for webapps, identifies missing fuzz tests, and audits test quality — in that order.
model: opus
---

# Test Review - Comprehensive Test Suite Review

Five-phase review: fill unit coverage gaps, survey integration coverage, survey E2E (browser) coverage when applicable, identify fuzz testing opportunities, then audit test quality. Each phase runs its own analysis → present → select → implement → verify cycle.

## Philosophy

**Tests are a system, not a checklist.** Unit gaps, integration gaps, E2E gaps, fuzz gaps, and bad tests are different facets of the same problem: the test suite isn't doing its job. This workflow addresses all of them in deliberate order — inside-out by test scope (unit → integration → E2E), then fuzz as an addendum, then quality covers everything that landed.

## Workflow Overview

```
┌──────────────────────────────────────────────────┐
│                  TEST REVIEW                     │
├──────────────────────────────────────────────────┤
│  1. Determine scope                              │
│  2. Phase 1: Unit coverage gaps                  │
│  3. Phase 2: Integration coverage                │
│  4. Phase 3: E2E coverage (webapps only)         │
│  5. Phase 4: Fuzz coverage                       │
│  6. Phase 5: Test quality audit                  │
│  7. Summary + optional commit                    │
└──────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope

**Ask the user:** "What should I review?"

Present these options:
- **Entire project**: Review all source and test files (default)
- **Specific directory**: A path like `src/`, `pkg/`, `lib/`
- **Specific files**: Individual source files
- **Recent changes**: Files modified on the current branch (via `git diff`)

**Default:** Entire project.

**If the project is large** (many source files), suggest narrowing scope. The user can always re-run on a different scope.

This scope applies to all five phases.

---

## Phase 1: Unit Coverage Gaps

Fill missing unit-level test coverage, prioritized by risk.

### 1a. Detect/Obtain Coverage Data

Follow this waterfall — stop at the first step that produces a usable report.

**Step A: Check for existing coverage artifacts**

Search for coverage files in common locations:

| Format       | Files to search for                                                              |
|--------------|----------------------------------------------------------------------------------|
| Go           | `coverage.out`, `cover.out`, `c.out`                                             |
| lcov         | `lcov.info`, `coverage/lcov.info`                                                |
| Istanbul/nyc | `coverage/coverage-summary.json`, `coverage/coverage-final.json`, `.nyc_output/` |
| coverage.py  | `coverage.xml`, `coverage.json`, `htmlcov/`                                      |
| JaCoCo       | `target/site/jacoco/jacoco.xml`, `build/reports/jacoco/*/jacoco.xml`             |
| Cobertura    | `coverage.xml`, `cobertura.xml`                                                  |

If a report is found, verify it's reasonably recent (warn if older than the most recent source change). Use the report and proceed.

**Step B: Detect coverage command**

If no report exists, detect how to generate one:

1. `Makefile` with a `cover` or `coverage` target → `make cover` (or `make coverage`)
2. `package.json` with a `coverage` script → `npm run coverage`
3. `go.mod` present → `go test -coverprofile=coverage.out ./...`
4. `pyproject.toml` / `setup.cfg` / `pytest.ini` with coverage config → `pytest --cov --cov-report=json`
5. `Cargo.toml` → `cargo tarpaulin --out json` (or `cargo llvm-cov --json`)
6. `build.gradle` / `build.gradle.kts` → `gradle jacocoTestReport`

Run the command and verify it produces a report. If it fails, ask the user for the correct command.

**Step C: Ask the user**

If no coverage tooling is detected: "What command generates a coverage report for this project?"

**Step D: Manual analysis fallback**

If no coverage tooling is available, proceed with manual analysis. The agent will read source and test files to identify gaps by inspection.

**Note:** In manual analysis mode, quantitative coverage improvement is unavailable.

**Store:** the coverage command (if any) and baseline coverage percentage.

### 1b. Analyze Coverage Gaps

**Assess scope size** with Glob.

**Small scope (roughly ≤15 source files):** Spawn a single `qa-test-coverage-reviewer` agent with the full scope and coverage data.

**Large scope (roughly >15 source files):** Partition by directory or module. Spawn multiple `qa-test-coverage-reviewer` agents **in parallel**, each with a focused partition and relevant coverage data.

Merge findings into a single list ordered by priority tier (CRITICAL → HIGH → LOW). Collect REFACTOR-FOR-TESTABILITY suggestions separately — these are presented at the end of the workflow, not here.

**Prompt for each agent:**

```
Analyze test coverage gaps.
Scope: [partition or full scope]
Mode: [coverage report / coverage command / manual analysis]
Coverage data: [file path or "manual analysis — no data"]

Identify:
- Untested code paths prioritized by risk (CRITICAL / HIGH / LOW)
- Code that is structurally hard to test (REFACTOR-FOR-TESTABILITY suggestions)

Return structured findings with ADD recommendations and refactoring suggestions.
```

**If no significant gaps found:** Report "No significant coverage gaps found" and proceed to Phase 2.

### 1c. Present Findings and User Selection

Display findings as a numbered list grouped by priority tier. Hold back refactoring suggestions for the end of the workflow.

**Example:**

```
## Phase 1: Unit Coverage Gap Analysis

Overall coverage: 68.3% lines (baseline)

### CRITICAL (2 found)
1. [ADD] auth.go:ValidateJWT (lines 45-72) — JWT validation error paths untested
   Risk: Invalid tokens could bypass authentication
2. [ADD] payment.go:ChargeCard (lines 88-120) — Retry and failure logic untested
   Risk: Silent charge failures or double charges

### HIGH (3 found)
3. [ADD] parser.go:ParseConfig (lines 30-55) — Malformed input handling untested
4. [ADD] api.go:CreateUser (lines 15-40) — Duplicate email conflict untested
5. [ADD] middleware.go:RateLimit (lines 22-45) — Limit exceeded path untested

### LOW (2 found)
6. [ADD] config.go:Defaults (lines 5-12) — Default value coverage
7. [ADD] router.go:RegisterRoutes (lines 8-25) — Route registration

Select which gaps to fill (e.g., "1-5" or "all"):
```

Use `AskUserQuestion` with multi-select. If more than ~10 findings, batch by tier.

### 1d. Implement Selected Tests

**Detect appropriate SME and spawn based on project language:**
- Go: `swe-sme-golang`
- Dockerfile: `swe-sme-docker`
- Makefile: `swe-sme-makefile`
- GraphQL: `swe-sme-graphql`
- Ansible: `swe-sme-ansible`
- Zig: `swe-sme-zig`
- TypeScript: `swe-sme-typescript`
- JavaScript: `swe-sme-javascript`
- HTML: `swe-sme-html`
- CSS: `swe-sme-css`

**For languages without a dedicated SME:** implement directly as orchestrator.

**Group findings by target test file**, then spawn one SME agent per file **in parallel**. Findings targeting the same test file go to the same agent.

**Prompt each SME agent with:**

```
Write tests to fill the following coverage gaps in [source file].
Target test file: [test file]

Gaps to cover:
1. [function_name (lines N-M)]: [what is untested]
   Should verify: [specific test description from analyst]

Guidelines:
- Write focused tests targeting the specific untested code paths.
- Follow the project's existing test conventions and framework.
- Test behavior, not implementation details.
- Cover the error/edge cases identified in the gap analysis.
- Each test should have a clear name indicating what it verifies.
- If existing test helpers or fixtures are available, use them.
```

### 1e. Verify

Run the test suite. Confirm new tests pass and existing tests still pass.

**If failures:** Report which tests failed. For new test failures, attempt one fix. For existing test failures, report to user. Let user decide how to proceed.

### 1f. Re-run Coverage

**If a coverage command was established:** Re-run it and display before/after comparison:

```
## Coverage Improvement

              Before    After     Change
Lines         68.3%     78.1%     +9.8%
```

**If manual analysis mode:** Skip with: "No coverage tooling available — cannot measure improvement quantitatively."

---

## Phase 2: Integration Coverage

Survey integration test coverage and recommend gaps or, if none exist, a starter strategy.

### 2a. Analyze Integration Coverage

Spawn a single `qa-test-integration-reviewer` agent.

**Prompt:**

```
Review integration test coverage for this project.
Scope: [full scope from step 1]

Detect:
- Existing integration test infrastructure (frameworks, directories, markers, runners, fixtures, CI)
- Integration seams (databases, queues, external APIs, etc.)

If no integration tests exist (Mode A), recommend a starter strategy with infrastructure
and ~5-8 starter tests. If integration tests exist (Mode B), identify gaps within the
strategy (cap ~10) and missing strategies (cap ~3).

Return findings per the agent's output format, with calibrated confidence.
```

### 2b. Handle Mode

The agent reports in one of two modes.

**Mode A (no integration tests detected):** the agent proposes a starter strategy with infrastructure and starter tests. Present to the user.

**Mode B (integration tests detected):** the agent reports gaps and expansion opportunities. Present them.

**If the agent reports "no findings"** (Mode B with empty B1 and B2), report the existing posture briefly and proceed to Phase 3.

### 2c. Present Findings and User Selection

Display findings.

**Example (Mode A):**

```
## Phase 2: Integration Coverage

Integration test posture: NONE DETECTED
Seams identified: 4 (PostgreSQL, Redis cache, Stripe API, queue consumer via Kafka)

### Proposed Strategy
- Service-level integration tests using testcontainers for Postgres + Kafka
- HTTP-level tests against the spun-up app with a real DB

### Proposed Infrastructure
- `make integration-test` target with `//go:build integration` tag
- `docker-compose.test.yml` for Postgres + Kafka
- `tests/integration/README.md` documenting how to run

### Starter Tests (5)
1. [ADD] User signup → DB persistence → email queued (CRITICAL flow)
   Catches: signup-pipeline integration regressions. Complexity: moderate
2. [ADD] Payment webhook handling → Stripe sig verification → DB write
   Catches: webhook handling regressions. Complexity: moderate
3. [ADD] Login → session token issuance → Redis store
   Catches: auth-token regression. Complexity: simple
4. [ADD] Order placement → queue produce → consumer process
   Catches: order-pipeline regressions. Complexity: complex
5. [ADD] Account deletion → cascade across tables
   Catches: data-residency regressions. Complexity: moderate

Select what to implement: [infrastructure, all tests, specific tests]
```

**Example (Mode B):**

```
## Phase 2: Integration Coverage

Integration test posture: testcontainers (Postgres), `make integration-test`
Existing tests: 12 (DB suite covering CRUD on Users, Orders, Payments)

### Gaps Within Existing Strategy (3 found)
1. [HIGH] DB suite — `DeleteUser` cascade not tested. Risk: orphan rows on account deletion.
2. [MEDIUM] DB suite — `UpdateOrder` concurrent-write path not tested.
3. [LOW] DB suite — pagination edge cases (empty result, max page size).

### Strategy Expansion (1 found)
4. [HIGH] Queue consumer — Kafka consumer has no integration tests despite carrying critical order-processing flow. Existing `docker-compose.test.yml` could host Kafka with minor changes.

Select which items to address (e.g., "1-4" or "all"):
```

Use `AskUserQuestion` with multi-select. In Mode A, the user can select infrastructure as a separate item from individual starter tests.

### 2d. Implement Selected Items

**If infrastructure was selected (Mode A):** Implement infrastructure first as a separate step:
- Add Makefile target / build tag / pytest mark
- Add `docker-compose.test.yml` (or equivalent) if needed
- Create the `tests/integration/` directory and README

**Then implement selected tests:** group by target test file, dispatch to language SMEs in parallel (same dispatch as Phase 1).

**Prompt each SME agent with:**

```
Write integration tests for [file/scenario] in this project.
Target test file: [path]

Tests to write:
1. [Test scenario]: [what to exercise]
   Seam: [seam being exercised]
   Should verify: [specific properties / regressions]

Guidelines:
- Use the project's existing integration test framework and fixture conventions.
- Follow the build tag / marker convention identified by the reviewer.
- Use testcontainers (or equivalent) for fixture services where appropriate.
- Tests should be deterministic — known initial state, predictable assertions.
- Keep each test focused on one seam / flow.
```

### 2e. Verify

**Do NOT run the integration test suite by default.** Integration tests are slow and may require fixtures up.

Compile-check only — confirm new tests compile and don't break unit tests:

```
Running unit tests to confirm no regressions...
[Unit tests pass]

New integration tests compile cleanly. Integration suite NOT run automatically
(may require fixtures up and take significant time).
```

**Then prompt the user:** "Run the new integration tests now? Requires fixtures (e.g., `docker-compose up`) and may take significant time. [y/N]"

If yes, run the integration test command and report results.

If no, note in the summary that integration tests are pending manual verification.

---

## Phase 3: E2E Coverage

Survey end-to-end (browser-driven) test coverage and recommend gaps or, if none exist, a starter strategy using Playwright. **This phase only applies to webapps.**

### 3a. Webapp Detection Gate

Spawn `qa-test-e2e-reviewer` for the gate check first. The agent's Step 0 detects whether the project is a webapp.

**If the agent reports "NOT A WEBAPP":**

```
## Phase 3: E2E Coverage

Webapp detection: NOT A WEBAPP — skipping phase.

[Brief one-line note about what was checked.]

Proceeding to Phase 4.
```

Skip to Phase 4. Do not proceed with the rest of Phase 3.

**If the agent reports webapp signals detected:** Continue to step 3b (the same agent invocation produces the full analysis; the gate is the first thing it reports).

### 3b. Analyze E2E Coverage

The agent (already spawned in 3a) produces the full analysis.

**Prompt:**

```
Review E2E (browser-driven) test coverage for this project.
Scope: [full scope from step 1]

Step 0: Detect whether this is a webapp. If not, exit immediately.

If a webapp:
- Detect existing E2E infrastructure (Playwright, Cypress, Selenium, etc.)
- Survey critical user journeys (Critical / Important / Nice-to-have)
- If no E2E exists (Mode A): prescribe Playwright unconditionally, propose
  infrastructure and ~5 starter tests
- If E2E exists (Mode B): respect the existing framework, identify gaps
  within strategy (cap ~6) and strategy expansion (cap ~2). Do NOT push
  Playwright migration.

Out of scope (declare in output): visual regression, accessibility, performance,
mobile-native UI, component-level testing.

Return findings per the agent's output format, with calibrated confidence and
explicit flag that journey classification is the most subjective input.
```

### 3c. Present Findings and Confirm Journey Classification

Display the agent's report. **Before presenting recommendations for selection, confirm the journey classification with the user** — this is the most subjective input in the analysis.

**Example confirmation prompt:**

```
## Phase 3: E2E Coverage

Webapp detection: DETECTED via @playwright/test in package.json + React deps
E2E posture: [Mode A or Mode B summary]

### Critical User Journeys (please confirm before proceeding)

CRITICAL:
- Signup → email confirmation → first-login flow
- Login → session establishment
- Core checkout flow (cart → payment → confirmation)

IMPORTANT:
- Password reset
- Profile settings update
- Order history view

NICE-TO-HAVE:
- Marketing page browsing
- Help center search

⚠️  Journey classification is the most subjective part of this analysis.
Please confirm or correct before I present implementation recommendations.

Are these classifications correct? [Yes / Correct: ...]
```

Use `AskUserQuestion`. Allow free-form correction.

If the user corrects any classification, update the analysis accordingly before moving to selection.

### 3d. Present Mode-Specific Findings and User Selection

After journey confirmation, present recommendations.

**Example (Mode A):**

```
### Mode A: No E2E Detected — Prescribed Framework: Playwright

### Proposed Infrastructure
- `playwright.config.ts` (Chromium + Firefox + WebKit, headless default)
- `tests/e2e/` directory
- `npm run test:e2e` script
- Fixture/seeding: dedicated test users seed script + per-test API setup
- `tests/e2e/README.md` documenting how to run, debug, and seed

### Starter Tests (5)
1. [ADD] Signup flow: visit /signup → fill form → submit → reach /welcome
   Journey: Signup (CRITICAL). Catches: signup-pipeline UI regressions.
2. [ADD] Login flow: visit /login → submit → reach /dashboard
   Journey: Login (CRITICAL). Catches: auth-flow UI regressions.
3. [ADD] Checkout happy path: cart → payment → confirmation
   Journey: Checkout (CRITICAL). Catches: full purchase pipeline regressions.
4. [ADD] Password reset: request → email link → set new password → login
   Journey: Password reset (IMPORTANT). Catches: account-recovery regressions.
5. [ADD] Profile update: navigate → edit → save → verify persistence
   Journey: Profile settings (IMPORTANT). Catches: settings-mutation regressions.

Out of scope (declared): visual regression, a11y, performance, mobile-native, component tests.

Select what to implement: [infrastructure, all tests, specific tests]
```

**Example (Mode B):**

```
### Mode B: Playwright detected (npm run test:e2e, 8 existing tests)

### Gaps Within Existing Strategy (3 found)
1. [HIGH] Signup flow tested but email-verification step not exercised. Risk: regression in email-link redemption.
2. [MEDIUM] Profile settings — only happy path tested; validation-error path missing.
3. [LOW] Search results — no test for empty-result state.

### Strategy Expansion (1 found)
4. [HIGH] Authenticated marketing app (logged-in dashboard customizations) untested; only public marketing is covered.

Out of scope (declared): visual regression, a11y, performance, mobile-native, component tests.

Select which items to address (e.g., "1-4" or "all"):
```

Use `AskUserQuestion` with multi-select.

### 3e. Implement Selected Items

**If infrastructure was selected (Mode A):** Implement infrastructure first via `swe-sme-typescript`:
- Generate `playwright.config.ts`
- Create `tests/e2e/` directory
- Add `npm run test:e2e` script
- Stub the fixture/seeding strategy (test user creation script, per-test API setup)
- Create `tests/e2e/README.md`

**Then implement selected tests:** dispatch to `swe-sme-typescript` (Playwright in TS by default) or the appropriate SME if the project uses a different stack.

For Mode B with non-Playwright frameworks (Cypress, Selenium, etc.), dispatch to the SME for the relevant language and instruct them to write tests in the project's existing framework — **do not migrate to Playwright**.

**Prompt each SME agent with:**

```
Write E2E tests for [user journey/scenario] in this project.
Framework: [Playwright TS | Cypress | Selenium | other]
Target test file: [path]

Tests to write:
1. [Test scenario]: [user journey to exercise]
   Journey: [CRITICAL/IMPORTANT/NICE-TO-HAVE]
   Should verify: [specific user-visible behavior]

Guidelines:
- Use the project's existing E2E framework conventions.
- For Playwright: prefer page.getByRole / getByLabel / getByText over CSS selectors.
- Tests should be deterministic — use known-state fixtures, not relying on prior test state.
- Keep tests focused on one journey.
- Use the fixture/seeding approach already established in the project.
```

### 3f. Verify

**Do NOT run the E2E suite by default.** E2E tests require a running test environment, fixtures, and browser binaries.

Compile-check only — confirm new tests parse / type-check cleanly:

```
Running TypeScript type-check on new E2E tests...
[Type-check passes]

Running unit tests to confirm no regressions...
[Unit tests pass]

E2E tests compile cleanly. E2E suite NOT run automatically
(requires environment up + browser binaries; may take significant time).
```

**Then prompt the user:** "Run the new E2E tests now? Requires test environment up and browser binaries installed. [y/N]"

If yes, run the E2E test command and report results.

If no, note in the summary that E2E tests are pending manual verification.

---

## Phase 4: Fuzz Coverage

Identify functions that should have fuzz tests.

### 4a. Analyze Fuzz Gaps

Spawn a single `qa-test-fuzz-reviewer` agent with the full scope.

```
Analyze fuzz testing coverage.
Scope: [full scope from step 1]

Identify:
- Whether fuzz testing infrastructure exists
- Functions that are good fuzz candidates but lack fuzz tests
```

### 4b. Handle Infrastructure Check

**If the agent reports no fuzz infrastructure:**

Report to the user:

```
## Phase 4: Fuzz Coverage

No fuzz testing infrastructure detected for [language].

To enable fuzz testing, consider: [tooling recommendation from agent]

Skipping fuzz analysis. Proceeding to Phase 5.
```

Proceed to Phase 5. Do not attempt to set up fuzz tooling.

**If the agent reports no candidates or all candidates are covered:**

```
## Phase 4: Fuzz Coverage

Fuzz infrastructure detected: [tooling]
No fuzz coverage gaps found. [brief explanation]

Proceeding to Phase 5.
```

Proceed to Phase 5.

### 4c. Present Findings and User Selection

Display fuzz candidates as a numbered list grouped by priority.

**Example:**

```
## Phase 4: Fuzz Coverage

Fuzz infrastructure: native testing.F (Go 1.22)
Existing fuzz tests: 2

### HIGH (2 found)
1. [ADD] parser.go:ParseConfig — Parses user-provided YAML config
   Input: arbitrary []byte
   Should verify: no panics, returns error on invalid input
2. [ADD] protocol.go:DecodeMessage — Decodes wire protocol messages
   Input: arbitrary []byte
   Should verify: no panics, bounded output size

### MEDIUM (1 found)
3. [ADD] template.go:Render — Renders user-provided templates
   Input: arbitrary string
   Should verify: no panics, no infinite loops

### Already covered
- parser.go:ParseJSON — fuzz test in parser_test.go:FuzzParseJSON
- auth.go:ParseToken — fuzz test in auth_test.go:FuzzParseToken

Select which fuzz tests to add (e.g., "1-3" or "all"):
```

Use `AskUserQuestion` with multi-select.

### 4d. Implement Selected Fuzz Tests

Same SME dispatch as Phase 1. Group by target test file, spawn in parallel.

**Prompt each SME agent with:**

```
Write fuzz tests for the following functions in [source file].
Target test file: [test file]

Fuzz targets:
1. [function_name]: [what to fuzz]
   Input type: [what to generate]
   Should verify: [properties to check]

Guidelines:
- Use the project's fuzz testing framework ([framework name]).
- Each fuzz test should target one function.
- Check the properties specified (no panics, round-trip consistency, etc.).
- Follow existing fuzz test conventions if any exist in the project.
- Keep the fuzz target function focused — minimize setup, maximize input coverage.
```

### 4e. Verify

Run the test suite (not the fuzz tests themselves — those run indefinitely). Confirm fuzz test functions compile and pass their seed corpus if any.

**If failures:** Same handling as Phase 1.

---

## Phase 5: Test Quality Audit

Identify and fix bad tests across the entire test suite, including tests written in Phases 1–4.

### 5a. Scan for Quality Issues

**Assess scope size** with Glob (count test files in scope).

**Small scope (roughly ≤15 test files):** Spawn a single `qa-test-reviewer` agent.

**Large scope (roughly >15 test files):** Partition by directory or module. Spawn multiple `qa-test-reviewer` agents **in parallel**, each with a focused partition.

Merge findings into a single list. Deduplicate overlaps at partition boundaries.

**Prompt for each agent:**

```
Review the test suite for quality issues.
Scope: [partition or full scope]

Look for:
- Tautological tests (can't fail)
- Brittle tests (coupled to implementation, weak assertions when stronger ones exist)
- Redundant tests (duplicate coverage — informational only, no action recommended)
- False confidence tests (don't verify what they claim)
- Missing coverage (important gaps only)
- Test smells (structural problems)
- Inconsistent assertion strategies (mixed error checking approaches, varied assertion styles)

Return structured findings with recommended actions (DELETE, REWRITE, ADD, SIMPLIFY).
Redundant tests should be reported as informational only (no action recommended).
```

**If no issues found:** Report "No test quality issues found" and proceed to summary.

### 5b. Present Findings and User Selection

Display findings as a numbered list grouped by category.

**Example:**

```
## Phase 5: Test Quality Audit

### Tautological (2 found)
1. [DELETE] model_test.go:TestUserStruct — Checks struct field existence
2. [DELETE] config_test.go:TestDefaultConfig — Asserts hardcoded values against themselves

### Brittle (2 found)
3. [REWRITE] api_test.go:TestCreateUserError — Exact error string match
4. [REWRITE] handler_test.go:TestNotFound — Asserts full JSON response body

### Redundant (1 noted — informational, no action)
- [INFO] math_test.go:TestAddVariants — 5 cases hitting same code path

### Missing Coverage (1 found)
5. [ADD] auth.go:RevokeToken — No tests for revocation path

Select which items to address (e.g., "1-5" or "all"):
```

Use `AskUserQuestion` with multi-select.

### 5c. Implement Selected Changes

Same SME dispatch as Phases 1, 2, 3, and 4. **Group findings by file**, spawn one SME per file **in parallel**.

**Prompt each SME agent with:**

```
The test auditor identified the following issues in [file]. Implement the recommended changes.

DELETE findings (remove these tests — but if you believe a test has value, rewrite it instead):
[List of DELETE items for this file]

REWRITE/SIMPLIFY findings (fix these tests):
[List of REWRITE/SIMPLIFY items for this file]

ADD findings (write new tests):
[List of ADD items for this file]

Guidelines:
- Focus on testing observable behavior rather than implementation details.
- Follow the project's existing test conventions.
- Keep tests simple and readable.
- For DELETE items: if the test covers real behavior that could regress, rewrite it rather than deleting it. Only delete tests that are genuinely self-fulfilling or completely orphaned.
```

### 5d. Verify

Run the test suite. Confirm all changes are clean.

**If failures:** Same handling as Phase 1.

---

## 6. Summary

Present a combined summary of all five phases, plus any refactoring suggestions collected in Phase 1.

```
## Test Review Complete

### Phase 1: Unit Coverage Gaps
- Tests added: N
- Coverage: XX% → YY% (+Z%)

### Phase 2: Integration Coverage
- Mode: [A: starter strategy adopted | B: gaps filled]
- Infrastructure added: [yes/no]
- Tests added: N
- Manual run pending: [yes/no]

### Phase 3: E2E Coverage
- Webapp: [yes / no — skipped]
- Mode: [A: starter strategy adopted | B: gaps filled]
- Framework: [Playwright | Cypress | other]
- Infrastructure added: [yes/no]
- Tests added: N
- Manual run pending: [yes/no]

### Phase 4: Fuzz Coverage
- Fuzz tests added: N
- [or: "Skipped — no fuzz infrastructure"]

### Phase 5: Test Quality Audit
- Tests deleted: N
- Tests rewritten: N
- Tests added: N

### Net Change
- Total tests added: N
- Total tests removed: N
- Net: +/-N

### Refactoring for Testability (informational)
[Refactoring suggestions from Phase 1 coverage analyst, if any]

1. [file:function] — [problem]
   Suggestion: [what to refactor]
   Would enable testing: [what becomes testable]

These suggestions are not implemented by this workflow. Use /refactor
or address them manually.

### Files Modified
- [file]: [what changed]
```

**Ask user if they want to commit.** If yes, create a commit:

```bash
git add [specific files]
git commit -m "$(cat <<'EOF'
test: comprehensive test suite review

[Brief description: added N unit tests, N integration tests, N E2E tests,
N fuzz tests, deleted N bad tests, rewrote N brittle tests]
Coverage: XX% → YY%
EOF
)"
```

## Agent Coordination

**Phase 1 analysis:** Spawn `qa-test-coverage-reviewer` agent(s). For large scopes, partition and run in parallel.
**Phase 2 analysis:** Spawn single `qa-test-integration-reviewer` agent.
**Phase 3 analysis:** Spawn single `qa-test-e2e-reviewer` agent (which performs the webapp gate first).
**Phase 4 analysis:** Spawn single `qa-test-fuzz-reviewer` agent.
**Phase 5 analysis:** Spawn `qa-test-reviewer` agent(s). For large scopes, partition and run in parallel.
**Implementation (all phases):** Parallel by file. Group findings by target file, spawn one SME per file. Phase 3 infrastructure setup uses `swe-sme-typescript` for Playwright-prescribed Mode A.

**Fresh instances:** Every agent spawn is a fresh instance. No state carried between invocations.

**State to maintain (as orchestrator):**
- Scope (shared across all phases)
- Coverage command and baseline metrics
- Webapp detection result (used to skip Phase 3 cleanly)
- Confirmed journey classification (Phase 3, after user correction)
- User selections for each phase
- Implementation results per phase
- Refactoring suggestions (held for final summary)
- Running totals for summary

## Abort Conditions

**Abort workflow:**
- User interrupts
- No source files found in scope

**Do NOT abort for:**
- Coverage command failure (fall back to manual analysis)
- Phase 2 reporting "no findings" (Mode B with no gaps; report and proceed)
- Phase 3 webapp gate negative (skip cleanly to Phase 4)
- Phase 4 finding no fuzz infrastructure (skip phase, continue)
- Individual SME failures (report and continue)
- Test suite failures after changes (report and let user decide)
- Any single phase finding no issues (report and continue to next phase)
- Integration or E2E suite not run in verify steps (this is intentional — user runs them ad-hoc)
