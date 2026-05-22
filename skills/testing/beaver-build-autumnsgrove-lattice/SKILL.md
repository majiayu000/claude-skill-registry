---
name: beaver-build
description: Build robust test dams that catch bugs before they flood production. The beaver surveys the stream, gathers materials wisely, builds with care, reinforces thoroughly, and ships with confidence. Use when writing tests, deciding what to test, or reinforcing code.
---

# Beaver Build 🦫

The beaver doesn't build blindly. First, it surveys the stream, understanding the flow. Then it gathers only the best materials — not every twig belongs in the dam. It builds with purpose, each piece placed carefully. It reinforces with mud and care, creating something that withstands the current. When the dam holds, the forest is safe.

## When to Activate

- User asks to "write tests" or "add tests"
- User says "test this" or "make sure this works"
- User calls `/beaver-build` or mentions beaver/building dams
- Deciding what deserves testing (not everything does)
- Reviewing existing tests for effectiveness
- A bug needs to become a regression test
- Asked to "add tests" without specific guidance
- Evaluating whether tests are providing real value
- Refactoring causes many tests to break (symptom of bad tests)

**Pair with:** `javascript-testing` for Vitest syntax, `python-testing` for pytest patterns

---

## The Dam

```
SURVEY → GATHER → BUILD → REINFORCE → FORTIFY
   ↓        ↲        ↓          ↲          ↓
Understand Collect  Construct   Harden    Ship with
Flow     Materials  Tests       Coverage  Confidence
```

### Phase 1: SURVEY

_The beaver surveys the stream, understanding the flow before placing a single twig..._

Before gathering materials, understand what you're building for.

- What does this feature DO for users? (Not how it works — what value it provides)
- What would break if this failed? (Critical paths)
- What confidence level is needed? (Prototype vs. production)
- The Testing Trophy: mostly integration, some unit, few E2E, static analysis always on

**Reference:** Load `references/testing-patterns.md` for the full Testing Trophy explanation, what to test vs. skip, the guiding questions, and what makes a test valuable

**Output:** Brief summary of what needs testing and at what layer

---

### Phase 2: GATHER

_Paws select only the best branches. Not everything belongs in the dam..._

Decide what to test using the Confidence Test.

- Skip: trivial getters/setters, framework behavior, implementation details, one-off scripts, volatile prototypes
- Test lightly: configuration (smoke test), third-party integrations (mock at boundary), visual design (snapshots)
- Test thoroughly: business logic, user-facing flows, edge cases, bug fixes

Ask: "Would I notice if this broke in production?" If yes, test it.

**Reference:** Load `references/testing-patterns.md` for the full skip/test-lightly/test-thoroughly tables and the guiding questions

**Output:** List of test cases to write, organized by layer (unit/integration/E2E)

---

### Phase 3: BUILD

_Twig by twig, the dam takes shape. Each piece has purpose..._

Write tests following Arrange-Act-Assert.

- The Act section should be one line — if it's not, the test does too much
- Test user behavior, not implementation details
- Use accessible queries: `getByRole`, `getByLabelText`, `getByText` — never `getByTestId` first
- Name tests so they explain what breaks: "should reject registration with invalid email"
- One test, one reason to fail

**Reference:** Load `references/test-templates.md` for complete SvelteKit test templates: service unit tests, API route tests, component tests with Testing Library, and integration tests for full flows

**Output:** Working tests that follow AAA pattern and test behavior, not implementation

---

### Phase 4: REINFORCE

_The beaver packs mud between twigs, hardening the structure..._

Strengthen tests.

- Mock only at external boundaries — if you're mocking something you wrote, reconsider
- Turn every bug into a regression test: reproduce → write failing test → fix → test passes → bug can't return
- Keep tests co-located with the code they test (`login.test.ts` next to `login.ts`)
- Verify Signpost error format in API tests: `error_code`, `error`, `error_description`

**Reference:** Load `references/testing-patterns.md` for the minimal mocking guide, bug-to-test pipeline, and Signpost error code coverage patterns

**Output:** Hardened tests with proper mocking boundaries and clear failure messages

---

### Phase 5: FORTIFY

_The dam holds. Water flows as intended. The beaver rests..._

**MANDATORY: Verify the dam holds before shipping:**

```bash
pnpm install
gw ci --affected --fail-fast --diagnose
```

If verification fails: the dam has a leak. Read the diagnostics, patch the weakness, re-run verification.

Additional coverage check (optional, after CI passes):

```bash
npx vitest run --coverage
```

Run the self-review checklist before considering tests "done".

**Reference:** Load `references/test-templates.md` for the test self-review checklist

**Output:** Clean test suite ready for CI

---

## Reference Routing Table

| Phase | Reference | Load When |
|-------|-----------|-----------|
| SURVEY | `references/testing-patterns.md` | Always (understand the Trophy and what to test) |
| GATHER | `references/testing-patterns.md` | Deciding what to skip vs. test thoroughly |
| BUILD | `references/test-templates.md` | Writing actual tests (service, API, component) |
| REINFORCE | `references/testing-patterns.md` | Mocking strategy and bug-to-test pipeline |
| FORTIFY | `references/test-templates.md` | Running the self-review checklist |

---

## Beaver Rules

### Energy

Build with purpose. The beaver doesn't add twigs just to add them. Each test must earn its place by providing confidence.

### Precision

Test behavior, not structure. If refactoring breaks your tests, they were testing the wrong things.

### Wisdom

Remember the trophy: mostly integration, some unit, few E2E. Static analysis is your first line of defense.

### Patience

Good tests let you ship with confidence. That's the whole point.

### Communication

Use building metaphors:

- "Surveying the stream..." (understanding what to test)
- "Gathering materials..." (deciding what to test)
- "The dam takes shape..." (writing tests)
- "Packing the mud..." (adding coverage)
- "The structure holds..." (tests passing)

---

## Anti-Patterns

**The beaver does NOT:**

- Chase 100% coverage theater (high coverage with bad tests is worse than moderate coverage with good tests)
- Test implementation details (internal state, private methods)
- Mock everything (removes confidence)
- Write tests that break on safe refactors
- Use snapshots for volatile UI
- Build the Ice Cream Cone (many E2E, few integration, few unit)

---

## Example Build

**User:** "Add tests for the login form"

**Beaver flow:**

1. 🦫 **SURVEY** — "Login form handles user authentication. Critical path: registration → dashboard flow. Integration tests where confidence lives."

2. 🦫 **GATHER** — "Test: invalid email rejection, API error handling, successful redirect, loading states. Skip: internal state changes."

3. 🦫 **BUILD** — Write integration tests using AAA pattern: `should reject registration with invalid email`, `should show loading indicator while logging in`, `should redirect to dashboard after successful login`

4. 🦫 **REINFORCE** — Add regression test for previous password reset bug. Mock only external API, not internal validation.

5. 🦫 **FORTIFY** — All tests pass, lint and typecheck clean, coverage at 78% (good enough), ready for CI.

---

## Quick Decision Guide

| Situation | Action |
|-----------|--------|
| New feature | Write integration tests for user-facing behavior |
| Bug fix | Write test that reproduces bug first, then fix |
| Refactoring | Run existing tests; if they break on safe changes, they're bad tests |
| "Need more coverage" | Add tests for uncovered **behavior**, not uncovered lines |
| Pure function/algorithm | Unit test it |
| API endpoint | Integration test with mocked external services |
| UI component | Component test with Testing Library |
| Critical user flow | E2E test with Playwright |

---

_Good tests let you ship with confidence. That's the whole point._ 🦫
