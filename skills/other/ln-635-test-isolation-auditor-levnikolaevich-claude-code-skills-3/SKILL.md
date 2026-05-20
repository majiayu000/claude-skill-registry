---
name: ln-635-test-isolation-auditor
description: "Test Isolation + Anti-Patterns audit worker (L3). Checks isolation (APIs/DB/FS/Time/Random/Network), determinism (flaky, order-dependent), and 7 anti-patterns."
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Test Isolation & Anti-Patterns Auditor (L3 Worker)

Specialized worker auditing test isolation and detecting anti-patterns.

## Purpose & Scope

- **Worker in ln-630 coordinator pipeline**
- Audit **Test Isolation** (Category 5: Medium Priority)
- Audit **Anti-Patterns** (Category 6: Medium Priority)
- Check determinism (no flaky tests)
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md#audit-coordinator--worker-contract` for contextStore structure.

Receives `contextStore` with: `tech_stack`, `testFilesMetadata`, `codebase_root`, `output_dir`.

## Workflow

1) **Parse Context:** Extract tech stack, isolation checklist, anti-patterns catalog, test file list, output_dir from contextStore
2) **Check Isolation:** Check isolation for 6 categories (APIs, DB, FS, Time, Random, Network)
3) **Check Determinism:** Check for flaky tests, time-dependent assertions, order-dependent tests, shared mutable state
4) **Detect Anti-Patterns:** Detect 6 anti-patterns (Liar, Giant, Slow Poke, Conjoined Twins, Happy Path, Framework Tester)
5) **Collect Findings:** Record each violation with severity, location (file:line), effort estimate (S/M/L), recommendation
6) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)
7) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/635-isolation.md` in single Write call
8) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Rules: Test Isolation

### 1. External APIs

**Good:** Mocked (jest.mock, sinon, nock)
**Bad:** Real HTTP calls to external APIs

**Detection:**
- Grep for `axios.get`, `fetch(`, `http.request` without mocks
- Check if test makes actual network calls

**Severity:** **HIGH**

**Recommendation:** Mock external APIs with `nock` or `jest.mock`

**Effort:** M

### 2. Database

**Good:** In-memory DB (sqlite :memory:) or mocked
**Bad:** Real database (PostgreSQL, MySQL)

**Detection:**
- Check DB connection strings (localhost:5432, real DB URL)
- Grep for `beforeAll(async () => { await db.connect() })` without `:memory:`

**Severity:** **MEDIUM**

**Recommendation:** Use in-memory DB or mock DB calls

**Effort:** M-L

### 3. File System

**Good:** Mocked (mock-fs, vol)
**Bad:** Real file reads/writes

**Detection:**
- Grep for `fs.readFile`, `fs.writeFile` without mocks
- Check if test creates/deletes real files

**Severity:** **MEDIUM**

**Recommendation:** Mock file system with `mock-fs`

**Effort:** S-M

### 4. Time/Date

**Good:** Mocked (jest.useFakeTimers, sinon.useFakeTimers)
**Bad:** `new Date()`, `Date.now()` without mocks

**Detection:**
- Grep for `new Date()` in test files without `useFakeTimers`

**Severity:** **MEDIUM**

**Recommendation:** Mock time with `jest.useFakeTimers()`

**Effort:** S

### 5. Random

**Good:** Seeded random (Math.seedrandom, fixed seed)
**Bad:** `Math.random()` without seed

**Detection:**
- Grep for `Math.random()` without seed setup

**Severity:** **LOW**

**Recommendation:** Use seeded random for deterministic tests

**Effort:** S

### 6. Network

**Good:** Mocked (supertest for Express, no real ports)
**Bad:** Real network requests (`localhost:3000`, binding to port)

**Detection:**
- Grep for `app.listen(3000)` in tests
- Check for real HTTP requests

**Severity:** **MEDIUM**

**Recommendation:** Use `supertest` (no real port)

**Effort:** M

## Audit Rules: Determinism

### 1. Flaky Tests

**What:** Tests that pass/fail randomly

**Detection:**
- Run tests multiple times, check for inconsistent results
- Grep for `setTimeout`, `setInterval` without proper awaits
- Check for race conditions (async operations not awaited)

**Severity:** **HIGH**

**Recommendation:** Fix race conditions, use proper async/await

**Effort:** M-L

### 2. Time-Dependent Assertions

**What:** Assertions on current time (`expect(timestamp).toBeCloseTo(Date.now())`)

**Detection:**
- Grep for `Date.now()`, `new Date()` in assertions

**Severity:** **MEDIUM**

**Recommendation:** Mock time

**Effort:** S

### 3. Order-Dependent Tests

**What:** Tests that fail when run in different order

**Detection:**
- Run tests in random order, check for failures
- Grep for shared mutable state between tests

**Severity:** **MEDIUM**

**Recommendation:** Isolate tests, reset state in beforeEach

**Effort:** M

### 4. Shared Mutable State

**What:** Global variables modified across tests

**Detection:**
- Grep for `let globalVar` at module level
- Check for state shared between tests

**Severity:** **MEDIUM**

**Recommendation:** Use `beforeEach` to reset state

**Effort:** S-M

## Audit Rules: Anti-Patterns

### 1. The Liar (Always Passes)

**What:** Test with no assertions or trivial assertion (`expect().toBeTruthy()`)

**Detection:**
- Count assertions per test
- If 0 assertions or only `toBeTruthy()` → Liar

**Severity:** **HIGH**

**Recommendation:** Add specific assertions or delete test

**Effort:** S

**Example:**
- **BAD (Liar):** Test calls `createUser()` but has NO assertions — always passes even if function breaks
- **GOOD:** Test calls `createUser()` and asserts `user.name` equals 'Alice', `user.id` is defined

### 2. The Giant (>100 lines)

**What:** Test with >100 lines, testing too many scenarios

**Detection:**
- Count lines per test
- If >100 lines → Giant

**Severity:** **MEDIUM**

**Recommendation:** Split into focused tests (one scenario per test)

**Effort:** S-M

### 3. Slow Poke (>5 seconds)

**What:** Test taking >5 seconds to run

**Detection:**
- Measure test duration
- If >5s → Slow Poke

**Severity:** **MEDIUM**

**Recommendation:** Mock external deps, use in-memory DB, parallelize

**Effort:** M

### 4. Conjoined Twins (Unit test without mocks = Integration)

**What:** Test labeled "Unit" but not mocking dependencies

**Detection:**
- Check if test name includes "Unit"
- Verify all dependencies are mocked
- If no mocks → actually Integration test

**Severity:** **LOW**

**Recommendation:** Either mock dependencies OR rename to Integration test

**Effort:** S

### 5. Happy Path Only (No error scenarios)

**What:** Only testing success cases, ignoring errors

**Detection:**
- For each function, check if test covers error cases
- If only positive scenarios → Happy Path Only

**Severity:** **MEDIUM**

**Recommendation:** Add negative tests (error handling, edge cases)

**Effort:** M

**Example:**
- **BAD (Happy Path Only):** Test only checks `login()` with valid credentials, ignores error scenarios
- **GOOD:** Add negative test that verifies `login()` with invalid credentials throws 'Invalid credentials' error

### 6. Framework Tester (Tests framework behavior)

**What:** Tests validating Express/Prisma/bcrypt (NOT our code)

**Detection:**
- Already detected by ln-631-test-business-logic-auditor
- Cross-reference findings

**Severity:** **MEDIUM**

**Recommendation:** Delete framework tests

**Effort:** S

### 7. Default Value Blindness (Tests with default config)

**What:** See `shared/references/risk_based_testing_guide.md` → Anti-Pattern 9.

**Detection:**
- Grep for common defaults in test setup: `:8080`, `:3000`, `30000`, `limit: 20`, `offset: 0`
- Check if test config values match framework/library defaults
- Look for `|| DEFAULT` patterns in source code with matching test values

**Severity:** **HIGH**

**Effort:** S

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

**Severity mapping:**
- Flaky tests, External API not mocked, The Liar, Default Value Blindness → HIGH
- Real database, File system, Time/Date, Network, The Giant, Happy Path Only → MEDIUM
- Random without seed, Order-dependent, Conjoined Twins → LOW

## Output Format

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/635-isolation.md` with `category: "Isolation & Anti-Patterns"` and checks: api_isolation, db_isolation, fs_isolation, time_isolation, random_isolation, network_isolation, flaky_tests, anti_patterns, default_value_blindness.

Return summary to coordinator:
```
Report written: docs/project/.audit/ln-630/{YYYY-MM-DD}/635-isolation.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

**Note:** Findings are flattened into single array. Use `principle` field prefix (Test Isolation / Determinism / Anti-Patterns) to identify issue category.

## Critical Rules

- **Do not auto-fix:** Report only
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Flat findings:** Merge isolation + determinism + anti-patterns into single findings array, use `principle` prefix to distinguish
- **Cross-reference ln-631:** Framework Tester anti-pattern (Rule 6) references ln-631 findings — do not duplicate
- **Context-aware:** Supertest with real Express app is acceptable for integration tests

## Definition of Done

- contextStore parsed successfully (including output_dir)
- All 3 audit groups completed:
  - Isolation (6 categories: APIs, DB, FS, Time, Random, Network)
  - Determinism (4 checks: flaky, time-dependent, order-dependent, shared state)
  - Anti-patterns (7 checks: Liar, Giant, Slow Poke, Conjoined Twins, Happy Path, Framework Tester, Default Value Blindness)
- Findings collected with severity, location, effort, recommendation
- Score calculated using penalty algorithm
- Report written to `{output_dir}/635-isolation.md` (atomic single Write call)
- Summary returned to coordinator

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
