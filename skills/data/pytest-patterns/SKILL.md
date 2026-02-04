---
name: pytest-patterns
description: Advanced Python testing strategies with Pytest, covering fixtures, matrix testing with parametrization, and async test architecture. Triggers: pytest, fixtures, parametrize, pytest-asyncio, matrix-testing, yield-fixture.
---

# Pytest Advanced Patterns

## Overview
Pytest is a powerful testing framework that emphasizes modularity via fixtures and scalability via parametrization. It simplifies setup/teardown logic and enables complex test matrices with minimal code.

## When to Use
- **Resource Intensive Tests**: Using scoped fixtures for database or API connections to avoid redundant setup.
- **Input Combinations**: Using parametrization to test a single function against dozens of inputs.
- **Async Codebases**: Testing coroutines directly without manual event loop management.

## Decision Tree
1. Is the setup expensive (e.g., creating a DB)? 
   - YES: Use a fixture with `scope='session'` or `scope='module'`.
2. Do you need to cleanup after a test? 
   - YES: Use a `yield` fixture.
3. Do you have 3+ similar test cases for one function? 
   - YES: Use `@pytest.mark.parametrize`.

## Workflows

### 1. Defining a Scoped Setup/Teardown
1. Create a fixture using the `@pytest.fixture(scope="module")` decorator for expensive resources like database connections.
2. Use `yield` to provide the resource to tests.
3. Add cleanup code (e.g., closing the connection) after the `yield` statement.
4. Request the fixture by name in any test function within the module.

### 2. Matrix Testing with Stacked Parametrize
1. Apply `@pytest.mark.parametrize("user", ["admin", "guest"])` to a test.
2. Apply a second `@pytest.mark.parametrize("action", ["read", "write"])` to the same test.
3. Pytest will run the test 4 times, once for each combination (admin-read, admin-write, etc.).

### 3. Testing Async Code
1. Install `pytest-asyncio`.
2. Mark the test function with `@pytest.mark.asyncio`.
3. Define the test as an `async def`.
4. Use `await` for the code under test and assertions.

## Non-Obvious Insights
- **Fixture Caching**: Fixtures are executed once per requested scope and the return value is cached for all tests in that scope.
- **Reverse Teardown**: Teardown logic in `yield` fixtures is executed in the exact reverse order of the setup sequence.
- **Auto-Async Marking**: Modern `pytest-asyncio` can be configured to treat all `async def` tests as async without needing the explicit decorator on every function.

## Evidence
- "pytest won’t execute them again for that test... return values are cached." - [Pytest Docs](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- "Yield fixtures yield instead of return... Any teardown code for that fixture is placed after the yield." - [Pytest Docs](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- "provides support for coroutines as test functions. This allows users to await code inside their tests." - [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

## Scripts
- `scripts/pytest-patterns_tool.py`: Examples of fixtures, parametrization, and async tests.
- `scripts/pytest-patterns_tool.js`: (Comparison) Equivalent logic in Vitest/Jest.

## Dependencies
- `pytest`
- `pytest-asyncio`

## References
- [references/README.md](references/README.md)