---
name: smoke-test
description: "Launch the app and hands-on verify that it works by interacting with it. Use when the user asks to \"smoke test\", \"test it manually\", \"verify it works\", \"try it out\", \"run a smoke test\", \"check it in the browser\", or \"does it actually work\". Not for unit/integration tests."
---

# Smoke Test

Launch the app and hands-on verify that it works. Not unit/integration tests.

## Step 1: Determine Scope

Resolve scope using the first match:

1. **User-specified** — the user says what to test. Use that.
2. **PR** — a PR URL or number is provided. Fetch the PR details (title, description, changed files, comments) and read the changed code.
3. **Conversation context** — prior conversation contains recent work (a feature, fix, or refactor). Extract what changed, where it lives, and expected behavior.
4. **App-level discovery** — fresh context with no prior work. Examine the project (entry points, routes, commands, README) to identify the app's core user-facing flows. Design tests that verify the app launches and its primary functionality works end-to-end.

## Step 2: Determine Testing Approach

Examine the project type and available skills/MCP tools to choose the right approach.

- **Web app** → `/agent-browser` skill
- **UI/native app** → project-specific UI testing skill or MCP tool if available, otherwise `/peekaboo` skill
- **CLI tool** → direct terminal execution
- **Library with no entry point** → report that smoke testing is not applicable and stop

## Step 3: Plan Smoke Tests

Design targeted smoke tests based on the scope. Each test should:

1. Exercise a specific flow from the determined scope
2. Verify the happy path works end-to-end
3. Check one obvious edge case if applicable

Output the plan as text:

```
Smoke Test Plan:
1. [Test description] — verifies [what]
2. [Test description] — verifies [what]
3. [Test description] — verifies [what]

Approach: [agent-browser / peekaboo / terminal]
Dev server command: [command]
```

## Step 4: Execute

### Web App Path

Start the dev server if not already running. Wait for it to be ready. Run `/agent-browser` skill for full browser automation documentation.

Core verification loop per test:

1. Navigate to the relevant page/route
2. Snapshot and verify expected UI elements exist
3. Interact (fill forms, click buttons, navigate)
4. Re-snapshot and verify the expected outcome
5. Record pass/fail

Close the browser session and stop the dev server when done.

### UI/Native App Path

Launch the app. Use available platform-specific MCP tools if present, otherwise run the project-specific UI testing skill if available, or fall back to `/peekaboo` skill.

Core verification loop per test:

1. Capture the UI state
2. Interact with the relevant controls
3. Re-capture and verify the expected outcome
4. Record pass/fail

### CLI Path

Run commands directly.

Core verification loop per test:

1. Run the command with expected inputs
2. Check stdout/stderr for expected output
3. Verify side effects (files created, data changed)
4. Record pass/fail

## Step 5: Report

Present a summary:

```
Smoke Test Results:
- [PASS] Test 1: description
- [FAIL] Test 2: description — [what went wrong]
- [PASS] Test 3: description

Overall: X/Y passed
```

If any test failed, include the relevant snapshot, screenshot, or output showing the failure.

## Rules

- Always clean up: close browser sessions, stop dev servers started by this skill.
- Never modify code. This skill is read-only verification. If a test fails, report the failure — do not attempt to fix it.
- If the dev server fails to start, report the error and stop.
- Keep tests focused on the determined scope.
- To diagnose failures, run the `/investigate` skill on the smoke test report.
