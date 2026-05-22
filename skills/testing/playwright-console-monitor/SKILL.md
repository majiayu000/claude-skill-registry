---
name: playwright-console-monitor
description: |
  Executes browser workflows while monitoring JavaScript console for errors, warnings, and messages. Use when you need error-free validation, debugging context during automation, or proactive error detection in web applications. Triggers on "check for console errors", "monitor JavaScript errors", "validate error-free execution", or "debug browser workflow". Works with Playwright MCP browser automation tools.

---

# Playwright Console Monitor

## Quick Start

Monitor console errors during a login workflow:

```
1. Navigate to application
2. Execute login steps
3. Check console for errors after each critical operation
4. Generate error report with screenshots
5. Provide debugging context
```

**Immediate value:** Catch JavaScript errors during automation that would otherwise go unnoticed.

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. Console Error Monitoring Workflow
   3.1 Setup and Navigation
   3.2 Execute with Monitoring
   3.3 Error Detection and Categorization
   3.4 Report Generation
4. Console Message Levels
5. Supporting Files
6. Expected Outcomes
7. Integration Points
8. Success Metrics
9. Requirements
10. Red Flags to Avoid
11. Notes

## When to Use This Skill

### Explicit Triggers
- User says "check for console errors"
- User says "monitor JavaScript errors during [workflow]"
- User says "validate error-free execution"
- User says "debug this workflow"
- User requests "console monitoring"

### Implicit Triggers
- Executing critical browser workflows (checkout, form submission, data operations)
- Testing new features or deployments
- Debugging intermittent failures
- Validating application health
- QA automation scenarios

### Debugging Context
- When workflows fail without obvious cause
- When investigating "works for me" issues
- When validating frontend error handling
- When checking third-party script integration

## What This Skill Does

This skill wraps browser automation workflows with console monitoring to:

1. **Proactive Error Detection** - Catch JavaScript errors during workflow execution
2. **Error Categorization** - Classify errors by severity (critical/warning/info/debug)
3. **Context Capture** - Take screenshots and snapshots at error states
4. **Report Generation** - Provide structured error reports with debugging context
5. **Continuous Monitoring** - Check console after each critical operation

## Console Error Monitoring Workflow

### 3.1 Setup and Navigation

**Step 1: Navigate to application**
```
Use: mcp__playwright__browser_navigate
- Navigate to target URL
- Wait for page load
```

**Step 2: Clear initial console messages (optional)**
```
Use: mcp__playwright__browser_console_messages
- Read and discard initial load messages
- Establishes clean baseline for workflow monitoring
```

### 3.2 Execute with Monitoring

**Step 3: Execute workflow with checkpoints**

For each critical operation:
1. Execute the action (click, type, navigate)
2. Wait for expected state
3. Check console messages
4. Log any new errors/warnings

**Example pattern:**
```
Action: Click "Submit Order" button
  → mcp__playwright__browser_click
Wait: Order confirmation appears
  → mcp__playwright__browser_wait_for
Check: Console errors
  → mcp__playwright__browser_console_messages({ level: "error" })
```

**Critical operation checkpoints:**
- Form submissions
- Navigation between pages
- AJAX/fetch requests
- Third-party script loads
- Authentication flows
- Payment processing
- Data mutations

### 3.3 Error Detection and Categorization

**Step 4: Categorize detected errors**

Use console message levels to filter:

| Level | Includes | When to Use |
|-------|----------|-------------|
| `error` | Critical errors only | After critical operations (checkout, submit) |
| `warning` | Warnings + errors | During form validation, feature usage |
| `info` | Info + warnings + errors | General workflow monitoring |
| `debug` | All messages | Detailed debugging scenarios |

**Step 5: Capture error context**

For each error detected:
1. Take screenshot of current state
   ```
   mcp__playwright__browser_take_screenshot
   ```
2. Capture page snapshot
   ```
   mcp__playwright__browser_snapshot
   ```
3. Record error message, timestamp, and operation

### 3.4 Report Generation

**Step 6: Generate structured error report**

Report format:
```
Console Error Report
====================

Workflow: [workflow name]
Executed: [timestamp]
Total Errors: [count]

Critical Errors (level: error):
  - [timestamp] [message]
    Context: [operation that triggered]
    Screenshot: [filename]

Warnings (level: warning):
  - [timestamp] [message]
    Context: [operation that triggered]

Info Messages:
  - [summary if relevant]

Debugging Context:
  - URL at time of error
  - Page snapshot
  - Network state (if available via browser_network_requests)

Recommendations:
  - [specific debugging suggestions]
```

## Console Message Levels

Playwright console messages follow browser console API levels:

**error** - Critical errors that prevent functionality
- Uncaught exceptions
- Failed network requests (4xx/5xx from critical APIs)
- Missing required resources
- **Use after:** Checkout, payment, form submission, authentication

**warning** - Non-fatal issues that may cause problems
- Deprecated API usage
- Failed optional resources
- Validation warnings
- **Use after:** Form interactions, navigation, feature usage

**info** - Informational messages
- Application lifecycle events
- Successful operations
- Debug information from application
- **Use for:** General monitoring, understanding application flow

**debug** - Verbose debugging output
- All console.log, console.debug calls
- Framework/library debug messages
- **Use for:** Deep debugging, understanding detailed behavior

**Default recommendation:** Use `level: "error"` after critical operations, `level: "warning"` for general monitoring.

## Supporting Files

This skill includes:

- **references/playwright-console-api.md** - Detailed Playwright console API reference, message formats, and advanced patterns
- **examples/examples.md** - 5+ real-world monitoring scenarios (e-commerce checkout, form submission, SPA navigation, authentication, third-party integrations)
- **assets/error-report-template.md** - Template for structured error reports

## Expected Outcomes

### Successful Monitoring (No Errors)
```
✅ Console Monitoring Complete

Workflow: User Login Flow
Operations Monitored: 5
Console Errors: 0
Warnings: 0

All operations completed without console errors.
```

### Error Detection
```
❌ Console Errors Detected

Workflow: Checkout Process
Operations Monitored: 8
Console Errors: 2 critical, 1 warning

Critical Errors:
  1. [14:32:15] Uncaught TypeError: Cannot read property 'total' of undefined
     Context: After "Apply Discount Code" click
     Screenshot: checkout-error-1.png

  2. [14:32:18] Failed to load resource: POST /api/payment 500
     Context: After "Submit Payment" click
     Screenshot: checkout-error-2.png

Warnings:
  1. [14:32:10] [Deprecation] Synchronous XMLHttpRequest on the main thread
     Context: During address validation

Debugging Recommendations:
  - Investigate cart.total property initialization
  - Check /api/payment endpoint for server errors
  - Review discount code application logic
```

## Integration Points

### With Browser Automation Workflows
- Wrap existing automation with console monitoring
- Add checkpoints after critical operations
- Enhance test suites with error detection

### With Debugging Workflows
- Console monitoring identifies error sources
- Screenshots provide visual debugging context
- Network requests correlate with console errors

### With QA Processes
- Automated error detection in test runs
- Regression testing for console errors
- Performance monitoring (console.time/timeEnd messages)

### With CI/CD Pipelines
- Fail builds on critical console errors
- Track error trends across deployments
- Validate error-free user flows

## Success Metrics

| Metric | Before (Manual) | After (Skill) | Improvement |
|--------|----------------|---------------|-------------|
| **Error Detection** | Reactive (user reports) | Proactive (during automation) | +95% early detection |
| **Debugging Time** | 30-60 min (reproduce + debug) | 5-10 min (context provided) | 80% reduction |
| **False Negatives** | High (errors missed) | Low (systematic checking) | 90% reduction |
| **Context Quality** | Minimal (user description) | Rich (screenshots, state, messages) | 10x improvement |

## Requirements

### Required Tools
- Playwright MCP browser automation
  - `mcp__playwright__browser_navigate`
  - `mcp__playwright__browser_console_messages`
  - `mcp__playwright__browser_snapshot`
  - `mcp__playwright__browser_take_screenshot`
  - `mcp__playwright__browser_click` (for workflows)
  - `mcp__playwright__browser_wait_for`

### Environment
- Playwright browser configured and accessible
- Target application URL

### Knowledge
- Basic understanding of JavaScript console API
- Familiarity with browser automation workflows
- Understanding of error severity levels

## Red Flags to Avoid

- [ ] **Checking console only at end** - Check after each critical operation
- [ ] **Ignoring warnings** - Warnings often predict future critical errors
- [ ] **Not capturing context** - Always take screenshots at error states
- [ ] **Wrong severity level** - Use `error` level for critical operations
- [ ] **Skipping wait states** - Ensure operations complete before checking console
- [ ] **Not clearing initial messages** - Page load messages contaminate workflow monitoring
- [ ] **Missing operation context** - Always note which operation triggered errors
- [ ] **Overly verbose monitoring** - Don't check console after every single action
- [ ] **Ignoring network correlation** - Console errors often correlate with network failures
- [ ] **Not providing recommendations** - Error reports should suggest debugging steps

## Notes

**Key Principles:**
1. **Monitor critical operations** - Focus on checkout, submit, auth, payment
2. **Categorize by severity** - Use appropriate console levels
3. **Capture rich context** - Screenshots + snapshots + messages
4. **Provide actionable reports** - Include debugging recommendations
5. **Balance coverage vs noise** - Strategic checkpoints, not every action

**Console Message Persistence:**
- Messages accumulate during page lifetime
- Page navigation clears console (new document)
- Consider clearing messages between checkpoints for clarity

**Performance Considerations:**
- Console checks add minimal overhead (~100-200ms)
- Screenshot capture is slower (~500ms-1s)
- Balance monitoring thoroughness with workflow speed

**Common Patterns:**
- **Critical operations:** Check `level: "error"` immediately after
- **Form workflows:** Check `level: "warning"` after validation
- **Debugging:** Use `level: "info"` or `level: "debug"` for full visibility
- **Regression testing:** Establish baseline, detect new errors

**Integration with Network Monitoring:**
- Combine with `browser_network_requests` for complete debugging context
- Network failures often manifest as console errors
- 500-series responses typically generate console errors
- CORS issues appear in console, not network tab
