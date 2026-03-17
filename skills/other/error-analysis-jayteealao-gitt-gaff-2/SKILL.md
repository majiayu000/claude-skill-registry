---
name: error-analysis
description: This skill should be used when analyzing errors, stack traces, and logs to identify root causes and implement fixes.
---

# Error Analysis Skill

Systematically analyze errors and logs to find root causes.

## When to Use

- Debugging production errors
- Analyzing stack traces
- Investigating log patterns
- Performing root cause analysis
- Categorizing error types

## Reference Documents

- [Log Patterns](./references/log-patterns.md) - Common error patterns by type
- [Root Cause Analysis](./references/root-cause-analysis.md) - RCA techniques
- [Error Categorization](./references/error-categorization.md) - Classifying errors
- [Fix Patterns](./references/fix-patterns.md) - Common fixes by error type

## Analysis Workflow

### 1. Gather Information

```markdown
## Error Report

### Error Message
```
TypeError: Cannot read property 'id' of undefined
    at UserService.getUser (src/services/user.ts:45:23)
    at async Router.handle (src/api/routes.ts:67:12)
```

### Context
- **Environment:** Production
- **Time:** 2024-01-15 14:30 UTC
- **Frequency:** 15 occurrences in last hour
- **Affected Users:** ~5% of requests
- **Recent Changes:** Deploy at 14:00 UTC
```

### 2. Categorize Error

```markdown
## Error Classification

**Type:** Runtime Error
**Category:** Null/Undefined Reference
**Severity:** High (user-facing)

### Common Causes
1. Missing data validation
2. Race condition
3. API contract change
4. Data migration issue
```

### 3. Root Cause Analysis

```markdown
## Root Cause Investigation

### Timeline
- 14:00 - Deploy to production
- 14:25 - First error reported
- 14:30 - Error rate increased

### Hypothesis 1: Deploy introduced bug
- Check: git diff between versions
- Result: New code path added

### Hypothesis 2: Data issue
- Check: Query for affected users
- Result: All have specific condition

### Root Cause
Deploy introduced code that assumes `user.profile` exists,
but 5% of users don't have profiles (legacy accounts).
```

### 4. Implement Fix

```markdown
## Fix Implementation

### Short-term (Hotfix)
```typescript
// Add null check
const userId = user?.profile?.id ?? user.id;
```

### Long-term
1. Add data validation at API boundary
2. Migrate legacy accounts
3. Add regression test
```

## Error Categories

### By Origin

| Category | Description | Example |
|----------|-------------|---------|
| Client | User/browser errors | Invalid input |
| Server | Application errors | Null reference |
| Infrastructure | System errors | Connection timeout |
| External | Third-party errors | API rate limit |

### By Severity

| Level | Impact | Response |
|-------|--------|----------|
| Critical | System down | Immediate |
| High | Major feature broken | Hours |
| Medium | Degraded experience | This sprint |
| Low | Minor inconvenience | Backlog |

## Stack Trace Analysis

### Reading Stack Traces

```markdown
## Stack Trace Components

```
Error: Connection refused        ← Error type and message
    at Database.connect          ← Where error was thrown
      (src/db/connection.ts:23)  ← File and line
    at async initialize          ← Call chain
      (src/server.ts:45)
    at async main                ← Entry point
      (src/index.ts:12)
```

### Key Questions
1. Where was the error thrown? (top of stack)
2. What called that code? (stack trace)
3. What was the input/state? (logs)
4. What changed recently? (git history)
```

### Common Patterns

```markdown
## Null Reference
```
TypeError: Cannot read property 'x' of undefined
```
**Check:** Variable existence, API response shape

## Connection Error
```
Error: ECONNREFUSED 127.0.0.1:5432
```
**Check:** Service running, network config, credentials

## Timeout
```
Error: Operation timed out after 30000ms
```
**Check:** Service health, query performance, network

## Memory
```
FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed
```
**Check:** Memory leaks, large data processing
```

## Log Analysis

### Correlation

```markdown
## Correlating Logs

### Using Request ID
```bash
grep "req-12345" application.log
```

### Timeline Reconstruction
```
14:30:00.123 [req-12345] User login started
14:30:00.456 [req-12345] Fetching user profile
14:30:00.789 [req-12345] ERROR: Profile not found
14:30:00.790 [req-12345] TypeError: Cannot read 'id'
```

### Pattern Identification
```bash
# Count error types
grep "ERROR" app.log | cut -d: -f2 | sort | uniq -c | sort -rn

# Find error spikes
grep "ERROR" app.log | cut -d' ' -f1 | uniq -c
```
```

## Resolution Tracking

### Fix Verification

```markdown
## Fix Verification Checklist

- [ ] Error no longer reproducible locally
- [ ] Unit test added for fix
- [ ] Integration test added
- [ ] Deployed to staging
- [ ] Verified in staging
- [ ] Deployed to production
- [ ] Monitoring error rate
- [ ] Error rate returned to baseline
```

### Post-mortem Template

```markdown
# Incident Post-mortem: [Title]

## Summary
Brief description of what happened.

## Timeline
- HH:MM - Event
- HH:MM - Detection
- HH:MM - Resolution

## Impact
- Users affected: X
- Duration: Y hours
- Revenue impact: $Z

## Root Cause
Detailed explanation.

## Resolution
What was done to fix it.

## Lessons Learned
1. What went well
2. What went poorly
3. Where we got lucky

## Action Items
- [ ] Prevent: [Action]
- [ ] Detect: [Action]
- [ ] Respond: [Action]
```
