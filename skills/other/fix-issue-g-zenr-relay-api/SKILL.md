---
name: fix-issue
description: Investigate and fix a bug from a report, traceback, log, or unexpected behavior
disable-model-invocation: true
---

Investigate and fix: $ARGUMENTS

## Step 1 — Gather Evidence
- Read the full error traceback, log output, or bug report
- Identify the exception type, message, file, and line number
- Note any relevant request data, state, or configuration
- Check if a test already covers this case

## Step 2 — Reproduce
Write a minimal test that triggers the error:
```
// Write a test that triggers the error
test_reproduces_issue(client) {
    resp = client.<METHOD>("<path>", ...)
    // This should reproduce the error — verify it fails
}
```
Run it to confirm it fails.

## Step 3 — Diagnose
Trace the error through the architecture layers (see Layers in project config):
1. **API layer** — Route handler, request parsing, DI
2. **Dependencies** — Auth chain, service injection
3. **Service layer** — Business logic, thread safety
4. **Core layer** — External resource communication, protocol
5. **Config** — Settings, environment variables

For each layer, ask:
- Is the input valid at this point?
- Is the exception caught or propagated correctly?
- Is thread safety maintained?
- Is the state consistent?

### Common root causes:
- **Resource errors**: External resource not open, invalid identifier
- **Auth errors**: API key misconfigured, missing timing-safe comparison
- **State errors**: State dict out of sync with actual resource state
- **Thread errors**: Lock not held during resource access
- **Config errors**: Env var not set or wrong type

## Step 4 — Fix
- Fix in the correct layer (core → service → API)
- Use typed exceptions, not generic `Exception`
- Maintain thread safety if touching service layer
- Rollback semantics if touching multi-entity operations

## Step 5 — Verify
- The reproduction test MUST now pass
- Run the test command and the type-check command (see project config)

## Step 6 — Audit
- Are there similar patterns elsewhere that have the same bug?
- Does the fix maintain backwards compatibility?
- If the root cause was non-obvious, add a code comment explaining why
- If the issue could recur, suggest a preventive measure