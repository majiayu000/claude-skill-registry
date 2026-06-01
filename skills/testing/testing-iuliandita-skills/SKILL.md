---
name: testing
description: >
  · Write/debug tests: unit, integration, E2E, TDD, mocks, fixtures, a11y, perf. Triggers: 'test', 'spec', 'TDD', 'playwright', 'vitest', 'jest', 'pytest', 'coverage', 'flaky'. Not for security tests (use security-audit).
license: MIT
compatibility: "Requires one or more of: vitest, jest, pytest, go test, cargo test, playwright"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-02"
  effort: high
  argument_hint: "[scope-or-file]"
---

# Testing: Write Tests That Catch Real Bugs

Write, structure, and maintain tests across unit, integration, E2E, accessibility, and performance layers. The goal is tests that catch regressions, document behavior, and run fast in CI - not tests that exist to inflate coverage numbers.

**Target versions** (May 2026):
- Vitest **4.1.2**, Jest **30.3.0**
- Playwright **1.59.0**, Cypress **15.13.0**
- pytest **9.0.2**, pytest-cov **7.1.0**
- Go **1.26.1** (testing stdlib, `testing/synctest` GA)
- Rust **1.94.1** (`cargo test`, cargo-nextest **0.9.132**)
- Testing Library **16.3.2** (`@testing-library/react`)
- axe-core **4.11.2** (`@axe-core/playwright`)
- Grafana k6 **1.7.1** (load testing)

## When to use

- Writing new tests (unit, integration, E2E, accessibility, performance)
- Debugging flaky or failing tests
- Designing test architecture for a project (fixture strategies, factory patterns, test data)
- Setting up test infrastructure in CI (parallelization, sharding, coverage gates)
- Choosing testing tools or migrating between test frameworks
- Implementing TDD workflow
- Adding accessibility or visual regression tests to an existing suite

## When NOT to use

- Reviewing existing test quality or correctness as part of a code review - use **code-review**
- Security-specific testing (penetration testing, OWASP checks) - use **security-audit**
- Cleaning up verbose/sloppy test code - use **anti-slop**
- Ad-hoc web browsing, scraping, or page interaction outside of tests - use **browse**
- CI/CD pipeline architecture (test jobs run inside pipelines, but pipeline design is ci-cd's domain) - use **ci-cd**
- Database testing patterns at the engine level - use **databases**
- Writing or refining LLM prompts (use **prompt-generator**)
- Infrastructure or configuration validation outside tests (use **terraform**, **ansible**, or **kubernetes**)
- AI/ML model evaluation or LLM output scoring - use **ai-ml**
- Infrastructure-level load or chaos testing beyond application tests (use **kubernetes** for cluster-level chaos, or **ci-cd** for pipeline-integrated load test orchestration)

---

## AI Self-Check

AI tools consistently produce the same testing mistakes. **Before returning any generated test code, verify against this list:**

- [ ] Tests assert behavior, not implementation - no testing private methods or internal state
- [ ] Each test has exactly one reason to fail (single assertion concept, not single `assert` call)
- [ ] Test names describe the scenario and expected outcome, not the method name
- [ ] Mocks/stubs are scoped to the test - no shared mutable mock state across tests
- [ ] No hardcoded ports, paths, or timestamps that break on other machines or in CI
- [ ] Async tests properly await all promises/futures - no fire-and-forget assertions
- [ ] Test data is isolated - each test creates its own state, no dependency on test execution order
- [ ] Cleanup happens even when assertions fail (use `afterEach`/`teardown`/`t.Cleanup`/`Drop`)
- [ ] No `sleep()` or fixed delays for async waits - use polling, retries, or event-based waits
- [ ] Coverage threshold is realistic (80% line coverage is a good default; 100% is a lie)
- [ ] Snapshot tests have been reviewed manually before committing (blind `--update` is a bug factory)
- [ ] E2E selectors use `data-testid`, `role`, or accessible names - not CSS classes or DOM structure
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Runner APIs current**: pytest, Vitest, Jest, Playwright, and Testing Library examples match current runner behavior
- [ ] **Flake source identified**: retries are not used to hide nondeterminism without diagnosis

---

## Performance

- Split fast unit tests from integration, browser, and performance suites.
- Use fixtures and test data builders to avoid repeated expensive setup.
- Shard or parallelize only after isolating shared state, ports, databases, and clocks.


---

## Best Practices

- Test behavior through stable public interfaces, not implementation details.
- Use stable roles/test IDs for UI tests; do not select generated CSS classes.
- Every regression fix gets a failing test that would have caught the bug.


## Workflow

### Step 1: Determine scope

Based on context:
- **New feature** -> write tests alongside or before the code (TDD when appropriate)
- **Bug fix** -> write a failing test first that reproduces the bug, then fix
- **Existing untested code** -> prioritize critical paths, not 100% coverage
- **Test infrastructure** -> set up runners, CI config, coverage gates

Identify the project's existing test framework from config files (`vitest.config.ts`, `jest.config.*`, `pyproject.toml`, `Cargo.toml`, `*_test.go`, `playwright.config.ts`). Match it. Don't introduce a second test runner without a reason.

### Step 2: Choose the test layer

| Layer | Tests what | Speed | When to use |
|-------|-----------|-------|-------------|
| **Unit** | Single function/module in isolation | ms | Pure logic, utilities, data transforms, state machines |
| **Integration** | Multiple modules, real dependencies | seconds | API handlers, database queries, service boundaries |
| **E2E** | Full user flows through the UI | seconds-minutes | Critical paths, checkout flows, auth, onboarding |
| **Accessibility** | WCAG compliance, screen reader compat | seconds | Every user-facing component/page |
| **Visual** | Screenshot comparison | seconds | UI components after style changes |
| **Performance** | Load, latency, throughput | minutes | Before releases, after arch changes |

**The testing pyramid still holds**: many unit tests, fewer integration tests, fewest E2E tests. Invert it and your CI takes 45 minutes and everyone ignores test failures.

### Step 3: Write the test

Follow the language-specific patterns below. Universal principles:

**Arrange-Act-Assert** (or Given-When-Then):
```
// Arrange: set up test data and dependencies
// Act: call the thing being tested
// Assert: verify the outcome
```

**Test naming**: describe the scenario, not the function.
```
# Bad:  test_calculate_total
# Good: test_calculate_total_applies_discount_when_cart_exceeds_100
# Good: it("returns 401 when token is expired")
```

### Step 4: Validate

- Run the full test suite: failures in other tests may indicate your change broke something
- Check coverage delta: new code should be covered, but don't chase vanity numbers
- Run in CI if possible - tests that pass locally but fail in CI are the worst kind

---

## TDD Workflow

Use TDD when the behavior is well-defined upfront. Skip it when exploring or prototyping.

1. **Red**: write a test that fails (confirm it fails for the right reason)
2. **Green**: write the minimum code to make the test pass (ugly is fine)
3. **Refactor**: clean up without changing behavior (tests still pass)

TDD works best for: pure functions, data transformations, state machines, API contracts, bug reproduction.

TDD works poorly for: UI layout, exploratory prototyping, integration with undocumented APIs.

---

## Mocking Strategy

Mock at boundaries, not everywhere. Over-mocking produces tests that pass while the real code is broken.

| What to mock | What NOT to mock |
|-------------|-----------------|
| External APIs (HTTP, gRPC) | Your own pure functions |
| Database (when unit testing) | Data transformations |
| Time/dates, random values | Simple utility code |
| File system (when impractical) | The module under test |
| Third-party SDKs | Standard library functions |

**Prefer fakes over mocks when possible.** An in-memory database implementation tests more real behavior than a mock that returns canned responses.

**Injectable clock for TTL/time-dependent tests** - pass a clock dependency rather than calling `Date.now()` or `time.Now()` directly:

```typescript
// Production: clock = () => Date.now()
// Test: clock = () => FIXED_TS + offset
function isExpired(createdAt: number, ttlMs: number, clock = Date.now): boolean {
  return clock() - createdAt > ttlMs;
}
// In test: advance virtual time without sleeping
const fakeNow = vi.fn().mockReturnValue(START);
expect(isExpired(START, 1000, fakeNow)).toBe(false);
fakeNow.mockReturnValue(START + 1001);
expect(isExpired(START, 1000, fakeNow)).toBe(true);
```

Read `references/language-patterns.md` for language-specific mocking idioms (Vitest `vi.mock`, Jest `jest.mock`, pytest `monkeypatch`, Go interfaces, Rust trait objects).

---

## Test Data and Fixtures

### Factory pattern (preferred)

Build test data with sensible defaults and per-test overrides:

```typescript
// TypeScript - factory function
function buildUser(overrides: Partial<User> = {}): User {
  return { id: randomUUID(), name: "Test User", email: "test@example.com", ...overrides };
}

// Python - factory function
def build_user(**overrides) -> User:
    defaults = {"id": uuid4(), "name": "Test User", "email": "test@example.com"}
    return User(**(defaults | overrides))
```

### Fixture rules

- **Isolate per test.** Shared mutable fixtures cause order-dependent failures.
- **Use builders/factories** over raw object literals - defaults prevent test brittleness.
- **Database fixtures**: use transactions that roll back after each test (pytest `db` fixture, Jest `beforeEach` with rollback). Seeded test databases beat shared staging data.
- **File fixtures**: use temp directories (`tmp_path` in pytest, `os.MkdirTemp` in Go, `tempfile` in Rust). Clean up in teardown.

---

## Accessibility Testing

Catch WCAG violations automatically. Not a replacement for manual testing, but catches the mechanical stuff (missing alt text, broken ARIA, contrast ratios, keyboard traps).

Use `@axe-core/playwright` - run `new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze()` and assert zero violations. Run axe scans on every page/component. Exclude known issues with `.exclude()` and track them as tech debt, not permanent exceptions.

Read `references/e2e-accessibility.md` for Playwright E2E patterns, visual regression setup, and CI accessibility gates.

---

## Performance Testing

Two categories: **micro-benchmarks** (is this function fast enough?) and **load tests** (does the system handle traffic?).

### Micro-benchmarks

- **Go**: `func BenchmarkX(b *testing.B)` - built into the stdlib
- **Rust**: `cargo bench` with criterion (`criterion = "0.6"`)
- **JS/TS**: `vitest bench` or `tinybench`
- **Python**: `pytest-benchmark` or `timeit`

### Load testing (k6)

```javascript
// k6 load test
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 50 },   // ramp up
    { duration: "1m",  target: 50 },   // sustain
    { duration: "10s", target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"],   // 95th percentile under 500ms
  },
};

export default function () {
  const res = http.get("http://localhost:3000/api/health");
  check(res, { "status 200": (r) => r.status === 200 });
  sleep(1);
}
```

Don't run load tests against production without explicit approval. Don't run them in CI unless you have dedicated infrastructure for it.

---

## CI Integration

### Test parallelization

- **Vitest/Jest**: built-in worker parallelism. Vitest uses Vite's module graph for smart test file distribution.
- **Playwright**: `--shard=1/4` for splitting across CI runners. `--workers=4` for parallel within a runner.
- **pytest**: `pytest-xdist` with `-n auto` for CPU-based parallelism.
- **Go**: `go test -parallel N` per package, `-p N` for package-level parallelism.
- **Rust**: `cargo nextest run` for per-test process isolation and parallelism.

### Flaky test management

Flaky tests erode trust. Fix or quarantine immediately.

1. **Identify**: track test stability over time (most CI systems have flaky test dashboards)
2. **Quarantine**: move to a separate job that doesn't block merges. Tag with `@flaky` or `skip`.
3. **Fix root causes** - common culprits by framework:
   - **Playwright/Cypress**: race conditions on navigation or animation. Use `waitForLoadState`,
     `waitForSelector`, or Playwright's auto-waiting. Avoid `page.waitForTimeout`. Stub network
     requests to eliminate backend variability. Headless mode (CI) has different rendering
     timing than headed - animations may be skipped or font metrics differ; use
     `--headed` locally to reproduce CI-only failures.
   - **Vitest/Jest**: shared module state between test files. Use `--pool forks` (Vitest) or
     `--runInBand` to isolate. Check for leaked timers (`vi.useFakeTimers` not restored).
   - **pytest**: database state leaking between tests. Use `@pytest.mark.usefixtures("db")`
     with transactional rollback. Check for global state mutation in fixtures.
   - **Go**: `t.Parallel()` tests sharing package-level state. Use `t.Cleanup` for teardown.
     Check for goroutine leaks with `goleak`.
4. **Retry with caution**: `--retries 2` (Playwright) or `--reruns 2` (pytest-rerunfailures) is a bandaid, not a fix

### Coverage thresholds

Set coverage gates in CI. Reasonable defaults:

| Metric | Threshold | Why |
|--------|-----------|-----|
| Line coverage | 80% | Catches obvious gaps |
| Branch coverage | 70% | Catches untested conditions |
| New code coverage | 90% | Prevents coverage erosion |

Enforce via `vitest --coverage --coverage.thresholds.lines=80`, `pytest --cov --cov-fail-under=80`, or `go test -coverprofile` + threshold script.

**Minimal CI example (pytest + GitHub Actions)**:
```yaml
- run: pip install pytest pytest-xdist pytest-cov
- run: pytest -n auto --cov=src --cov-fail-under=80 --tb=short
```

---

## Reference Files

- `references/language-patterns.md` - language-specific test patterns for JS/TS (Vitest, Jest), Python (pytest), Go (testing stdlib), and Rust (cargo test). Covers mocking, table-driven tests, async testing, snapshot testing, and framework-specific idioms.
- `references/e2e-accessibility.md` - E2E testing with Playwright, visual regression (screenshot comparison, component snapshots), accessibility testing patterns, and CI integration for browser tests.

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** TESTING
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/testing/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **code-review** - reviews test quality and correctness as part of code reviews. This skill writes the tests; code-review evaluates whether they actually test the right things.
- **security-audit** - handles security-specific testing (OWASP, penetration testing, credential scanning). This skill handles functional testing.
- **anti-slop** - cleans up verbose, over-abstracted, or AI-generated test code. If the test works but reads like a novel, route to anti-slop.
- **ci-cd** - designs the pipeline that runs tests. This skill writes the tests and configures test runners; ci-cd handles the pipeline structure around them.
- **databases** - covers database engine testing and configuration. This skill handles application-level database test patterns (transactions, fixtures, test data).
- **ai-ml** - AI/ML model evaluation, LLM output scoring, and benchmark harnesses. This skill handles functional application testing; ai-ml handles model-level evaluation.
- **kubernetes** - cluster-level chaos, resilience, and infrastructure-layer load testing. This skill handles application test code; kubernetes handles cluster-level fault injection.

---

## Rules

1. **Test behavior, not implementation.** Tests coupled to internal structure break on every refactor and catch zero bugs. If a test mocks 8 things and asserts a method was called with specific args, it's testing the mock, not the code.
2. **No `sleep()` in tests.** Use `waitFor`, `Eventually`, `poll`, retry loops, or event-based synchronization. Fixed delays are flaky by definition.
3. **Isolate test state.** Each test creates its own data, runs independently, and cleans up after itself. Shared mutable state between tests is the #1 cause of order-dependent failures.
4. **Fix or quarantine flaky tests immediately.** A test suite people ignore is worse than no test suite. Track flaky tests, fix root causes, don't just retry.
5. **Don't test the framework.** Testing that React renders a div, or that Express routes to a handler, is testing someone else's code. Test YOUR logic.
6. **Run the AI self-check.** Every generated test gets verified against the checklist before returning. AI-generated tests love to test implementation details, use `sleep()`, and share state.
7. **Match the existing framework.** Don't introduce Vitest into a Jest project or pytest into a unittest project without the user explicitly asking for a migration.
8. **Snapshot tests require manual review.** Never auto-update snapshots (`-u` / `--update`) without reviewing the diff. Blind snapshot updates are equivalent to deleting the test.
