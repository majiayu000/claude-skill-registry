---
name: browser-verification
description: Verify browser-based acceptance criteria using ExecuteAutomation Playwright MCP with multi-tool fallback chain. Invoked by verify-task and phase-checkpoint for BROWSER:* criteria.
---

# Browser Verification Skill

Verify UI-related acceptance criteria using MCP browser tooling with evidence
(snapshots, logs, or screenshots).

## Inputs

For each criterion, use metadata from `Verify:`:
- route (e.g., `/login`)
- selector (e.g., `[data-testid="login-form"]`)
- expected state (visible, text, attribute, etc.)
- optional actions (click, type, hover)
- optional viewport

## Workflow Overview

Copy this checklist and track progress:

```
Browser Verification Progress:
- [ ] Step 1: Load configuration
- [ ] Step 1.5: Resolve base URL (preview or localhost)
- [ ] Step 1.6: HTTP-first evaluation (skip browser if possible)
- [ ] Step 2: Select browser tool (with fallback chain)
- [ ] Step 3: Authenticate (if required)
- [ ] Step 4: Navigate and validate
- [ ] Step 5: Capture evidence
- [ ] Step 6: Handle errors and recover
- [ ] Step 7: Report results
```

## Step 1: Load Configuration

Read `.claude/verification-config.json` for:

**Dev Server:**
- `devServer.command`
- `devServer.url`
- `devServer.startupSeconds`

**Authentication:**
- `auth.strategy` — `none`, `env`, or `storage-state`
- `auth.loginRoute` — URL path for login form
- `auth.credentials.usernameVar` — Env var name for username
- `auth.credentials.passwordVar` — Env var name for password
- `auth.storageState` — Path to save/load session state

**Browser:**
- `browser.tool` — `auto`, `executeautomation`, `browsermcp`, `playwright`, `chromedevtools`
- `browser.headless` — Run headless (default: true)
- `browser.timeout` — Default timeout in ms (default: 30000)
- `browser.navigationTimeout` — Navigation timeout in ms (default: 60000)

**Deployment:**
- `deployment.enabled` — Whether to use preview deployments
- `deployment.useForBrowserVerification` — Use preview URL for browser tests
- `deployment.fallbackToLocal` — Fall back to localhost if no preview
- `deployment.waitForDeployment` — Wait for deployment to be ready
- `deployment.deploymentTimeout` — Max seconds to wait

If config is missing or incomplete, ask the human to run `/configure-verification`.

## Step 1.5: Resolve Base URL

Determine the base URL for browser verification based on deployment configuration.

### Decision Logic

```
IF deployment.enabled AND deployment.useForBrowserVerification:
  1. Invoke vercel-preview skill to get preview URL
  2. IF URL found:
       BASE_URL = preview URL
       Skip dev server startup (not needed)
       Log: "Using Vercel preview: {URL}"
  3. ELSE IF fallbackToLocal:
       BASE_URL = devServer.url
       Log: "WARNING: No preview URL found, falling back to localhost"
       Ensure dev server is running
  4. ELSE (no fallback):
       BLOCK with error: "No preview deployment and fallback disabled"
ELSE:
  BASE_URL = devServer.url (current behavior)
  Ensure dev server is running
```

### Preview URL Resolution

When deployment is enabled, invoke the vercel-preview skill:

1. Get current git branch
2. Query Vercel for ready deployments matching branch
3. If `waitForDeployment` enabled and deployment building, wait up to timeout
4. Return URL or null

### Output

```
BASE URL RESOLUTION
===================
Mode: Vercel Preview | Local Dev Server | Fallback to Local
URL: {resolved URL}
Branch: {git branch} (if preview)
Status: Ready | Building | Not Found (if preview)
```

### Using BASE_URL

All subsequent steps use `BASE_URL` instead of hardcoded `devServer.url`:

- Step 1.6 (HTTP-First): Use `BASE_URL` for curl checks
- Step 4 (Navigate): Navigate to `BASE_URL + route`
- Step 7 (Output): Report which URL was used
- Manual fallback instructions: Use `BASE_URL` in all generated URLs

**IMPORTANT:** When browser verification falls back to manual, all URLs in the
generated instructions MUST use BASE_URL. This ensures manual verification
guides point to the correct environment (preview URL when deployment enabled).

## Step 1.6: HTTP-First Evaluation

Before launching browser tools, evaluate if the criterion can be satisfied with HTTP.
This optimization skips browser overhead for criteria that don't require DOM inspection.

### Criteria Eligible for HTTP-First

| Criterion Pattern | HTTP Check | Skip Browser If... |
|-------------------|------------|-------------------|
| "Page loads at {url}" | `curl -sf {url}` | HTTP 200 returned |
| "API returns {status}" | `curl -o /dev/null -w "%{http_code}" {url}` | Status matches |
| "Endpoint responds with {data}" | `curl -s {url} \| jq/grep` | Data found |
| "Service health check" | `curl -sf {url}/health` | Health endpoint OK |
| "Redirect to {url}" | `curl -sI {url} \| grep Location` | Location header matches |

### HTTP-First Execution

```bash
# Generic page accessibility check
curl -sf "{BASE_URL}{route}" -o /dev/null && echo "HTTP_PASS" || echo "HTTP_FAIL"

# Response content check
curl -s "{BASE_URL}{route}" | grep -q "{expected_text}" && echo "HTTP_PASS" || echo "HTTP_FAIL"

# Status code check
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "{url}")
[ "$HTTP_CODE" = "{expected}" ] && echo "HTTP_PASS" || echo "HTTP_FAIL"
```

### Decision Logic

**If HTTP_PASS and criterion does NOT require:**
- Specific DOM element verification (`selector`, `data-testid`, `visible`)
- Visual appearance check (`screenshot`, `layout`, `style`)
- User interaction simulation (`click`, `type`, `hover`)
- Console log inspection (`console`, `errors`, `warnings`)
- Network timing analysis (`performance`, `timing`)

**Then:**
- Mark criterion as PASS
- Skip browser verification entirely
- Note method as "HTTP-first" in evidence
- Log: "Verified via HTTP (browser tools not required)"

**Otherwise:**
- Continue to Step 2 (browser tool selection)
- HTTP result can inform browser verification (e.g., server is reachable)

### HTTP-First Benefits

- **Speed:** curl is ~10x faster than browser launch
- **Reliability:** No browser MCP dependency issues
- **Simplicity:** Works even if no browser tools configured
- **Resources:** Lower memory and CPU usage

## Step 2: Tool Selection (Automatic with Fallback)

Automatically detect and use the best available browser tool. Try tools in
order until one responds:

```
1. ExecuteAutomation Playwright MCP (primary)
   - Package: @executeautomation/playwright-mcp-server
   - Test: Check for mcp__playwright__* or mcp__executeautomation__* tools
   - Why primary: Most stable, actively maintained (312+ commits), 143 device presets
   - Avoids @playwright/mcp@latest beta instability issues

2. Browser MCP (if extension installed)
   - Source: browsermcp.io browser extension
   - Test: Check for mcp__browsermcp__* tools
   - Advantage: Uses existing browser profile (stays logged in, avoids bot detection)
   - Requires: User has Browser MCP extension installed

3. Microsoft Playwright MCP (pinned version)
   - Package: @anthropic-ai/mcp-server-playwright (pinned, NOT @latest)
   - Test: Check for mcp__playwright__* tools (if not already found)
   - Why fallback: Official but @latest includes unstable betas
   - Use pinned version only

4. Chrome DevTools MCP (basic fallback)
   - Test: Call mcp__chrome-devtools__list_pages
   - Often pre-installed with Claude Code
   - Limited: Not designed for automation, less stable for complex workflows
   - Use for: Simple navigation, screenshots, basic interactions

5. Manual Verification (last resort) — SOFT BLOCK
   - If all tools fail, do NOT silently continue
   - Display warning and prompt user:
     ```
     ⚠️  NO BROWSER TOOLS AVAILABLE

     Attempted to detect browser MCP tools but none responded:
     - ExecuteAutomation Playwright: {status}
     - Browser MCP: {status}
     - Microsoft Playwright: {status}
     - Chrome DevTools: {status}

     Browser criteria cannot be verified automatically.

     Options:
     1. Continue anyway (criteria become manual verification)
     2. Stop and configure browser tools first

     To enable automated browser verification, add to ~/.mcp.json:
     {
       "mcpServers": {
         "executeautomation-playwright": {
           "command": "npx",
           "args": ["-y", "@executeautomation/playwright-mcp-server"]
         }
       }
     }
     ```
   - Use AskUserQuestion to let user choose:
     - "Continue with manual verification" → Mark criteria as BLOCKED, list for human
     - "Stop to configure tools" → Halt and provide detailed setup instructions
```

**Log tool selection:**
```
Browser Tool: ExecuteAutomation Playwright MCP (auto-detected)
Fallback chain: Browser MCP → Microsoft Playwright → Chrome DevTools → Manual (soft block)
```

## Step 3: Authentication

**Skip if `auth.strategy` is `none`.**

### Strategy: `storage-state`

1. Check if `auth.storageState` file exists and is recent (< 24h)
2. If exists, load session state into browser
3. Navigate to a protected route to verify session validity
4. If session invalid, proceed to login flow

### Strategy: `env` (or storage-state with invalid session)

1. Read credential env var names from config (NOT the values)
2. Navigate to `auth.loginRoute`
3. Identify login form fields (username/email, password)
4. Fill credentials using browser tool's form fill
   - Pass env var names to the tool, which reads values from environment
   - Agent NEVER sees plaintext credentials
5. Submit the form
6. Wait for successful login indicator (redirect, logged-in element)
7. Save session to `auth.storageState` for reuse

### Auth Failure Handling

If login fails after 2 attempts:
- Mark criteria as BLOCKED (not FAIL)
- Report: "Authentication failed. Check credentials in .env.verification"
- Do NOT expose credential values in error messages

## Step 4: Navigate and Validate

For each browser criterion:

1. Start from base URL (`BASE_URL` — preview or localhost per Step 1.5)
2. Navigate to the criterion's route
3. Wait for content to load:
   - Use wait-for-text or wait-for-selector
   - Respect `browser.navigationTimeout`
4. Perform optional actions in order (click, type, hover)
5. Validate expected state:
   - visibility
   - text content
   - attribute values
   - layout position
6. Capture console errors and network failures when relevant

## Step 5: Evidence Capture

Capture evidence appropriate to the criterion type using the selected browser MCP tool (not Bash commands):

| Type | Evidence |
|------|----------|
| DOM | Accessibility snapshot, selector details |
| VISUAL | Screenshot |
| CONSOLE | Console log excerpt |
| NETWORK | Request/response summary |
| PERFORMANCE | Timing metrics (if supported) |
| ACCESSIBILITY | ARIA/semantic checks and notes |

Save evidence under `.claude/verification/` with stable names:
- `browser-{task-id}-{criterion-id}.png`
- `browser-{task-id}-{criterion-id}.json`

## Step 6: Error Recovery

**Detect failures:**
- Tool returns "undefined" or "Error calling tool"
- Connection timeout
- Server not responding

**Recovery procedure:**

```
1. Log the error with context:
   "Tool {name} returned: {error}"

2. If transient error (timeout, connection):
   - Wait 2 seconds
   - Retry current operation (max 2 retries)

3. If persistent error or tool unavailable:
   - Attempt tool restart (kill and re-init MCP)
   - If restart succeeds, retry current criterion

4. If restart fails:
   - Try next tool in fallback chain
   - Log: "Switching from {current} to {fallback}"

5. If all tools exhausted:
   - Mark remaining criteria as BLOCKED
   - Report: "Browser tools unavailable after trying:
     - ExecuteAutomation Playwright: {error}
     - Browser MCP: {error or 'not installed'}
     - Microsoft Playwright: {error}
     - Chrome DevTools: {error}
     Manual verification required."
```

**Session degradation detection:**

Some tools work initially then fail after extended use. Monitor for:
- Increasing response times
- Intermittent "undefined" errors
- Loss of page state

If detected, proactively switch to fallback before complete failure.

## Step 7: Output Format

Return a structured result for each criterion:

```
BROWSER VERIFICATION RESULT
---------------------------
Instruction ID: [ID]
Status: PASS | FAIL | BLOCKED
Type: DOM | VISUAL | CONSOLE | NETWORK | PERFORMANCE | ACCESSIBILITY
Target: Vercel Preview (https://...) | Local Dev Server (http://localhost:...)
URL: [full URL tested] | Viewport: [width]x[height]

Finding: [What was observed]
Expected: [What was expected]

Evidence:
- {path}

Suggested Fix: [If FAIL]
```

## Failure Handling Summary

| Condition | Action | Status |
|-----------|--------|--------|
| Dev server unreachable | Report failing command | BLOCKED |
| Selector missing | Capture screenshot | FAIL |
| Auth fails | Check credentials | BLOCKED |
| Tool unavailable | Try fallback chain | Continue or BLOCKED |
| Tool returns undefined | Retry then switch | Continue or BLOCKED |
| All tools fail | Require manual verification | BLOCKED |

## Tool-Specific Notes

See [TOOL_NOTES.md](TOOL_NOTES.md) for detailed information on each browser MCP tool option:
- ExecuteAutomation Playwright MCP (recommended primary)
- Browser MCP (best for auth-heavy apps)
- Microsoft Playwright MCP (use pinned version)
- Chrome DevTools MCP (basic fallback)
- Browserbase + Stagehand (cloud option)
