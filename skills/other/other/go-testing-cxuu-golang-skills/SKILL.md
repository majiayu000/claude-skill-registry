---
name: go-testing
description: Use when writing, reviewing, or improving Go test code — including table-driven tests, subtests, parallel tests, test helpers, test doubles, and assertions with cmp.Diff. Also use when a user asks to write a test for a Go function, even if they don't mention specific patterns like table-driven tests or subtests. Does not cover benchmark performance testing (see go-performance).
license: Apache-2.0
compatibility: Uses github.com/google/go-cmp for cmp.Diff comparisons
metadata:
  sources: "Google Style Guide, Uber Style Guide"
allowed-tools: Bash(bash:*)
---

# Go Testing

## Quick Reference

| Pattern | Use When |
|---------|----------|
| `t.Error` | Default — report failure, keep running |
| `t.Fatal` | Setup failed or continuing is meaningless |
| `cmp.Diff` | Comparing structs, slices, maps, protos |
| Table-driven | Many cases share identical logic |
| Subtests | Need filtering, parallel execution, or naming |
| `t.Helper()` | Any test helper function (call as first statement) |
| `t.Cleanup()` | Teardown in helpers instead of defer |

---

## Useful Test Failures

> **Normative**: Test failures must be diagnosable without reading the test
> source.

Every failure message must include: function name, inputs, actual (got), and
expected (want). Use the format `YourFunc(%v) = %v, want %v`.

```go
// Good:
t.Errorf("Add(2, 3) = %d, want %d", got, 5)

// Bad: Missing function name and inputs
t.Errorf("got %d, want %d", got, 5)
```

Always print got before want: `got %v, want %v` — never reversed.

---

## No Assertion Libraries

> **Normative**: Do not use assertion libraries. Use `cmp.Diff` for complex
> comparisons.

```go
if diff := cmp.Diff(want, got); diff != "" {
    t.Errorf("GetPost() mismatch (-want +got):\n%s", diff)
}
```

For protocol buffers, add `protocmp.Transform()` as a cmp option. Always
include the direction key `(-want +got)` in diff messages. Avoid comparing
JSON/serialized output — compare semantically instead.

> Read [references/TEST-HELPERS.md](references/TEST-HELPERS.md) when writing
> custom comparison helpers or domain-specific test utilities.

---

## t.Error vs t.Fatal

> **Normative**: Use `t.Error` by default to report all failures in one run.
> Use `t.Fatal` only when continuing is impossible.

**Choose `t.Fatal` when:**
- Setup fails (DB connection, file load)
- The next assertion depends on the previous one succeeding (e.g., decode after
  encode)

**Never call `t.Fatal`/`t.FailNow` from a goroutine** other than the test
goroutine — use `t.Error` instead.

> Read [references/TEST-HELPERS.md](references/TEST-HELPERS.md) when writing
> helpers that need to choose between t.Error and t.Fatal, or for detailed
> examples of both.

---

## Table-Driven Tests

> See `assets/table-test-template.go` when scaffolding a new table-driven test and need the canonical struct, loop, and subtest layout.

> **Advisory**: Use table-driven tests when many cases share identical logic.

**Use table tests when:** all cases run the same code path with no conditional
setup, mocking, or assertions. A single `shouldErr` bool is acceptable.

**Don't use table tests when:** cases need complex setup, conditional mocking,
or multiple branches — write separate test functions instead.

**Key rules:**
- Use field names when cases span many lines or have same-type adjacent fields
- Include inputs in failure messages — never identify rows by index

> Read [references/TABLE-DRIVEN-TESTS.md](references/TABLE-DRIVEN-TESTS.md)
> when writing table-driven tests, subtests, or parallel tests.

> **Validation**: After generating or modifying tests, run `go test -run TestXxx -v` to verify the tests compile and pass. Fix any compilation errors before proceeding.

---

## Test Helpers

> **Normative**: Test helpers must call `t.Helper()` first and use `t.Cleanup()`
> for teardown.

```go
func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()
    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        t.Fatalf("Could not open database: %v", err)
    }
    t.Cleanup(func() { db.Close() })
    return db
}
```

> Read [references/TEST-HELPERS.md](references/TEST-HELPERS.md) when writing
> test helpers, cleanup functions, or custom comparison utilities.

---

## Test Error Semantics

> **Advisory**: Test error semantics, not error message strings.

```go
// Bad: Brittle string comparison
if err.Error() != "invalid input" { ... }

// Good: Semantic check
if !errors.Is(err, ErrInvalidInput) { ... }
```

For simple presence checks when specific semantics don't matter:

```go
if gotErr := err != nil; gotErr != tt.wantErr {
    t.Errorf("f(%v) error = %v, want error presence = %t", tt.input, err, tt.wantErr)
}
```

---

## Test Organization

> Read [references/TEST-ORGANIZATION.md](references/TEST-ORGANIZATION.md) when
> working with test doubles, choosing test package placement, or scoping test
> setup.

> Read [references/VALIDATION-APIS.md](references/VALIDATION-APIS.md) when
> designing reusable test validation functions.

---

## Integration Testing

> Read [references/INTEGRATION.md](references/INTEGRATION.md) when writing
> TestMain, acceptance tests, or tests that need real HTTP/RPC transports.

---

## Available Scripts

- **`scripts/gen-table-test.sh`** — Generates a table-driven test scaffold

```bash
bash scripts/gen-table-test.sh ParseConfig config > config/parse_config_test.go
bash scripts/gen-table-test.sh --parallel ParseConfig config      # with t.Parallel()
bash scripts/gen-table-test.sh --output config/parse_config_test.go ParseConfig config
```

---

## Related Skills

- **Error testing**: See [go-error-handling](../go-error-handling/SKILL.md) when testing error semantics with `errors.Is`/`errors.As` or sentinel errors
- **Interface mocking**: See [go-interfaces](../go-interfaces/SKILL.md) when creating test doubles by implementing interfaces at the consumer side
- **Naming test functions**: See [go-naming](../go-naming/SKILL.md) when naming test functions, subtests, or test helper utilities
- **Linter integration**: See [go-linting](../go-linting/SKILL.md) when running linters alongside tests in CI or pre-commit hooks
