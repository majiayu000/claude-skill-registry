---
name: beaver-build
description: Build robust test dams that catch bugs before they flood production. The beaver surveys the stream, gathers materials wisely, builds with care, reinforces thoroughly, and ships with confidence. Use when writing tests, deciding what to test, or reinforcing code.
---

# Beaver Build 🦫

The beaver doesn't build blindly. First, it surveys the stream, understanding the flow. Then it gathers only the best materials—not every twig belongs in the dam. It builds with purpose, each piece placed carefully. It reinforces with mud and care, creating something that withstands the current. When the dam holds, the forest is safe.

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

*The beaver surveys the stream, understanding the flow before placing a single twig...*

Before gathering materials, understand what you're building for:

**What does this feature DO for users?** (Not how it works—what value it provides)

**What would break if this failed?** (Critical paths)

**What's the confidence level needed?** (Prototype vs. production)

**The Testing Trophy** (where confidence lives):

```
                    ╭─────────╮
                    │   E2E   │  ← Few: critical user journeys
                    ╰────┬────╯
               ╭─────────┴─────────╮
               │   Integration     │  ← Many: this is where confidence lives
               ╰─────────┬─────────╯
                  ╭──────┴──────╮
                  │    Unit     │  ← Some: pure functions, algorithms
                  ╰──────┬──────╯
              ╭──────────┴──────────╮
              │   Static Analysis   │  ← TypeScript, ESLint (always on)
              ╰─────────────────────╯
```

**What Each Layer Does:**

**Static Analysis (TypeScript, ESLint)**
- Catches typos, type errors, obvious mistakes
- Zero runtime cost, always running
- This is your first line of defense

**Unit Tests**
- Pure functions, algorithms, utilities
- Fast, isolated, easy to debug
- Don't mock everything—test real behavior where practical

**Integration Tests (THE SWEET SPOT)**
- Multiple units working together
- Tests behavior users actually experience
- Less brittle than unit tests, faster than E2E
- **This is where most of your tests should live**

**E2E Tests (Playwright)**
- Critical user journeys only: login, checkout, core flows
- Expensive to write and maintain
- Reserve for flows where failure = business impact

**Output:** Brief summary of what needs testing and at what layer

---

### Phase 2: GATHER

*Paws select only the best branches. Not everything belongs in the dam...*

Decide **what** to test using the Confidence Test:

**Skip Testing:**

| What | Why |
|------|-----|
| **Trivial code** | Getters, setters, data models with no logic |
| **Framework behavior** | Trust that SvelteKit routing works |
| **Implementation details** | Internal state, private methods, CSS classes |
| **One-off scripts** | Maintenance cost exceeds value |
| **Volatile prototypes** | Requirements unclear, code will change |

**Test Lightly:**

| What | Approach |
|------|----------|
| **Configuration** | Smoke test that it loads, not every option |
| **Third-party integrations** | Mock at boundaries, test your code's response |
| **Visual design** | Snapshot tests or visual regression, not unit tests |

**Test Thoroughly:**

| What | Why |
|------|-----|
| **Business logic** | Core value of the application |
| **User-facing flows** | What users actually experience |
| **Edge cases** | Error states, empty states, boundaries |
| **Bug fixes** | Every bug becomes a test to prevent regression |

**The Guiding Principle:**

> *"The more your tests resemble the way your software is used, the more confidence they can give you."*
> — Kent C. Dodds (Testing Library)

Ask: **Would I notice if this broke in production?** If yes, test it.

Ask: **Does this test fail when the feature breaks?** If no, don't write it.

Ask: **Does this test resemble how users interact with the feature?** If no, reconsider.

**What Makes a Test Valuable** (Kent Beck's Test Desiderata):

| Property | What It Means |
|----------|---------------|
| **Behavior-sensitive** | Fails when actual functionality breaks |
| **Structure-immune** | Doesn't break when you refactor safely |
| **Deterministic** | Same result every time, no flakiness |
| **Fast** | Gives feedback in seconds, not minutes |
| **Clear diagnosis** | When it fails, you know exactly what broke |
| **Cheap to write** | Effort proportional to code complexity |

**Output:** List of test cases to write, organized by layer (unit/integration/E2E)

---

### Phase 3: BUILD

*Twig by twig, the dam takes shape. Each piece has purpose...*

Write tests following **Arrange-Act-Assert:**

```typescript
it('should reject invalid email during registration', async () => {
    // Arrange: Set up the scenario
    const invalidEmail = 'not-an-email';

    // Act: Do the thing (ONE line)
    const result = await registerUser({ email: invalidEmail, password: 'valid123' });

    // Assert: Check the outcome
    expect(result.success).toBe(false);
    expect(result.error).toContain('email');
});
```

The **Act** section should be one line. If it's not, the test is probably doing too much.

**Test User Behavior, Not Implementation:**

```typescript
// Bad: Testing implementation
it('should set isLoading state to true', async () => {
    const { component } = render(LoginForm);
    await fireEvent.click(getByRole('button'));
    expect(component.isLoading).toBe(true);  // Testing internal state!
});

// Good: Testing user experience
it('should show loading indicator while logging in', async () => {
    render(LoginForm);
    await fireEvent.click(getByRole('button', { name: /sign in/i }));
    expect(getByRole('progressbar')).toBeInTheDocument();
});
```

**Use Accessible Queries** (how users find elements):

```typescript
// Priority order (best to worst):
getByRole('button', { name: /submit/i })  // How screen readers see it
getByLabelText('Email')                    // Form fields
getByText('Welcome back')                  // Visible text
getByTestId('login-form')                  // Last resort
```

**Test Names That Explain:**

**Good names:**
- `should reject registration with invalid email`
- `should show error message when API fails`
- `should preserve draft when navigating away`

**Bad names:**
- `test email validation` (what about it?)
- `handleSubmit works` (what does "works" mean?)
- `test case 1` (no)

**Test One Thing:**

Each test should have **one reason to fail**. If a test fails, you should immediately know what broke.

```typescript
// Bad: Testing multiple things
it('should handle registration', async () => {
    // Tests validation, API call, redirect, AND email sending
});

// Good: Focused tests
it('should reject invalid email format', ...);
it('should call API with valid data', ...);
it('should redirect after successful registration', ...);
it('should send welcome email after registration', ...);
```

**Integration Test Pattern** (where most tests should live):

```typescript
// Multiple units working together
it('should complete checkout flow', async () => {
    // Arrange
    const cart = await createCart({ items: [item1, item2] });
    
    // Act
    const order = await checkout(cart.id, paymentMethod);
    
    // Assert
    expect(order.status).toBe('confirmed');
    expect(order.total).toBe(cart.total);
    expect(await getInventory(item1.id)).toBe(item1.stock - 1);
});
```

**Output:** Working tests that follow AAA pattern and test behavior, not implementation

---

### Phase 4: REINFORCE

*The beaver packs mud between twigs, hardening the structure...*

Strengthen tests with:

**Minimal Mocking:**

```typescript
// Over-mocked: False confidence
vi.mock('./api');
vi.mock('./validation');
vi.mock('./utils');
// You're testing... nothing real

// Better: Mock at boundaries only
vi.mock('./external-api');  // Mock the network, not your code
// Let validation, utils, etc. run for real
```

**Rule of thumb:** If you're mocking something you wrote, reconsider.

**Bug → Test Pipeline:**

Every production bug should become a test:

1. **Bug reported** — User can't check out with certain items
2. **Reproduce locally** — Find the exact conditions
3. **Write failing test** — Captures the bug's conditions
4. **Fix the bug** — Test now passes
5. **Test prevents regression** — Bug can never return

This is one of the highest-value testing practices. It turns pain into protection.

**Test Location:**

Keep tests close to code:

```
src/
└── lib/
    └── features/
        └── auth/
            ├── login.ts
            ├── login.test.ts      ← Right next to the code
            └── register.ts
```

**Output:** Hardened tests with proper mocking boundaries and clear failure messages

---

### Phase 5: FORTIFY

*The dam holds. Water flows as intended. The beaver rests...*

**Final checks:**

```bash
# Run tests
npx vitest run

# Check coverage (signal, not goal)
npx vitest run --coverage

# Run with other quality checks
npm run lint && npm run typecheck && npx vitest run
```

**Self-Review Checklist:**

Before considering tests "done":

- [ ] Tests describe user behavior, not implementation
- [ ] Each test has one clear reason to fail
- [ ] Tests use accessible queries (getByRole, getByLabelText)
- [ ] Mocks are limited to external boundaries
- [ ] Test names explain what breaks when they fail
- [ ] No snapshot tests for volatile content
- [ ] Bug fixes include regression tests
- [ ] Tests run fast (seconds, not minutes)

**When Tests Break:**

Tests that break are telling you something. Listen.

**Good Breaks (Expected):**
- **Feature changed** — Test caught that behavior shifted. Update the test.
- **Bug fixed** — Old test was wrong. Fix it.
- **Requirement changed** — Test reflects old requirement. Update it.

**Bad Breaks (Symptoms of Poor Tests):**
- **Refactored internal code** — Test was coupled to implementation. Rewrite it.
- **Changed CSS class** — Test was querying implementation details. Use accessible queries.
- **Reordered code** — Test depended on execution order. Make it order-independent.

**If refactoring frequently breaks tests, your tests are testing the wrong things.**

**Output:** Clean test suite ready for CI

---

## Beaver Rules

### Energy
Build with purpose. The beaver doesn't add twigs just to add them. Each test must earn its place by providing confidence.

### Precision
Test behavior, not structure. If refactoring breaks your tests, they were testing the wrong things.

### Wisdom
Remember the trophy: Mostly integration, some unit, few E2E. Static analysis is your first line of defense.

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

**The Ice Cream Cone (AVOID):**

```
        ╭───────────────────────────╮
        │      Many E2E tests       │  ← Slow, brittle, expensive
        ╰───────────┬───────────────╯
              ╭─────┴─────╮
              │ Few int.  │
              ╰─────┬─────╯
                ╭───┴───╮
                │ Few   │
                │ unit  │
                ╰───────╯
```

This is backwards. E2E tests are expensive. Integration tests give the best ROI.

---

## Example Build

**User:** "Add tests for the login form"

**Beaver flow:**

1. 🦫 **SURVEY** — "Login form handles user authentication. Critical path: registration → dashboard flow. Integration tests where confidence lives."

2. 🦫 **GATHER** — "Test: invalid email rejection, API error handling, successful redirect, loading states. Skip: internal state changes."

3. 🦫 **BUILD** — Write integration tests using AAA pattern:
   - `should reject registration with invalid email`
   - `should show loading indicator while logging in`
   - `should redirect to dashboard after successful login`

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

*Good tests let you ship with confidence. That's the whole point.* 🦫
