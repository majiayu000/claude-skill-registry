---
name: code-review
description: Reviews code for bugs, style, and best practices. Use when reviewing PRs or checking code quality.
---

# Code Review

## Checklist

**Correctness:** Logic errors, edge cases, off-by-one, resource leaks, race conditions, error handling

**Security:** Input validation, injection (SQL/XSS), auth/authz, secrets exposure, CSRF

**Performance:** N+1 queries, redundant work, memory leaks, blocking I/O, missing indexes

**Maintainability:** Clear naming, single responsibility, DRY, test coverage

## Severity

| Level | Action |
|-------|--------|
| CRITICAL | Security/data-loss risk — must fix |
| MAJOR | Bug/performance — should fix |
| MINOR | Code smell — consider fixing |
| STYLE | Formatting — optional |

## Comment Format

```
### [SEVERITY] Brief description
**File:** path:line
**Issue:** What's wrong
**Suggestion:** Proposed fix
```

## Flag These

- `== true/false` → use boolean directly
- `catch(e) {}` → swallowed error
- Magic numbers → named constants
- Deep nesting → early returns
- Commented-out code → delete it
