# BDD Red-Green-Refactor Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-25

Execute the TDD inner loop with tight red-green-refactor cycles.

## When to Activate

Use this skill when:
- During implementation
- Red green refactor
- TDD cycle
- Implement behavior
- Make tests pass

## Core Principles

### 1. Red Before Green

Verify tests fail before writing implementation.

*Confirms tests actually test something; passing tests without red phase may be meaningless.*

### 2. Minimal Implementation

Write just enough code to make the current test pass.

*YAGNI - don't implement what's not tested. More code = more bugs.*

### 3. One Test at a Time

Focus on making one failing test pass, then move to the next.

*Smaller scope reduces complexity and makes debugging easier.*

### 4. Refactor Only When Green

Clean up code only after all targeted tests pass.

*Green tests are a safety net for refactoring; refactoring during red is risky.*

### 5. Minute-Scale Cycles

Each red-green-refactor cycle should take minutes, not hours.

*Tight feedback loops catch problems early; large batches hide issues.*

---

## The Cycle

```
    ┌─────────────────────────────────────────┐
    │                                         │
    ▼                                         │
┌───────┐    implement    ┌───────┐   clean   │
│  RED  │ ───────────────►│ GREEN │───────────┤
│       │  (minimal)      │       │  up code  │
└───────┘                 └───────┘           │
    ▲                         │               │
    │         tests pass?     │               │
    │            no           │      yes      │
    └─────────────────────────┘               │
                                              │
    ◄─────────────────────────────────────────┘
           more failing tests? loop back
```

---

## Workflow

### Phase 1: RED - Confirm Failure

Verify tests fail for the expected reason.

1. Run the test suite (`cargo test` for specific test)
2. Confirm at least one test fails
3. Verify the failure is the EXPECTED failure (not compile error)
4. If no failures, step definitions may be incomplete

**Outputs:** Confirmation of RED state, Failure message understood

### Phase 2: GREEN - Minimal Implementation

Write just enough code to make tests pass.

1. Focus on ONE failing test
2. Write the simplest implementation that passes
3. Avoid premature optimization or generalization
4. Run tests to confirm GREEN
5. If still RED, debug the specific failure

**Outputs:** Passing test(s), Minimal implementation code

### Phase 3: REFACTOR - Clean Up

Improve code while keeping tests green.

1. Look for code smells (duplication, poor naming, long functions)
2. Apply one small refactoring at a time
3. Run tests after each refactoring
4. If tests go RED, undo and try smaller refactoring
5. Stop when code is clean enough

**Outputs:** Clean implementation, Tests still passing

### Phase 4: REPEAT

Continue with next failing test.

1. Check if more tests are failing
2. If yes, return to RED phase
3. If all tests pass, implementation is complete
4. Run full test suite as final verification

**Outputs:** All tests passing OR next RED cycle

---

## Step Size Guide

### Too Small (tedious)

```rust
// Don't do single-character iterations
fn add(a: i32, b: i32) -> i32 { a }  // Step 1
fn add(a: i32, b: i32) -> i32 { a + }  // Step 2 (won't compile)
```

### Just Right (productive)

```rust
// One logical unit at a time
fn add(a: i32, b: i32) -> i32 { a + b }  // Complete implementation
```

### Too Large (risky)

```rust
// Don't implement everything at once
fn create_user(data: UserData) -> Result<User> {
    validate_email(&data.email)?;
    validate_password(&data.password)?;
    check_duplicates(&data.email)?;
    let user = User::new(data)?;
    db.insert(&user)?;
    send_welcome_email(&user)?;
    Ok(user)
}
```

**Rule of Thumb:** 3-10 lines per GREEN step. If more, break it down.

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Obvious Implementation** | Trivially clear | Just write it | Don't be dogmatic for simple code |
| **Fake It Till You Make It** | Unsure of generalization | Hardcode first, generalize later | Verify test before implementing |
| **Triangulation** | Hardcoded passes | Add test with different values | Forces real implementation |
| **Backout** | Refactoring breaks tests | Undo immediately (git checkout) | Don't debug refactoring failures |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| **Big Bang Implementation** | Write all code then run tests | Implement one test at a time |
| **Refactoring During Red** | No safety net | Get to green first |
| **Skipping Red Verification** | May have false-passing tests | Always observe RED |
| **Over-Engineering** | Untested code | Only implement what tests demand |
| **Long Cycle Times** | Large batches, hard debugging | Run tests every few minutes |

---

## Command Reference

### Running Specific Tests

```bash
# Run all tests in a module
cargo test steps::user_creation

# Run a single test
cargo test steps::user_creation::create_user_scenario

# Run with output visible
cargo test -- --nocapture

# Run and stop on first failure
cargo test -- --fail-fast
```

### Quick Undo

```bash
# Undo all uncommitted changes
git checkout -- .

# Undo changes to specific file
git checkout -- src/lib.rs

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

## State Indicators

### RED Indicators

- Test output shows failures
- `FAILED` in test summary
- Non-zero exit code
- Expected failure message matches intention

### GREEN Indicators

- All tests pass
- `ok` for all tests
- Zero exit code
- No unexpected warnings

### Ready to REFACTOR Indicators

- All targeted tests pass
- Code has obvious smells
- Duplication exists
- Names could be clearer
- Functions are too long

---

## Quality Checklist

Before moving to next cycle:

- [ ] Test run confirms RED state before implementing
- [ ] Failure message understood (not just "something failed")
- [ ] Implementation is minimal (no extra features)
- [ ] Tests pass after implementation (GREEN)
- [ ] Code reviewed for smells before moving on
- [ ] Refactorings are small and tested individually
- [ ] Full test suite passes at completion

---

## Example: Complete Cycle

### Scenario: Creating User with Duplicate Email Should Fail

**RED Phase:**
```bash
$ cargo test duplicate_email
running 1 test
test steps::user_creation::duplicate_email ... FAILED

failures:
    steps::user_creation::duplicate_email
    assertion failed: expected Err, got Ok(User { ... })
```

Confirmed: Test fails because duplicate check isn't implemented.

**GREEN Phase:**
```rust
// Add minimal check
fn create_user(email: &str, password: &str) -> Result<User> {
    if db.user_exists_by_email(email)? {
        return Err(Error::DuplicateEmail);
    }
    // ... rest of implementation
}
```

```bash
$ cargo test duplicate_email
running 1 test
test steps::user_creation::duplicate_email ... ok
```

**REFACTOR Phase:**
```rust
// Extract validation function
fn validate_unique_email(email: &str) -> Result<()> {
    if db.user_exists_by_email(email)? {
        return Err(Error::DuplicateEmail);
    }
    Ok(())
}

fn create_user(email: &str, password: &str) -> Result<User> {
    validate_unique_email(email)?;
    // ...
}
```

```bash
$ cargo test duplicate_email
running 1 test
test steps::user_creation::duplicate_email ... ok
```

**REPEAT:** Check for next failing test or run full suite.

---

## Timing Guide

| Activity | Target Time |
|----------|-------------|
| RED verification | 30 seconds |
| GREEN implementation | 2-5 minutes |
| REFACTOR step | 1-3 minutes |
| Full cycle | 5-10 minutes |

If a cycle takes longer than 15 minutes, the step is too large.

---

## References

- "Test Driven Development by Example" - Kent Beck
- [skills/bdd-step-implementation](../skills/bdd-step-implementation/) - Input step definitions
- [skills/bdd-scenario-evolution](../skills/bdd-scenario-evolution/) - Adapting scenarios
