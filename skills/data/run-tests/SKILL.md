---
name: run-tests
description: Run the appropriate test suite based on what you're testing and whether you need database access
---

# Run Tests Skill

Use this skill when running or writing tests for this project.

---

## Test Types

This project uses filename and function name conventions for test categorization:

- **Unit tests**: Files without "Integration" in test function names. No external dependencies, fast.
- **Integration tests**: `*_integration_test.go` files with "Integration" in function names. Requires database, slower.
- **Benchmarks**: Standard Go benchmarks (`func Benchmark...`). See `internal/evaluator/evaluator_benchmark_test.go` for an example.

## When to Use Each

### Unit Tests (`task test:unit`)

**Use when:**
- Doing TDD or tight iteration loops
- Testing pure functions or business logic
- No database or network calls needed
- Want fast feedback (runs in seconds)

**Command:**
```bash
task test:unit
```

**What it runs:**
```bash
go test ./... -run "Test[^I]"
```

This runs all tests that don't have "Integration" in the name.

**Example test files:**
- `internal/helpers/maths_test.go`
- `internal/candidate_tree/item_test.go`
- `internal/evaluator/trader_constraints_test.go`

### Integration Tests (`task test:integration`)

**Use when:**
- Testing database operations (models package)
- Testing full workflows that span multiple components
- Verifying migrations work correctly
- Before merging to main

**Commands:**
```bash
# Recommended for DevContainer (assuming database is running)
task test:integration

# Use if database needs to be started via Docker Compose
task test:integration:docker
```

**What it does:**
1. `test:integration`: Runs tests matching `.*Integration.*` pattern.
2. `test:integration:docker`: Starts Docker services (PostgreSQL) via `compose:up`, then runs integration tests.

**What it runs:**
```bash
go test ./... -run ".*Integration.*"
```

**Example test files:**
- `internal/evaluator/find_best_build_integration_test.go`
- `internal/db/db_test.go`

**Requirements:**
- Docker running
- `.env` file configured
- Database migrations applied

### All Tests (`task test`)

**Use when:**
- Running CI/CD pipeline
- Final verification before pushing
- Want comprehensive coverage check

**Command:**
```bash
task test
```

**What it runs:**
```bash
go test ./...
```

Runs everything: unit, integration, and any other tests.

## Test Workflow Recommendations

### During Active Development (TDD)

```bash
# Run unit tests repeatedly after changes
task test:unit
```

### Before Committing

```bash
# Run unit tests (fast check)
task test:unit

# If touching database code, run integration tests
task test:integration
```

### Before Pushing/Merging

```bash
# Run everything
task test

# Run linter too
task lint
```

## Running Specific Tests

### Single test function:
```bash
go test ./internal/evaluator -run TestFindBestBuild
```

### Single package:
```bash
go test ./internal/evaluator/...
```

### Verbose output:
```bash
go test -v ./...
```

### With coverage:
```bash
go test -cover ./...
```

## Writing New Tests

When creating tests, follow the naming convention:

```go
// Unit test (no external dependencies)
// File: internal/helpers/maths_unit_test.go
func TestCalculateAverage(t *testing.T) {
    // ...
}

// Integration test (uses database)
// File: internal/models/weapons_integration_test.go
func TestWeaponsIntegration(t *testing.T) {
    // ...
}
```

**Rules:**
- Unit tests: `*_unit_test.go` files, no database/network
- Integration tests: `*_integration_test.go` files, function name must include "Integration"
- Use table-driven tests for multiple cases
- Keep tests focused and independent

## Troubleshooting

**Integration tests fail with connection error:**
- Ensure database is running.
- Check `.env` has correct connection details.
- In a devcontainer, the database is usually already running. Outside, you might need `task compose:up`.

**Tests pass locally but fail in CI:**
- Ensure you're not relying on local state or files
- Check if tests have proper cleanup
- Verify tests are idempotent (can run multiple times)

**Tests are slow:**
- Ensure unit tests aren't hitting the database
- Check if you can mock external dependencies
- Consider moving integration logic to integration test files
