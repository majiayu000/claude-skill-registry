---
name: test-driven-execution
description: >
  Before writing any implementation code, define the acceptance criteria and
  test cases that the code must satisfy. Agents then write code to pass these
  tests — not to match a vague description. Eliminates "it works on my machine"
  and "I think this is what you wanted" outcomes.
---

<!--
  TÜRKÇE AÇIKLAMA
  ───────────────
  Bu skill, implementasyon kodu yazmadan önce "başarı kriterleri"ni ve test senaryolarını
  tanımlar. Agent, kodu belirsiz bir tanıma değil — somut testleri geçmek için yazar.
  Kırmızı→Yeşil→Refactor döngüsünü uygular. "Bence çalışıyor" yerine "testler geçiyor" der.

  NE ZAMAN: Her yeni feature veya bug fix'ten önce. Test spec olmadan kod yazılmaz.
  ÇIKTI:    Geçen testler, coverage raporu, "Task Complete" özeti.
-->

# Test-Driven Execution Skill

## When to Trigger

- At the start of any feature or task from a plan
- When a bug fix is requested (test first, then fix)
- When a subagent is about to implement a module
- When "done" is ambiguous and needs a clear definition

## Philosophy

> "A feature is not done when code is written. It is done when the tests pass."

Tests written *before* code serve three purposes:
1. They force clarity on what "correct" actually means
2. They prevent the agent from drifting into over-engineering
3. They provide instant verification that the task is complete

## Step-by-Step Process

### 1. Extract Acceptance Criteria

Read the task description and extract every "must" and "should":

**Example task:** *"Add a user registration endpoint"*

Extracted criteria:
- Must accept `email`, `password`, `name` in request body
- Must return 201 on success with the created user (excluding password)
- Must return 400 if email is already registered
- Must return 422 if fields are missing or invalid
- Must hash the password before storing

### 2. Write the Test Specification

Before writing any implementation, write the tests (or test outlines):

#### For unit tests:

```javascript
describe('registerUser()', () => {
  it('creates a user with hashed password', async () => { ... })
  it('throws DuplicateEmailError if email already exists', async () => { ... })
  it('throws ValidationError if email format is invalid', async () => { ... })
  it('never stores plaintext password', async () => { ... })
})
```

#### For integration/API tests:

```javascript
describe('POST /api/auth/register', () => {
  it('returns 201 and user object (without password) on success', async () => { ... })
  it('returns 400 when email already registered', async () => { ... })
  it('returns 422 when required fields missing', async () => { ... })
})
```

#### For UI/E2E tests:

```
Scenario: Successful registration
  Given I am on the /register page
  When I fill in valid email, password, and name
  And I click "Create Account"
  Then I should be redirected to /dashboard
  And I should see "Welcome, <name>"
```

### 3. Confirm Tests Fail (Red)

Run the tests *before* writing any implementation:

```bash
npm test
# or
pytest
# etc.
```

**Expected:** All new tests fail. This confirms the tests are correctly detecting the absence of the feature. If a test passes before implementation, the test is wrong — fix it.

### 4. Write the Minimum Implementation (Green)

Now implement the feature. The goal is simple: **make the tests pass**.

Rules during implementation:
- Write only what is needed to pass the tests — nothing more
- If you find yourself writing code with no corresponding test, stop and write the test first
- Don't optimize yet — correctness first

```bash
# Keep running tests as you go
npm test --watch
```

### 5. Refactor (Refactor)

Once all tests pass:
- Clean up the code (naming, structure, duplication)
- Run tests again after every refactor step to confirm nothing broke
- Add edge case tests for anything discovered during implementation

### 6. Define the Done Checklist

A task is complete when:

- [ ] All acceptance criteria from Step 1 have a corresponding test
- [ ] All tests pass (`npm test` exits with code 0)
- [ ] No test is skipped (no `.skip`, `xtest`, `# noqa`)
- [ ] Code coverage for the new module is ≥ 80% (check with `--coverage`)
- [ ] No existing tests were broken by this change

### 7. Report Completion

```
## Task Complete: <feature name>

**Tests written:** <N>
**Tests passing:** <N>/<N>
**Coverage:** <X>%
**Acceptance criteria covered:**
  ✅ Creates user with hashed password
  ✅ Returns 400 on duplicate email
  ✅ Returns 422 on validation failure
  ✅ Never stores plaintext password

**Not covered (and why):**
  ⚠️ Email delivery test — skipped, requires mock SMTP setup
```

## Test Naming Convention

Test names must read as requirements:

✅ `it('returns 400 when email already exists')`
✅ `it('never exposes password in API response')`
❌ `it('test email duplicate')`
❌ `it('works correctly')`

If you can't name the test clearly, the requirement isn't clear enough — clarify before writing.

## Rules

- **No implementation before test spec.** The spec can be pseudocode / outlines, but it must exist.
- **A failing test is not a failure** — it is a correctly written test in the red phase.
- **Never delete a test to make the suite pass.** Fix the code or fix the test — with justification.
- **Integration tests are not optional** for public-facing APIs.
- **Coverage % is a proxy, not a goal.** 100% coverage with meaningless assertions is worse than 70% with real ones.
