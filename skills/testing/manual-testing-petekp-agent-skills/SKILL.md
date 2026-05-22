---
name: manual-testing
description: Guide users step-by-step through manually testing whatever is currently being worked on. Use when asked to "test this", "verify it works", "let's test", "manual testing", "QA this", "check if it works", or after implementing a feature that needs verification before proceeding.
---

# Manual Testing

Verify current work through automated testing first, falling back to user verification only when necessary.

## Core Principle

**Automate everything possible.** Only ask the user to manually verify what Claude cannot verify through tools.

## Workflow

### 1. Analyze Current Context

Examine recent work to identify what needs testing:
- Review recent file changes and conversation history
- Identify the feature, fix, or change to verify
- Determine testable behaviors and expected outcomes

### 2. Classify Each Verification Step

For each thing to verify, determine if Claude can test it automatically:

**Claude CAN verify (do these automatically):**
- Code compiles/builds: `npm run build`, `cargo build`, `go build`, etc.
- Tests pass: `npm test`, `pytest`, `cargo test`, etc.
- Linting/type checking: `eslint`, `tsc --noEmit`, `mypy`, etc.
- API responses: `curl`, `httpie`, or scripted requests
- File contents: Read files, grep for expected patterns
- CLI tool output: Run commands and check output
- Server starts: Start server, check for errors, verify endpoints respond
- Database state: Query databases, check records exist
- Log output: Tail logs, grep for expected/unexpected messages
- Process behavior: Check exit codes, stdout/stderr content
- File existence/permissions: `ls`, `stat`, `test -f`
- JSON/config validity: Parse and validate structure
- Port availability: `lsof`, `netstat`, curl localhost
- Git state: Check diffs, commits, branch state

**Claude CANNOT verify (ask user):**
- Visual appearance (colors, layout, spacing, alignment)
- Animations and transitions
- User experience feel (responsiveness, intuition)
- Cross-browser rendering
- Mobile device behavior
- Physical hardware interaction
- Third-party service UIs (OAuth flows, payment forms)
- Accessibility with actual screen readers
- Performance perception (feels fast/slow)

### 3. Execute Automated Verifications

Run all automatable checks first. Be thorough:

```bash
# Example: Testing a web feature
npm run build          # Compiles?
npm run lint           # No lint errors?
npm test               # Tests pass?
npm run dev &          # Server starts?
sleep 3
curl localhost:3000/api/endpoint  # API responds correctly?
```

Report results as you go. If automated tests fail, stop and address before asking user to verify anything.

### 4. User Verification (Only When Necessary)

For steps Claude cannot automate, present them sequentially with selectable outcomes:

```
Step N of M: [Brief description]

**Action:** [Specific instruction - what to do]

**Expected:** [What should happen if working correctly]
```

Then use AskUserQuestion with predicted outcomes:
- 2-4 most likely outcomes as selectable options
- First option: expected/success outcome
- Remaining options: common failure modes
- Free-text "Other" option is provided automatically

**Example:**
```json
{
  "questions": [{
    "question": "How does the button look?",
    "header": "Visual check",
    "options": [
      {"label": "Looks correct", "description": "Blue button, proper spacing, readable text"},
      {"label": "Wrong color/style", "description": "Button exists but styling is off"},
      {"label": "Layout broken", "description": "Elements overlapping or misaligned"},
      {"label": "Not visible", "description": "Button missing or hidden"}
    ],
    "multiSelect": false
  }]
}
```

### 5. Handle Results

**Automated test fails:** Stop and fix before proceeding.

**User reports issue:** Note it, ask if they want to investigate now or continue testing.

### 6. Summarize

After all steps complete:
- List what was verified automatically (with pass/fail)
- List what user verified (with results)
- Summarize any issues found
- Recommend next actions

## Guidelines

- Run automated checks in parallel when possible
- Be creative with verification—most things can be tested programmatically
- If unsure whether something can be automated, try it first
- Keep user verification steps minimal and focused on truly visual/experiential checks
