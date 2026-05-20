---
name: vibe-concurrent-test-safety
description: Audits tests for concurrency safety — race conditions, shared mock state, cleanup ordering. Use when writing tests that involve goroutines, async operations, or shared mutable state.
user-invocable: true
---

# vibe-concurrent-test-safety

Flaky tests are almost always concurrency bugs in the test, not the code.

## When to Use This Skill

- Writing tests that launch goroutines or async operations
- Tests use shared mock objects accessed by multiple goroutines
- Tests that fail intermittently ("flaky")
- After adding `-race` flag and getting failures
- Tests that involve daemon/server startup and shutdown

## When NOT to Use This Skill

- Purely synchronous tests with no concurrency
- Tests that are already race-free (verified with `-race` flag)
- Simple mock-based tests with single-threaded access

## Common Concurrency Bugs in Tests

### 1. Direct Mock State Access
```go
// BAD: Race condition -- mock.Requests accessed while goroutine writes
go daemon.Run(ctx)
time.Sleep(100 * time.Millisecond)
assert.Equal(t, 3, len(mock.Requests)) // RACE!

// GOOD: Thread-safe accessor
go daemon.Run(ctx)
time.Sleep(100 * time.Millisecond)
assert.Equal(t, 3, mock.RequestCount()) // Safe
```

### 2. Missing Context Cancellation Before Cleanup
```go
// BAD: Close bus while daemon goroutine still using it
go daemon.Run(ctx)
defer bus.Close() // daemon may still be writing!

// GOOD: Cancel context first, wait, then cleanup
go daemon.Run(ctx)
defer func() {
    cancel()          // Signal daemon to stop
    <-daemon.Done()   // Wait for it
    bus.Close()        // Now safe
}()
```

### 3. Assertions on Timing
```go
// BAD: Relies on timing
go startServer()
time.Sleep(50 * time.Millisecond) // May not be enough
resp := callServer()

// GOOD: Wait for readiness
go startServer()
waitForReady(server) // Poll or use channel
resp := callServer()
```

## Audit Checklist

- [ ] No direct access to shared mock fields (use accessors)
- [ ] Context cancelled before resource cleanup
- [ ] Goroutines joined before test ends (`<-done` or `wg.Wait()`)
- [ ] No `time.Sleep` for synchronization (use channels, waitgroups, or polling)
- [ ] Assertions use `Eventually` or polling for async results
- [ ] Test passes with `-race` flag
- [ ] Test passes when run 100 times (`-count=100`)

## Output Format

### Concurrent Test Safety Audit: [Test File]

**Issues Found**: X

| # | Issue | Line | Fix |
|---|-------|------|-----|
| 1 | Direct mock access | :42 | Use mock.RequestCount() |
| 2 | Missing cancel before Close | :15 | Add cancel() before defer |

### Suggested Fixes
[Code snippets for each fix]
