---
name: test-and-break
description: "Autonomous testing skill that opens a deployed app, goes through user flows, tries to break things, and writes detailed bug reports. Use after deploying to staging. Triggers on: test the app, find bugs, QA the deployment, break the app, test staging."
---

# Test and Break

Systematically test a deployed application by going through user flows, trying edge cases, and attempting to break things. Outputs structured bug reports that can be converted to user stories for autonomous fixing.

---

## Prerequisites

- **agent-browser** installed (`npm install -g agent-browser && agent-browser install`)
- App deployed to a URL (staging/preview)
- Basic understanding of what the app should do (read the PRD)

---

## The Job

1. Read the PRD to understand what the app should do
2. Open the deployed app in agent-browser
3. Go through each major user flow
4. Try to break things at each step
5. Document all bugs and issues found
6. Output structured bug reports

---

## Testing Process

### Step 1: Understand the App

Read `tasks/prd.md` and `tasks/architecture.md` to understand:
- What user flows exist
- What the app should do
- What the expected behavior is

### Step 2: Open the App

```bash
agent-browser open [DEPLOYMENT_URL]
agent-browser snapshot -i
```

### Step 3: Test Each User Flow

For each major feature/flow in the PRD:

#### A. Happy Path Testing
1. Go through the flow as a normal user would
2. Verify each step works as expected
3. Check that success states appear correctly

#### B. Edge Case Testing
Try these at each input/interaction point:

**Input Edge Cases:**
- Empty inputs (submit with nothing)
- Very long text (500+ characters)
- Special characters (`<script>alert('xss')</script>`, `'; DROP TABLE users;--`)
- Unicode/emojis (🎉, 中文, العربية)
- Negative numbers where positive expected
- Zero where non-zero expected
- Future dates, past dates, invalid dates
- Invalid email formats
- Spaces only
- Leading/trailing whitespace

**Interaction Edge Cases:**
- Double-click buttons rapidly
- Click back button during operations
- Refresh page mid-flow
- Open same page in multiple tabs
- Submit form twice quickly

**State Edge Cases:**
- Log out mid-operation (if auth exists)
- Let session expire
- Navigate directly to URLs that require prior steps
- Use browser back/forward buttons

**Visual/UX Issues:**
- Check mobile responsiveness (resize browser)
- Look for overlapping elements
- Check loading states exist
- Verify error messages are helpful
- Look for console errors

### Step 4: Document Each Bug

For each issue found, document:

```markdown
## BUG-XXX: [Short descriptive title]

**Severity:** Critical | High | Medium | Low
**Type:** Functional | UI/UX | Security | Performance | Accessibility

**Steps to Reproduce:**
1. Go to [URL]
2. Do [action]
3. Enter [input]
4. Click [button]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Screenshot:** [if applicable]

**Console Errors:** [if any]

**Notes:** [any additional context]
```

---

## Severity Guidelines

| Severity | Definition | Examples |
|----------|------------|----------|
| **Critical** | App broken, data loss, security issue | Crash, XSS vulnerability, data not saving |
| **High** | Major feature broken, bad UX | Can't complete main flow, confusing errors |
| **Medium** | Feature works but has issues | Minor validation missing, UI glitches |
| **Low** | Polish/minor issues | Typos, slight misalignment, minor UX |

---

## Output Format

Save bug report to `tasks/bug-report-[date].md`:

```markdown
# Bug Report: [App Name]
**Tested:** [Date]
**URL:** [Deployment URL]
**Tester:** Claude (Automated)

## Summary
- Total bugs found: X
- Critical: X
- High: X
- Medium: X
- Low: X

## Critical Bugs
[List critical bugs first]

## High Priority Bugs
[List high bugs]

## Medium Priority Bugs
[List medium bugs]

## Low Priority Bugs
[List low bugs]

## Positive Findings
[List things that worked well - important for context]

## Recommendations
[Overall suggestions for improvement]
```

---

## Converting Bugs to User Stories

After generating the bug report, convert each bug to a user story format:

```json
{
  "id": "BUG-001",
  "title": "Fix: [Bug title]",
  "description": "As a user, I expect [expected behavior] but currently [actual behavior].",
  "acceptanceCriteria": [
    "Specific fix criterion 1",
    "Specific fix criterion 2",
    "Regression test: [original bug steps] no longer reproduces",
    "Typecheck passes"
  ],
  "priority": 1,
  "passes": false,
  "notes": "Original bug: [reference]"
}
```

Priority mapping:
- Critical bugs → priority 1-2
- High bugs → priority 3-5
- Medium bugs → priority 6-10
- Low bugs → priority 11+

---

## Integration with Ralph

After generating bug stories, they can be:

1. **Added to existing prd.json** - Append bug fixes to current project
2. **Create new prd.json** - Start a bug-fix-only Ralph run

To add to existing prd.json:
```bash
# Read current max priority
MAX_PRIORITY=$(cat prd.json | jq '[.userStories[].priority] | max')

# Add bug stories starting after max priority
# (Claude should do this programmatically)
```

---

## Example Testing Session

```bash
# 1. Open the app
agent-browser open https://my-app-staging.vercel.app

# 2. Take initial snapshot
agent-browser snapshot -i

# 3. Test login flow
agent-browser fill @e1 "test@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i

# 4. Try to break it
agent-browser fill @e1 ""  # empty email
agent-browser click @e3    # submit anyway
agent-browser snapshot -i  # check error handling

# 5. Try XSS
agent-browser fill @e1 "<script>alert('xss')</script>"
agent-browser snapshot -i

# Continue testing other flows...
```

---

## Checklist

Before finishing testing:

- [ ] Tested all user flows from PRD
- [ ] Tried empty inputs on all forms
- [ ] Tried special characters/XSS on all inputs
- [ ] Checked mobile responsiveness
- [ ] Looked for console errors
- [ ] Verified error messages are helpful
- [ ] Documented all bugs with reproduction steps
- [ ] Assigned severity to each bug
- [ ] Saved bug report to tasks/bug-report-[date].md
