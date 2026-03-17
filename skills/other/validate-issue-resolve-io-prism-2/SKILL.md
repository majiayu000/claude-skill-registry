---
name: validate-issue
description: Use to validate reported issues. Confirms reproducibility and documents validation evidence.
---
<!-- Powered by Prism Core™ -->

# validate-issue

Validate customer-reported issues using Playwright-MCP to reproduce and document the problem with evidence.

## When to Use

- When customer reports a bug or issue
- When issue needs reproduction for confirmation
- When documenting evidence for development team
- As first step in issue triage process

## Quick Start

1. Gather issue details from customer report
2. Initialize Playwright session with application URL
3. Reproduce customer steps with screenshots
4. Capture evidence (screenshots, console, network)
5. Document validation result (confirmed/not-reproducible)

## Purpose

Use automated browser testing to reproduce exactly what the customer experienced, capture evidence, and confirm if the issue is real and reproducible.

## SEQUENTIAL Task Execution

### 1. Gather Issue Details
- Customer description of the problem
- Steps to reproduce provided by customer
- Environment details (browser, device, account)
- Expected vs actual behavior
- Any error messages reported

### 2. Initialize Playwright Session
```yaml
playwright_setup:
  - Use mcp__playwright-mcp__init-browser with the application URL
  - Navigate to the affected page/feature
  - Set up appropriate viewport for device type (mobile/desktop)
  - Clear cookies/storage if needed for clean state
```

### 3. Reproduce Customer Steps
Execute each step the customer reported:
```yaml
reproduction_steps:
  - action: Navigate to specific page
    playwright: mcp__playwright-mcp__execute-code
    capture: screenshot before action
  - action: Perform user interactions (click, type, submit)
    playwright: mcp__playwright-mcp__execute-code
    capture: screenshot after each action
  - action: Wait for expected results
    playwright: Check for errors in console
    capture: final state screenshot
```

### 4. Capture Evidence
```yaml
evidence_collection:
  screenshots:
    - Initial state
    - Each interaction step
    - Error state (if reproduced)
    - Console errors: mcp__playwright-mcp__execute-code to get console.log
  network:
    - Failed API calls
    - Response status codes
    - Timing issues
  state:
    - DOM state at failure point
    - JavaScript variable values
    - Local storage/session data
```

### 5. Validation Report
```yaml
validation_result:
  reproducible: true/false
  severity: P0/P1/P2/P3
  
  reproduction_details:
    steps_taken: [exact Playwright commands used]
    success_rate: "3/3 attempts reproduced issue"
    environment: 
      browser: "Chrome 120"
      viewport: "1920x1080"
      account_type: "trial/paid/admin"
  
  evidence:
    screenshots: [list of captured images]
    console_errors: [any JavaScript errors]
    network_failures: [failed requests]
    
  impact_assessment:
    affected_users: "All users on checkout flow"
    business_impact: "Blocking purchases"
    workaround_available: "Yes/No - describe if yes"
```

## Example Playwright Validation Script

```javascript
// Example validation using mcp__playwright-mcp__execute-code
async function run(page) {
  // Navigate to the problem area
  await page.goto('/checkout');
  
  // Capture initial state
  const initialScreenshot = await page.screenshot();
  
  // Reproduce customer actions
  await page.fill('#email', 'customer@example.com');
  await page.fill('#card-number', '4242424242424242');
  
  // Check for the reported issue
  const submitButton = await page.locator('#submit-payment');
  await submitButton.click();
  
  // Wait and check for infinite spinner (customer's complaint)
  await page.waitForTimeout(5000);
  const spinnerStillVisible = await page.locator('.spinner').isVisible();
  
  // Capture console errors
  const consoleLogs = [];
  page.on('console', msg => consoleLogs.push(msg.text()));
  
  // Return validation result
  return {
    reproduced: spinnerStillVisible,
    errors: consoleLogs,
    finalState: await page.screenshot()
  };
}
```

## Success Criteria
- [ ] Issue reproduction attempted with Playwright
- [ ] Evidence captured (screenshots, logs)
- [ ] Clear reproducible/not-reproducible determination
- [ ] Root cause hypothesis if reproduced
- [ ] Impact assessment completed

## Output
- Validation report with reproduction status
- Evidence package (screenshots, errors)
- Recommendation for next steps (investigate, create test, escalate)
