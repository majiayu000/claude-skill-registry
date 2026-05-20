---
name: grove-testing
description: Write effective, maintainable tests that catch real bugs and enable confident refactoring. Use when deciding what to test, reviewing test quality, or writing tests for Grove features. Focuses on philosophy and strategy—pair with javascript-testing for implementation details.
---

# Grove Testing Skill

## When to Activate

Activate this skill when:
- Deciding **what** to test (not just how)
- Writing tests for new Grove features
- Reviewing existing tests for effectiveness
- Asked to "add tests" without specific guidance
- Evaluating whether tests are providing real value
- Refactoring causes many tests to break (symptom of bad tests)

**For technical implementation** (Vitest syntax, mocking patterns, assertions), use the `javascript-testing` skill alongside this one.

---

## The Testing Philosophy

> *"Write tests. Not too many. Mostly integration."*
> — Guillermo Rauch

This captures everything Grove believes about testing:

**Write tests** — Automated tests are worthwhile. They enable confident refactoring, serve as documentation, and catch regressions before users do.

**Not too many** — Tests have diminishing returns. The goal isn't coverage numbers. It's confidence. When you feel confident shipping, you have enough tests.

**Mostly integration** — Integration tests catch real problems without being brittle. They test behavior users actually experience, not internal implementation.

### The Guiding Principle

> *"The more your tests resemble the way your software is used, the more confidence they can give you."*
> — Kent C. Dodds (Testing Library)

Ask yourself: **Does this test fail when the feature breaks?** If yes, it's valuable. If it only fails during refactors, it's testing implementation details.

---

## What Makes a Test Valuable

A good test has these properties (Kent Beck's Test Desiderata):

| Property | What It Means |
|----------|---------------|
| **Behavior-sensitive** | Fails when actual functionality breaks |
| **Structure-immune** | Doesn't break when you refactor safely |
| **Deterministic** | Same result every time, no flakiness |
| **Fast** | Gives feedback in seconds, not minutes |
| **Clear diagnosis** | When it fails, you know exactly what broke |
| **Cheap to write** | Effort proportional to code complexity |

### The Confidence Test

Before writing a test, ask:

1. **Would I notice if this broke in production?** If yes, test it.
2. **Would this test fail if the feature broke?** If no, don't write it.
3. **Does this test resemble how users interact with the feature?** If no, reconsider.

---

## What NOT to Test

Not everything needs tests. Some things actively harm your codebase when tested.

### Skip Testing

| What | Why |
|------|-----|
| **Trivial code** | Getters, setters, data models with no logic |
| **Framework behavior** | Trust that SvelteKit routing works |
| **Implementation details** | Internal state, private methods, CSS classes |
| **One-off scripts** | Maintenance cost exceeds value |
| **Volatile prototypes** | Requirements unclear, code will change |

### Test Lightly

| What | Approach |
|------|----------|
| **Configuration** | Smoke test that it loads, not every option |
| **Third-party integrations** | Mock at boundaries, test your code's response |
| **Visual design** | Snapshot tests or visual regression, not unit tests |

### Test Thoroughly

| What | Why |
|------|-----|
| **Business logic** | Core value of the application |
| **User-facing flows** | What users actually experience |
| **Edge cases** | Error states, empty states, boundaries |
| **Bug fixes** | Every bug becomes a test to prevent regression |

---

## The Testing Trophy

Modern JavaScript testing follows the Testing Trophy, not the old Testing Pyramid:

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

### What Each Layer Does

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

---

## Writing Effective Tests

### Structure: Arrange-Act-Assert

Every test should follow this pattern:

```typescript
it('should reject invalid email during registration', async () => {
    // Arrange: Set up the scenario
    const invalidEmail = 'not-an-email';

    // Act: Do the thing
    const result = await registerUser({ email: invalidEmail, password: 'valid123' });

    // Assert: Check the outcome
    expect(result.success).toBe(false);
    expect(result.error).toContain('email');
});
```

The **Act** section should be one line. If it's not, the test is probably doing too much.

### Naming: Say What Breaks

Test names should describe the behavior, not the implementation:

**Good names:**
- `should reject registration with invalid email`
- `should show error message when API fails`
- `should preserve draft when navigating away`

**Bad names:**
- `test email validation` (what about it?)
- `handleSubmit works` (what does "works" mean?)
- `test case 1` (no)

### Test One Thing

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

---

## Integration Tests in Practice

Integration tests are the heart of Grove's testing strategy. Here's how to write them well.

### Test User Behavior, Not Implementation

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

### Use Accessible Queries

Query elements the way users find them:

```typescript
// Priority order (best to worst):
getByRole('button', { name: /submit/i })  // How screen readers see it
getByLabelText('Email')                    // Form fields
getByText('Welcome back')                  // Visible text
getByTestId('login-form')                  // Last resort
```

### Don't Over-Mock

Mocks remove confidence in the integration. Use them sparingly:

```typescript
// Over-mocked: False confidence
vi.mock('./api');
vi.mock('./validation');
vi.mock('./utils');
// You're testing... nothing real

// Better: Mock at boundaries
vi.mock('./external-api');  // Mock the network, not your code
// Let validation, utils, etc. run for real
```

**Rule of thumb:** If you're mocking something you wrote, reconsider.

---

## When Tests Break

Tests that break are telling you something. Listen.

### Good Breaks (Expected)

- **Feature changed** — Test caught that behavior shifted. Update the test.
- **Bug fixed** — Old test was wrong. Fix it.
- **Requirement changed** — Test reflects old requirement. Update it.

### Bad Breaks (Symptoms of Poor Tests)

- **Refactored internal code** — Test was coupled to implementation. Rewrite it.
- **Changed CSS class** — Test was querying implementation details. Use accessible queries.
- **Reordered code** — Test depended on execution order. Make it order-independent.

**If refactoring frequently breaks tests, your tests are testing the wrong things.**

---

## The Bug → Test Pipeline

Every production bug should become a test:

1. **Bug reported** — User can't check out with certain items
2. **Reproduce locally** — Find the exact conditions
3. **Write failing test** — Captures the bug's conditions
4. **Fix the bug** — Test now passes
5. **Test prevents regression** — Bug can never return

This is one of the highest-value testing practices. It turns pain into protection.

---

## Anti-Patterns to Avoid

### The Ice Cream Cone

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

### Testing Implementation Details

```typescript
// Testing implementation (bad)
expect(component.state.items).toHaveLength(3);
expect(handleClick).toHaveBeenCalledWith({ id: 1 });

// Testing behavior (good)
expect(getByRole('list').children).toHaveLength(3);
expect(getByText('Item added!')).toBeInTheDocument();
```

### Coverage Theater

Chasing 100% coverage leads to bad tests:

```typescript
// Written only to hit coverage, provides zero value
it('should have properties', () => {
    const user = new User();
    expect(user.email).toBeDefined();
    expect(user.name).toBeDefined();
});
```

Coverage is a **signal**, not a **goal**. High coverage with bad tests is worse than moderate coverage with good tests.

### Snapshot Abuse

Snapshots are useful for:
- Complex serialized output
- Error message formatting
- API response shapes

Snapshots are harmful for:
- UI components (break on every style change)
- Anything with timestamps or random IDs
- Large objects (nobody reviews 500-line snapshot diffs)

---

## The Grove Testing Workflow

When asked to add tests, follow this workflow:

### 1. Understand the Feature

What does this feature **do** for users? Not how it's implemented—what value does it provide?

### 2. Identify Critical Paths

What would break if this feature failed? Those are your test cases.

### 3. Write Integration Tests First

Start with tests that exercise real user behavior. Add unit tests only for complex logic.

### 4. Keep Tests Close to Code

```
src/
└── lib/
    └── features/
        └── auth/
            ├── login.ts
            ├── login.test.ts      ← Right next to the code
            └── register.ts
```

### 5. Run Tests Continuously

```bash
npx vitest              # Watch mode during development
npx vitest run          # CI verification
```

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

## Integration with Other Skills

### javascript-testing

Use `javascript-testing` for:
- Vitest configuration syntax
- Mocking patterns and APIs
- Assertion reference
- SvelteKit-specific test patterns

### grove-documentation

When writing test descriptions, follow Grove voice:
- Clear, direct names
- No jargon
- Say what the user experiences

### code-quality

Run linting and type checking before/after writing tests. Static analysis catches different bugs than tests do.

---

## Self-Review Checklist

Before considering tests "done":

- [ ] Tests describe user behavior, not implementation
- [ ] Each test has one clear reason to fail
- [ ] Tests use accessible queries (getByRole, getByLabelText)
- [ ] Mocks are limited to external boundaries
- [ ] Test names explain what breaks when they fail
- [ ] No snapshot tests for volatile content
- [ ] Bug fixes include regression tests
- [ ] Tests run fast (seconds, not minutes)

---

*Good tests let you ship with confidence. That's the whole point.*
