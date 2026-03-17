---
name: go-testing
description: Go testing patterns from Google and Uber style guides including test naming, table-driven tests, subtests, parallel tests, test helpers, test doubles, and assertions. Use when writing or reviewing Go test code, creating test helpers, or setting up table-driven tests.
---

# Go Testing

Guidelines for writing clear, maintainable Go tests following Google's style.

## Useful Test Failures

> **Normative**: Test failures must be diagnosable without reading the test
> source.

Every failure message should include:
- What caused the failure
- The function inputs
- The actual result (got)
- The expected result (want)

### Failure Message Format

Use the standard format: `YourFunc(%v) = %v, want %v`

```go
// Good:
if got := Add(2, 3); got != 5 {
    t.Errorf("Add(2, 3) = %d, want %d", got, 5)
}

// Bad: Missing function name and inputs
if got := Add(2, 3); got != 5 {
    t.Errorf("got %d, want %d", got, 5)
}
```

### Got Before Want

Always print actual result before expected:

```go
// Good:
t.Errorf("Parse(%q) = %v, want %v", input, got, want)

// Bad: want/got reversed
t.Errorf("Parse(%q) want %v, got %v", input, want, got)
```

---

## No Assertion Libraries

> **Normative**: Do not create or use assertion libraries.

Assertion libraries fragment the developer experience and often produce
unhelpful failure messages.

```go
// Bad:
assert.IsNotNil(t, "obj", obj)
assert.StringEq(t, "obj.Type", obj.Type, "blogPost")
assert.IntEq(t, "obj.Comments", obj.Comments, 2)

// Good: Use cmp package and standard comparisons
want := BlogPost{
    Type:     "blogPost",
    Comments: 2,
    Body:     "Hello, world!",
}
if diff := cmp.Diff(want, got); diff != "" {
    t.Errorf("GetPost() mismatch (-want +got):\n%s", diff)
}
```

For domain-specific comparisons, return values or errors instead of calling
`t.Error`:

```go
// Good: Return value for use in failure message
func postLength(p BlogPost) int { return len(p.Body) }

func TestBlogPost(t *testing.T) {
    post := BlogPost{Body: "Hello"}
    if got, want := postLength(post), 5; got != want {
        t.Errorf("postLength(post) = %v, want %v", got, want)
    }
}
```

---

## Comparisons and Diffs

> **Advisory**: Prefer `cmp.Equal` and `cmp.Diff` for complex types.

```go
// Good: Full struct comparison with diff - always include direction key
want := &Doc{Type: "blogPost", Authors: []string{"isaac", "albert"}}
if diff := cmp.Diff(want, got); diff != "" {
    t.Errorf("AddPost() mismatch (-want +got):\n%s", diff)
}

// Good: Protocol buffers
if diff := cmp.Diff(want, got, protocmp.Transform()); diff != "" {
    t.Errorf("Foo() mismatch (-want +got):\n%s", diff)
}
```

**Avoid unstable comparisons** - don't compare JSON/serialized output that may
change. Compare semantically instead.

---

## t.Error vs t.Fatal

> **Normative**: Use `t.Error` to keep tests going; use `t.Fatal` only when
> continuing is impossible.

### Keep Going

Tests should report all failures in a single run:

```go
// Good: Report all mismatches
if diff := cmp.Diff(wantMean, gotMean); diff != "" {
    t.Errorf("Mean mismatch (-want +got):\n%s", diff)
}
if diff := cmp.Diff(wantVariance, gotVariance); diff != "" {
    t.Errorf("Variance mismatch (-want +got):\n%s", diff)
}
```

### When to Use t.Fatal

Use `t.Fatal` when subsequent tests would be meaningless:

```go
// Good: Fatal on setup failure or when continuation is pointless
gotEncoded := Encode(input)
if gotEncoded != wantEncoded {
    t.Fatalf("Encode(%q) = %q, want %q", input, gotEncoded, wantEncoded)
    // Decoding unexpected output is meaningless
}
gotDecoded, err := Decode(gotEncoded)
if err != nil {
    t.Fatalf("Decode(%q) error: %v", gotEncoded, err)
}
```

### Don't Call t.Fatal from Goroutines

> **Normative**: Never call `t.Fatal`, `t.Fatalf`, or `t.FailNow` from a
> goroutine other than the test goroutine. Use `t.Error` instead and let the
> test continue.

---

## Table-Driven Tests

> **Advisory**: Use table-driven tests when many cases share similar logic.

### Basic Structure

```go
// Good:
func TestCompare(t *testing.T) {
    tests := []struct {
        a, b string
        want int
    }{
        {"", "", 0},
        {"a", "", 1},
        {"", "a", -1},
        {"abc", "abc", 0},
    }
    for _, tt := range tests {
        got := Compare(tt.a, tt.b)
        if got != tt.want {
            t.Errorf("Compare(%q, %q) = %v, want %v", tt.a, tt.b, got, tt.want)
        }
    }
}
```

### Best Practices

**Use field names** when test cases span many lines or have adjacent fields of
the same type.

**Don't identify rows by index** - include inputs in failure messages instead of
`Case #%d failed`.

### Avoid Complexity in Table Tests

> **Source**: Uber Go Style Guide

When test cases need complex setup, conditional mocking, or multiple branches,
prefer separate test functions over table tests.

```go
// Bad: Too many conditional fields make tests hard to understand
tests := []struct {
    give          string
    want          string
    wantErr       error
    shouldCallX   bool      // Conditional logic flag
    shouldCallY   bool      // Another conditional flag
    giveXResponse string
    giveXErr      error
    giveYResponse string
    giveYErr      error
}{...}

for _, tt := range tests {
    t.Run(tt.give, func(t *testing.T) {
        if tt.shouldCallX {  // Conditional mock setup
            xMock.EXPECT().Call().Return(tt.giveXResponse, tt.giveXErr)
        }
        if tt.shouldCallY {  // More branching
            yMock.EXPECT().Call().Return(tt.giveYResponse, tt.giveYErr)
        }
        // ...
    })
}

// Good: Separate focused tests are clearer
func TestShouldCallX(t *testing.T) {
    xMock.EXPECT().Call().Return("XResponse", nil)
    got, err := DoComplexThing("inputX", xMock, yMock)
    // assert...
}

func TestShouldCallYAndFail(t *testing.T) {
    yMock.EXPECT().Call().Return("YResponse", nil)
    _, err := DoComplexThing("inputY", xMock, yMock)
    // assert error...
}
```

**Table tests work best when:**

- All cases run identical logic (no conditional assertions)
- Setup is the same for all cases
- No conditional mocking based on test case fields
- All table fields are used in all tests

A single `shouldErr` field for success/failure is acceptable if the test body is
short and straightforward.

---

## Subtests

> **Advisory**: Use subtests for better organization, filtering, and parallel
> execution.

### Subtest Names

- Use clear, concise names: `t.Run("empty_input", ...)`, `t.Run("hu_to_en",
  ...)`
- Avoid wordy descriptions or slashes (slashes break test filtering)
- Subtests must be independent - no shared state or execution order dependencies

```go
// Good: Table tests with subtests
func TestTranslate(t *testing.T) {
    tests := []struct {
        name, srcLang, dstLang, input, want string
    }{
        {"hu_en_basic", "hu", "en", "köszönöm", "thank you"},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Translate(tt.srcLang, tt.dstLang, tt.input); got != tt.want {
                t.Errorf("Translate(%q, %q, %q) = %q, want %q",
                    tt.srcLang, tt.dstLang, tt.input, got, tt.want)
            }
        })
    }
}
```

### Parallel Tests

> **Source**: Uber Go Style Guide

When using `t.Parallel()` in table tests, be aware of loop variable capture:

```go
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        t.Parallel()
        // Go 1.22+: tt is correctly captured per iteration
        // Go 1.21-: add "tt := tt" here to capture the variable
        got := Process(tt.give)
        if got != tt.want {
            t.Errorf("Process(%q) = %q, want %q", tt.give, got, tt.want)
        }
    })
}
```

---

## Test Helpers

> **Normative**: Test helpers must call `t.Helper()` and should use `t.Fatal`
> for setup failures.

```go
// Good: Complete test helper pattern
func mustLoadTestData(t *testing.T, filename string) []byte {
    t.Helper()  // Makes failures point to caller
    data, err := os.ReadFile(filename)
    if err != nil {
        t.Fatalf("Setup failed: could not read %s: %v", filename, err)
    }
    return data
}

func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()
    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        t.Fatalf("Could not open database: %v", err)
    }
    t.Cleanup(func() { db.Close() })  // Use t.Cleanup for teardown
    return db
}
```

**Key rules:**
- Call `t.Helper()` first to attribute failures to the caller
- Use `t.Fatal` for setup failures (don't return errors)
- Use `t.Cleanup()` for teardown instead of defer

---

## Test Doubles

> **Advisory**: Follow consistent naming for test doubles (stubs, fakes, mocks,
> spies).

**Package naming**: Append `test` to the production package (e.g.,
`creditcardtest`).

```go
// Good: In package creditcardtest

// Single double - use simple name
type Stub struct{}
func (Stub) Charge(*creditcard.Card, money.Money) error { return nil }

// Multiple behaviors - name by behavior
type AlwaysCharges struct{}
type AlwaysDeclines struct{}

// Multiple types - include type name
type StubService struct{}
type StubStoredValue struct{}
```

**Local variables**: Prefix test double variables for clarity (`spyCC` not
`cc`).

---

## Test Packages

| Package Declaration | Use Case |
|---------------------|----------|
| `package foo` | Same-package tests, can access unexported identifiers |
| `package foo_test` | Black-box tests, avoids circular dependencies |

Both go in `foo_test.go` files. Use `_test` suffix when testing only public API
or to break import cycles.

---

## Test Error Semantics

> **Advisory**: Test error semantics, not error message strings.

```go
// Bad: Brittle string comparison
if err.Error() != "invalid input" {
    t.Errorf("unexpected error: %v", err)
}

// Good: Test semantic error
if !errors.Is(err, ErrInvalidInput) {
    t.Errorf("got error %v, want ErrInvalidInput", err)
}

// Good: Simple presence check when semantics don't matter
if gotErr := err != nil; gotErr != tt.wantErr {
    t.Errorf("f(%v) error = %v, want error presence = %t", tt.input, err, tt.wantErr)
}
```

---

## Setup Scoping

> **Advisory**: Keep setup scoped to tests that need it.

```go
// Good: Explicit setup in tests that need it
func TestParseData(t *testing.T) {
    data := mustLoadDataset(t)
    // ...
}

func TestUnrelated(t *testing.T) {
    // Doesn't pay for dataset loading
}

// Bad: Global init loads data for all tests
var dataset []byte

func init() {
    dataset = mustLoadDataset()  // Runs even for unrelated tests
}
```

---

## Quick Reference

| Situation | Approach |
|-----------|----------|
| Compare structs/slices | `cmp.Diff(want, got)` |
| Simple value mismatch | `t.Errorf("F(%v) = %v, want %v", in, got, want)` |
| Setup failure | `t.Fatalf("Setup: %v", err)` |
| Multiple comparisons | `t.Error` for each, continue testing |
| Goroutine failures | `t.Error` only, never `t.Fatal` |
| Test helper | Call `t.Helper()` first |
| Large test data | Table-driven with subtests |

## See Also

- For core style principles: `go-style-core`
- For naming conventions: `go-naming`
- For error handling patterns: `go-error-handling`
- For linter configuration: `go-linting`
