---
name: acceptance-criteria-verification
description: Use after implementing features - verifies each acceptance criterion with structured testing and posts verification reports to the GitHub issue
allowed-tools:
  - Bash
  - Read
  - mcp__github__*
model: opus
---

# Acceptance Criteria Verification

## Overview

Systematically verify each acceptance criterion and post structured reports.

**Core principle:** Every criterion verified. Every verification documented.

**Announce at start:** "I'm using acceptance-criteria-verification to verify the implementation."

## The Verification Process

### Step 1: Extract Criteria

Read the issue and extract all acceptance criteria:

```bash
# Get issue body
gh issue view [ISSUE_NUMBER] --json body -q '.body'
```

Parse out criteria (look for `- [ ]` or `- [x]` patterns in acceptance criteria section).

### Step 2: Plan Verification

For each criterion, determine:

| Criterion | Test Type | How to Verify |
|-----------|-----------|---------------|
| [Criterion 1] | Unit test | Run specific test |
| [Criterion 2] | Integration | API call + response check |
| [Criterion 3] | E2E | Browser automation |
| [Criterion 4] | Manual | Visual inspection |

### Step 3: Execute Verification

For each criterion, run the appropriate verification:

#### Unit/Integration Tests

```bash
# Run specific tests
pnpm test --grep "[test pattern]"

# Or run test file
pnpm test path/to/specific.test.ts
```

#### E2E Tests

```bash
# If using Playwright
npx playwright test [test file]

# If using browser automation MCP
# Use mcp__playwright or mcp__puppeteer
```

#### Manual Verification

For criteria requiring visual or interactive verification:

1. Start the application
2. Navigate to relevant area
3. Perform the action
4. Capture screenshot if relevant
5. Document result

### Step 4: Record Results

For each criterion, record:

```
Criterion: [Text from issue]
Status: PASS | FAIL | PARTIAL | SKIP
Evidence: [Test output, screenshot, observation]
Notes: [Any relevant details]
```

### Step 5: Post Verification Report

Post a structured comment to the issue:

```bash
gh issue comment [ISSUE_NUMBER] --body "## Verification Report

**Run**: $(date -u +%Y-%m-%dT%H:%M:%SZ)
**By**: agent
**Commit**: $(git rev-parse --short HEAD)
**Branch**: $(git branch --show-current)

### Results

| # | Criterion | Status | Notes |
|---|-----------|--------|-------|
| 1 | [Criterion text] | PASS | [Notes] |
| 2 | [Criterion text] | FAIL | [What failed] |
| 3 | [Criterion text] | PARTIAL | [What works, what doesn't] |

### Summary

| Status | Count |
|--------|-------|
| PASS | X |
| FAIL | X |
| PARTIAL | X |
| SKIP | X |
| **Total** | **X** |

### Test Output

<details>
<summary>Test Results</summary>

\`\`\`
[test output here]
\`\`\`

</details>

### Next Steps

- [ ] [Action items for failures/partials]
"
```

### Step 6: Update Issue Checkboxes

For each passing criterion, check it off in the issue body:

```bash
# Get current body
BODY=$(gh issue view [ISSUE_NUMBER] --json body -q '.body')

# Update checkboxes for passing criteria
# (Implementation depends on body format)

# Update issue
gh issue edit [ISSUE_NUMBER] --body "$NEW_BODY"
```

### Step 7: Update Project Fields

```bash
# Update project fields using project-status-sync skill

# Verification status
# - All PASS → Passing
# - Any FAIL → Failing
# - Mix of PASS/PARTIAL → Partial

# Criteria Met count
# - Count of PASS criteria

# Last Verified
# - Current date

# Verified By
# - "agent"
```

## Status Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| **PASS** | Criterion fully met, verified working | Check off in issue |
| **FAIL** | Criterion not met, requires fix | Document what failed, return to development |
| **PARTIAL** | Works with issues, needs improvement | Document issues, may need fix |
| **SKIP** | Could not verify (blocked, N/A, etc.) | Document reason |

## E2E Verification Best Practices

When using browser automation:

1. **Start fresh** - New browser session for each verification
2. **Capture evidence** - Screenshots at key points
3. **Check visible state** - Not just DOM, but visible rendering
4. **Test error cases** - Not just happy path
5. **Clean up** - Close sessions after verification

```javascript
// Example verification flow (pseudo-code)
await page.goto(appUrl);
await page.click('[data-testid="new-chat"]');
await page.waitForSelector('[data-testid="chat-input"]');
await page.screenshot({ path: 'new-chat-verification.png' });
// Verify expected state
const title = await page.title();
expect(title).toContain('New Chat');
```

## Handling Failures

When criteria fail:

1. **Document specifically** what failed
2. **Include reproduction steps** if not obvious
3. **Capture error messages** or screenshots
4. **Return to development** to fix
5. **Re-run verification** after fix

Do NOT:
- Mark as PASS when it failed
- Skip verification because "it should work"
- Ignore intermittent failures

## Verification Checklist

Before completing verification:

- [ ] All acceptance criteria evaluated
- [ ] Each criterion has clear PASS/FAIL/PARTIAL/SKIP status
- [ ] Evidence captured for each (test output, screenshots)
- [ ] Verification report posted to issue
- [ ] Issue checkboxes updated for passing criteria
- [ ] Project fields updated
- [ ] If any failures, next steps documented

## After Verification

Based on results:

| Overall Result | Next Action |
|----------------|-------------|
| All PASS | Proceed to code review |
| Any FAIL | Return to development, fix, re-verify |
| Partial only | Discuss with user - acceptable or needs fix? |

## Integration

This skill is called by:
- `issue-driven-development` - Step 8

This skill calls:
- `project-status-sync` - Update verification fields
- `issue-lifecycle` - Post comments
