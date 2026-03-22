---
name: testing
description: Test the specific feature/fix implemented in the current session using browser or API tools.
---

# Testing

Tests the specific feature or bug fix implemented in the current session. NOT full E2E testing - focused on the session's work.

## Requirements

- Active session with implemented changes
- Implementation phase completed
- Working Dir available (for starting app)
- If no active session: **STOP and ask user** for session path

## Execution Steps

1. **Read session context:**
   - Read `_overview.md` to understand what was implemented
   - Review implementation docs to identify what needs testing

2. **Determine test strategy:**
   - Frontend changes -> Browser testing
   - Backend changes -> API testing via curl/httpie
   - Full-stack -> Both approaches

3. **Select browser testing tool** (if frontend testing needed):

   Choose the most suitable tool for your needs:

   | Tool | Best For | Setup |
   |------|----------|-------|
   | chrome-devtools MCP | Quick inspection, console access | Add to `.mcp.json` |
   | Puppeteer | Scripted browser automation | `npx puppeteer` |
   | Playwright | Cross-browser testing, screenshots | `npx playwright` |

   **Recommendation:**
   - Simple UI verification -> chrome-devtools MCP
   - Complex interactions -> Puppeteer or Playwright
   - Need screenshots/traces -> Playwright

   **If adding MCP:** After modifying `.mcp.json`, signal `continue` to restart the agent process (MCP doesn't hot-reload).

4. **Start the application:**
   - Read project's `.samocode` file or README for startup instructions
   - Follow project-specific setup commands
   - Verify app is running (check ports, health endpoints)
   - If fails to start -> document error, signal blocked

5. **Execute feature tests:**

   **Browser testing:**
   - Navigate to relevant page
   - Interact with new/modified UI elements
   - Verify expected behavior
   - Check console for errors

   **API testing:**
   ```bash
   # Example: Test endpoint
   curl -X POST http://localhost:8000/api/endpoint \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```
   - Use project-specific auth if needed (check .samocode or README)
   - Verify response codes and data

6. **Smoke test (side effect):**
   - App started successfully = smoke test passed
   - No crashes during feature test = smoke test passed

7. **Document results:**

   Create `[SESSION_PATH]/[TIMESTAMP_FILE]-test-[feature-slug].md`:

   ```markdown
   # Test: [feature name]
   Date: [TIMESTAMP_LOG]

   ## What Was Tested
   [Brief description of implemented feature]

   ## Test Environment
   - Working Dir: [path]
   - App Status: [running/failed to start]
   - Testing Tools: [chrome-devtools/puppeteer/playwright/curl]

   ## Test Steps
   1. [Step and result]
   2. [Step and result]
   ...

   ## Results
   - Feature Test: [PASS/FAIL]
   - Smoke Test: [PASS/FAIL]

   ## Issues Found
   [None or list of issues]
   ```

8. **Update session:**
   - Edit `_overview.md`:
     - Flow Log: `- [TIMESTAMP_ITERATION] Feature tested: [result] -> [filename].md`
     - Files: `- [filename].md - Test report`
   - Commit (if git repo): `cd [SESSION_DIR] && git add . && git commit -m "Test: [feature]"`

9. **Signal result:**
    - Tests PASS -> signal `continue`, recommend quality phase
    - Tests FAIL -> signal `blocked` with failure details (don't auto-fix)

## Browser Tool Setup

### chrome-devtools MCP

Add to `.mcp.json`:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--headless=true"]
    }
  }
}
```

Then signal `continue` to restart with new MCP.

### Puppeteer (via Bash)

```bash
# Quick test script
npx puppeteer <<'EOF'
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('http://localhost:3000');
  // ... test steps
  await browser.close();
})();
EOF
```

### Playwright (via Bash)

```bash
# Quick test
npx playwright test --headed=false

# Or inline script
npx playwright <<'EOF'
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:3000');
  await page.screenshot({ path: 'test.png' });
  await browser.close();
})();
EOF
```

## Edge Cases

- Working Dir not in `_overview.md` -> Check project .samocode file for MAIN_REPO, or ask user
- App fails to start -> Document in test report, signal blocked
- MCP not available -> Use Puppeteer/Playwright via bash instead
- Can't determine what to test -> Review implementation docs, ask if unclear
- No implementation phase completed -> Signal blocked (nothing to test)

## Important Notes

- Test ONLY the session's implemented work
- Don't attempt to fix failures automatically - signal blocked instead
- Document everything for human review
- Smoke test happens naturally (app start + no crashes)
- Read project .samocode file or README for project-specific setup instructions
