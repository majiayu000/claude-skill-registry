---
name: console-debugging
description: Use when debugging JavaScript errors, checking console warnings, analyzing browser logs, finding runtime errors, investigating console output, or troubleshooting browser issues. Provides console message analysis.
---

# Console Debugging Skill

Systematic approach to analyzing browser console messages using Chrome DevTools MCP.

## Console Message Categories

### Error Messages (Highest Priority)

| Type | Example | Typical Cause |
|------|---------|---------------|
| JavaScript Error | `Uncaught TypeError: Cannot read property 'x' of undefined` | Null reference |
| Network Error | `Failed to load resource: net::ERR_CONNECTION_REFUSED` | API unavailable |
| CORS Error | `Access-Control-Allow-Origin` | Backend configuration |
| CSP Error | `Content Security Policy` | Security restriction |
| Syntax Error | `SyntaxError: Unexpected token` | Invalid JavaScript |
| Reference Error | `ReferenceError: x is not defined` | Undefined variable |

### Warning Messages (Medium Priority)

| Type | Example | Action |
|------|---------|--------|
| Deprecation | `'componentWillMount' is deprecated` | Plan migration |
| Performance | `Long task took 200ms` | Optimize |
| Security | `Insecure form submission` | Fix HTTPS |
| Mixed Content | `Mixed Content: loading HTTP on HTTPS` | Update resource URLs |

### Info/Log Messages (Context)

| Type | Purpose |
|------|---------|
| Debug output | Developer console.log statements |
| Library info | Framework initialization messages |
| Analytics | Tracking events |
| State changes | Application state updates |

## Analysis Workflow

### 1. Collect Console Messages

Use Chrome DevTools MCP to list all console messages:

```
Tool: mcp__chrome-devtools__list_console_messages
Parameters: { "level": "error" }  // or "warning", "info", "debug"
```

### 2. Filter by Severity

Start with errors, then warnings:

1. **Errors first** - These break functionality
2. **Warnings second** - These indicate problems
3. **Info last** - These provide context

### 3. Group by Source

Categorize errors by their origin:

- **Application code** - Your own JavaScript
- **Third-party libraries** - External dependencies
- **Browser/extension** - Not your code
- **Network** - API/resource failures

### 4. Stack Trace Analysis

For JavaScript errors, analyze the stack trace:

```
Error: Cannot read property 'id' of undefined
    at UserComponent.render (UserComponent.js:45)
    at processChild (react-dom.js:1234)
    at reconcileChildren (react-dom.js:5678)
```

- **First line**: Error type and message
- **Second line**: Where error occurred (your code)
- **Following lines**: Call stack (often framework code)

### 5. Timing Correlation

Note when errors occur:

- On page load?
- After user action?
- After API response?
- Periodically (interval/timeout)?

## Common JavaScript Errors Reference

### TypeError

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot read property 'x' of undefined` | Accessing property on undefined | Add null check |
| `Cannot read property 'x' of null` | Accessing property on null | Add null check |
| `x is not a function` | Calling non-function as function | Check variable type |
| `Cannot set property 'x' of undefined` | Setting property on undefined | Initialize object first |

### ReferenceError

| Error | Cause | Fix |
|-------|-------|-----|
| `x is not defined` | Using undefined variable | Declare variable or check spelling |
| `Cannot access 'x' before initialization` | Temporal dead zone (let/const) | Move declaration above usage |

### SyntaxError

| Error | Cause | Fix |
|-------|-------|-----|
| `Unexpected token` | Invalid syntax | Check for missing brackets/quotes |
| `Unexpected identifier` | Missing operator or keyword | Review line for typos |

### NetworkError

| Error | Cause | Fix |
|-------|-------|-----|
| `net::ERR_CONNECTION_REFUSED` | Server not running | Start server or check URL |
| `net::ERR_NAME_NOT_RESOLVED` | DNS failure | Check domain spelling |
| `net::ERR_CERT_AUTHORITY_INVALID` | SSL certificate issue | Fix certificate or bypass in dev |

## Error Prioritization Matrix

| Severity | Impact | Action Required |
|----------|--------|-----------------|
| **Critical** | App crashes, data loss | Immediate fix |
| **High** | Feature broken | Fix before release |
| **Medium** | Degraded experience | Fix in next sprint |
| **Low** | Cosmetic issue | Track for later |

## Debugging Report Template

```markdown
## Console Debugging Report

**URL**: [page URL]
**Date**: [timestamp]
**Browser**: [browser version]

### Summary

- Total Errors: X
- Total Warnings: Y
- Critical Issues: Z

### Critical Errors

| Error | Location | Frequency | Impact |
|-------|----------|-----------|--------|
| [error message] | [file:line] | [count] | [description] |

### Stack Trace Analysis

#### Error 1: [title]

**Message**: [full error message]

**Stack Trace**:
```
[stack trace]
```

**Root Cause**: [analysis]

**Suggested Fix**: [recommendation]

### Warnings to Address

| Warning | Source | Recommendation |
|---------|--------|----------------|
| [warning] | [source] | [action] |

### Next Steps

1. [prioritized action 1]
2. [prioritized action 2]
```

## Integration with Network Inspection

Console errors often correlate with network issues:

1. **Failed API call** -> Console shows error about missing data
2. **CORS blocked** -> Console shows CORS error + network 0 status
3. **JSON parse error** -> Network returned invalid JSON

Use `network-inspection` skill alongside for comprehensive debugging.

## Best Practices

1. **Reproduce consistently** - Ensure error can be triggered reliably
2. **Document exact steps** - Note what user action causes the error
3. **Capture timestamps** - When did the error first appear?
4. **Check multiple browsers** - Is it browser-specific?
5. **Review recent changes** - What changed before error started?
