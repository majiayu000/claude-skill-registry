---
name: writing-go-tests
description: Write Go tests following project conventions. Use when creating test files, writing unit or integration tests, choosing mocks, or setting up test fixtures. Covers test naming, assertions, mock usage, table-driven patterns, and common pitfalls.
---

# Writing Go Tests

Project-specific test conventions for this codebase.

## Critical Rules

- **Always use mockery-generated `Moq*` mocks** when one exists for the interface. Never hand-roll a mock struct for an interface that has a `*_mock.go` file. Run `mockery` (no args) from the module root to regenerate mocks after interface changes.
- **Use `logger.NoopLogger{}` when tests don't need to assert on log output.** It already implements the full `Logger` interface. Never create a custom mock logger just to satisfy the interface — that duplicates `NoopLogger` for no reason.
- **Use `logger.MoqLogger{}` only when the test needs to verify specific log calls** (e.g., asserting that `Warning` was called with a specific message).

## Mock Selection Guide

| Situation | Use | Import |
|-----------|-----|--------|
| Interface has a `*_mock.go` file | `Moq*` struct from that file | Same package (in-package tests) |
| Logger needed but output doesn't matter | `logger.NoopLogger{}` | `utils/logger` |
| Logger needed and must assert on calls | `logger.MoqLogger{}` | `utils/logger` |
| Interface has NO mock file (e.g., `MultiSelectSelector[T]`) | Inline mock struct in test file | N/A |

Before creating an inline mock, check if a `*_mock.go` file exists in the interface's package:

```bash
ls installer/<package-path>/*_mock.go
```

## Test Naming

**Format:** `Test_<DescriptiveStatement>`

Test names describe behavior, not implementation:

```go
// Good: describes behavior
func Test_CompatibilityConfigCanBeLoadedFromFile(t *testing.T)
func Test_CreatingClientShouldLoadCompatibilityMapFromFile(t *testing.T)

// Bad: describes implementation
func Test_LoadConfig(t *testing.T)
func Test_ConfigLoader_Success(t *testing.T)
```

## Assertions

Use `testify/require` for all assertions. When expecting errors, match by keyword, not full message:

```go
// Good: checks for key error indicator
require.Error(t, err)
require.Contains(t, err.Error(), "not found")

// Bad: matches entire error message
require.EqualError(t, err, "file could not be found in the path /config/nonexistent.yaml")
```

## Unit Tests

Unit tests verify a single function or method in isolation.

- Use mocks to isolate the function being tested.
- Place unit tests in the same package as the code being tested.
- Each test verifies a single behavior.

```go
package brew

func Test_BrewPackageManagerInstallsPackageSuccessfully(t *testing.T) {
    // Arrange
    commander := &MoqCommander{
        RunCommandFunc: func(ctx context.Context, name string, args []string, opts ...Option) (Result, error) {
            return Result{ExitCode: 0}, nil
        },
    }
    pm := NewBrewPackageManager(&logger.NoopLogger{}, commander, osManager, "/opt/homebrew/bin/brew")

    // Act
    err := pm.InstallPackage(ctx, RequestedPackageInfo{Name: "git"})

    // Assert
    require.NoError(t, err)
}
```

## Table-Driven Tests

Use when testing multiple scenarios of the same function:

```go
func Test_VerbosityLevelDetermination(t *testing.T) {
    tests := []struct {
        name     string
        verbose  bool
        extra    bool
        expected VerbosityLevel
    }{
        {"default returns normal", false, false, VerbosityNormal},
        {"verbose flag returns verbose", true, false, VerbosityVerbose},
        {"both flags returns extra verbose", true, true, VerbosityExtraVerbose},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := determineVerbosity(tt.verbose, tt.extra)
            require.Equal(t, tt.expected, result)
        })
    }
}
```

## Integration Tests

Integration tests verify interaction between components, including OS-dependent interactions.

- Allow opting out with `testing.Short()`.
- Place in the test package (e.g., `brew_test` for `brew` package).
- Use BDD-style naming: `Test_<gerund>_Should_<behavior>_When_<condition>`.

```go
package brew_test

func Test_InstallingPackage_Should_SucceedWithoutError_When_BrewIsAvailable(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test in short mode")
    }

    pm := NewBrewPackageManager(/* real dependencies */)
    err := pm.InstallPackage(ctx, RequestedPackageInfo{Name: "tree"})
    require.NoError(t, err)
}
```

## Tech Stack

- `testify/require` — assertions (never `assert` for error checks)
- `mockery` with moq template — mock generation (see `.mockery.yml`)
- `logger.NoopLogger{}` — silent logger for tests
