---
name: manual_tests.reset
description: "Runs FIRST to ensure clean environment. Also called internally by other steps when they need to revert changes and clear the queue."
user-invocable: false

---

# manual_tests.reset

**Step 1/4** in **run_all** workflow

> Run all manual tests: reset, NOT-fire tests, fire tests, and infinite block tests

> Runs all manual hook/rule tests using sub-agents. Use when validating that DeepWork rules fire correctly.


## Instructions

**Goal**: Runs FIRST to ensure clean environment. Also called internally by other steps when they need to revert changes and clear the queue.

# Reset Manual Tests Environment

## Objective

Reset the manual tests environment by reverting all file changes and clearing the rules queue.

## Purpose

This step contains all the reset logic that other steps can call when they need to clean up between or after tests. It ensures consistent cleanup across all test steps.

## Reset Commands

Run these commands to reset the environment:

```bash
git reset HEAD manual_tests/ && git checkout -- manual_tests/ && rm -f manual_tests/test_created_mode/new_config.yml
deepwork rules clear_queue
```

## Command Explanation

- `git reset HEAD manual_tests/` - Unstages files from the index (rules_check uses `git add -A` which stages changes)
- `git checkout -- manual_tests/` - Reverts working tree to match HEAD
- `rm -f manual_tests/test_created_mode/new_config.yml` - Removes any new files created during tests (the created mode test creates this file)
- `deepwork rules clear_queue` - Clears the rules queue so rules can fire again (prevents anti-infinite-loop mechanism from blocking subsequent tests)

## When to Reset

- **After each serial test**: Reset immediately after observing the result to prevent cross-contamination
- **After parallel tests complete**: Reset once all parallel sub-agents have returned
- **On early termination**: Reset before reporting failure results
- **Before starting a new test step**: Ensure clean state

## Quality Criteria

- **All changes reverted**: `git status` shows no changes in `manual_tests/`
- **Queue cleared**: `.deepwork/tmp/rules/queue/` is empty
- **New files removed**: `manual_tests/test_created_mode/new_config.yml` does not exist


### Job Context

A workflow for running manual tests that validate DeepWork rules/hooks fire correctly.

The **run_all** workflow tests that rules fire when they should AND do not fire when they shouldn't.
Each test is run in a SUB-AGENT (not the main agent) because:
1. Sub-agents run in isolated contexts where file changes can be detected
2. The Stop hook automatically evaluates rules when each sub-agent completes
3. The main agent can observe whether hooks fired without triggering them manually

CRITICAL: All tests MUST run in sub-agents. The main agent MUST NOT make the file
edits itself - it spawns sub-agents to make edits, then observes whether the hooks
fired automatically when those sub-agents returned.

Sub-agent configuration:
- All sub-agents should use `model: "haiku"` to minimize cost and latency
- All sub-agents should use `max_turns: 5` to prevent hanging indefinitely

Steps:
1. reset - Ensure clean environment before testing (clears queue, reverts files)
2. run_not_fire_tests - Run all "should NOT fire" tests in PARALLEL sub-agents (6 tests)
3. run_fire_tests - Run all "should fire" tests in SERIAL sub-agents with resets between (6 tests)
4. infinite_block_tests - Run infinite block tests in SERIAL (4 tests - both fire and not-fire)

Reset procedure (see steps/reset.md):
- Reset runs FIRST to ensure a clean environment before any tests
- Each step also calls reset internally when needed (between tests, after completion)
- Reset reverts git changes, removes created files, and clears the rules queue

Test types covered:
- Trigger/Safety mode
- Set mode (bidirectional)
- Pair mode (directional)
- Command action
- Multi safety
- Infinite block (prompt and command) - in dedicated step
- Created mode (new files only)



## Work Branch

Use branch format: `deepwork/manual_tests-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/manual_tests-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `clean_environment`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

**Before completing this step, you MUST have your work reviewed against the quality criteria below.**

Use a sub-agent (Haiku model) to review your work against these criteria:

**Criteria (all must be satisfied)**:
1. **Environment Clean**: Git changes reverted, created files removed, and rules queue cleared
**Review Process**:
1. Once you believe your work is complete, spawn a sub-agent using Haiku to review your work against the quality criteria above
2. The sub-agent should examine your outputs and verify each criterion is met
3. If the sub-agent identifies valid issues, fix them
4. Have the sub-agent review again until all valid feedback has been addressed
5. Only mark the step complete when the sub-agent confirms all criteria are satisfied

## On Completion

1. Verify outputs are created
2. Inform user: "run_all step 1/4 complete, outputs: clean_environment"
3. **Continue workflow**: Use Skill tool to invoke `/manual_tests.run_not_fire_tests`

---

**Reference files**: `.deepwork/jobs/manual_tests/job.yml`, `.deepwork/jobs/manual_tests/steps/reset.md`