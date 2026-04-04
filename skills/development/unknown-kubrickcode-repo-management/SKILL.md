---
name: go-test
description: |
  Provides Go standard testing package expertise and best practices. Ensures proper table-driven test patterns, subtests organization, benchmark implementation, and test coverage strategies. Specializes in testing.T/testing.B usage, test helpers, mock interfaces, race detection, and integration testing patterns following Go conventions.
  Use when: writing Go test files (_test.go), implementing table-driven tests with subtests (t.Run), creating benchmark tests (testing.B), writing example tests for documentation, implementing test helpers and fixtures, mocking interfaces for unit tests, measuring code coverage with go test -cover, detecting race conditions with -race flag, or organizing integration tests in Go projects.
---

# Go Testing Code Guide

## Test File Structure

One-to-one matching with the file under test. Test files should be located in the same directory as the target file.

## File Naming

Format: `{target-file-name}_test.go`.

**Example:** `user.go` → `user_test.go`

## Test Hierarchy

Organize by method (function) unit as major sections, and by test case as minor sections. Complex methods can have intermediate sections by scenario.

## Test Coverage Selection

Omit obvious or overly simple logic (simple getters, constant returns). Prioritize testing business logic, conditional branches, and code with external dependencies.

## Test Case Composition

At least one basic success case is required. Focus primarily on failure cases, boundary values, edge cases, and exception scenarios.

## Test Independence

Each test should be executable independently. No test execution order dependencies. Initialize shared state for each test.

## Given-When-Then Pattern

Structure test code in three stages—Given (setup), When (execution), Then (assertion). Separate stages with comments or blank lines for complex tests.

## Test Data

Use hardcoded meaningful values. Avoid random data as it causes unreproducible failures. Fix seeds if necessary.

## Mocking Principles

Mock external dependencies (API, DB, file system). For modules within the same project, prefer actual usage; mock only when complexity is high.

## Test Reusability

Extract repeated mocking setups, fixtures, and helper functions into common utilities. Be careful not to harm test readability through excessive abstraction.

## Integration/E2E Testing

Unit tests are the priority. Write integration/E2E tests when complex flows or multi-module interactions are difficult to understand from code alone. Place in separate directories (`tests/integration`, `tests/e2e`).

## Test Naming

Test names should clearly express "what is being tested". Recommended format: "should do X when Y". Focus on behavior rather than implementation details.

## Assertion Count

Multiple related assertions in one test are acceptable, but separate tests when validating different concepts.

## Test Functions

Format: `func TestXxx(t *testing.T)`. Write `TestMethodName` functions per method, compose subtests with `t.Run()`.

## Subtests

Pattern: `t.Run("case name", func(t *testing.T) {...})`. Each case should be independently executable. Call `t.Parallel()` when running in parallel.

## Table-Driven Tests

Recommended when multiple cases have similar structure. Define cases with `[]struct{ name, input, want, wantErr }`.

**Example:**

```go
tests := []struct {
    name    string
    input   int
    want    int
    wantErr bool
}{
    {"normal case", 5, 10, false},
    {"negative input", -1, 0, true},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        got, err := Func(tt.input)
        if (err != nil) != tt.wantErr { ... }
        if got != tt.want { ... }
    })
}
```

## Mocking

Utilize interface-based dependency injection. Prefer manual mocking; consider gomock for complex cases. Define test-only implementations within `_test.go`.

## Error Verification

Use `errors.Is()` and `errors.As()`. Avoid string comparison of error messages; verify with sentinel errors or error types instead.

## Setup/Teardown

Use `TestMain(m *testing.M)` for global setup/teardown. For individual test preparation, do it within each test function or extract to helper functions.

## Test Helpers

Extract repeated setup/verification into `testXxx(t *testing.T, ...)` helpers. Receive `*testing.T` as first argument and call `t.Helper()`.

## Benchmarks

Write `func BenchmarkXxx(b *testing.B)` for performance-critical code. Loop with `b.N` and use `b.ResetTimer()` to exclude setup time.
