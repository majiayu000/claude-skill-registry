---
name: testing
description: Generate, execute, and analyze tests for codebases, covering unit, integration, and end-to-end testing with coverage reporting. Use when the user requests testing or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills contributors
  version: 1.0.0
---

# Testing

This skill enables an AI agent to systematically generate, run, and evaluate tests for a given codebase. It covers the full testing lifecycle — from analyzing source code and identifying meaningful test cases, through writing and executing tests, to measuring coverage and recommending improvements. The agent supports unit tests, integration tests, and end-to-end tests across multiple languages and frameworks.

## Workflow

1. **Analyze the source code.** Read the target file or module and build a dependency graph of its functions, classes, and external interactions. Identify public interfaces, internal helpers, input parameters, return types, and side effects. This step determines what is testable and what kinds of tests are appropriate.

2. **Identify test cases.** For each function or method, enumerate the scenarios that need coverage: happy-path inputs, boundary values, invalid or null inputs, exception paths, and state transitions. For integration points, identify the collaborators that need to be mocked or stubbed versus tested live. Prioritize cases by risk — complex branching logic and public API surfaces come first.

3. **Write the tests.** Generate well-structured test code using the project's existing test framework (e.g., pytest, Jest, JUnit). Each test should have a descriptive name that states the scenario and expected outcome. Use the Arrange-Act-Assert pattern: set up preconditions, invoke the code under test, and assert the expected result. Add parameterized tests where a single logical case applies to multiple input sets.

4. **Run the tests.** Execute the test suite using the appropriate runner command. Capture the full output including pass/fail status, assertion messages, and timing information. If any tests fail, parse the failure output to determine whether the failure indicates a bug in the source code or an error in the test itself.

5. **Analyze coverage.** Run the test suite with coverage instrumentation enabled (e.g., `pytest --cov`, `jest --coverage`). Parse the coverage report to identify uncovered lines, branches, and functions. Flag any critical code paths — error handlers, security checks, data validation — that lack coverage.

6. **Suggest improvements.** Based on coverage gaps and code complexity, recommend additional test cases. Suggest refactoring opportunities that would make the code more testable, such as extracting pure functions or introducing dependency injection. Provide a summary report with coverage percentages and a prioritized list of next actions.

## Supported Languages

| Language   | Framework       | Runner Command                  |
|------------|-----------------|---------------------------------|
| Python     | pytest          | `pytest --cov=src -v`           |
| JavaScript | Jest            | `npx jest --coverage --verbose` |
| TypeScript | Jest / Vitest   | `npx vitest run --coverage`     |
| Java       | JUnit 5         | `mvn test`                      |
| Go         | testing (stdlib) | `go test -cover ./...`         |
| Rust       | cargo test      | `cargo test`                    |

## Usage

Provide one or more of the following inputs:

- **Source file or directory** to generate tests for (e.g., `src/utils/parser.py`).
- **Existing test file** if you want the agent to extend or improve current tests.
- **Test framework preference** if the project does not already have one configured.
- **Coverage threshold** if you want the agent to target a specific percentage (e.g., 90%).

## Examples

### Example 1 — Python with pytest

Given this source file `src/cart.py`:

```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name: str, price: float, quantity: int = 1):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        self.items.append({"name": name, "price": price, "quantity": quantity})

    def total(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self.items)

    def remove_item(self, name: str):
        self.items = [item for item in self.items if item["name"] != name]
```

The agent generates `tests/test_cart.py`:

```python
import pytest
from src.cart import ShoppingCart

@pytest.fixture
def cart():
    return ShoppingCart()

def test_add_item_and_total(cart):
    cart.add_item("Widget", 9.99, 2)
    assert cart.total() == pytest.approx(19.98)

def test_empty_cart_total_is_zero(cart):
    assert cart.total() == 0.0

def test_add_item_negative_price_raises(cart):
    with pytest.raises(ValueError, match="Price cannot be negative"):
        cart.add_item("Bad", -1.0)

def test_add_item_zero_quantity_raises(cart):
    with pytest.raises(ValueError, match="Quantity must be at least 1"):
        cart.add_item("Bad", 5.0, 0)

def test_remove_item(cart):
    cart.add_item("A", 1.0)
    cart.add_item("B", 2.0)
    cart.remove_item("A")
    assert cart.total() == 2.0

def test_remove_nonexistent_item_does_nothing(cart):
    cart.add_item("A", 1.0)
    cart.remove_item("Z")
    assert cart.total() == 1.0
```

Run: `pytest tests/test_cart.py --cov=src -v`

### Example 2 — JavaScript with Jest

Given this source file `src/validator.js`:

```javascript
function isValidEmail(email) {
  if (typeof email !== "string") return false;
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function isStrongPassword(password) {
  if (typeof password !== "string") return false;
  return (
    password.length >= 8 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /[0-9]/.test(password)
  );
}

module.exports = { isValidEmail, isStrongPassword };
```

The agent generates `src/__tests__/validator.test.js`:

```javascript
const { isValidEmail, isStrongPassword } = require("../validator");

describe("isValidEmail", () => {
  test.each([
    ["user@example.com", true],
    ["name+tag@sub.domain.org", true],
    ["missing-at-sign.com", false],
    ["@no-local.com", false],
    ["spaces in@email.com", false],
    ["", false],
  ])("isValidEmail(%s) => %s", (input, expected) => {
    expect(isValidEmail(input)).toBe(expected);
  });

  test("returns false for non-string input", () => {
    expect(isValidEmail(null)).toBe(false);
    expect(isValidEmail(42)).toBe(false);
  });
});

describe("isStrongPassword", () => {
  test("accepts a strong password", () => {
    expect(isStrongPassword("Str0ngPwd")).toBe(true);
  });

  test("rejects short password", () => {
    expect(isStrongPassword("Ab1")).toBe(false);
  });

  test("rejects password without uppercase", () => {
    expect(isStrongPassword("alllower1")).toBe(false);
  });

  test("rejects non-string input", () => {
    expect(isStrongPassword(undefined)).toBe(false);
  });
});
```

Run: `npx jest --coverage --verbose`

## Best Practices

- **Name tests after the scenario, not the implementation.** Use names like `test_empty_cart_total_is_zero` rather than `test_total_method`. This makes failures self-documenting.
- **Keep tests independent.** Each test should set up its own state via fixtures or setup methods. Never rely on test execution order.
- **Prefer parameterized tests for input variations.** When the same logic applies to many inputs, use `@pytest.mark.parametrize` or `test.each` instead of duplicating test bodies.
- **Mock external dependencies, not internal logic.** Stub network calls, databases, and file I/O. Avoid mocking the code under test itself — that defeats the purpose.
- **Target meaningful coverage, not 100%.** Aim for thorough branch coverage of critical paths. Trivial getters and framework-generated code rarely need dedicated tests.
- **Run tests in CI on every commit.** Integrate the test command into the project's CI pipeline so regressions are caught immediately.

## Edge Cases

- **Dynamically generated code:** If the codebase uses metaprogramming, decorators, or code generation, the agent may not detect all callable paths. Provide hints about generated interfaces.
- **Global state and singletons:** Tests for code that mutates global state require careful teardown. The agent will flag these but may need guidance on acceptable reset strategies.
- **Async and concurrent code:** Testing async functions requires framework-specific patterns (`pytest-asyncio`, Jest's async handling). The agent will use the appropriate pattern but may ask for confirmation on timeout thresholds.
- **Environment-dependent tests:** Tests that depend on environment variables, file system layout, or network access should be clearly marked as integration tests and excluded from fast unit-test runs.
- **Flaky tests:** If test runs produce intermittent failures, the agent will flag non-deterministic patterns (e.g., reliance on wall-clock time, unordered collection comparisons) and suggest fixes.
