---
name: testing
description: MANDATORY - Load before writing tests. Enforces fakes over mocks, golden files, goleak, httptest.
---

# Go Testing Standards

## Philosophy

1. **Fakes over mocks** — Test real implementation when possible; fakes when not
2. **Stdlib first** — Use `testing` package; third-party only when it adds real value
3. **Test behavior, not implementation** — Public API matters, internals don't
4. **Fast and deterministic** — Flaky tests are worse than no tests

---

## Fakes Over Mocks

This is the 2025 consensus: prefer fakes over mocks.

| Type | When to Use |
|------|-------------|
| **Real** | Always prefer if fast and reliable |
| **Fake** | Dependency is slow/unreliable (DB, network, time) |
| **Mock** | Only when verifying specific call sequences |

```go
// Interface defined where USED, not where implemented
type Clock interface {
    Now() time.Time
    After(d time.Duration) <-chan time.Time
}

// Fake with logic (not predetermined responses)
type FakeClock struct {
    current time.Time
}

func (c *FakeClock) Now() time.Time { return c.current }
func (c *FakeClock) Advance(d time.Duration) { c.current = c.current.Add(d) }
```

**Key rules:**
- Define interfaces where they are **used**, not where implemented
- Keep interfaces small (1-3 methods)
- Fakes have logic; mocks have canned responses

Sources: [Learn Go with Tests](https://quii.gitbook.io/learn-go-with-tests/testing-fundamentals/working-without-mocks), [Leapcell: gomock vs Fakes](https://leapcell.io/blog/mastering-mocking-in-go-gomock-vs-interface-based-fakes)

---

## Testing Time-Dependent Code

Cache TTLs, timeouts — all need deterministic time.

### Option 1: Interface Injection (benbjohnson/clock)

```go
import "github.com/benbjohnson/clock"

type Cache struct {
    clock clock.Clock
}

// Production
cache := &Cache{clock: clock.New()}

// Test
mock := clock.NewMock()
cache := &Cache{clock: mock}
mock.Add(5 * time.Minute)  // Advance time programmatically
```

### Option 2: testing/synctest (Go 1.25+)

Runs code in a "bubble" with fake time that auto-advances when goroutines block:

```go
import "testing/synctest"

func TestTimeout(t *testing.T) {
    synctest.Test(t, func(t *testing.T) {
        ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
        defer cancel()

        // Time advances instantly when all goroutines are blocked
        <-ctx.Done()  // Returns immediately, fake clock jumped 5s
    })
}
```

**Note:** Go 1.24 requires `GOEXPERIMENT=synctest`. Go 1.25 includes it in stdlib.

Sources: [Go Blog: Testing Time](https://go.dev/blog/testing-time), [benbjohnson/clock](https://github.com/benbjohnson/clock), [Go Blog: synctest](https://go.dev/blog/synctest)

---

## Testing HTML Handlers with httptest

The primary integration testing pattern for cooked. Use `httptest.NewServer` for full end-to-end tests and `httptest.NewRecorder` for unit-testing individual handlers.

### Full Server Test

```go
func TestRenderMarkdown(t *testing.T) {
    // Set up a fake upstream that serves raw markdown
    upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain")
        w.Write([]byte("# Hello\n\nWorld"))
    }))
    defer upstream.Close()

    // Start cooked with the fake upstream
    srv := httptest.NewServer(cookedHandler(deps))
    defer srv.Close()

    resp, err := http.Get(srv.URL + "/" + upstream.URL + "/README.md")
    if err != nil {
        t.Fatal(err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != 200 {
        t.Fatalf("got status %d, want 200", resp.StatusCode)
    }
    if ct := resp.Header.Get("Content-Type"); !strings.HasPrefix(ct, "text/html") {
        t.Fatalf("got content-type %q, want text/html", ct)
    }
}
```

### Checking Response Headers

```go
func TestResponseHeaders(t *testing.T) {
    // ...setup...
    resp, _ := http.Get(srv.URL + "/" + upstream.URL + "/file.md")

    // Verify X-Cooked-* headers
    if got := resp.Header.Get("X-Cooked-Cache"); got == "" {
        t.Error("missing X-Cooked-Cache header")
    }
    if got := resp.Header.Get("X-Cooked-Content-Type"); got != "markdown" {
        t.Errorf("X-Cooked-Content-Type = %q, want markdown", got)
    }
}
```

---

## Goroutine Leak Detection (goleak)

Detects goroutines that outlive tests — critical for long-running services.

### Package-Wide (Recommended)

```go
// main_test.go
func TestMain(m *testing.M) {
    goleak.VerifyTestMain(m)
}
```

### Per-Test (When Debugging)

```go
func TestSpecificLeak(t *testing.T) {
    defer goleak.VerifyNone(t)
    // test code
}
```

### Ignoring Known Leaks

```go
func TestMain(m *testing.M) {
    goleak.VerifyTestMain(m,
        goleak.IgnoreTopFunction("net/http.(*persistConn).writeLoop"),
    )
}
```

**Note:** goleak doesn't work well with `t.Parallel()` — use `VerifyTestMain` instead.

Sources: [uber-go/goleak](https://github.com/uber-go/goleak), [Brandur: Goroutine Leaks](https://brandur.org/fragments/goroutine-leaks)

---

## Fuzzing

Use for URL parsing, markdown preprocessing, HTML sanitization, and security-sensitive input handling.

**File organization:** Fuzz tests go in separate `*_fuzz_test.go` files, not mixed with unit tests.

```
url.go
url_test.go           # Unit tests
url_fuzz_test.go      # Fuzz tests
```

```go
func FuzzParseUpstreamURL(f *testing.F) {
    // Seed corpus
    f.Add("https://example.com/file.md")
    f.Add("http://cgit.internal/repo/plain/README.md")
    f.Add("")
    f.Add("not-a-url")

    f.Fuzz(func(t *testing.T, input string) {
        _, _ = ParseUpstreamURL(input)  // Should not panic
    })
}
```

### Running

```bash
go test -fuzz=FuzzParseUpstreamURL -fuzztime=30s ./internal/...

# Clear cache when large
go clean -fuzzcache
```

Sources: [Go Fuzzing Docs](https://go.dev/doc/security/fuzz/)

---

## Golden Files

The primary testing pattern for HTML output. Keep in `testdata/golden/`.

```go
var update = flag.Bool("update", false, "update golden files")

func TestRenderOutput(t *testing.T) {
    got := renderMarkdown(input)
    golden := filepath.Join("testdata", "golden", t.Name()+".html")

    if *update {
        os.WriteFile(golden, got, 0644)
        return
    }

    want, _ := os.ReadFile(golden)
    if !bytes.Equal(got, want) {
        t.Errorf("mismatch; run with -update to regenerate")
    }
}
```

Run `go test -update` to regenerate. Always commit golden files.

---

## Parallel Tests

```go
for _, tc := range tests {
    t.Run(tc.name, func(t *testing.T) {
        t.Parallel()
        // test
    })
}
```

**Critical:** Use `t.Cleanup()` not `defer` — defer runs when the outer function returns, before parallel subtests complete.

```go
// Wrong - cleanup happens too early
t.Run("test", func(t *testing.T) {
    t.Parallel()
    defer cleanup()  // Runs immediately!
})

// Correct
t.Run("test", func(t *testing.T) {
    t.Parallel()
    t.Cleanup(cleanup)  // Runs after subtest completes
})
```

Always run with `-race`:
```bash
go test -race ./...
```

Sources: [Parallel Table-Driven Tests](https://www.glukhov.org/post/2025/12/parallel-table-driven-tests-in-go/)

---

## Project Commands

```bash
# All tests
go test ./...

# With race detection
go test -race ./...

# Coverage (use /tmp, not project root)
go test -coverprofile=/tmp/coverage.out ./...
go tool cover -func=/tmp/coverage.out | grep total
```

## Key Files

- `internal/*_test.go` — Package tests
- `testdata/golden/` — Golden HTML output files
- `testdata/fixtures/` — Input test fixtures (markdown, code files)
