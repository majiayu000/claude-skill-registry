---
name: pm-verification-protocols
version: "1.0.0"
description: QA verification gate and evidence requirements
when_to_use: verification needed, QA delegation, evidence collection
category: pm-workflow
tags: [qa, verification, evidence, pm-required]
---

# QA Verification Gate Protocol

## 🔴 MANDATORY QA VERIFICATION GATE

**CRITICAL**: PM MUST delegate to QA BEFORE claiming work complete. NO completion claim without QA verification evidence.

### When QA Gate Applies

ALL implementation work:
- UI features
- Local server UI
- API endpoints
- Bug fixes
- Full-stack features
- Test modifications

### QA Gate Enforcement

**BLOCKING**: PM CANNOT claim "done/complete/ready/working/fixed" without QA evidence

**CORRECT SEQUENCE**:
```
Implementation
  → PM delegates to QA
  → PM WAITS for evidence
  → PM reports WITH QA verification
```

## Verification Requirements by Work Type

| Work Type | QA Agent | Required Evidence | Forbidden Claim |
|-----------|----------|-------------------|-----------------|
| **Local Server UI** | web-qa | Chrome DevTools MCP (navigate, snapshot, screenshot, console) | "Page loads correctly" |
| **Deployed Web UI** | web-qa | Playwright/Chrome DevTools (screenshots + console logs) | "UI works" |
| **API/Server** | api-qa | HTTP responses + logs | "API deployed" |
| **Database** | data-engineer | Schema queries + data samples | "DB ready" |
| **Local Backend** | local-ops | lsof + curl + pm2 status | "Running on localhost" |
| **CLI Tools** | Engineer/Ops | Command output + exit codes | "Tool installed" |

## Forbidden Phrases (CIRCUIT BREAKER VIOLATION)

**❌ NEVER say these without QA evidence:**
- "production-ready"
- "page loads correctly"
- "UI is working"
- "should work"
- "looks good"
- "seems fine"
- "it works"
- "all set"
- "ready for users"
- "deployment successful"

**✅ ALWAYS say this instead:**
```
"[Agent] verified with [tool/method]: [specific evidence]"
```

## Evidence Quality Standards

### Good Evidence

**Specific details**:
- File paths and line numbers
- URLs and endpoints tested
- HTTP status codes
- Test counts and pass/fail results
- Console log excerpts
- Screenshots with annotations

**Measurable outcomes**:
- "12 tests passed, 0 failed"
- "HTTP 200 OK response"
- "Server listening on port 3000"
- "No console errors found"

**Agent attribution**:
- "web-qa verified with Playwright"
- "api-qa tested endpoints"
- "local-ops confirmed process running"

**Reproducible steps**:
- "Navigate to /login, enter credentials, click submit"
- "curl http://localhost:3000/api/health"
- "lsof -i :3000 shows node process"

### Insufficient Evidence (VIOLATIONS)

**Vague claims**:
- "works"
- "looks good"
- "should be fine"

**No measurements**:
- "deployed successfully" (without health check)
- "UI updated" (without verification)

**PM assessment**:
- PM saying "I checked and it works"
- PM making claims without delegation

**Not reproducible**:
- "tested it" (no steps)
- "verified" (no method)

## Required Evidence by Claim Type

| Claim Type | Required Evidence | Example |
|------------|------------------|---------|
| **Implementation Complete** | • Engineer confirmation<br>• Files changed (paths)<br>• Git commit (hash/branch)<br>• Summary | `Engineer: Added OAuth2 auth. Files: src/auth/oauth2.js (new, 245 lines), src/routes/auth.js (+87). Commit: abc123.` |
| **Deployed Successfully** | • Ops confirmation<br>• Live URL<br>• Health check (HTTP status)<br>• Deployment logs<br>• Process status | `Ops: Deployed to https://app.example.com. Health: HTTP 200. Logs: Server listening on :3000. Process: lsof shows node listening.` |
| **Bug Fixed** | • QA bug reproduction (before)<br>• Engineer fix (files changed)<br>• QA verification (after)<br>• Regression tests | `QA: Bug reproduced (HTTP 401). Engineer: Fixed session.js (+12-8). QA: Now HTTP 200, 24 tests passed.` |

## Browser State Verification (MANDATORY)

**CRITICAL RULE**: PM MUST NOT assert browser/UI state without Chrome DevTools MCP evidence.

When verifying local server UI or browser state, PM MUST:
1. Delegate to web-qa agent
2. web-qa MUST use Chrome DevTools MCP tools (NOT assumptions)
3. Collect actual evidence (snapshots, screenshots, console logs)

### Chrome DevTools MCP Tools (via web-qa only)

Available tools:
- `mcp__chrome-devtools__navigate_page` - Navigate to URL
- `mcp__chrome-devtools__take_snapshot` - Get page content/DOM state
- `mcp__chrome-devtools__take_screenshot` - Visual verification
- `mcp__chrome-devtools__list_console_messages` - Check for errors
- `mcp__chrome-devtools__list_network_requests` - Verify API calls

### Required Evidence for UI Verification

✅ **CORRECT**: web-qa verified with Chrome DevTools:
```
- navigate_page: http://localhost:3000 → HTTP 200
- take_snapshot: Page shows login form with email/password fields
- take_screenshot: [screenshot shows rendered UI]
- list_console_messages: No errors found
- list_network_requests: GET /api/config → 200 OK
```

❌ **WRONG**: "The page loads correctly at localhost:3000"
(No Chrome DevTools evidence - CIRCUIT BREAKER VIOLATION)

### Local Server UI Verification Template

```
Task:
  agent: "web-qa"
  task: "Verify local server UI at http://localhost:3000"
  acceptance_criteria:
    - Navigate to page (mcp__chrome-devtools__navigate_page)
    - Take page snapshot (mcp__chrome-devtools__take_snapshot)
    - Take screenshot (mcp__chrome-devtools__take_screenshot)
    - Check console for errors (mcp__chrome-devtools__list_console_messages)
    - Verify network requests (mcp__chrome-devtools__list_network_requests)
```

## Example Good Report

```
Work complete: User authentication feature implemented

Implementation: Engineer added OAuth2 authentication using Auth0.
Changed files: src/auth.js, src/routes/auth.js, src/middleware/session.js
Commit: abc123

Deployment: Ops deployed to https://app.example.com
Health check: HTTP 200 OK, Server logs show successful startup

Testing: QA verified end-to-end authentication flow
- Login with email/password: PASSED
- OAuth2 token management: PASSED
- Session persistence: PASSED
- Logout functionality: PASSED

All acceptance criteria met. Feature is ready for users.
```

## Circuit Breaker Enforcement

**Circuit Breaker #8**: QA Verification Gate
- **Trigger**: PM claims completion without QA delegation
- **Action**: BLOCK - Delegate to QA now
- **Enforcement Levels**:
  - Violation #1: ⚠️ WARNING - Must delegate immediately
  - Violation #2: 🚨 ESCALATION - Session flagged for review
  - Violation #3: ❌ FAILURE - Session non-compliant
