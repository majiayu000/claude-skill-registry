---
name: code-verification
description: Multi-agent code verification workflow using a main agent and sub-agent loop. Use when verifying code against requirements, acceptance criteria, or quality standards. Triggers on requests to verify, validate, or check code against specifications, checklists, or instructions.
---

# Code Verification Skill

Verify code against requirements using a main agent / sub-agent loop with structured feedback and automatic retry.

## Workflow Overview

Copy this checklist and track progress:

```
Code Verification Progress:
- [ ] Step 1: Parse verification instructions
- [ ] Step 2: Pre-flight validation
- [ ] Step 3: Verification loop (per instruction)
- [ ] Step 4: Fix attempts (if failed)
- [ ] Step 5: Update checklist with results
- [ ] Step 6: Generate verification report
- [ ] Step 7: Log results to verification-log.jsonl
```

## Step 1: Parse Verification Instructions

Extract each verification instruction into a discrete, testable item:

- **ID**: Unique identifier (e.g., `V-001`)
- **Instruction**: The requirement text
- **Test approach**: How to verify (file inspection, run tests, lint, type check, etc.)
- **Files involved**: Which files to examine
- **Requires Browser**: Whether the instruction needs Playwright MCP verification
  - Auto-detect from keywords: UI, render, display, visible, hidden, show, hide, click, hover, focus, blur, scroll, DOM, element, component, layout, responsive, style, CSS, color, font, screenshot, visual, appearance, console, error, warning, log, network, request, response, accessibility, a11y, ARIA, animation, transition, loading, performance
  - Mark as: `browser: true` or `browser: false`
- **Browser Verification Type** (if `browser: true`):
  - `DOM_INSPECTION` - Element presence, visibility, content via accessibility tree snapshots
  - `SCREENSHOT` - Visual appearance, layout verification
  - `CONSOLE` - Browser console errors, warnings, logs
  - `NETWORK` - API requests, responses, status codes (via network interception)
  - `PERFORMANCE` - Load times, Core Web Vitals (via tracing)
  - `ACCESSIBILITY` - ARIA attributes, semantic HTML, accessibility tree analysis

## Step 2: Pre-flight Validation

Before the verification loop, confirm each instruction is testable:

- Instruction is specific and unambiguous
- Success criteria are clear
- Required files/resources exist

Flag untestable instructions immediately rather than attempting verification.

### Browser-Specific Pre-Flight

For instructions with `browser: true`:

1. **HTTP-First Check (before browser tools)**

   Many "browser" criteria can be satisfied with a simple HTTP check. Before
   launching browser tools, evaluate if the criterion only requires:
   - Page accessibility (HTTP 200 status)
   - API response validation
   - Redirect verification
   - Basic content presence

   **Attempt HTTP verification first using curl:**
   ```bash
   # Page loads check
   curl -sf "{devServer.url}{route}" -o /dev/null && echo "PASS" || echo "FAIL"

   # Response contains text
   curl -s "{url}" | grep -q "{expected}" && echo "PASS" || echo "FAIL"

   # API returns expected status
   curl -sf -o /dev/null -w "%{http_code}" "{url}"
   ```

   **Curl error handling:**
   - Use `-m 10` (10-second timeout) to prevent hanging on unresponsive services
   - If curl returns exit code 7 (connection refused): dev server may not be running
   - If curl returns exit code 28 (timeout): service is slow or unreachable
   - On any curl failure, fall through to browser verification (do not mark as FAIL yet)

   **If HTTP check passes AND criterion does NOT explicitly require:**
   - DOM element inspection (selector, visibility)
   - Visual appearance verification
   - User interaction simulation
   - Console log inspection
   - Network timing/performance

   **Then:** Mark as PASS (HTTP-first), skip browser verification.

   **Otherwise:** Continue to browser tool fallback chain.

2. **Check browser tool availability (fallback chain)**
   - Try tools in order: ExecuteAutomation Playwright → Browser MCP → Microsoft Playwright → Chrome DevTools
   - Use first available tool for browser verification

   **If NO tools available (SOFT BLOCK):**

   Before marking as BLOCKED, attempt HTTP fallback for any remaining criteria.
   **EXECUTE these commands** via Bash tool (substitute actual URLs):
   - Page loading: `curl -sf {url}`
   - API responses: `curl -s {url} | jq .`
   - Redirects: `curl -sI {url}`

   Only mark as BLOCKED if both browser tools AND HTTP fallback are insufficient.

   If still blocked after HTTP fallback:
   - Display warning:
     ```
     ⚠️  NO BROWSER TOOLS AVAILABLE

     This verification includes browser-based criteria but no browser
     MCP tools are available, and HTTP fallback is insufficient.

     Criteria requiring DOM/visual inspection:
     - {list criteria that truly need browser}

     Options:
     1. Continue anyway (these criteria become manual verification)
     2. Stop and configure browser tools first
     ```
   - Use AskUserQuestion to let user choose:
     - "Continue with manual verification" → Mark browser instructions as BLOCKED, continue with non-browser criteria
     - "Stop to configure tools" → Halt verification, provide setup instructions

2. **Verify dev server is running** (if browser tools available)
   - Check if configured dev server URL responds (e.g., `http://localhost:3000`)
   - If not running, attempt to start using the configured dev server command
   - Wait for configured startup time before proceeding
   - If unable to start, mark as BLOCKED: "Dev server not accessible at {URL}"

3. **Confirm target route exists** (if browser tools available)
   - Navigate to the page specified in the instruction using the selected browser tool
   - If 404 or error, mark as BLOCKED: "Target route not found: {route}"

## Step 3: Sub-Agent Verification Protocol

Spawn a sub-agent to verify each instruction. The sub-agent MUST return structured output:

```
VERIFICATION RESULT
-------------------
Instruction ID: [ID]
Status: PASS | FAIL | BLOCKED
Location: [file:line or "N/A"]
Severity: BLOCKING | MINOR
Finding: [What was found]
Expected: [What was expected]
Suggested Fix: [Specific fix recommendation]
```

Sub-agent rules:
- Check ONLY the specific instruction assigned
- Do not attempt fixes—report findings only
- Be precise about location (file, line number, function name)
- Distinguish between blocking failures and minor issues

### Browser-Enhanced Verification Output

For instructions with `browser: true`, the sub-agent MUST use Playwright MCP and return:

```
BROWSER VERIFICATION RESULT
---------------------------
Instruction ID: [ID]
Status: PASS | FAIL | BLOCKED
Type: DOM | VISUAL | CONSOLE | NETWORK | PERFORMANCE | ACCESSIBILITY
URL: [URL] | Viewport: [width]x[height]

Finding: [What was observed]
Expected: [What was expected]

Details: [Type-specific information]
  - DOM: selector, found, visible, content
  - Visual: screenshot path, description
  - Console: errors, warnings, logs
  - Network: endpoint, method, status, response summary
  - Performance: load time, LCP, FID, CLS
  - Accessibility: ARIA, semantic HTML, contrast, keyboard nav

Suggested Fix: [Specific fix recommendation]
```

#### Browser Sub-Agent Rules

In addition to standard sub-agent rules, browser verification sub-agents MUST:
- Start with an accessibility tree snapshot (`browser_snapshot`) of the initial state
- Use stable selectors (prefer `data-testid` over complex CSS paths, or use accessibility tree element refs)
- Wait for dynamic content to load before inspecting (`browser_wait_for_text` or `browser_wait`)
- Capture console output before and after actions
- Take screenshots (`browser_screenshot`) when verifying visual appearance
- Test at default viewport unless criterion specifies responsive/mobile (use `browser_resize` to change)

## Step 4: Main Agent Fix Protocol

When sub-agent reports FAIL:

1. **Review the finding** - Understand what failed and why
2. **Check fix history** - Do not repeat a previously attempted fix
3. **Apply targeted fix** - Make the minimum change to address the issue
4. **Log the attempt** - Record what was changed

### Fix attempt tracking

Maintain a fix log per instruction:

```
FIX LOG: [Instruction ID]
--------------------------
Attempt 1: [Description of change] → [Result]
Attempt 2: [Description of change] → [Result]
...
```

### Strategy escalation

- Attempts 1-2: Direct fix based on sub-agent suggestion
- Attempt 3: Try alternative approach
- Attempts 4-5: Broaden scope, consider architectural changes

If the same failure pattern repeats twice, explicitly try a different strategy.

**After applying fix, re-verify the specific criterion:**
1. Re-run the sub-agent check for the failed criterion only
2. If still failing after 2 fix attempts, mark as FAIL with evidence from both attempts
3. Do NOT re-run all criteria — only the failing one

### Browser-Specific Fix Strategies

| Failure Type | Common Fixes |
|--------------|--------------|
| **DOM/Visibility** | Conditional rendering, CSS display/visibility, z-index, prop passing |
| **Console errors** | JS exceptions, missing mocks, env vars, CORS |
| **Network** | Endpoint URLs, auth headers, payload format, CORS config |
| **Visual** | CSS cascade, responsive breakpoints, font loading |
| **Performance** | Bundle size, image optimization, lazy loading, render-blocking |
| **Accessibility** | ARIA attributes, color contrast, heading hierarchy, keyboard handlers |

## Step 5: Exit Conditions

Exit the verification loop when ANY condition is met:

| Condition | Action |
|-----------|--------|
| Sub-agent reports PASS | ✅ Check off instruction |
| 5 attempts exhausted | ❌ Mark failed with notes |
| Same failure 3+ times | ⚠️ Exit early, flag for review |
| Fix introduces regression | ⚠️ Revert, flag for review |
| Issue is MINOR severity | ⚠️ Note and continue |

## Step 6: Regression Check

After each fix attempt, verify:

- The targeted instruction (primary check)
- Any previously-passing related instructions (regression check)

If a fix breaks something else, revert and note the conflict.

### Browser Regression Checks

After each browser-related fix, verify no regressions in: console errors, visual appearance, performance metrics, accessibility. If regression detected, capture before/after state and log in fix history.

## Step 7: Generate Verification Report

After all instructions are processed:

```
VERIFICATION REPORT
===================
Total Instructions: [N]
Passed: [N] ✅
Failed: [N] ❌
Needs Review: [N] ⚠️

DETAILS
-------
[V-001] ✅ [Instruction summary]
[V-002] ❌ [Instruction summary]
  - Failed after 5 attempts
  - Last error: [description]
  - Attempts: [brief log]
[V-003] ⚠️ [Instruction summary]
  - Flagged: Repeated same failure pattern
  - Recommendation: [suggestion]

AUDIT TRAIL
-----------
[Timestamp] V-001: Verified PASS on first check
[Timestamp] V-002: Attempt 1 - Changed X → FAIL
[Timestamp] V-002: Attempt 2 - Changed Y → FAIL
...

BROWSER VERIFICATION (if applicable)
------------------------------------
Browser Checks: [passed]/[total] | Blocked: [N]
Playwright: Available | Unavailable
Dev Server: [URL] | Not Running

Issues Found:
- [V-XXX] {type}: {description}

Screenshots: [list of captured files]
```

## Example

Given a checklist:
```
[ ] All functions have docstrings
[ ] No unused imports
[ ] Tests pass with >80% coverage
```

Workflow execution:
1. Parse into V-001, V-002, V-003
2. Pre-flight confirms all are testable
3. Sub-agent checks V-001 → FAIL (missing docstring in `utils.py:45`)
4. Main agent adds docstring
5. Sub-agent re-checks → PASS
6. Continue to V-002...
7. Final report shows 3/3 passed

## Key Principles

- **Structured feedback**: Sub-agent always returns actionable, located findings
- **No repeated fixes**: Track what was tried to avoid loops
- **Early exit**: Don't burn attempts on unfixable issues
- **Regression awareness**: Fixes shouldn't break other things
- **Audit everything**: The journey matters for debugging
