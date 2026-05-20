---
name: python-testing-patterns
description: Guide pytest patterns and testing strategies when the user asks about Python testing, fixtures, mocking, or test organization
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep
argument-hint: "[test file, module to test, or testing concern]"
read-only: true
destructive: false
idempotent: true
open-world: false
user-invocable: true
tags: python, testing, patterns
---

# Python Testing Patterns

## Overview

Guide pytest-based testing for Python services. Covers fixture design, factory patterns, mocking strategies, async testing, and parametrize usage. Applies the testing pyramid: unit tests for services, integration tests for repos and DB, end-to-end tests for API endpoints. Stack-specific Tier 3 reference skill.

## Workflow

1. **Read project setup** — Check `.chalk/docs/engineering/` for architecture docs. Determine the testing stack: pytest version, async framework (asyncio, trio), HTTP client (httpx, requests, aiohttp), ORM (SQLAlchemy, Django ORM, Tortoise), and any existing test conventions. Read `conftest.py` files to understand current fixture organization.

2. **Identify the scope** — Parse `$ARGUMENTS` for the specific module, test file, or testing concern. Categories include: fixture design, factory patterns, mocking, async testing, parametrize, or test organization.

3. **Audit fixture design** — Check for:
   - Fixture scope: `function` (default, safest), `class`, `module`, `session` (fastest but risk shared state). Use the narrowest scope that avoids unacceptable slowness.
   - `conftest.py` organization: fixtures in the right `conftest.py` level (project root for shared, per-directory for scoped). Avoid importing fixtures across test directories.
   - Fixture dependencies: fixtures that depend on other fixtures should form a clean DAG, not a tangled web.
   - `yield` fixtures for setup/teardown: prefer over `addfinalizer` for readability.

4. **Audit factory patterns** — Check for:
   - Inline test data construction (repeated `User(name="test", email="test@test.com")` across tests). Recommend `factory_boy` or custom factory functions.
   - Factory classes that mirror models: `UserFactory`, `OrderFactory` with sensible defaults and traits for variations.
   - Factories that hit the database when they do not need to (`factory.build()` vs. `factory.create()`).

5. **Audit mocking strategy** — Check for:
   - Over-mocking: mocking the thing you are testing (tests pass but prove nothing).
   - Under-mocking: tests that hit real external services (slow, flaky, costly).
   - Mock placement: patch where the object is used, not where it is defined (`unittest.mock.patch("mymodule.requests.get")` not `patch("requests.get")`).
   - HTTP mocking: `respx` for `httpx`, `responses` for `requests`, `aioresponses` for `aiohttp`.
   - Missing `spec=True` on mocks (allows calling methods that do not exist on the real object).

6. **Audit async testing** — If the project uses async code, check for:
   - `pytest-asyncio` with `mode="auto"` or explicit `@pytest.mark.asyncio` decorators.
   - Missing `async` on test functions that test async code (test passes silently without actually awaiting).
   - Async fixtures using `@pytest_asyncio.fixture` instead of `@pytest.fixture`.
   - Event loop scope mismatches between fixtures and tests.

7. **Audit parametrize usage** — Check for:
   - Duplicate test functions that differ only in input/output (should be `@pytest.mark.parametrize`).
   - Missing edge case parameters: empty input, None, boundary values, unicode, very large inputs.
   - Parametrize IDs for readable test output (`pytest.param(..., id="empty-list")`).

8. **Assess testing pyramid** — Check the balance:
   - **Unit tests** (services, pure functions): fast, isolated, high coverage. Should be the majority.
   - **Integration tests** (repos + DB, external service wrappers): test real interactions, use test databases or containers.
   - **E2E tests** (API endpoints): test the full stack via `TestClient` / `httpx.AsyncClient`. Should be the fewest, covering critical paths.

9. **Report findings** — Present findings with specific file references, current patterns, recommended improvements, and examples.

## Output

- **Format**: Audit report delivered in the conversation
- **Key sections**: Fixture Organization, Factory Patterns, Mocking Strategy, Async Testing (if applicable), Parametrize Opportunities, Testing Pyramid Balance, Prioritized Recommendations with Code Examples

## Anti-patterns

- **Testing implementation, not behavior** — Tests that assert on internal method calls or private attributes break when you refactor. Test the public interface and observable outcomes.
- **Shared mutable state between tests** — Session-scoped fixtures with mutable state cause tests to pass individually but fail together. Default to function scope; widen only with immutable data.
- **Mock everything** — If every dependency is mocked, the test proves the mock works, not the code. Integration tests exist for a reason. Mock external boundaries (APIs, databases in unit tests), not internal collaborators.
- **No assertion messages** — While `pytest` provides rich diffs for failures, complex assertions can benefit from a message explaining the *intent* of the check. For example, `assert user.is_active, "New users should be active by default"` is more informative than just `assert user.is_active is True`.
- **Ignoring test performance** — A test suite that takes 10 minutes will not be run locally. Profile slow tests, use appropriate fixture scopes, and parallelize with `pytest-xdist`.
- **Copy-paste test functions** — Five test functions that differ by one line should be one parametrized test. Duplication in tests is just as harmful as duplication in production code.
