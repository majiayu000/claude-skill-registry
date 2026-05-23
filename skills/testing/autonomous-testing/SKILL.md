# Autonomous Testing Skill

> Version: 1.0.0
> Compiler: manual (bootstrap)
> Last Updated: 2026-01-22

Use automated browser testing (Puppeteer/Playwright) instead of asking humans to manually verify UI changes.

## When to Activate

Use this skill when:
- Verifying a fix works
- Testing a UI change
- Checking if an error is resolved
- About to ask user to click something
- Tempted to write "please test this"

## Core Principles

### 1. Machines Click Faster Than Humans
Browser automation can verify UI changes in seconds; asking a human takes minutes and breaks flow.

*Every "please test this" is a context switch for the human and a blocking wait for you.*

### 2. Verify Programmatically When Possible
If something can be tested via API, script, or headless browser, do that first.

*Programmatic verification is repeatable, fast, and doesn't require human attention.*

### 3. Reserve Humans for Judgment Calls
Only involve humans when subjective evaluation is genuinely needed.

*Automatable questions like "Does this button work?" should be tested programmatically; subjective questions like "Does this feel right?" genuinely need a human.*

### 4. Build Verification Into the Fix
When fixing a bug, write the verification step as code, not as instructions for humans.

*The test becomes documentation and regression prevention.*

---

## Workflow

### Phase 1: Assess Testability

Determine if the change can be verified programmatically.

1. Identify what "working" means - visible element, API response, state change
2. Check if environment has automation tools available (Puppeteer, Playwright, curl)
3. Estimate automation time vs asking human time
4. If automation takes <5 minutes and is repeatable, automate it

**Outputs:** Decision (automate vs ask human), Test strategy

### Phase 2: Write Automated Test

Create the verification script.

1. Choose appropriate tool (Puppeteer for browser, curl for API, scripts for CLI)
2. Write minimal test that verifies the specific change
3. Include setup steps (navigate to page, log in if needed)
4. Add clear pass/fail criteria with assertions
5. Handle common flakiness (wait for elements, retry on network issues)

**Outputs:** Executable test script, Expected vs actual comparison

### Phase 3: Execute and Interpret

Run the test and analyze results.

1. Run the test in the target environment
2. Capture output, screenshots, or logs
3. Compare actual behavior to expected behavior
4. If test fails, diagnose whether it's test bug or real bug

**Outputs:** Test results, Evidence (screenshots, logs), Diagnosis if failed

### Phase 4: Iterate or Escalate

Based on results, either fix and retest, or escalate to human.

1. If test passes, report success with evidence
2. If test fails with clear cause, fix and retest
3. If test is flaky or unclear, add debugging and retry
4. Only escalate to human if automation genuinely can't determine pass/fail

**Outputs:** Verified fix OR escalation with context

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Screenshot Diff** | Verifying visual UI changes | Take before/after screenshots, compare | Visual changes are hard to describe but easy to see |
| **Element Assertion** | Verifying element exists or has correct content | Use selectors to find element, assert on text/attributes | Most UI bugs are "element missing" or "wrong text" |
| **Network Intercept** | Verifying API calls are made correctly | Intercept requests/responses, verify payload and status | API integration bugs often hide behind UI that "looks" working |
| **State Verification** | Verifying application state changed correctly | Check localStorage, cookies, database, or API state after action | UI might show success while state is actually broken |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Human Button-Clicking** | Slow, breaks flow, makes human a proxy for automation | Write Puppeteer script to click and verify |
| **Manual Refresh Cycles** | Tedious, no evidence captured, human becomes test runner | Automate the refresh and check with assertions |
| **Screenshot Requests** | Slow back-and-forth, manual comparison | Capture screenshot programmatically during automated test |
| **Skipping Automation Because It's "Quick"** | One click becomes ten iterations; each requires human attention | Invest 2 minutes in automation, save 20 minutes of back-and-forth |

---

## Quality Checklist

Before completing:

- [ ] Identified what "success" looks like programmatically
- [ ] Checked if automation tools are available in environment
- [ ] Wrote test with clear pass/fail assertion
- [ ] Handled common flakiness (waits, retries)
- [ ] Captured evidence (screenshots, logs) for verification
- [ ] Only escalated to human if automation genuinely couldn't determine result

---

## Examples

**Verifying a button click triggers correct API call**

Write Puppeteer script that:
1. Navigates to page
2. Sets up network interception
3. Clicks the button
4. Asserts API was called with correct payload
5. Asserts success response received

Run script, report pass/fail with captured network log.

**Verifying error message no longer appears**

Write Puppeteer script that:
1. Navigates to page that previously showed error
2. Waits for page load
3. Asserts error element is NOT present (or success element IS present)
4. Takes screenshot as evidence

Run script, report "Error resolved - screenshot attached" or "Error still present - investigating"

---

## References

- Puppeteer documentation - page automation
- Playwright documentation - cross-browser testing
- Testing Library principles - testing implementation vs behavior
- Session insight - repeated human-gating during Oracy web app debugging
