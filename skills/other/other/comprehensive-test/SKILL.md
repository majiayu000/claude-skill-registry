---
name: comprehensive-test
description: "Execute comprehensive, multi-level testing of the app covering basic functionality, complex operations, adversarial testing, and cross-cutting scenarios. Deeper than /smoke-test. Use when the user asks to \"test thoroughly\", \"comprehensive test\", \"test all scenarios\", \"deep test\", \"test edge cases\", \"test everything\", \"break it\", or \"find bugs by testing\"."
---

# Comprehensive Test

Execute comprehensive, multi-level testing that goes beyond smoke testing to actively find bugs through escalating test scenarios.

## Step 1: Load or Create Test Plan

Check if `.turbo/test-plan.md` exists.

- **If it exists** — read the test plan and continue to Step 2. If the user specifies a narrower scope, filter the plan to relevant scenarios rather than executing all of them.
- **If it does not exist** — run the `/create-test-plan` skill first, then continue.

## Step 2: Determine Testing Approach

Use the approach specified in the test plan. If the plan does not specify one, determine it using the same logic as `/create-test-plan` Step 3.

## Step 3: Execute Tests by Level

Work through each level sequentially. Complete all tests in a level before moving to the next.

### Execution Loop (Per Test)

1. Set up the preconditions described in the test scenario
2. Perform the exact steps
3. Capture the result (screenshot, output, or state observation)
4. Compare against the expected outcome
5. Record **PASS** or **FAIL** with details

### Level Progression

1. **Level 1: Basic Functionality** — If any Level 1 test fails, report early and use `AskUserQuestion` to ask whether to continue. Basic failures may indicate the feature is too broken for deeper testing.
2. **Level 2: Complex Operations** — Execute all tests regardless of individual failures.
3. **Level 3: Adversarial Testing** — Execute all tests. Failures here are expected and valuable.
4. **Level 4: Cross-Cutting Scenarios** — Execute all tests.

If a project-specific testing skill or MCP tool was identified in Step 2, use that. The paths below are fallbacks.

### Web App Path

Start the dev server if not already running. Wait for it to be ready. If `/agent-browser` is available, run the `/agent-browser` skill. Otherwise, use `claude-in-chrome` MCP to interact with the app.

### UI/Native App Path

Launch the app. Use `computer-use` MCP to interact with the UI.

### CLI Path

Run commands directly.

## Step 4: Report

Present results organized by level:

```
Comprehensive Test Results:

## Level 1: Basic Functionality (X/Y passed)
- [PASS] Test name: description
- [FAIL] Test name: description — [what went wrong]

## Level 2: Complex Operations (X/Y passed)
- [PASS] Test name: description
- [FAIL] Test name: description — [what went wrong]

## Level 3: Adversarial Testing (X/Y passed)
- [PASS] Test name: description
- [FAIL] Test name: description — [what went wrong]

## Level 4: Cross-Cutting Scenarios (X/Y passed)
- [PASS] Test name: description
- [FAIL] Test name: description — [what went wrong]

Overall: X/Y passed across all levels
```

For each failure, include the relevant screenshot, output, or state observation.

Update `.turbo/test-plan.md` by checking off completed tests and annotating results.

## Rules

- Always clean up: close browser sessions, stop dev servers started by this skill.
- Never modify application code. This skill is read-only verification. Report failures without attempting to fix them.
- If the dev server fails to start, report the error and stop.
- To diagnose failures, run the `/investigate` skill on the test report.
