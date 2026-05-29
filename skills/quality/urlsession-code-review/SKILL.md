---
name: urlsession-code-review
description: Reviews URLSession networking code for iOS/macOS. Covers async/await patterns, request building, error handling, caching, and background sessions.
triggers:
  - URLSession
  - URLRequest
  - URLCache
  - URLError
  - iOS networking
---

# URLSession Code Review

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Async/Await | [async-networking.md](references/async-networking.md) |
| Requests | [request-building.md](references/request-building.md) |
| Errors | [error-handling.md](references/error-handling.md) |
| Caching | [caching.md](references/caching.md) |

## Review Checklist

### Response Validation
- [ ] HTTP status codes validated - URLSession does NOT throw on 404/500
- [ ] Response cast to HTTPURLResponse before checking status
- [ ] Both transport errors (URLError) and HTTP errors handled

### Memory & Resources
- [ ] Downloaded files moved/deleted (async API doesn't auto-delete)
- [ ] Sessions with delegates call `finishTasksAndInvalidate()`
- [ ] Long-running tasks use `[weak self]`
- [ ] Stored Task references cancelled when appropriate

### Configuration
- [ ] `timeoutIntervalForResource` set (default is 7 days!)
- [ ] URLCache sized adequately (default 512KB too small)
- [ ] Sessions reused for connection pooling

### Background Sessions
- [ ] Unique identifier (especially with app extensions)
- [ ] File-based uploads (not data-based)
- [ ] Delegate methods used (not completion handlers)

### Security
- [ ] No hardcoded secrets (use Keychain)
- [ ] Header values sanitized for CRLF injection
- [ ] Query params via URLComponents (not string concat)

## Hard gates (before reporting findings)

Complete in order. Do not advance while a prior gate is open.

1. **Scope** — **Pass:** You name at least one file under review where `URLSession`, `URLRequest`, `HTTPURLResponse` / `URLResponse`, `URLCache`, or `URLError` appears on a networking path. If none apply, stop with “out of scope.”
2. **HTTP vs transport** — **Pass:** Before claiming missing HTTP status handling or “404 treated as success,” you cite `file:line` for the completion/async/`for await` path that receives `response` and state whether `HTTPURLResponse` is cast and `statusCode` is checked (or cite the helper that does). If you cannot see the handler, say **unknown** and ask for it—do not assume.
3. **Session lifecycle** — **Pass:** For a custom `URLSession` with a delegate, you cite `finishTasksAndInvalidate()` or the documented long-lived/singleton pattern you rely on; for `.shared`, say so if the finding depends on configuration. Skip if only ad hoc `URLSession.shared` one-shots with no delegate issues.
4. **Background or file transfer (if applicable)** — **Pass:** If `URLSessionConfiguration.background`, `downloadTask`, or app-extension–scoped sessions appear, findings cite identifier uniqueness, delegate vs completion-handler usage, or file URLs as required. If none of those APIs appear, mark **N/A** and continue.
5. **Severity and checklist** — **Pass:** Every **Critical** item includes `file:line` and names which **Review Checklist** subsection it violates (e.g. Response Validation, Background Sessions). Lower-severity items still name the file(s) they are drawn from.

## Output Format

```markdown
### Critical
1. [FILE:LINE] Missing HTTP status validation
   - Issue: 404/500 responses not treated as errors
   - Fix: Check `httpResponse.statusCode` is 200-299
```
