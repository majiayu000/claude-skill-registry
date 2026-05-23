---
name: golang-concurrency-safety
description: Go concurrency safety review. Use when checking goroutines, channels, race conditions, or synchronization. Detects goroutine leaks, deadlocks, race conditions, and unsafe channel operations.
license: MIT
metadata:
  author: saifoelloh
  version: "2.0.0"
  parent_skill: golang-best-practices
  sources:
    - "Concurrency in Go (Katherine Cox-Buday)"
    - "Learning Go: An Idiomatic Approach (Jon Bodner)"
  last_updated: "2026-01-22"
---

# Golang Concurrency Safety

Expert-level concurrency safety review for Go applications. Detects common concurrency bugs that cause production failures, race conditions, deadlocks, and resource leaks.

## When to Apply

Use this skill when:
- Reviewing code with goroutines or channels
- Debugging race conditions or deadlocks
- Auditing concurrent data access
- Investigating goroutine leaks or memory issues
- Writing new concurrent code
- Preparing concurrent code for production

## Rule Categories by Priority

| Priority | Count | Focus |
|----------|-------|-------|
| Critical | 5 | Prevents crashes, leaks, deadlocks |
| High | 4 | Correctness and reliability |
| Medium | 3 | Code quality and idioms |

## Rules Covered (12 total)

### Critical Issues (5)

- `critical-goroutine-leak` - Goroutines must have exit conditions
- `critical-race-condition` - Protect shared state with mutex/channels
- `critical-channel-deadlock` - Ensure paired send/receive operations
- `critical-close-panic` - Sender closes channel, not receiver
- `critical-defer-in-loop` - Avoid defer in loops (resource leaks)

### High-Impact Patterns (4)

- `high-goroutine-unbounded` - Limit concurrent goroutines (worker pool)
- `high-channel-not-closed` - Always close channels when done
- `high-loop-variable-capture` - Avoid closure over loop variables
- `high-waitgroup-mismatch` - Match Add() and Done() calls

### Medium Improvements (3)

- `medium-directional-channels` - Use send/receive-only channels
- `medium-buffered-channel-size` - Choose appropriate buffer size
- `medium-select-default` - Avoid busy-wait with select

## How to Use

### For Code Review

1. Scan code for goroutine launches and channel operations
2. Check against rules in priority order (Critical first)
3. For each violation found, reference the specific rule file
4. Provide exact line numbers and explanation
5. Show corrected code example

### Accessing Detailed Rules

Each rule file in `rules/` contains:
- Brief explanation of why it matters
- Detection criteria (how to spot the issue)
- Incorrect code example (❌ BAD)
- Correct code example (✅ GOOD)
- Impact assessment
- References

**Example**:
```
rules/critical-goroutine-leak.md
rules/high-channel-not-closed.md
```

## Trigger Phrases

This skill activates when you say:
- "Check for race conditions"
- "Review concurrency"
- "Find goroutine leaks"
- "Check for deadlocks"
- "Review channel usage"
- "Audit goroutine safety"
- "Check synchronization"
- "Review concurrent code"

## Common Patterns

**Goroutine leak detection**:
```
Check this code for goroutine leaks
```

**Race condition audit**:
```
Verify this concurrent code is safe
```

**Channel safety review**:
```
Review channel usage for deadlocks
```

## Output Format

When reviewing code, use this format:

```
## Critical Concurrency Issues: X

### [Rule Name] (Line Y)
**Issue**: Brief description
**Impact**: Race condition / Deadlock / Goroutine leak
**Fix**: Suggested correction
**Example**:
```go
// Corrected code here
```

## High-Impact Patterns: X

[Similar format for high priority items]

## Medium Improvements: X

[Similar format for medium priority items]
```

## Philosophy

Based on Katherine Cox-Buday's "Concurrency in Go":

- **Concurrency is not parallelism** - Design for coordination, not just speed
- **Channels are for communication** - Use for passing ownership
- **Mutexes are for state** - Use for protecting shared memory
- **Always have exit conditions** - Every goroutine must be able to stop
- **Context is the standard** - Use context.Context for cancellation

## Related Skills

- [golang-error-handling](../error-handling/SKILL.md) - For context propagation patterns
- [golang-clean-architecture](../clean-architecture/SKILL.md) - For usecase/repository concurrency patterns

## Notes

- Rules are evidence-based from authoritative Go concurrency books
- All examples are tested and production-ready
- Detection patterns help identify issues systematically
- Focused exclusively on concurrency safety (not general Go patterns)
