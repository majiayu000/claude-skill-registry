---
name: testing
description: >
  Test patterns with Playwright browser automation. Navigate to deployed patterns,
  interact with UI elements, verify functionality. Use when testing patterns after
  deployment or when debugging pattern behavior in browser.
---

# Testing Patterns with Playwright

If Playwright MCP is available, use it to test patterns in a real browser.

## ⚠️ CRITICAL URL FORMAT

**When testing patterns, the URL MUST be:**

```
http://localhost:8000/SPACE-NAME/CHARM-ID
```

**⚠️ COMMON MISTAKES TO AVOID:**
- ❌ `http://localhost:5173/...` - WRONG PORT (that's the shell, not toolshed)
- ❌ `http://localhost:8000/CHARM-ID` - MISSING SPACE NAME
- ❌ `http://localhost:5173/CHARM-ID` - WRONG PORT AND MISSING SPACE

**If you use the wrong URL format, the pattern will NOT work. No exceptions.**

## Navigate to Deployed Pattern

```
Use Playwright to navigate to: http://localhost:8000/SPACE-NAME/CHARM-ID
```

**Example:**
```
http://localhost:8000/claude-counter-1130-1/baedreicqpqie6td...
```

## Test Pattern Functionality

Once the page loads:
1. **Wait briefly before first snapshot** - Sometimes the initial load shows a login/registration screen for a moment. Wait 1-2 seconds before taking your first snapshot to ensure the pattern has fully rendered.
2. Take a snapshot to see the UI: `browser_snapshot`
3. Interact with elements: click buttons, fill inputs, check boxes
4. Verify behavior: check that counters increment, items are added, etc.
5. Report any issues found

## Registering (First Time Only)

If you see a login/registration page:
1. Click "Register" or "Generate Passphrase"
2. Follow the registration flow
3. Then navigate back to the pattern URL

## Space Naming Convention

Use descriptive space names with the `claude-` prefix:

**Format:** `claude-<pattern-name>-<MMDD>-<counter>`

**Examples:**
- `claude-counter-1130-1`
- `claude-shopping-list-1201-2`
- `claude-prompt-injection-tracker-1130-1`

## Testing Workflow

**After deploying a new pattern:**
```
1. Deploy with: deno task ct piece new --api-url http://localhost:8000 --identity ../labs/claude.key --space claude-my-pattern-1130-1 pattern.tsx
2. Note the piece ID from output
3. Use Playwright to navigate to: http://localhost:8000/claude-my-pattern-1130-1/CHARM-ID
   ⚠️ MUST be port 8000, MUST include space name
4. Verify all functionality works
5. Report to user if tests pass or if issues found
```

**After updating a pattern:**
```
1. Deploy NEW instance with `piece new` (see warning below)
2. Note the NEW piece ID
3. Use Playwright to test at http://localhost:8000/SPACE-NAME/NEW-CHARM-ID
4. Test that changes work as expected
```

**🚨 NEVER use `piece setsrc` to update patterns!**

`piece setsrc` corrupts piece state and causes pieces to render blank on direct navigation. ALWAYS use `piece new` to deploy a fresh instance instead. Getting a new piece ID each time is expected and correct.

**When Playwright unavailable:**
- Suggest user test manually in browser
- Provide the URL to test
- Ask them to report any issues

## Playwright Troubleshooting

**If screenshot shows login/registration screen instead of pattern:**

The page may not have fully loaded. Wait 1-2 seconds before taking the first snapshot:
```
Use browser_wait_for with time: 2 before taking the snapshot
```

This is common when navigating to a pattern URL—the authentication check may briefly show the login screen before the pattern renders.

**If Playwright starts opening many tabs:**

This can happen after user suspends/resumes their computer. The Chrome connection gets confused.

**Solution:** Ask user to:
1. Quit the Chrome instance that Playwright opened (the one with "Chrome is being controlled by automated test software" banner)
2. Next Playwright command will open a fresh browser and work normally

**Tell user:**
```
Playwright's browser connection got confused after your computer woke up.
Please quit the Chrome window with the yellow "automated test software" banner,
then I'll try again with a fresh browser.
```
