---
name: perf-check
description: Use when the user wants to check performance, find slow code, identify bottlenecks, or audit efficiency.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
argument-hint: "[file or directory]"
---

Analyze **$ARGUMENTS** for performance issues.

## Check Categories

### Database & Queries
- N+1 query patterns (loop with query inside)
- Missing indexes on frequently queried columns
- SELECT * instead of specific columns
- Missing pagination on list endpoints
- Unoptimized joins or subqueries

### Memory & Resources
- Unclosed connections, streams, file handles
- Growing arrays/maps without limits
- Event listeners not removed on cleanup
- Large objects held in memory unnecessarily
- Missing cleanup in useEffect (React)

### Frontend Performance
- Unnecessary re-renders (missing useMemo, useCallback, React.memo)
- Large bundle imports (import entire library vs specific module)
- Images without lazy loading or optimization
- Missing code splitting
- Synchronous operations blocking UI thread
- Missing virtualization for long lists

### API & Network
- Missing caching (Redis, in-memory, HTTP cache headers)
- Redundant API calls
- Missing request deduplication
- Large payloads without compression
- Missing connection pooling

### General
- O(n²) or worse algorithms where O(n) is possible
- Synchronous file I/O in async context
- Regex backtracking (catastrophic regex)
- Unnecessary deep cloning

## Output Format

```
## Performance Report: [target]

### Critical (fix now)
- [file:line] [issue] [impact] [fix]

### Warning (should fix)
- [file:line] [issue] [impact] [fix]

### Suggestion (optimization)
- [file:line] [issue] [impact] [fix]

### Good Patterns Found
- [what's already well-optimized]
```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
