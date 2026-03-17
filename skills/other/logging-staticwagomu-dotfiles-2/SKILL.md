---
name: logging
description: Guide logging practices based on Dave Cheney's minimalist philosophy. Use when adding log.Info/Debug/Error/Warn/Fatal calls, reviewing logging code, handling errors with log+return pattern, discussing log levels, or designing error handling strategies.
---

# INSTRUCTIONS

Apply Dave Cheney's logging philosophy: simplify ruthlessly, handle errors properly, and log only what matters.

## Core Principles

1. **Only Two Log Levels Matter**
   - **Info**: For operators/users—things they need to know during normal operation
   - **Debug**: For developers—controlled per-package during development

2. **Eliminate Unnecessary Levels**
   | Level | Verdict | Reason |
   |-------|---------|--------|
   | Warning | Remove | "Nobody reads warnings"—either it's an error or info |
   | Fatal | Avoid | Bypasses `defer`, prevents cleanup. Let errors bubble to `main()` |
   | Error | Rethink | If handled, it's info. If not handled, return it to caller |

   **Exception**: Warnings from runtimes and external libraries should be logged at warning level. You don't control these sources, and their warnings often signal deprecations or upcoming breaking changes that operators need to track.

3. **The Golden Rule of Error Logging**
   > "You should either handle the error, or pass it back to the caller."

   - **Don't** log an error AND return it (causes duplicate logs up the stack)
   - **Don't** log errors in library code (caller decides what to do)
   - **Do** let errors bubble up to where they can be meaningfully handled

4. **Terminal Error Handlers: When Error Level IS Appropriate**

   At the boundary where errors become **user-facing unexpected failures** (e.g., 5xx responses), error-level logging is correct:

   - The error chain ends here—no caller to return to
   - The user receives a generic message (for security/UX)
   - Operators need the full error details for debugging

   ```go
   // At HTTP handler boundary - error level is appropriate
   if err != nil {
       log.Error("unexpected failure",
           "error", err,
           "request_id", requestID,
       )
       http.Error(w, "Internal Server Error", http.StatusInternalServerError)
       return
   }
   ```

   **This is NOT the same as logging mid-stack**—this is the terminal handler where errors are finally consumed, not propagated.

## Review Checklist

When reviewing or writing logging code:

- [ ] Is this log statement for users (info) or developers (debug)?
- [ ] Am I logging an error AND returning it? (Remove the log)
- [ ] Is this a terminal handler (5xx boundary)? (Error level is appropriate here)
- [ ] Is this a warning? (Convert to info or error, or remove)
- [ ] Is this `Fatal`/`panic` in library code? (Return error instead)
- [ ] Does this log message help the operator understand system state?

## Anti-Patterns to Avoid

```go
// BAD: Log and return (duplicate logs)
if err != nil {
    log.Error("failed to connect", err)
    return err
}

// GOOD: Just return (let caller decide)
if err != nil {
    return fmt.Errorf("connect: %w", err)
}

// BAD: Warning that nobody will act on
log.Warn("connection pool running low")

// GOOD: Either info (if expected) or error (if action needed)
log.Info("connection pool at 80% capacity")
```

## Structured Logging

When logging is appropriate, prefer structured formats:

```go
// Prefer structured fields over string interpolation
log.Info("request completed",
    "method", r.Method,
    "path", r.URL.Path,
    "duration", time.Since(start),
)
```

## Reference

Based on: [Let's talk about logging](https://dave.cheney.net/2015/11/05/lets-talk-about-logging) by Dave Cheney (2015)
