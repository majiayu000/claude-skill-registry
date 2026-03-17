---
name: go-code-review
description: Auto-review Go code for 100+ common mistakes when analyzing .go files, discussing Go patterns, or reviewing PRs with Go code. Checks error handling, concurrency, interfaces, performance, testing, and stdlib usage.
allowed-tools: Read,Grep
---

# Go Code Review Skill

Auto-triggers when reviewing Go code to catch common mistakes from <https://100go.co/>

## Review Process

1. Read Go file(s) mentioned
2. Check against patterns in [[knowledge-base.md]]
3. Report issues with:
   - Severity (Critical/Major/Minor)
   - Location (file:line)
   - Mistake # from knowledge base
   - Suggested fix
   - Code example if applicable

## Priority Checks

**Critical (must fix):**

- Error handling (#48-54): ignored errors, incorrect wrapping/comparison
- Concurrency (#58, 69, 70, 74): data races, mutex misuse, sync type copying
- Resource leaks (#26, 28, 76, 79): unclosed resources, memory leaks

**Major (should fix):**

- Interface design (#5-7): pollution, wrong side, returning interfaces
- Goroutine lifecycle (#62, 63): no stop mechanism, loop var capture
- Testing (#83, 86): no race flag, sleep in tests

**Minor (consider):**

- Code organization (#1, 2, 15): shadowing, nesting, missing docs
- Performance (#21, 27, 39): unoptimized init, string concat

## Reference Knowledge Base

See [[knowledge-base.md]] for full 100 Go mistakes reference.

## Example Output

```text
**Issue**: Error not wrapped with context
**Severity**: Major
**Location**: handler.go:42
**Mistake**: #49 - Ignoring When to Wrap an Error
**Fix**: Use `fmt.Errorf("fetch user: %w", err)` instead of returning raw error
**Pattern**: Always wrap errors for context/traceability
```
