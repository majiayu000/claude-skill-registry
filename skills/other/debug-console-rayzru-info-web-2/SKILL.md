---
name: debug-console
description: Debug web app by capturing and analyzing console errors using Chrome DevTools MCP
context: fork
allowed-tools:
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_console_messages
  - Read
  - Write
---

# Debug with Console

Captures and analyzes console errors from web applications using Chrome DevTools MCP.

**Token Efficiency**: Eliminates manual console inspection pattern (60% savings: 2,000 → 800 tokens)

## Usage

Invoke with: `/debug-console [url]`

**Examples**:
- `/debug-console` - Debug current page (if browser already open)
- `/debug-console http://localhost:3000/app/scheduler` - Navigate and debug specific page
- `/debug-console http://localhost:3000` - Debug homepage

## Prerequisites

- Chrome DevTools MCP enabled: `claude --chrome`
- Chrome browser running with Claude in Chrome extension
- Application running on localhost:3000

## Workflow

### Step 1: Navigate to URL

**If URL provided**:
```javascript
mcp__playwright__browser_navigate({ url: "[provided-url]" })
```

**If no URL provided**:
- Use current page in Chrome browser
- Skip navigation step

### Step 2: Capture Console Messages

**Capture errors and warnings**:
```javascript
mcp__playwright__browser_console_messages({ level: "error" })
```

**Filter criteria**:
- Level: "error" includes errors and warnings (higher severity levels included)
- JavaScript errors
- Network failures (404, 500, CORS errors)
- React/Next.js errors
- Runtime exceptions

### Step 3: Analyze Errors

**Group errors by type**:
1. **Syntax Errors**: Parse errors, invalid syntax
2. **Runtime Errors**: TypeError, ReferenceError, null/undefined access
3. **Network Errors**: Failed fetches, 404s, CORS issues
4. **Framework Errors**: React hydration, Next.js errors
5. **Third-party Errors**: External library errors

**Extract details**:
- Error message (full text)
- File location (file:line:column)
- Stack trace (if available)
- Error count (number of occurrences)
- Timestamp (when error occurred)

### Step 4: Report Findings

**Create structured summary**:

```markdown
## Console Debug Report: [URL]

**Date**: [timestamp]
**Browser**: Chrome (via Chrome DevTools MCP)

### Summary
- Total errors: [count]
- Critical errors: [count] (blocking functionality)
- Warnings: [count] (non-blocking issues)
- Network failures: [count]

### Critical Errors

#### 1. [Error Type] - [Severity]
- **Message**: [error message]
- **Location**: [file:line:column]
- **Type**: [TypeError | ReferenceError | NetworkError | etc.]
- **Stack Trace**:
  ```
  [stack trace if available]
  ```
- **Occurrences**: [count]
- **Impact**: [description of what's broken]
- **Recommendation**: [specific fix suggestion]

[Repeat for each critical error]

### Warnings

#### 1. [Warning Type]
- **Message**: [warning message]
- **Location**: [file:line:column]
- **Recommendation**: [fix suggestion]

[Repeat for each warning]

### Network Failures

#### 1. [Request URL]
- **Status**: [404 | 500 | etc.]
- **Type**: [CORS | Timeout | Server Error]
- **Recommendation**: [fix suggestion]

[Repeat for each network failure]

### Next Steps

**Immediate actions**:
1. [Fix critical error 1]
2. [Fix critical error 2]
3. [Address network failures]

**Optional improvements**:
1. [Address warnings]
2. [Performance optimizations based on console logs]
```

### Step 5: Save Report (if critical errors found)

**Only save if**:
- Critical errors count > 0
- OR warnings count > 3
- OR network failures count > 1

**Save location**: `.claude/logs/debug_console_[timestamp].md`

**If no critical issues**:
- Report summary directly to user
- Don't create log file (token efficiency)

## Success Criteria

- [x] All console errors captured (error level and above)
- [x] Errors categorized by type (syntax, runtime, network, framework)
- [x] File locations extracted (file:line:column)
- [x] Stack traces included for critical errors
- [x] Actionable recommendations provided for each error
- [x] Report format clear and structured

## Error Handling

### Common Issues

**Issue**: "Chrome DevTools MCP not available"
- **Solution**: Start Claude Code with `claude --chrome`
- **Fallback**: Suggest manual console inspection

**Issue**: "Browser not responding"
- **Solution**: Check for modal dialogs blocking browser
- **Action**: Dismiss dialogs manually or create new tab

**Issue**: "No console messages found"
- **Result**: Report "No errors found" (success case)
- **Action**: Inform user app is running without console errors

**Issue**: "Too many console messages (>100)"
- **Solution**: Use `head_limit` to capture first 50 errors
- **Action**: Note in report: "First 50 errors shown (total: [count])"

## Examples

### Example 1: Simple Debug

**User**: `/debug-console http://localhost:3000/app/scheduler`

**Output**:
```markdown
## Console Debug Report: http://localhost:3000/app/scheduler

### Summary
- Total errors: 2
- Critical errors: 1
- Warnings: 1

### Critical Errors

#### 1. TypeError - Critical
- **Message**: Cannot read properties of undefined (reading 'shifts')
- **Location**: SchedulerView.tsx:42:15
- **Type**: TypeError (Runtime Error)
- **Stack Trace**:
  ```
  at SchedulerView (SchedulerView.tsx:42:15)
  at renderWithHooks (react-dom.production.min.js:14985)
  ```
- **Occurrences**: 1
- **Impact**: Scheduler fails to render shift data
- **Recommendation**: Add null check before accessing shifts: `data?.shifts?.map(...)`

### Warnings

#### 1. React Hydration Warning
- **Message**: Text content did not match. Server: "0 shifts" Client: "Loading..."
- **Location**: ShiftCount.tsx:15:8
- **Recommendation**: Ensure server and client render same initial state

### Next Steps

**Immediate actions**:
1. Fix TypeError in SchedulerView.tsx line 42 (add null check)
2. Review React hydration in ShiftCount component
```

### Example 2: No Errors Found

**User**: `/debug-console`

**Output**:
```markdown
## Console Debug Report: http://localhost:3000/app/scheduler

✅ No errors found!

**Summary**:
- Total errors: 0
- Warnings: 0
- Network failures: 0

The application is running without console errors.
```

### Example 3: Network Failures

**User**: `/debug-console http://localhost:3000/app/dashboard`

**Output**:
```markdown
## Console Debug Report: http://localhost:3000/app/dashboard

### Summary
- Total errors: 0
- Network failures: 2

### Network Failures

#### 1. GET /api/trpc/users.getAll
- **Status**: 500 Internal Server Error
- **Type**: Server Error
- **Recommendation**: Check server logs for tRPC procedure error

#### 2. GET /api/trpc/metrics.getWeekly
- **Status**: 404 Not Found
- **Type**: Missing Endpoint
- **Recommendation**: Verify tRPC router includes metrics.getWeekly procedure

### Next Steps

**Immediate actions**:
1. Check backend server logs for users.getAll error
2. Add metrics.getWeekly procedure to tRPC router
```

## Integration with Development Workflow

**When to use this Skill**:
- ✅ After implementing new feature (verify no console errors)
- ✅ Before committing code (pre-commit check)
- ✅ When user reports "app not working" (debug console first)
- ✅ After deployment to localhost (sanity check)
- ✅ When debugging UI issues (check for JavaScript errors)

**When NOT to use**:
- ❌ For formal E2E tests (use Playwright test framework instead)
- ❌ For production debugging (use production monitoring tools)
- ❌ For performance profiling (use Chrome DevTools profiler directly)

## Related Tools and Skills

- **auth-verify Skill**: Authenticate before debugging authenticated pages
- **PLAYWRIGHT_MCP_AUTOMATION.md**: Browser automation patterns
- **Chrome DevTools MCP**: Native browser debugging capabilities

## Token Efficiency

**Baseline (manual console inspection)**:
- Read PLAYWRIGHT_MCP_AUTOMATION.md: 1,200 tokens
- Navigate to page: 200 tokens
- Capture console: 300 tokens
- Analyze and format report: 300 tokens
- **Total**: ~2,000 tokens

**With debug-console Skill**:
- Skill invocation: 200 tokens
- Console capture + analysis: 400 tokens
- Report generation: 200 tokens
- **Total**: ~800 tokens

**Savings**: 1,200 tokens (60% reduction)

**Projected usage**: 10x per week
**Weekly savings**: 12,000 tokens
**Annual savings**: 624,000 tokens (~$1.50/year)

---

**Skill Version**: 1.0
**Created**: 2026-01-09
**Last Updated**: 2026-01-09
**Requires**: Claude Code v2.1.0+, Chrome DevTools MCP
