---
name: review-test
description: Comprehensive test suite review across five phases. Surveys unit coverage, integration coverage, E2E (browser) coverage for webapps, fuzz coverage, and test quality — in that order. Advisory only — produces findings and proposes tickets; does not implement test changes.
model: opus
---

# Test Review — Comprehensive Test Suite Survey

Five-phase survey: unit coverage gaps, integration coverage gaps, E2E (browser) coverage gaps when applicable, fuzz coverage gaps, then test quality issues. Each phase runs its analysis and contributes findings to a consolidated report; at the end, the skill proposes a ticket structure for the recommended work and creates tickets after operator approval.

**Advisory only.** The skill produces findings and proposes tickets; it does not implement test changes. The cognitive seam between "find a coverage gap" and "design a test for it" is wide enough that mixing them under one workflow degrades both — test design requires fresh reasoning about edge cases, mocking strategy, and assertion shape, and the discovery agents shouldn't be biased toward gaps whose fixes are easy. Tickets capture findings durably across that seam and compose with `/implement` and `/implement-project` for remediation.

The same logic applies in reverse to test-quality findings (DELETE / REWRITE / SIMPLIFY): the operator should approve removing or rewriting an existing test explicitly, via a ticket, rather than have a workflow do it as a side effect of running a review.

## Philosophy

**Tests are a system, not a checklist.** Unit gaps, integration gaps, E2E gaps, fuzz gaps, and bad tests are different facets of the same problem: the test suite isn't doing its job. This workflow surveys all of them in deliberate order — inside-out by test scope (unit → integration → E2E), then fuzz as an addendum, then quality covers everything that exists today.

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
│  7. Present consolidated findings                │
│  8. Cut tickets (proposed structure, operator-   │
│     approved)                                    │
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

Survey missing unit-level test coverage, prioritized by risk.

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

**Note:** In manual analysis mode, quantitative coverage measurement is unavailable.

**Store:** the coverage command (if any) and baseline coverage percentage.

### 1b. Analyze Coverage Gaps

**Assess scope size** with Glob.

**Small scope (roughly ≤15 source files):** Spawn a single `qa-test-coverage-reviewer` agent with the full scope and coverage data.

**Large scope (roughly >15 source files):** Partition by directory or module. Spawn multiple `qa-test-coverage-reviewer` agents **in parallel**, each with a focused partition and relevant coverage data.

Merge findings into a single list ordered by priority tier (CRITICAL → HIGH → LOW). Collect REFACTOR-FOR-TESTABILITY suggestions separately — these are presented in the consolidated findings, not as ticket candidates by default.

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

**If no significant gaps found:** Record "No significant coverage gaps found" and proceed to Phase 2.

### 1c. Record Phase 1 Findings

Record findings grouped by priority tier (CRITICAL / HIGH / LOW) for the consolidated report in step 7. Hold the REFACTOR-FOR-TESTABILITY suggestions separately — they appear as an informational section in the final report; they may or may not be cut as tickets per the runtime ticket-structure proposal in step 8.

Proceed to Phase 2.

---

## Phase 2: Integration Coverage

Survey integration test coverage and identify gaps or, if none exist, a starter strategy.

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

### 2b. Record Phase 2 Findings

The agent reports in one of two modes.

**Mode A (no integration tests detected):** the agent proposes a starter strategy with infrastructure and starter tests. Record the strategy, infrastructure proposal, and starter tests.

**Mode B (integration tests detected):** the agent reports gaps within the strategy and strategy-expansion opportunities. Record them with their priorities.

**If the agent reports "no findings"** (Mode B with empty gaps and expansion), record the existing posture briefly and proceed.

Proceed to Phase 3.

---

## Phase 3: E2E Coverage

Survey end-to-end (browser-driven) test coverage and identify gaps or, if none exist, a starter strategy using Playwright. **This phase only applies to webapps.**

### 3a. Webapp Detection Gate

Spawn `qa-test-e2e-reviewer` for the gate check first. The agent's Step 0 detects whether the project is a webapp.

**If the agent reports "NOT A WEBAPP":**

Record "Phase 3 skipped — not a webapp" and proceed to Phase 4. Do not proceed with the rest of Phase 3.

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

### 3c. Confirm Journey Classification

Before recording the Phase 3 findings, **confirm the agent's journey classification with the user** — this is the most subjective input in the analysis and shapes the priority assigned to each gap.

**Example confirmation prompt:**

```
## Phase 3: E2E Coverage — confirm journey classification

Webapp detection: DETECTED via @playwright/test in package.json + React deps

### Critical User Journeys (please confirm before findings are finalized)

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
Please confirm or correct.

Are these classifications correct? [Yes / Correct: ...]
```

Use `AskUserQuestion`. Allow free-form correction.

If the user corrects any classification, update the agent's findings before recording.

### 3d. Record Phase 3 Findings

Record the gaps (Mode A starter strategy, infrastructure, and starter tests; or Mode B gaps and expansion opportunities) with the confirmed journey priorities. The agent's "out of scope" declarations stay in the recorded report.

Proceed to Phase 4.

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

### 4b. Record Phase 4 Findings

**If the agent reports no fuzz infrastructure:** Record "No fuzz testing infrastructure detected for [language]" plus the agent's tooling recommendation. The tooling recommendation appears as an informational entry in the consolidated report and may be cut as a ticket per the runtime ticket-structure proposal (step 8). Do not attempt to set up fuzz tooling.

**If the agent reports no candidates or all candidates are covered:** Record "No fuzz coverage gaps" with the brief explanation.

**Otherwise:** Record candidates grouped by priority (HIGH / MEDIUM / LOW). Record covered candidates separately as informational context.

Proceed to Phase 5.

---

## Phase 5: Test Quality Audit

Identify quality issues across the existing test suite.

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

**If no issues found:** Record "No test quality issues found" and proceed to the consolidated report.

### 5b. Record Phase 5 Findings

Record findings grouped by category (Tautological / Brittle / False-confidence / Inconsistent / Missing / Redundant) with the per-finding recommended action (DELETE / REWRITE / SIMPLIFY / ADD / informational). The redundant category stays informational.

Proceed to step 7.

---

## 7. Present Consolidated Findings

Compile all phases into a single report:

```
## Test Review Summary

Scope: [what was reviewed]
Baseline coverage: XX% (if measured) — or "manual analysis — not measured"

## Phase 1: Unit Coverage Gaps
- N gaps found: X CRITICAL, Y HIGH, Z LOW
- [Numbered list of gaps with file:line and risk description]

## Phase 2: Integration Coverage
- Mode: [A — none detected / B — exists]
- [Mode A: proposed strategy + infrastructure + starter tests, or
   Mode B: N gaps within strategy, M strategy-expansion opportunities,
   with priorities]

## Phase 3: E2E Coverage
- Webapp: [yes / no — skipped]
- Mode: [A — none detected / B — exists / N/A — skipped]
- Framework: [Playwright / Cypress / other]
- [Mode A: prescribed Playwright + infrastructure + starter tests, or
   Mode B: N gaps within strategy, M strategy-expansion opportunities,
   with confirmed journey priorities]

## Phase 4: Fuzz Coverage
- Infrastructure: [present / absent + tooling recommendation]
- [N candidates with priority and properties to verify]

## Phase 5: Test Quality Audit
- N findings: X to DELETE, Y to REWRITE, Z to ADD, W to SIMPLIFY, V redundant (info)
- [Findings by category]

## Refactoring for Testability (informational)
[Refactoring suggestions from Phase 1 coverage analyst, if any. These
suggestions are not implemented by this workflow; use /refactor or
address them manually if cut as tickets.]
```

Present to the user. Walk through CRITICAL items and high-impact starter-strategy proposals (Mode A items in Phases 2 and 3) explicitly — these are the highest-leverage findings and the operator should engage with them before the ticket-structure proposal.

---

## 8. Cut Tickets

After presenting findings, propose a ticket structure based on the review's shape. Each review produces a different finding distribution — high-risk unit gaps with sparse integration coverage, Mode A starter strategies for two phases, a quality audit that is mostly tautological-test removal — and the right ticket granularity depends on that shape. Rather than prescribe a fixed mapping, examine the findings and propose a structure that fits.

### 8a. Analyze Findings and Propose Structure

Examine the consolidated findings produced in step 7:
- Count by phase and priority.
- Note Mode A starter strategies (Phases 2 and 3) — these are typically ticket-shaped as one "set up infrastructure + write starter tests" ticket or split (infrastructure separate from each starter test).
- Note clustering — multiple findings in the same file or component.
- Note REFACTOR-FOR-TESTABILITY suggestions and the fuzz tooling recommendation if present.
- Note redundant tests — informational only, no ticket needed by default.

From that shape, propose a ticket structure. Common shapes:

- **Concentrated unit gaps + small integration/E2E asks:** 1 ticket per CRITICAL unit gap; 1 batch ticket per HIGH/LOW tier; 1 ticket per integration or E2E gap; 1 batch ticket for Phase-5 quality issues.
- **Mode A starter strategies dominate:** 1 ticket per phase's starter strategy (e.g., "Set up integration test infrastructure + write 5 starter tests"); individual tickets for unit/quality findings only if there are few.
- **Lots of Phase-5 churn (many DELETE/REWRITE):** 1 batch ticket per quality category (e.g., "Delete tautological tests," "Rewrite brittle tests in `pkg/api/`").
- **Light review, scattered findings:** 1 batch ticket per phase covering all findings.
- **No actionable findings:** No tickets. The review report stands alone.

Present the proposed structure to the operator with the reasoning:

```
Proposed ticket structure for this review:

Phase 1: 8 gaps (2 CRITICAL, 3 HIGH, 3 LOW)
Phase 2: Mode B — 4 gaps within strategy
Phase 3: Mode A — Playwright not present; 5 starter tests + infrastructure
Phase 4: 2 fuzz candidates (1 HIGH, 1 MEDIUM)
Phase 5: 6 findings (2 DELETE, 3 REWRITE, 1 ADD; 2 redundant — informational)

Proposed: 7 tickets
  - 1 ticket per CRITICAL unit gap (2 tickets)
  - 1 batch ticket: "Phase 1 — HIGH/LOW unit coverage gaps" (6 gaps)
  - 1 batch ticket: "Phase 2 — Integration gaps within existing strategy" (4 gaps)
  - 1 ticket: "Set up Playwright E2E infrastructure + 5 starter tests"
  - 1 batch ticket: "Phase 4 — Fuzz test additions" (2 candidates)
  - 1 batch ticket: "Phase 5 — Test quality cleanup" (DELETE + REWRITE + ADD)
  - (Refactor-for-testability suggestions held as informational — no ticket)

Approve / edit / decline?
```

Wait for the response. Three outcomes:

- **Approve:** Proceed to 8b.
- **Edit:** The operator modifies the structure (merge two tickets, split one, drop a finding, change granularity, promote the refactoring suggestions into a ticket). Apply the edits, present the revised structure, and repeat until approved.
- **Decline:** The review report stands alone. The operator can act on findings at their discretion. The skill exits cleanly.

### 8b. Create Tickets

Use the canonical tracker integration documented in [`references/trackers.md`](../../references/trackers.md). For each ticket in the approved structure:

**Title:** `[<PHASE/TYPE>] <concise summary>` (e.g., `[Phase 1 CRITICAL] Add unit tests for auth.ValidateJWT error paths`, `[Phase 3 Mode A] Set up Playwright E2E infrastructure + starter tests`, `[Phase 5] Delete tautological tests in model_test.go and config_test.go`).

**Body sections (per-finding tickets):**
- **Gap** — what is untested or what test is problematic.
- **Files** — `file.go:LINE` for the source code and target test file.
- **Risk / Reason** — why this matters (for ADD) or what makes the test bad (for DELETE/REWRITE).
- **Should verify** — the property a new test should establish, copied from the reviewer's recommendation.
- **Acceptance criteria** — measurable definition of done (e.g., "tests added for invalid-token, expired-token, and signature-mismatch paths in `auth_test.go`; `go test ./auth/...` passes").
- **Recommended implementation skill** — names the next move with scope hint. Examples: `/implement` for a single ticket; for Mode A starter strategies, `/scope` first if the operator wants to refine the strategy before implementing.

**Body sections (batch tickets):**
- A brief intro paragraph stating the batch theme (e.g., "Phase 1 HIGH/LOW unit coverage gaps — group remediation as a single implementation pass").
- One section per included finding using the per-finding structure above.
- A single set of acceptance criteria covering the batch.

**For Mode A starter-strategy tickets (Phases 2 and 3):**
- **Strategy** — the proposed strategy (e.g., "testcontainers-based integration tests; HTTP-level against spun-up app").
- **Infrastructure** — itemized: Makefile target, build tag, fixture compose file, README.
- **Starter tests** — N starter tests with the journey/seam each exercises.
- **Out of scope** — the agent's declared out-of-scope items (especially Phase 3).
- **Acceptance criteria** — infrastructure runs, starter tests pass on first invocation.

**For Phase 5 quality tickets:**
- Preserve the per-test recommendation (DELETE / REWRITE / SIMPLIFY). For DELETE: include the "if the test covers real behavior, rewrite instead of delete" caveat from the reviewer so the implementer doesn't blindly remove tests with hidden value.

**For the fuzz tooling recommendation (if Phase 4 reported absence):**
- Optional ticket: "Adopt fuzz testing infrastructure for [language]" with the agent's tooling recommendation as the body. Cut only if the operator approves it during step 8a.

**Labels:** Apply phase-type labels (`test-coverage`, `integration-test`, `e2e`, `fuzz`, `test-quality`) when the tracker supports them. The implementation may apply a `test` umbrella label if one exists.

After all tickets are created, report the URLs to the operator and exit.

### Orchestrator-Invoked Behavior

When `/review-test` is invoked by an orchestrator (`/lead-project`, `/review-deep`, `/implement-project`), the workflow above is unchanged. The skill proposes the ticket structure to the orchestrator, which applies its own judgment per [`references/autonomy.md`](../../references/autonomy.md) — approving, editing, or declining the proposal, then deciding which of any created tickets to work in the current flow versus defer.

The contract change versus pre-v9.0.0 is that test work surfaced by `/review-test` is now durably documented in the tracker rather than implemented in-skill via SME routing. The orchestrator's decision-making is otherwise unchanged.

## Agent Coordination

**Phase 1 analysis:** Spawn `qa-test-coverage-reviewer` agent(s). For large scopes, partition and run in parallel.
**Phase 2 analysis:** Spawn single `qa-test-integration-reviewer` agent.
**Phase 3 analysis:** Spawn single `qa-test-e2e-reviewer` agent (which performs the webapp gate first).
**Phase 4 analysis:** Spawn single `qa-test-fuzz-reviewer` agent.
**Phase 5 analysis:** Spawn `qa-test-reviewer` agent(s). For large scopes, partition and run in parallel.

**No remediation agents.** Step 8 cuts tickets via the tracker integration; no `swe-sme-*` or `qa-engineer` invocations happen inside `/review-test`. Test design and implementation are handled out-of-skill by `/implement` or `/implement-project` against the cut tickets.

**Fresh instances:** Every agent spawn is a fresh instance. No state carried between invocations.

**State to maintain (as orchestrator):**
- Scope (shared across all phases)
- Coverage command and baseline metrics (Phase 1)
- Webapp detection result (used to skip Phase 3 cleanly)
- Confirmed journey classification (Phase 3, after user correction)
- Per-phase findings (accumulating)
- Refactoring suggestions (held for informational section of consolidated report)
- Tickets created at step 8 (if any)

## Abort Conditions

**Abort workflow:**
- User interrupts
- No source files found in scope

**Do NOT abort for:**
- Coverage command failure (fall back to manual analysis)
- Phase 2 reporting "no findings" (Mode B with no gaps; record and proceed)
- Phase 3 webapp gate negative (skip cleanly to Phase 4)
- Phase 4 finding no fuzz infrastructure (record tooling recommendation as informational; continue)
- Any single phase finding no issues (record and continue to next phase)
- Operator declining to cut tickets at step 8 — review report stands alone
- Tracker unavailable when the operator has approved ticket creation — surface the error; preserve the approved ticket set in the completion summary so the operator can create the tickets manually

## Integration with Other Skills

**`/review-test` vs `/test-mutation`:** Complementary. `/review-test` builds breadth (surfaces gap and quality tickets); `/test-mutation` builds depth (verifies that existing tests actually catch bugs). Recommended sequence: `/review-test` → work the cut tickets via `/implement` or `/implement-project` → `/test-mutation` to strengthen.

**`/review-test` before `/refactor`:** Run `/review-test` first to ensure the test suite is strong enough to catch regressions before refactoring. Note that gaps surfaced this way land as tickets, not as immediately-filled tests — work the cut tickets via `/implement` before invoking `/refactor` if immediate strengthening is needed.

## Example Session

```
> /review-test

What should I review?
> Entire project

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

## Phase 2: Integration Coverage

Integration test posture: NONE DETECTED (Mode A)
Seams identified: 4 (PostgreSQL, Redis cache, Stripe API, Kafka consumer)

### Proposed Strategy
- Service-level integration tests using testcontainers for Postgres + Kafka
- HTTP-level tests against the spun-up app with a real DB

### Proposed Infrastructure
- `make integration-test` with `//go:build integration` tag
- `docker-compose.test.yml` for Postgres + Kafka
- `tests/integration/README.md`

### Starter Tests (5)
1. [ADD] Signup → DB persistence → email queued (CRITICAL flow)
2. [ADD] Payment webhook handling → Stripe sig verification → DB write
3. [ADD] Login → session token issuance → Redis store
4. [ADD] Order placement → queue produce → consumer process
5. [ADD] Account deletion → cascade across tables

## Phase 3: E2E Coverage — confirm journey classification

Webapp detection: DETECTED via @playwright/test in package.json + React deps

### Critical User Journeys (please confirm)
CRITICAL: Signup, Login, Checkout
IMPORTANT: Password reset, Profile settings

⚠️  Journey classification is the most subjective part of this analysis.

Are these classifications correct?
> Yes

### Mode A — Playwright prescribed

Infrastructure: playwright.config.ts, tests/e2e/, npm run test:e2e, seeding script.
Starter tests: 5 (Signup, Login, Checkout happy path, Password reset, Profile update).
Out of scope: visual regression, a11y, performance, mobile-native, component tests.

## Phase 4: Fuzz Coverage

Fuzz infrastructure: native testing.F (Go 1.22)
Existing fuzz tests: 2

### HIGH (2 found)
1. [ADD] parser.go:ParseConfig — Parses user-provided YAML config
2. [ADD] protocol.go:DecodeMessage — Decodes wire protocol messages

## Phase 5: Test Quality Audit

### Tautological (2 found) — DELETE
- model_test.go:TestUserStruct — Checks struct field existence
- config_test.go:TestDefaultConfig — Asserts hardcoded values against themselves

### Brittle (2 found) — REWRITE
- api_test.go:TestCreateUserError — Exact error string match
- handler_test.go:TestNotFound — Asserts full JSON response body

### Missing Coverage (1 found) — ADD
- auth.go:RevokeToken — No tests for revocation path

### Redundant (1 noted — informational)
- math_test.go:TestAddVariants — 5 cases hitting same code path

## Refactoring for Testability (informational)

1. internal/scheduler/queue.go — global mutable state prevents isolated testing.
   Suggestion: thread a `Clock` interface through Schedule() so time can be controlled.
   Would enable testing: timeout / retry edge cases without sleep().

Proposed ticket structure for this review:

Phase 1: 7 gaps (2 CRITICAL, 3 HIGH, 2 LOW)
Phase 2: Mode A — full starter strategy (infra + 5 tests)
Phase 3: Mode A — full Playwright starter strategy (infra + 5 tests)
Phase 4: 2 fuzz candidates (HIGH)
Phase 5: 5 findings (2 DELETE, 2 REWRITE, 1 ADD; 1 redundant — informational)

Proposed: 8 tickets
  - 1 ticket per CRITICAL unit gap (2 tickets)
  - 1 batch ticket: "Phase 1 — HIGH/LOW unit coverage gaps" (5 gaps)
  - 1 ticket: "Set up integration test infrastructure + 5 starter tests"
  - 1 ticket: "Set up Playwright E2E infrastructure + 5 starter tests"
  - 1 batch ticket: "Phase 4 — Fuzz test additions" (2 candidates)
  - 1 batch ticket: "Phase 5 — Test quality cleanup" (DELETE + REWRITE + ADD)
  - (Refactor-for-testability suggestion held as informational — no ticket
     unless you'd like one)

Approve / edit / decline?
> Approve, and please add a ticket for the queue.go refactor-for-testability item.

Editing structure: + 1 ticket "Refactor scheduler.queue.go to enable timeout testing"

Final structure: 9 tickets. Creating...
  #N — [Phase 1 CRITICAL] Add unit tests for auth.ValidateJWT error paths
  #N — [Phase 1 CRITICAL] Add unit tests for payment.ChargeCard retry/failure
  #N — [Phase 1 HIGH/LOW] Unit coverage gap batch (5 gaps)
  #N — [Phase 2 Mode A] Integration test infrastructure + 5 starter tests
  #N — [Phase 3 Mode A] Playwright E2E infrastructure + 5 starter tests
  #N — [Phase 4] Fuzz test additions for parser and protocol (2 candidates)
  #N — [Phase 5] Test quality cleanup (delete tautological, rewrite brittle)
  #N — [Refactor-for-testability] Thread Clock interface through scheduler.queue

8 tickets created. Review complete.
```
