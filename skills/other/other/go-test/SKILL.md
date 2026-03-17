---
name: go-test
description: Generate deterministic Go unit tests using `testutil`, table-driven patterns, and infra mocks with ≥80% coverage.
compatibility: Requires Go
metadata:
  short-description: Deterministic Go tests with helpers, mocks, ≥80% coverage.
---

Generate Go unit tests for the provided code using Go testing best practices.

## Requirements
- Use **table-driven tests** for all testable functions.
- Use **mocking** where appropriate:
    - Prefer `testify/mock` for interface dependencies.
    - Avoid real external dependencies (DB, network, filesystem).
- Focus on **test coverage**, including:
    - Success cases
    - Error cases
    - Edge cases
    - Boundary conditions
- Tests must be **deterministic** and **_translation-safe_** (no reliance on time, randomness, or global state unless mocked).
- Follow idiomatic Go conventions:
    - File name: `<file>_test.go`
    - Test name: `Test<FunctionName>`
- Always use **English** in test names and comments.
- Enforce minimum **package coverage of ≥80%**.
- Coverage must include:
    - At least one error path per public function (if applicable).
    - Boundary or edge cases where reasonable.

## Output Expectations
- Generate complete, compilable test code.
- Include necessary imports.
- Clearly separate:
    - Arrange
    - Act
    - Assert
- Prefer readability to cleverness.
- Generated tests should realistically achieve ≥80% coverage when executed with: `go test -cover ./...`

## Additional Guidelines
- Prefer **small, focused tests** over large monolithic ones.
- If a function is hard to test:
    - Explain briefly **why**
    - Suggest a **refactor** (e.g., dependency injection).
- Do not test private implementation details—test behavior.
- Avoid snapshot-style assertions unless explicitly requested.
- If achieving ≥ 80% coverage is not possible without testing private implementation details:
    - Explain the limitation briefly
    - Suggest a refactor (interface extraction, dependency injection)
- Avoid fake coverage (e.g. meaningless assertions).

## Please Read the References
- Detailed technical reference: [REFERENCE.md](./references/REFERENCE.md).
