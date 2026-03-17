---
name: debug
description: Systematic debugging methodology with binary search, observability, and root cause analysis
version: 1.1.0
tags: [debugging, troubleshooting, observability, diagnostics]
owner: engineering
status: active
---

# Debug Skill

## Overview

Use a structured debugging workflow to isolate and resolve issues.

## Usage

```
/debug
```

## Identity
**Role**: Debugging Specialist
**Objective**: Systematically identify, isolate, and resolve bugs using proven methodologies and modern tooling.

## Debugging Philosophy

### Core Principles
1. **Reproduce first**: Can't fix what you can't see
2. **Understand before changing**: Know the root cause, not just symptoms
3. **One change at a time**: Isolate variables
4. **Verify the fix**: Prove it actually works
5. **Prevent recurrence**: Add tests, improve logging

### The Scientific Method
1. **Observe**: What is the actual behavior?
2. **Hypothesize**: What could cause this?
3. **Predict**: If hypothesis is true, what else should we see?
4. **Test**: Verify or falsify the hypothesis
5. **Iterate**: Refine hypothesis based on results

## Debugging Workflow

### Phase 1: Reproduce

**Goal**: Create reliable reproduction steps.

```markdown
## Bug Report Template
**Expected**: What should happen
**Actual**: What actually happens
**Steps to reproduce**:
1. Step one
2. Step two
3. Observe error

**Environment**: OS, browser, versions
**Frequency**: Always / Sometimes / Once
```

If intermittent:
- Increase logging verbosity
- Run in loop until failure
- Check for race conditions, timing issues

### Phase 2: Isolate

**Binary Search Method**:
```
1. Find a known "good" state (working commit, config, etc.)
2. Find the "bad" state (current broken state)
3. Test the midpoint
4. Narrow to the half that contains the bug
5. Repeat until you find the exact change
```

**Git Bisect** (for regressions):
```bash
git bisect start
git bisect bad HEAD           # Current commit is bad
git bisect good v1.2.3        # This tag was good
# Git checks out middle commit
# Test and mark:
git bisect good  # or
git bisect bad
# Repeat until found
git bisect reset
```

**Divide and Conquer**:
- Comment out half the code, does bug persist?
- Remove half the data, does bug persist?
- Disable half the features, does bug persist?

### Phase 3: Diagnose

**Observability Pillars**:

1. **Logs**: What happened chronologically
   ```python
   import logging
   logging.debug(f"Processing item {item.id}, state={item.state}")
   ```

2. **Metrics**: Quantitative measurements
   - Request latency, error rates, queue depths
   - Memory usage, CPU, connection counts

3. **Traces**: Request flow across services
   - Distributed tracing (Jaeger, Zipkin, OpenTelemetry)
   - Call stacks, timing breakdowns

**Debugging Tools**:

| Language | Debugger | Commands |
|----------|----------|----------|
| Python | pdb/ipdb | `breakpoint()`, `import pdb; pdb.set_trace()` |
| JavaScript | Chrome DevTools | `debugger;` statement |
| TypeScript | VS Code debugger | Launch config + breakpoints |
| Go | Delve | `dlv debug`, `dlv attach` |
| Rust | lldb/gdb | `rust-gdb`, `rust-lldb` |

**Strategic Logging**:
```python
# Add context at boundaries
logger.info("API request", extra={
    "method": request.method,
    "path": request.path,
    "user_id": user.id,
    "request_id": request.id
})

# Log state transitions
logger.debug(f"State change: {old_state} -> {new_state}")

# Log decision points
logger.debug(f"Cache {'hit' if cached else 'miss'} for key={key}")
```

### Phase 4: Fix

**Fix Validation**:
1. Verify fix resolves the original issue
2. Check for regressions (run full test suite)
3. Test edge cases related to the bug
4. Consider: Does this fix mask a deeper issue?

**Fix Documentation**:
```markdown
## Root Cause
The cache TTL was set in seconds but the timestamp comparison
used milliseconds, causing premature cache invalidation.

## Fix
Changed `Date.now()` to `Date.now() / 1000` in cache check.

## Prevention
Added unit test for cache expiration timing.
Added type annotation to clarify time unit: `ttl_seconds: int`
```

### Phase 5: Prevent

1. **Add regression test**: Proves bug stays fixed
2. **Improve observability**: Log what would have helped
3. **Update documentation**: Warn about the pitfall
4. **Fix root cause**: Not just symptoms

## Common Bug Patterns

### Off-by-One Errors
- Check loop boundaries: `<` vs `<=`
- Array indexing: 0-based vs 1-based
- Date/time: inclusive vs exclusive ranges

### Null/Undefined
- Check optional chaining: `obj?.prop`
- Verify data exists before access
- Handle empty arrays/objects

### Race Conditions
- Async operations completing out of order
- Shared state modified concurrently
- Check for missing `await`

### State Management
- Stale state from closures
- Mutations without triggering re-render
- State not reset on navigation

### Type Coercion
- String vs number comparisons
- Truthy/falsy edge cases
- JSON serialization issues

## Debugging Specific Scenarios

### API Not Responding
```bash
# Check if service is running
curl -I http://localhost:3000/health

# Check logs
docker logs <container> --tail 100

# Check network
netstat -an | grep 3000
```

### Memory Leak
```bash
# Node.js heap dump
node --inspect app.js
# Connect Chrome DevTools, take heap snapshots

# Python memory profiling
pip install memory_profiler
python -m memory_profiler script.py
```

### Database Issues
```sql
-- Check slow queries
EXPLAIN ANALYZE SELECT ...;

-- Check connections
SELECT * FROM pg_stat_activity;

-- Check locks
SELECT * FROM pg_locks;
```

### Frontend Issues
```javascript
// React: Check re-render causes
React.useEffect(() => {
  console.log('Effect triggered', { deps });
}, [deps]);

// Check network tab for failed requests
// Check console for errors
// Use React DevTools for component state
```

## Time-Travel Debugging

For complex state bugs, use time-travel debugging:

**rr (Record and Replay)**:
```bash
# Record execution
rr record ./program

# Replay and debug
rr replay
(rr) reverse-continue  # Run backwards!
(rr) watch -l &variable # Break when variable changes
```

**Redux DevTools** (Frontend):
- See every action dispatched
- Time-travel through state changes
- Export/import state for reproduction

## AI-Assisted Debugging

When using AI for debugging:
1. **Provide context**: Full error message, stack trace, relevant code
2. **Describe attempts**: What you already tried
3. **Verify suggestions**: AI can hallucinate fixes
4. **Understand the fix**: Don't blindly apply changes

## Output Format

After debugging, document:

```json
{
  "bug_id": "BUG-123",
  "status": "resolved",
  "root_cause": "Cache TTL comparison used wrong time unit",
  "fix_applied": "Converted milliseconds to seconds in cache.ts:45",
  "verification": [
    "Unit test added: cache.test.ts",
    "Manual reproduction no longer occurs",
    "Deployed to staging, monitored for 1 hour"
  ],
  "prevention": [
    "Added TypeScript type for TimeSeconds",
    "Updated cache documentation"
  ]
}
```

## Outputs

- Root cause summary and verified fix steps.

## Related Skills

- `/test-writer-unit-integration` - Add tests to prevent regressions
