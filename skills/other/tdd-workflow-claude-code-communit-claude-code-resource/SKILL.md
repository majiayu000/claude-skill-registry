---
name: tdd-workflow
description: Test-driven development methodology — red-green-refactor cycle, writing failing tests first, minimal implementation, and iterative refinement. Use when implementing features test-first, when the user asks for TDD, or when writing tests before code.
---

# Test-Driven Development Workflow

## Core Philosophy

TDD is a design discipline, not just a testing technique. Writing tests first forces you to think about the interface before the implementation, producing code that is inherently testable, loosely coupled, and driven by actual requirements.

## The Red-Green-Refactor Loop

### Step 1: RED — Write a Failing Test

1. Identify the smallest piece of behavior to implement next.
2. Write a test that describes that behavior from the caller's perspective.
3. Run the test suite. The new test MUST fail.
4. If the test passes without writing new code, either the behavior already exists or the test is wrong.

**Checklist before moving to GREEN:**
- [ ] The test describes WHAT, not HOW.
- [ ] The test name reads like a specification (e.g., `it should return 404 when resource not found`).
- [ ] The test fails for the right reason (expected assertion failure, not a syntax error or import error).
- [ ] The test is isolated — it does not depend on other tests or external state.

### Step 2: GREEN — Write the Minimal Implementation

1. Write the simplest code that makes the failing test pass.
2. It is acceptable — even encouraged — to hardcode values, use naive algorithms, or write "ugly" code at this stage.
3. Do NOT add logic that is not required by a failing test.
4. Run the full test suite. ALL tests must pass.

**The "simplest thing that could work" principle:**
- If one test expects `return 42`, write `return 42`. Do not write a general formula yet.
- If two tests expect different outputs, write an `if` statement. Do not write a loop yet.
- If three tests show a pattern, NOW consider a general algorithm.

**Checklist before moving to REFACTOR:**
- [ ] The new test passes.
- [ ] All previously passing tests still pass.
- [ ] No code was added beyond what the tests demand.

### Step 3: REFACTOR — Improve the Design

1. Look for duplication in both production code and test code.
2. Extract methods, rename variables, simplify conditionals.
3. Apply design patterns only when the code asks for them (three or more instances).
4. Run the full test suite after every change. All tests must stay green.

**Refactoring targets:**
- [ ] Duplicate code extracted into shared functions.
- [ ] Variable and method names clearly express intent.
- [ ] No method exceeds 10-15 lines.
- [ ] No function has more than 3 parameters.
- [ ] Test code is also clean and readable.

### Step 4: REPEAT

Return to Step 1 with the next smallest behavior.

---

## Test Naming Conventions

Use descriptive names that serve as documentation:

```
// Pattern: [unit]_[scenario]_[expected result]
test_calculateTotal_withEmptyCart_returnsZero
test_calculateTotal_withSingleItem_returnsItemPrice
test_calculateTotal_withDiscount_appliesDiscountToSubtotal

// BDD-style
describe("calculateTotal") {
  it("should return zero for an empty cart")
  it("should return the item price for a single item")
  it("should apply discount to subtotal")
}

// Given-When-Then
given_emptyCart_when_calculateTotal_then_returnsZero
```

**Rules:**
- Never use "test1", "test2", or other meaningless names.
- The test name should tell you what broke without reading the test body.
- Group related tests under a `describe` or test class.

---

## Choosing What to Test Next

### Start with the degenerate cases:
1. Null / empty / zero inputs.
2. Single element / simplest valid input.
3. Typical valid inputs.
4. Boundary values and edge cases.
5. Error conditions and invalid inputs.

### Prioritization:
- Begin with the behavior that drives the most architectural decisions.
- Defer I/O, persistence, and external service tests until core logic is solid.
- Test the happy path first, then edge cases, then error paths.

---

## TDD for Different Test Types

### Unit Tests (most common in TDD)
```
RED:   Write a test for a single function or method.
GREEN: Implement just that function.
REFACTOR: Clean up the function and its test.
Cycle time: 1-5 minutes.
```

### Integration Tests
```
RED:   Write a test that exercises two or more components together.
GREEN: Wire the components and implement any missing glue code.
REFACTOR: Extract shared setup, clean interfaces between components.
Cycle time: 5-15 minutes.
```

### API / HTTP Tests
```
RED:   Write a test that sends an HTTP request and asserts on status + body.
GREEN: Implement the route handler with minimal logic.
REFACTOR: Extract validation, business logic, and serialization into separate layers.
Cycle time: 5-20 minutes.
```

### Example: Building a URL Shortener (Unit Level)

```python
# RED: First test — empty slug
def test_shorten_rejects_empty_url():
    with pytest.raises(ValueError):
        shorten("")

# GREEN: Minimal implementation
def shorten(url):
    if not url:
        raise ValueError("URL cannot be empty")
    pass  # nothing else needed yet

# RED: Second test — returns a short code
def test_shorten_returns_six_char_code():
    result = shorten("https://example.com")
    assert len(result) == 6

# GREEN: Hardcode, then generalize
def shorten(url):
    if not url:
        raise ValueError("URL cannot be empty")
    return url[:6]  # naive but passing

# RED: Third test — codes are unique
def test_shorten_returns_unique_codes():
    a = shorten("https://example.com/a")
    b = shorten("https://example.com/b")
    assert a != b

# GREEN: Now we need real logic
import hashlib
def shorten(url):
    if not url:
        raise ValueError("URL cannot be empty")
    return hashlib.md5(url.encode()).hexdigest()[:6]

# REFACTOR: Extract hashing, add type hints, rename for clarity
```

---

## Handling Untested Legacy Code

When adding features to code without tests:

1. **Characterization tests first.** Write tests that document what the code currently does, not what it should do. Lock down existing behavior.
2. **Find the seam.** Identify a point where you can intercept behavior (dependency injection, method override, function parameter).
3. **Apply TDD to the new feature.** Write failing tests for the new behavior, implement it, then refactor.
4. **Expand the safety net.** Gradually add tests around the touched code.

**The Mikado Method for legacy TDD:**
1. Try a naive change.
2. If tests break, note what broke and revert.
3. Fix the prerequisites first (add missing tests, extract dependencies).
4. Retry the original change.

---

## Common TDD Pitfalls

### Writing too large a test
- **Symptom:** The GREEN step takes more than 15 minutes.
- **Fix:** Break the test into smaller behavioral increments.

### Testing implementation details
- **Symptom:** Tests break when you refactor, even though behavior is unchanged.
- **Fix:** Test inputs and outputs, not internal method calls or data structures.

### Skipping the RED step
- **Symptom:** You write code and tests at the same time.
- **Fix:** Discipline. Always see the test fail first. A test you have never seen fail is a test you cannot trust.

### Skipping the REFACTOR step
- **Symptom:** Code works but is messy, duplicated, or hard to read.
- **Fix:** Set a timer. After every GREEN, spend at least 2 minutes looking for cleanup opportunities.

### Gold-plating during GREEN
- **Symptom:** You add error handling, logging, or optimizations not required by any test.
- **Fix:** If no test demands it, delete it. You can add it later when a test asks for it.

### Fragile test fixtures
- **Symptom:** Many tests break when a shared fixture changes.
- **Fix:** Use factory functions or builders. Each test should set up only what it needs.

### Test interdependence
- **Symptom:** Tests pass in one order but fail in another.
- **Fix:** Each test must set up and tear down its own state. Run tests in random order to detect this.

---

## TDD Decision Framework

```
Is the behavior well-understood?
  YES -> Classic TDD (test-first)
  NO  -> Spike first (throwaway prototype), then TDD the real implementation

Is the code interacting with external systems?
  YES -> Write a contract/interface test, then use a fake/stub for unit TDD
  NO  -> Pure function TDD (easiest case)

Is the code algorithmically complex?
  YES -> Start with simple examples, build up with property-based tests
  NO  -> Standard example-based TDD

Are you fixing a bug?
  YES -> Write a test that reproduces the bug FIRST, then fix it
  NO  -> Normal TDD cycle
```

---

## Key Metrics

- **Cycle time:** Each red-green-refactor should take 1-15 minutes. Longer cycles mean the step is too big.
- **Test count growth:** Roughly 1 test per 5-15 lines of production code.
- **Refactor frequency:** You should refactor at least every 3 cycles.
- **All tests passing:** At the end of every GREEN and REFACTOR step. Never commit with failing tests.

---

## Summary: The Three Laws of TDD (Robert C. Martin)

1. You may not write production code until you have written a failing test.
2. You may not write more of a test than is sufficient to fail (and not compiling counts as failing).
3. You may not write more production code than is sufficient to pass the currently failing test.
