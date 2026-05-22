---
name: debugging
description: Troubleshoot and fix bugs systematically. Use when errors occur, tests fail, or unexpected behavior is observed. Covers root cause analysis and debugging strategies.
allowed-tools: Read, Bash, Glob, Grep, mcp__chrome-devtools__*
---

# Debugging and Troubleshooting

## MCP Tools

**Chrome DevTools** (frontend debugging):
- Capture console errors and network failures
- Set breakpoints and inspect state
- Profile performance bottlenecks
- Capture screenshots of error states

## Workflows

- [ ] **Reproduce**: Can you reliably reproduce the issue?
- [ ] **Isolate**: What is the minimal code that exhibits the bug?
- [ ] **Trace**: Use Grep to follow the call chain
- [ ] **Hypothesize**: What could cause this behavior?
- [ ] **Test**: Verify or disprove your hypothesis
- [ ] **Fix**: Implement the solution
- [ ] **Verify**: Confirm the fix and add regression test

## Debugging Strategy

### 1. Gather Information
- Read error messages and stack traces carefully
- Check logs for context around the error
- Identify when the issue started (recent changes?)
- **Use Grep** to locate related code around the error

### 2. Trace the Flow
- Use Grep to trace data flow through function calls
- Map the call chain from entry point to error
- Identify where data transforms unexpectedly

### 3. Reproduce Consistently
- Create a minimal test case
- Document exact steps to reproduce
- For frontend bugs, use Chrome DevTools to record network/console

### 4. Common Causes
- **Null/undefined**: Check for missing null checks
- **Off-by-one**: Verify loop boundaries and array indices
- **Async timing**: Check race conditions and await usage
- **State mutation**: Look for unexpected side effects
- **Type coercion**: Verify type handling (especially in JS/TS)

## Tools (Examples by Language)

```bash
# Check logs
tail -f /var/log/app.log

# Search for error patterns
grep -r "ERROR" ./logs/

# Debug Node.js
node --inspect-brk app.js

# Python debugging
python -m pdb script.py
```

## Frontend Debugging with Chrome DevTools

- Open DevTools → Console for errors
- Network tab for failed requests
- Sources tab for breakpoints
- Performance tab for slow operations

## Post-Fix Checklist

- [ ] Root cause identified and documented
- [ ] Regression test added
- [ ] Similar code checked (use Grep to locate)
- [ ] Fix reviewed by another developer
