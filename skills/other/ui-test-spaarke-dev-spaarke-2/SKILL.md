# ui-test

---
description: Browser-based UI testing using Claude Code Chrome integration for PCF controls and model-driven apps
tags: [testing, ui, browser, pcf, frontend, visual, chrome]
techStack: [chrome, pcf-framework, react, fluent-ui, dynamics-365]
appliesTo: ["pcf", "frontend", "fluent-ui", "visual", "e2e-test"]
alwaysApply: false
---

> **Category**: Quality Assurance
> **Last Updated**: January 6, 2026

---

## Purpose

Automate browser-based UI testing for PCF controls and model-driven apps using Claude Code's Chrome integration. This skill enables:

- **Visual verification** - Confirm UI matches design specs
- **Dark mode testing** - Verify ADR-021 compliance (Fluent UI v9, no hard-coded colors)
- **Console monitoring** - Catch runtime errors during user flows
- **Form validation testing** - Test input validation and error messages
- **Demo recording** - Create GIFs for PR documentation
- **Authenticated testing** - Test within Dynamics 365 without API mocking

---

## Requirements

| Requirement | How to Check | Installation |
|-------------|--------------|--------------|
| Claude Code 2.0.73+ | `claude --version` | `npm install -g @anthropic-ai/claude-code@latest` |
| Google Chrome | Must be Chrome (not Edge/Brave) | Install from google.com/chrome |
| Claude in Chrome extension 1.0.36+ | Check Chrome extensions | Chrome Web Store |
| Paid Claude plan | Pro, Team, or Enterprise | Required |

**Not Supported**: WSL (Windows Subsystem for Linux)

---

## Setup

### One-Time Setup

```powershell
# 1. Update Claude Code
npm install -g @anthropic-ai/claude-code@latest

# 2. Verify version
claude --version  # Should be 2.0.73+

# 3. Install Chrome extension
# Go to: chrome.google.com/webstore → search "Claude in Chrome"
# Install version 1.0.36+

# 4. Start Claude Code with Chrome enabled
claude --chrome

# 5. Verify connection
/chrome
```

### Enable by Default (Optional)

Run `/chrome` and select "Enabled by default" to avoid the `--chrome` flag.

**Note**: Enabling by default increases context usage since browser tools are always loaded.

---

## When to Use

This skill triggers when:

- User says "test in browser", "visual test", "UI test", or "check in Chrome"
- Task has tags: `pcf`, `frontend`, `fluent-ui`, `visual`, `e2e-test`
- After `dataverse-deploy` completes for PCF controls
- Explicitly invoked with `/ui-test`
- User wants to verify ADR-021 dark mode compliance

**NOT applicable when:**

- Claude Code started without `--chrome` flag
- Task is backend-only (API, plugin)
- No deployed environment available
- Headless testing required (use Playwright/Cypress instead)

---

## Autonomous Capabilities

Claude Code with Chrome can perform these actions **autonomously**:

| Capability | Example | Notes |
|------------|---------|-------|
| Navigate pages | Open `https://org.crm.dynamics.com/...` | Works with authenticated sessions |
| Click elements | Click buttons, links, menu items | Uses CSS selectors or visible text |
| Type text | Fill form fields, search boxes | Can clear and replace |
| Read content | Extract text, check visibility | DOM inspection |
| Check console | Detect errors, warnings | Filter by type |
| Scroll | Scroll to elements, page positions | Virtual scroll supported |
| Record GIFs | Capture user flows as demos | Save to project assets |
| Manage tabs | Open new tabs, switch contexts | Shares login state |
| Resize windows | Test responsive layouts | Set specific dimensions |

### Requires Manual Intervention

| Situation | Action |
|-----------|--------|
| Login prompts | User logs in manually, tells Claude to continue |
| CAPTCHA | User solves, tells Claude to continue |
| MFA/2FA | User completes, tells Claude to continue |
| Modal dialogs (JS alerts) | User dismisses, tells Claude to continue |

---

## Workflow

### Step 1: Verify Chrome Connection

```
CHECK Claude Code started with --chrome:
  IF /chrome shows "Connected":
    → Continue
  ELSE:
    → REPORT: "Chrome integration not available. Start with: claude --chrome"
    → STOP
```

### Step 2: Load Test Context

```
IDENTIFY test requirements from:
  1. Task POML <acceptance-criteria> - specific test cases
  2. Task POML <ui-tests> section - if defined
  3. Project CLAUDE.md - environment URLs, test accounts
  4. ADR-021 - dark mode requirements for PCF/frontend tasks

EXTRACT:
  - Target URL (localhost or deployed environment)
  - Elements to verify
  - User flows to test
  - Expected behaviors
```

### Step 3: Environment Preparation

```
CHECK deployment status:
  IF PCF control:
    VERIFY pac pcf push completed
    GET environment URL from dataverse-deploy output

  IF localhost:
    VERIFY dev server running (npm start, dotnet run, etc.)

HANDLE authentication:
  REPORT: "I'll navigate to {URL}. Please log in if prompted."
  OPEN URL in new Chrome tab
  WAIT for user confirmation if login required
```

### Step 4: Execute UI Tests

```
FOR EACH test case in test context:

  NAVIGATE to target page/form

  VERIFY element visibility:
    → Check component renders
    → Check expected text/labels present

  TEST interactions:
    → Click buttons, links
    → Fill form fields
    → Trigger validation

  CHECK console:
    → Monitor for errors
    → Report any warnings

  IF dark mode test (ADR-021):
    → Toggle dark mode setting
    → Verify colors adapt (no white/black hard-coded)
    → Check semantic tokens used
    → Verify icon colors use currentColor

  CAPTURE evidence:
    → Take screenshots of key states
    → Record GIF for user flows (if requested)

REPORT results after each test
```

### Step 5: Generate Test Report

```markdown
## UI Test Results

**Component**: {PCF control or page name}
**Environment**: {URL}
**Date**: {timestamp}

### Tests Executed

| Test | Status | Notes |
|------|--------|-------|
| Component renders | ✅ Pass | Loaded in 1.2s |
| Dark mode toggle | ✅ Pass | Colors adapted correctly |
| Form validation | ⚠️ Warning | Error message unclear |
| Console errors | ✅ Pass | No errors detected |

### Issues Found

1. **[Warning]** Error message for invalid email is generic
   - Location: Email field validation
   - Expected: "Please enter a valid email address"
   - Actual: "Invalid input"

### Screenshots

- [Light mode](assets/light-mode.png)
- [Dark mode](assets/dark-mode.png)

### Recommendations

1. Update email validation message for clarity
2. Consider adding loading spinner for slow connections
```

---

## Test Definition Patterns

### Pattern A: In Task POML (Recommended)

Define specific UI tests in the task's acceptance criteria or dedicated section:

```xml
<task id="015" project="my-project">
  <metadata>
    <tags>pcf, deploy, fluent-ui, e2e-test</tags>
  </metadata>

  <!-- ... other sections ... -->

  <ui-tests>
    <test name="Component Renders">
      <url>https://org.crm.dynamics.com/main.aspx?appid=xxx&pagetype=entityrecord&etn=account</url>
      <steps>
        <step>Navigate to Account form</step>
        <step>Verify AISummaryPanel control is visible</step>
        <step>Check console for errors</step>
      </steps>
      <expected>Control renders without console errors</expected>
    </test>

    <test name="Dark Mode Compliance">
      <steps>
        <step>Toggle dark mode in D365 settings</step>
        <step>Verify panel background adapts</step>
        <step>Verify text colors adapt</step>
        <step>Verify no hard-coded white/black colors visible</step>
      </steps>
      <expected>All colors use semantic tokens per ADR-021</expected>
    </test>

    <test name="User Interaction">
      <steps>
        <step>Click "Refresh" button in panel</step>
        <step>Verify loading indicator appears</step>
        <step>Verify new data loads</step>
      </steps>
      <expected>Data refreshes within 3 seconds</expected>
    </test>
  </ui-tests>

  <acceptance-criteria>
    <criterion testable="true">PCF control renders on Account form</criterion>
    <criterion testable="true">Dark mode colors adapt correctly (ADR-021)</criterion>
    <criterion testable="true">No console errors during normal operation</criterion>
  </acceptance-criteria>
</task>
```

### Pattern B: In Project CLAUDE.md

Define environment-specific details in project context:

```markdown
## UI Testing Context

### Environment URLs

| Environment | URL | Notes |
|-------------|-----|-------|
| Development | https://spaarke-dev.crm.dynamics.com | Test account: testuser@dev |
| Staging | https://spaarke-staging.crm.dynamics.com | Requires VPN |
| Production | https://spaarke.crm.dynamics.com | Read-only testing |

### Common Navigation

- **Account form**: `/main.aspx?appid={app-id}&pagetype=entityrecord&etn=account`
- **Contact form**: `/main.aspx?appid={app-id}&pagetype=entityrecord&etn=contact`
- **Custom page**: `/main.aspx?appid={app-id}&pagetype=custom&name=spk_custompage`

### Test Accounts

| Account | Purpose | MFA |
|---------|---------|-----|
| testuser@spaarke-dev | Development testing | No |
| qauser@spaarke | QA validation | Yes (manual) |

### Dark Mode Toggle Location

Settings gear → Personalization → Dark mode
```

### Pattern C: Inline Test Request

For ad-hoc testing, describe tests in natural language:

```
"Test the AISummaryPanel PCF control:
1. Open an account record at https://org.crm.dynamics.com/...
2. Verify the panel shows in the form
3. Toggle dark mode and check colors adapt
4. Click refresh and verify data updates
5. Check console for any errors"
```

---

## ADR-021 Dark Mode Checklist

When task has `pcf`, `fluent-ui`, or `frontend` tags, verify:

```
DARK MODE COMPLIANCE (ADR-021):

□ Using Fluent UI v9 components (@fluentui/react-components)
  → NOT @fluentui/react (v8)

□ Using semantic tokens for colors
  → tokens.colorNeutralBackground1 (not #ffffff)
  → tokens.colorNeutralForeground1 (not #000000)

□ Icons use currentColor
  → Icons adapt to theme automatically

□ FluentProvider wrapper with theme
  → Theme context provided to component tree

□ No hard-coded hex colors
  → Search for #fff, #000, rgb(, rgba( in code

□ Test both modes visually
  → Light mode: readable, proper contrast
  → Dark mode: colors invert appropriately
```

---

## Integration with task-execute

This skill is called in **Step 9.7** after deployment tasks complete:

```
task-execute workflow:
  ...
  Step 9.5: Quality Gates (code-review, adr-check, lint)
  Step 9.6: Conflict Sync Check
  Step 9.7: UI Testing (this skill) ← NEW
  Step 10: Update Task Status
```

**Trigger Conditions for Step 9.7**:

```
IF all conditions met:
  - Task tags include: pcf, frontend, fluent-ui, e2e-test
  - Claude Code started with --chrome
  - Deployment completed successfully (dataverse-deploy or localhost)
  - Task has <ui-tests> section OR <acceptance-criteria> with UI tests

THEN:
  → PROMPT: "UI tests defined. Run browser-based testing? [Y/n]"
  → IF yes: Execute this skill
  → IF no: Skip with documented reason
```

---

## Recording Demos

To create GIF recordings for PR documentation:

```
"Record a GIF demonstrating the document upload flow:
1. Open the document library
2. Click the upload button
3. Select a file
4. Show the progress indicator
5. Show the success message
Save to projects/{project-name}/assets/upload-demo.gif"
```

GIFs are useful for:
- PR descriptions (showing what changed)
- User documentation
- Bug reports (reproducing issues)
- Design reviews (comparing to mockups)

---

## Error Handling

| Situation | Response |
|-----------|----------|
| Chrome not connected | "Start Claude Code with `--chrome` flag" |
| Login required | "Please log in manually, then say 'continue'" |
| Element not found | "Element '{selector}' not found. Check if page loaded correctly." |
| Console errors detected | Report errors with stack traces, suggest fixes |
| Modal blocking | "Modal dialog detected. Please dismiss it, then say 'continue'" |
| Network timeout | "Page load timeout. Check network/VPN connection." |
| Test failure | Report failure details, suggest next steps |

---

## Limitations

| Limitation | Workaround |
|------------|------------|
| Chrome only (not Edge) | Use Chrome for UI testing |
| No headless mode | Run on visible screen |
| WSL not supported | Run from Windows directly |
| Login/CAPTCHA manual | User handles, then continues |
| Session timeout | Re-authenticate when prompted |
| Context overhead | Only use when testing UI |

---

## Examples

### Example 1: PCF Control Deployment Test

**Trigger**: After `pac pcf push` completes

**Claude**:
```
I'll test the AISummaryPanel control in the browser.

1. Opening https://spaarke-dev.crm.dynamics.com/main.aspx?...
   → Please log in if prompted.

[User logs in]

2. Navigating to Account form...
   ✅ AISummaryPanel control is visible

3. Checking console...
   ✅ No errors detected

4. Testing dark mode...
   → Toggling dark mode setting
   ✅ Background color adapted (tokens.colorNeutralBackground1)
   ✅ Text color adapted (tokens.colorNeutralForeground1)
   ✅ No hard-coded colors visible

5. Testing refresh button...
   ✅ Loading indicator appeared
   ✅ Data refreshed in 1.8s

UI Test Results: ✅ All tests passed
```

### Example 2: Form Validation Test

**Trigger**: "Test the contact form validation"

**Claude**:
```
Testing contact form validation...

1. Opening contact form...
2. Submitting empty form...
   ✅ "First Name is required" error shown
   ✅ "Email is required" error shown

3. Entering invalid email "notanemail"...
   ✅ "Please enter a valid email" error shown

4. Entering valid data and submitting...
   ✅ Form submitted successfully
   ✅ Success message displayed

Console check:
   ⚠️ Warning: React key prop missing in list
   → Location: ContactList component
   → Recommendation: Add key prop to list items
```

### Example 3: Record Demo GIF

**Trigger**: "Record a demo of the file upload flow"

**Claude**:
```
Recording demo GIF...

1. Starting recording...
2. Clicking "Upload" button
3. Selecting file from dialog (please select a file)
4. Showing upload progress...
5. Showing success state...
6. Stopping recording

✅ Demo saved to: projects/sdap-enhancements/assets/upload-demo.gif
```

---

## Related Skills

- **dataverse-deploy** - Deploys PCF controls before UI testing
- **code-review** - Code quality (this skill focuses on runtime behavior)
- **adr-check** - Architecture validation (ADR-021 checked visually here)
- **task-execute** - Calls ui-test in Step 9.7 for PCF/frontend tasks

---

## Quick Reference

```powershell
# Start Claude Code with Chrome
claude --chrome

# Check connection
/chrome

# Run UI test
/ui-test

# Enable by default
# Run /chrome → Select "Enabled by default"
```

---

*This skill enables visual verification of PCF controls and model-driven apps using Claude Code's Chrome integration.*
