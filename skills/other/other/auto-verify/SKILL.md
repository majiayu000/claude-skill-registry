---
name: auto-verify
description: Attempt automated verification of criteria before falling back to manual. Parses criterion text for automation hints and executes appropriate tool (curl, browser, file check). Invoked by verify-task and phase-checkpoint for MANUAL and MANUAL:DEFER criteria.
---

# Auto-Verify Skill

Attempt automated verification of criteria that would otherwise require manual review.
This skill parses criterion text for automation hints, checks tool availability, and
executes verification commands before marking items as truly manual.

## When This Skill Runs

- Invoked by `/verify-task` when processing MANUAL and MANUAL:DEFER type criteria
- Invoked by `/phase-checkpoint` for Manual Local Verification items
- Invoked by `code-verification` skill before browser fallback
- Invoked by `browser-verification` skill for HTTP-first optimization

## Workflow Overview

Copy this checklist and track progress:

```
Auto-Verify Progress:
- [ ] Step 1: Parse criterion for automation hints
- [ ] Step 2: Check tool availability
- [ ] Step 3: Select tool and generate command
- [ ] Step 4: Execute with timeout
- [ ] Step 5: Interpret result
- [ ] Step 6: Return structured output
```

## Step 1: Pattern Detection

Analyze criterion text and optional `Verify:` line for automation keywords.
Patterns are checked in priority order — first match wins.

### Pattern Matching

See [PATTERNS.md](PATTERNS.md) for the full pattern matching table and command templates.

Key pattern categories:
- HTTP patterns (curl): API endpoints, status codes, redirects, health checks
- Browser patterns: DOM elements, visual checks, console logs
- File patterns (bash): File/directory existence, content checks
- Environment patterns: Environment variable checks
- Truly manual: Subjective criteria (UX, brand, tone)

## Step 2: Tool Availability Check

### Always Available

These tools are always present and can be used without checking:

| Tool | Capabilities |
|------|--------------|
| **Bash** | curl, grep, jq, test, file operations, environment checks |
| **Read** | File content inspection |
| **Glob** | File pattern matching |
| **Grep** | Content search |

### Conditionally Available

Check availability before use:

| Tool | Check Method | Fallback |
|------|--------------|----------|
| ExecuteAutomation Playwright | `mcp__playwright__*` or `mcp__executeautomation__*` tools exist | Browser MCP |
| Browser MCP | `mcp__browsermcp__*` tools exist | Microsoft Playwright |
| Microsoft Playwright MCP | `mcp__playwright__*` tools exist | Chrome DevTools |
| Chrome DevTools MCP | `mcp__chrome-devtools__list_pages` responds | Manual |

### Availability Matrix

```
TOOL_AVAILABILITY = {
  "curl": ALWAYS,
  "bash": ALWAYS,
  "file_ops": ALWAYS,
  "browser": CHECK_REQUIRED
}
```

## Step 3: Command Generation

Based on detected pattern, generate the appropriate verification command.
See [PATTERNS.md](PATTERNS.md) for complete command templates.

**Quick reference:**
- HTTP patterns: Use curl for status, content, redirect, health checks
- File patterns: Use bash test/grep for existence and content checks
- Browser patterns: Delegate to browser-verification skill with fallback chain

## Step 4: Execution Protocol

### Timeouts

| Tool | Timeout | Rationale |
|------|---------|-----------|
| curl | 5 seconds | Network requests should be fast |
| bash (file ops) | 2 seconds | Local operations are quick |
| browser | 30 seconds | Page loading and interaction take time |

### Execution Steps

1. **Generate command** from detected pattern
2. **Set timeout** based on tool
3. **Execute via Bash tool** (for curl/bash patterns)
4. **Parse output** for PASS/FAIL prefix
5. **Capture full output** for evidence
6. **Handle errors** (timeout, connection refused, etc.)

### Error Handling

| Error Type | Action |
|------------|--------|
| Timeout | Mark as FAIL with "timeout after {N}s" |
| Connection refused | Mark as FAIL with "connection refused - is server running?" |
| Command not found | Mark as FAIL with "tool not available" |
| Unexpected output | Mark as FAIL with captured output |

## Step 5: Result Interpretation

Return a structured result for each criterion:

```
AUTO-VERIFY RESULT
------------------
Criterion: "{original criterion text}"
Pattern Detected: {pattern name or "none"}
Tool Used: {curl | bash | browser | none}
Command: {executed command or "N/A"}
Status: PASS | FAIL | MANUAL
Duration: {execution time in ms}
Output: {captured output, truncated if >500 chars}
Suggested Fix: {if FAIL, provide actionable suggestion}
Reason: {if MANUAL, explain why automation not possible}
```

### Status Definitions

| Status | Meaning | Next Action |
|--------|---------|-------------|
| **PASS** | Criterion verified automatically | No human review needed |
| **FAIL** | Automation attempted but failed | Show error, suggest fix, allow human override |
| **MANUAL** | No automation possible | List for human review with reason |

## Step 6: Integration Examples

### Example 1: API Endpoint Verification

**Input:**
```
Criterion: "POST /api/users returns 201 with user object"
Verify: POST /api/users with body {"name": "test"}
```

**Processing:**
1. Pattern detected: `API`, `returns`, `201` → curl pattern
2. Tool: curl (always available)
3. Command: `curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"name":"test"}' http://localhost:3000/api/users`
4. Execute: Returns "201"
5. Result: PASS

**Output:**
```
AUTO-VERIFY RESULT
------------------
Criterion: "POST /api/users returns 201 with user object"
Pattern Detected: API status code
Tool Used: curl
Command: curl -s -o /dev/null -w "%{http_code}" -X POST ...
Status: PASS
Duration: 234ms
Output: 201
```

### Example 2: Page Load Check

**Input:**
```
Criterion: "Dashboard page loads at /dashboard"
```

**Processing:**
1. Pattern detected: `page loads` → curl first (HTTP status sufficient)
2. Tool: curl
3. Command: `curl -sf http://localhost:3000/dashboard -o /dev/null`
4. Execute: Success (exit code 0)
5. Result: PASS (no browser needed)

**Output:**
```
AUTO-VERIFY RESULT
------------------
Criterion: "Dashboard page loads at /dashboard"
Pattern Detected: page accessibility
Tool Used: curl (HTTP-first)
Command: curl -sf http://localhost:3000/dashboard -o /dev/null
Status: PASS
Duration: 156ms
Output: HTTP 200 OK
```

### Example 3: Truly Manual Criterion

**Input:**
```
Criterion: "Copy matches brand tone and feels professional"
```

**Processing:**
1. Pattern detected: `feels`, `brand`, `tone` → truly manual
2. Tool: none
3. Result: MANUAL

**Output:**
```
AUTO-VERIFY RESULT
------------------
Criterion: "Copy matches brand tone and feels professional"
Pattern Detected: subjective judgment
Tool Used: none
Command: N/A
Status: MANUAL
Duration: 0ms
Output: N/A
Reason: Subjective criteria requiring human judgment (brand tone, professional feel)
```

### Example 4: Failed Automation

**Input:**
```
Criterion: "API returns list of users"
```

**Processing:**
1. Pattern detected: `API`, `returns` → curl pattern
2. Tool: curl
3. Command: `curl -sf http://localhost:3000/api/users`
4. Execute: Connection refused
5. Result: FAIL

**Output:**
```
AUTO-VERIFY RESULT
------------------
Criterion: "API returns list of users"
Pattern Detected: API response
Tool Used: curl
Command: curl -sf http://localhost:3000/api/users
Status: FAIL
Duration: 5012ms
Output: curl: (7) Failed to connect to localhost port 3000: Connection refused
Suggested Fix: Start the dev server with `npm run dev` or check if port 3000 is correct
```

## URL and Path Extraction

See [PATTERNS.md](PATTERNS.md) for URL and path extraction patterns.

## Configuration

This skill respects settings from `.claude/verification-config.json`:

```json
{
  "devServer": {
    "url": "http://localhost:3000"
  },
  "autoVerify": {
    "enabled": true,
    "httpTimeout": 5000,
    "fileTimeout": 2000,
    "browserTimeout": 30000,
    "httpFirst": true
  }
}
```

**URL resolution:** Use `devServer.url` for all HTTP checks. Ensure the dev server is running before verification.

If `autoVerify.enabled` is false, skip automation attempts and return MANUAL for all criteria.
