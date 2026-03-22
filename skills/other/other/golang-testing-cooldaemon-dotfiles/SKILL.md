---
name: golang-testing
description: Go testing patterns and policies. Use when writing Go test code, following TDD, or reviewing Go test code. Do NOT use for application code -- use golang-patterns instead.
durability: encoded-preference
---

# Go Testing Patterns

## Table-Driven Tests (REQUIRED)

Use table-driven tests for all Go tests:

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.expected)
            }
        })
    }
}
```

### With Error Cases

```go
tests := []struct {
    name    string
    input   string
    want    *Config
    wantErr bool
}{
    {"valid", `{"host":"localhost"}`, &Config{Host: "localhost"}, false},
    {"invalid", `{bad}`, nil, true},
}

for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        got, err := Parse(tt.input)
        if tt.wantErr {
            if err == nil {
                t.Error("expected error")
            }
            return
        }
        if err != nil {
            t.Fatalf("unexpected error: %v", err)
        }
        // assert got == tt.want
    })
}
```

## Test Helper Policies

### Always Use t.Helper()

```go
func assertNoError(t *testing.T, err error) {
    t.Helper() // REQUIRED - improves error location reporting
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}
```

### Always Use t.Cleanup()

```go
func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()
    db, _ := sql.Open("sqlite3", ":memory:")
    t.Cleanup(func() { db.Close() }) // REQUIRED - auto cleanup
    return db
}
```

### Use t.TempDir() for Files

```go
tmpDir := t.TempDir() // Auto-cleaned after test
testFile := filepath.Join(tmpDir, "test.txt")
```

## Parallel Tests

```go
for _, tt := range tests {
    tt := tt // Capture loop variable (required before Go 1.22)
    t.Run(tt.name, func(t *testing.T) {
        t.Parallel() // Run in parallel when tests are independent
        // ...
    })
}
```

## Interface-Based Mocking

Define interfaces where used, create mock implementations:

```go
// In consumer package
type UserStore interface {
    GetUser(id string) (*User, error)
}

// Mock for tests
type MockUserStore struct {
    GetUserFunc func(id string) (*User, error)
}

func (m *MockUserStore) GetUser(id string) (*User, error) {
    return m.GetUserFunc(id)
}
```

## Coverage Targets

| Code Type | Target |
|-----------|--------|
| Critical business logic | 100% |
| Public APIs | 90%+ |
| General code | 80%+ |
| Generated code | Exclude |

## Commands

**See `makefile-first` skill** for command execution policy.

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Testing private functions | Test through public API |
| `time.Sleep()` in tests | Use channels or sync primitives |
| Ignoring flaky tests | Fix or remove immediately |
| Skip error path testing | Always test error cases |
| Missing `t.Helper()` | Always add to helper functions |

