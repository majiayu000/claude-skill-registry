---
name: go-testing-code-review
description: Reviews Go test code for proper table-driven tests, assertions, and coverage patterns. Use when reviewing *_test.go files.
---

# Go Testing Code Review

## Review Workflow

Follow this sequence **in order**. Do not emit findings until every **Pass** below is satisfied.

1. **Baseline `go.mod`** — Open `go.mod` for the module under review and read the `go` directive.  
   **Pass:** You can state the exact `go X.YY` value (in the review preamble or working notes). Apply version-gated advice only when it matches this baseline (e.g. fuzz tests Go 1.18+, loop-variable capture pre-Go 1.22).

2. **Read surrounding tests** — For each `*_test.go` (or benchmark/fuzz file) in scope, read full test functions and any table `struct{...}` / helpers they use, not only the diff hunk.  
   **Pass:** At least one full `func Test...` / `func Benchmark...` / `func Fuzz...` (or helper it calls) containing the change was read per in-scope file.

3. **Scope the checklist** — Decide which [Review Checklist](#review-checklist) rows apply (table-driven structure, parallelism, HTTP, golden files, mocks). Open [references/structure.md](references/structure.md) and/or [references/mocking.md](references/mocking.md) for those topics; skip rows N/A to the diff with a one-line reason (e.g. “no `t.Parallel` in change”).  
   **Pass:** The review (or working notes) lists which checklist themes you applied, or marks themes N/A with a diff-tied reason.

4. **Pre-report verification** — Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md).  
   **Pass:** The protocol’s **Pre-Report Verification Checklist** is satisfied for each finding you will report (actual test code read, surrounding context checked, “wrong” vs “different style” distinguished, etc.).

## Hard gates (same sequence, shorter)

| Step | Objective pass condition |
| --- | --- |
| 1 | `go X.YY` from `go.mod` is recorded before version-specific test advice. |
| 2 | Full enclosing test (or helper it uses) read per in-scope test file, not diff-only. |
| 3 | In-scope checklist themes listed or N/A with diff-tied reason; references opened as needed. |
| 4 | `review-verification-protocol` completed for every reported issue. |

## Output Format

Report findings as:

```text
[FILE:LINE] ISSUE_TITLE
Severity: Critical | Major | Minor | Informational
Description of the issue and why it matters.
```

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Test structure, naming | [references/structure.md](references/structure.md) |
| Mocking, interfaces | [references/mocking.md](references/mocking.md) |

## Review Checklist

- [ ] Tests are table-driven with clear case names
- [ ] Subtests use t.Run for parallel execution
- [ ] Test names describe behavior, not implementation
- [ ] Errors include got/want with descriptive message
- [ ] Cleanup registered with t.Cleanup
- [ ] Parallel tests don't share mutable state
- [ ] Mocks use interfaces defined in test file
- [ ] Coverage includes edge cases and error paths
- [ ] Performance-critical functions have `Benchmark*` tests
- [ ] Input parsers/validators have `Fuzz*` tests (Go 1.18+)
- [ ] HTTP handlers tested with `httptest.NewRequest`/`httptest.NewRecorder`
- [ ] Golden file tests use `testdata/*.golden` pattern with `-update` flag

## Critical Patterns

### Table-Driven Tests

```go
// BAD - repetitive
func TestAdd(t *testing.T) {
    if Add(1, 2) != 3 {
        t.Error("wrong")
    }
    if Add(0, 0) != 0 {
        t.Error("wrong")
    }
}

// GOOD
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        want     int
    }{
        {"positive numbers", 1, 2, 3},
        {"zeros", 0, 0, 0},
        {"negative", -1, 1, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Add(tt.a, tt.b)
            if got != tt.want {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.want)
            }
        })
    }
}
```

### Error Messages

```go
// BAD
if got != want {
    t.Error("wrong result")
}

// GOOD
if got != want {
    t.Errorf("GetUser(%d) = %v, want %v", id, got, want)
}

// For complex types
if diff := cmp.Diff(want, got); diff != "" {
    t.Errorf("GetUser() mismatch (-want +got):\n%s", diff)
}
```

### Parallel Tests

```go
func TestFoo(t *testing.T) {
    tests := []struct{...}

    for _, tt := range tests {
        tt := tt  // capture (not needed Go 1.22+)
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            // test code
        })
    }
}
```

### Cleanup

```go
// BAD - manual cleanup, skipped on failure
func TestWithTempFile(t *testing.T) {
    f, _ := os.CreateTemp("", "test")
    defer os.Remove(f.Name())  // skipped if test panics
}

// GOOD
func TestWithTempFile(t *testing.T) {
    f, _ := os.CreateTemp("", "test")
    t.Cleanup(func() {
        os.Remove(f.Name())
    })
}
```

## Additional Patterns

### Benchmarks
```go
func BenchmarkProcess(b *testing.B) {
    data := generateTestData(1000)
    b.ResetTimer()

    for i := 0; i < b.N; i++ {
        Process(data)
    }
}

// Run: go test -bench=BenchmarkProcess -benchmem
```

### Fuzz Tests (Go 1.18+)
```go
func FuzzParseInput(f *testing.F) {
    // Seed corpus
    f.Add(`{"name": "test"}`)
    f.Add(``)
    f.Add(`{invalid}`)

    f.Fuzz(func(t *testing.T, input string) {
        result, err := ParseInput(input)
        if err != nil {
            return // invalid input is expected
        }
        // If parsing succeeded, re-encoding should work
        if _, err := json.Marshal(result); err != nil {
            t.Errorf("Marshal after Parse: %v", err)
        }
    })
}

// Run: go test -fuzz=FuzzParseInput -fuzztime=30s
```

### HTTP Handler Tests
```go
func TestHandler(t *testing.T) {
    srv := NewServer(mockDeps)

    req := httptest.NewRequest("GET", "/api/users/123", nil)
    w := httptest.NewRecorder()

    srv.ServeHTTP(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("status = %d, want %d", w.Code, http.StatusOK)
    }
}
```

### Golden Files
```go
var update = flag.Bool("update", false, "update golden files")

func TestRender(t *testing.T) {
    got := Render(input)
    golden := filepath.Join("testdata", t.Name()+".golden")

    if *update {
        if err := os.WriteFile(golden, got, 0644); err != nil {
            t.Fatalf("writing golden file: %v", err)
        }
    }

    want, err := os.ReadFile(golden)
    if err != nil {
        t.Fatalf("reading golden file: %v (run with -update to create)", err)
    }
    if !bytes.Equal(got, want) {
        t.Errorf("output mismatch:\ngot:\n%s\nwant:\n%s", got, want)
    }
}
```

## Anti-Patterns

### 1. Testing Internal Implementation

```go
// BAD - tests private state
func TestUser(t *testing.T) {
    u := NewUser("alice")
    if u.id != 1 {  // testing internal field
        t.Error("wrong id")
    }
}

// GOOD - tests behavior
func TestUser(t *testing.T) {
    u := NewUser("alice")
    if u.ID() != 1 {
        t.Error("wrong ID")
    }
}
```

### 2. Shared Mutable State

```go
// BAD - tests interfere with each other
var testDB = setupDB()

func TestA(t *testing.T) {
    t.Parallel()
    testDB.Insert(...)  // race!
}

// GOOD - isolated per test
func TestA(t *testing.T) {
    db := setupTestDB(t)
    t.Cleanup(func() { db.Close() })
    db.Insert(...)
}
```

### 3. Assertions Without Context

```go
// BAD
assert.Equal(t, want, got)  // "expected X got Y" - which test?

// GOOD
assert.Equal(t, want, got, "user name after update")
```

## When to Load References

- Reviewing test file structure → structure.md
- Reviewing mock implementations → mocking.md

## Review Questions

1. Are tests table-driven with named cases?
2. Do error messages include input, got, and want?
3. Are parallel tests isolated (no shared state)?
4. Is cleanup done via t.Cleanup?
5. Do tests verify behavior, not implementation?
