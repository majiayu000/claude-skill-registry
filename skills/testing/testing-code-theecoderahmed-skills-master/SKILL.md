---
name: testing-code
description: Generates unit and integration tests using industry-standard frameworks (Jest, Vitest, Pytest). Enforces "Testing Triangle" principles to ensure reliability without slowing down development.
---

# Test Generator & QA Engineer

## When to use this skill
- When the user asks to "test this feature" or "make sure this works".
- When a bug is fixed (Regression Testing).
- When setting up a new project (Test Scaffold).

## Workflow
1.  **Framework Detection**: Identify the stack (React/Next.js -> Vitest/Jest; Python -> Pytest; Flutter -> flutter_test).
2.  **Strategy Selection**:
    - **Unit Tests**: For independent usage logic (utils, hooks). Mock all external dependencies.
    - **Integration Tests**: For API routes and database interactions. Use a test database.
    - **E2E Tests**: (Only if requested) For full user flows (Playwright).
3.  **Code Generation**: Write the test file using the "Arrange-Act-Assert" pattern.
4.  **Verification**: Provide the exact command to run the tests.

## Instructions
1.  **Filesystem**: Always co-locate tests with code (e.g., `features/auth/login.test.ts` next to `login.ts`) or use a top-level `__tests__` folder for integration.
2.  **Mocking**:
    - NEVER make real network calls in Unit Tests. Use `vi.mock()` or `jest.mock()`.
    - If testing DB logic, use an in-memory DB or transaction rollbacks.
3.  **Coverage**: Focus on "Happy Path" (it works) and "Edge Cases" (null values, errors), not 100% coverage vanity metrics.

## Self-Correction Checklist
- "Did I mock the database call?" -> Yes, unless it's an integration test.
- "Did I test for empty input?" -> Yes, always test edge cases.
