---
name: ln-635-test-isolation-auditor
description: Test Isolation + Anti-Patterns audit worker (L3). Checks isolation (APIs/DB/FS/Time/Random/Network), determinism (flaky, order-dependent), and 6 anti-patterns.
allowed-tools: Read, Grep, Glob, Bash
---

# Test Isolation & Anti-Patterns Auditor (L3 Worker)

Specialized worker auditing test isolation and detecting anti-patterns.

## Purpose & Scope

- **Worker in ln-630 coordinator pipeline**
- Audit **Test Isolation** (Category 5: Medium Priority)
- Audit **Anti-Patterns** (Category 6: Medium Priority)
- Check determinism (no flaky tests)
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with isolation checklist, anti-patterns catalog, test file list.

## Workflow

1) Parse context
2) Check isolation for 6 categories
3) Check determinism
4) Detect 6 anti-patterns
5) Collect findings
6) Calculate score
7) Return JSON

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

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

**Severity mapping:**
- Flaky tests, External API not mocked, The Liar → HIGH
- Real database, File system, Time/Date, Network, The Giant, Happy Path Only → MEDIUM
- Random without seed, Order-dependent, Conjoined Twins → LOW

## Output Format

**Return JSON to coordinator (flat findings array):**
```json
{
  "category": "Isolation & Anti-Patterns",
  "score": 6,
  "total_issues": 18,
  "critical": 0,
  "high": 5,
  "medium": 10,
  "low": 3,
  "checks": [
    {"id": "api_isolation", "name": "API Isolation", "status": "failed", "details": "2 tests make real HTTP calls"},
    {"id": "db_isolation", "name": "Database Isolation", "status": "warning", "details": "1 test uses real PostgreSQL"},
    {"id": "fs_isolation", "name": "File System Isolation", "status": "passed", "details": "All FS calls mocked"},
    {"id": "time_isolation", "name": "Time Isolation", "status": "passed", "details": "All Date/Time mocked"},
    {"id": "flaky_tests", "name": "Flaky Tests", "status": "failed", "details": "3 race conditions detected"},
    {"id": "anti_patterns", "name": "Anti-Patterns", "status": "warning", "details": "2 Liars, 1 Giant found"}
  ],
  "findings": [
    {
      "severity": "HIGH",
      "location": "user.test.ts:45-52",
      "issue": "External API not mocked — test makes real HTTP call to https://api.github.com",
      "principle": "Test Isolation / External APIs",
      "recommendation": "Mock external API with nock or jest.mock",
      "effort": "M"
    },
    {
      "severity": "HIGH",
      "location": "async.test.ts:28-35",
      "issue": "Flaky test (race condition) — setTimeout without proper await",
      "principle": "Determinism / Race Condition",
      "recommendation": "Fix race condition with proper async/await",
      "effort": "M"
    },
    {
      "severity": "HIGH",
      "location": "user.test.ts:45",
      "issue": "Anti-pattern 'The Liar' — test 'createUser works' has no assertions",
      "principle": "Anti-Patterns / The Liar",
      "recommendation": "Add specific assertions or delete test",
      "effort": "S"
    },
    {
      "severity": "MEDIUM",
      "location": "db.test.ts:12",
      "issue": "Real database used — test connects to localhost:5432 PostgreSQL",
      "principle": "Test Isolation / Database",
      "recommendation": "Use in-memory SQLite (:memory:) or mock DB",
      "effort": "L"
    },
    {
      "severity": "MEDIUM",
      "location": "order.test.ts:200-350",
      "issue": "Anti-pattern 'The Giant' — test 'order flow' is 150 lines (>100)",
      "principle": "Anti-Patterns / The Giant",
      "recommendation": "Split into focused tests (one scenario per test)",
      "effort": "M"
    },
    {
      "severity": "MEDIUM",
      "location": "payment.test.ts",
      "issue": "Anti-pattern 'Happy Path Only' — only success scenarios, no error tests",
      "principle": "Anti-Patterns / Happy Path Only",
      "recommendation": "Add negative tests for error handling",
      "effort": "M"
    }
  ]
}
```

**Note:** Findings are flattened into single array. Use `principle` field prefix (Test Isolation / Determinism / Anti-Patterns) to identify issue category.

## Reference Files

- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
