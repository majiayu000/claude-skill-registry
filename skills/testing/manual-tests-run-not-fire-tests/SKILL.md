---
name: manual_tests.run_not_fire_tests
description: "Runs all 6 'should NOT fire' tests in parallel sub-agents. Use to verify rules don't fire when safety conditions are met."
user-invocable: false

---

# manual_tests.run_not_fire_tests

**Step 2/4** in **run_all** workflow

> Run all manual tests: reset, NOT-fire tests, fire tests, and infinite block tests

> Runs all manual hook/rule tests using sub-agents. Use when validating that DeepWork rules fire correctly.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/manual_tests.reset`

## Instructions

**Goal**: Runs all 6 'should NOT fire' tests in parallel sub-agents. Use to verify rules don't fire when safety conditions are met.

# Run Should-NOT-Fire Tests

## Objective

Run all "should NOT fire" tests in parallel sub-agents to verify that rules do not fire when their safety conditions are met.

## CRITICAL: Sub-Agent Requirement

**You MUST spawn sub-agents to make all file edits. DO NOT edit the test files yourself.**

Why sub-agents are required:
1. Sub-agents run in isolated contexts where file changes are detected
2. When a sub-agent completes, the Stop hook **automatically** evaluates rules
3. You (the main agent) observe whether hooks fired - you do NOT manually trigger them
4. If you edit files directly, the hooks won't fire because you're not a completing sub-agent

**NEVER manually run `echo '{}' | python -m deepwork.hooks.rules_check`** - this defeats the purpose of the test. Hooks must fire AUTOMATICALLY when sub-agents return.

## Task

Run all 6 "should NOT fire" tests in **parallel** sub-agents, then verify no blocking hooks fired.

### Process

1. **Launch parallel sub-agents for all "should NOT fire" tests**

   Use the Task tool to spawn **ALL of the following sub-agents in a SINGLE message** (parallel execution).

   **Sub-agent configuration for ALL sub-agents:**
   - `model: "haiku"` - Use the fast model to minimize cost and latency
   - `max_turns: 5` - Prevent sub-agents from hanging indefinitely

   **Sub-agent prompts (launch all 6 in parallel):**

   a. **Trigger/Safety test** - "Edit `manual_tests/test_trigger_safety_mode/feature.py` to add a comment, AND edit `manual_tests/test_trigger_safety_mode/feature_doc.md` to add a note. Both files must be edited so the rule does NOT fire."

   b. **Set Mode test** - "Edit `manual_tests/test_set_mode/module_source.py` to add a comment, AND edit `manual_tests/test_set_mode/module_test.py` to add a test comment. Both files must be edited so the rule does NOT fire."

   c. **Pair Mode (forward) test** - "Edit `manual_tests/test_pair_mode/handler_trigger.py` to add a comment, AND edit `manual_tests/test_pair_mode/handler_expected.md` to add a note. Both files must be edited so the rule does NOT fire."

   d. **Pair Mode (reverse) test** - "Edit ONLY `manual_tests/test_pair_mode/handler_expected.md` to add a note. Only the expected file should be edited - this tests that the pair rule only fires in one direction."

   e. **Multi Safety test** - "Edit `manual_tests/test_multi_safety/core.py` to add a comment, AND edit `manual_tests/test_multi_safety/core_safety_a.md` to add a note. Both files must be edited so the rule does NOT fire."

   f. **Created Mode test** - "Modify the EXISTING file `manual_tests/test_created_mode/existing.yml` by adding a comment. Do NOT create a new file - only modify the existing one. The created mode rule should NOT fire for modifications."

2. **Observe the results**

   When each sub-agent returns:
   - **If no blocking hook fired**: Preliminary pass - proceed to queue verification
   - **If a blocking hook fired**: The test FAILED - investigate why the rule fired when it shouldn't have

   **Remember**: You are OBSERVING whether hooks fired automatically. Do NOT run any verification commands manually during sub-agent execution.

3. **Verify no queue entries** (CRITICAL for "should NOT fire" tests)

   After ALL sub-agents have completed, verify the rules queue is empty:
   ```bash
   ls -la .deepwork/tmp/rules/queue/
   cat .deepwork/tmp/rules/queue/*.json 2>/dev/null
   ```

   - **If queue is empty**: All tests PASSED - rules correctly did not fire
   - **If queue has entries**: Tests FAILED - rules fired when they shouldn't have. Check which rule fired and investigate.

   This verification is essential because some rules may fire without visible blocking but still create queue entries.

4. **Record the results and check for early termination**

   Track which tests passed and which failed:

   | Test Case | Should NOT Fire | Visible Block? | Queue Entry? | Result |
   |-----------|:---------------:|:--------------:|:------------:|:------:|
   | Trigger/Safety | Edit both files | | | |
   | Set Mode | Edit both files | | | |
   | Pair Mode (forward) | Edit both files | | | |
   | Pair Mode (reverse) | Edit expected only | | | |
   | Multi Safety | Edit both files | | | |
   | Created Mode | Modify existing | | | |

   **Result criteria**: PASS only if NO visible block AND NO queue entry. FAIL if either occurred.

   **EARLY TERMINATION**: If **2 tests have failed**, immediately:
   1. Stop running any remaining tests
   2. Reset (see step 5)
   3. Report the results summary showing which tests passed/failed
   4. Do NOT proceed to the next step - the job halts here

5. **Reset** (MANDATORY - call the reset step internally)

   **IMPORTANT**: This step is MANDATORY and must run regardless of whether tests passed or failed.

   Follow the reset step instructions. Run these commands to clean up:
   ```bash
   git reset HEAD manual_tests/ && git checkout -- manual_tests/ && rm -f manual_tests/test_created_mode/new_config.yml
   deepwork rules clear_queue
   ```

   See [reset.md](reset.md) for detailed explanation of these commands.

## Quality Criteria

- **Sub-agents spawned**: All 6 tests were run using the Task tool to spawn sub-agents - the main agent did NOT edit files directly
- **Correct sub-agent config**: All sub-agents used `model: "haiku"` and `max_turns: 5`
- **Parallel execution**: All 6 sub-agents were launched in a single message (parallel)
- **Hooks observed (not triggered)**: The main agent observed hook behavior without manually running rules_check
- **Queue verified empty**: After all sub-agents completed, the rules queue was checked and confirmed empty (no queue entries = rules did not fire)
- **Early termination on 2 failures**: If 2 tests failed, testing halted immediately and results were reported
- **Reset performed**: Reset step was followed after tests completed (regardless of pass/fail)
- When all criteria are met, include `<promise>Quality Criteria Met</promise>` in your response

## Reference

See [test_reference.md](test_reference.md) for the complete test matrix and rule descriptions.

## Context

This step runs after the reset step (which ensures a clean environment) and tests that rules correctly do NOT fire when safety conditions are met. The "should fire" tests run after these complete. Infinite block tests are handled in a separate step.


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


## Required Inputs


**Files from Previous Steps** - Read these first:
- `clean_environment` (from `reset`)

## Work Branch

Use branch format: `deepwork/manual_tests-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/manual_tests-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `not_fire_results`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

**Before completing this step, you MUST have your work reviewed against the quality criteria below.**

Use a sub-agent (Haiku model) to review your work against these criteria:

**Criteria (all must be satisfied)**:
1. **Sub-Agents Used**: Did the main agent spawn sub-agents (using the Task tool) to make the file edits? The main agent must NOT edit the test files directly.
2. **Sub-Agent Config**: Did all sub-agents use `model: "haiku"` and `max_turns: 5`?
3. **Parallel Execution**: Were all 6 sub-agents launched in parallel (in a single message with multiple Task tool calls)?
4. **Hooks Observed**: Did the main agent observe that no blocking hooks fired when the sub-agents returned? The hooks fire AUTOMATICALLY - the agent must NOT manually run the rules_check command.
5. **Queue Verified Empty**: After all sub-agents completed, was the rules queue checked and confirmed empty (no entries = rules did not fire)?
6. **Early Termination**: If 2 tests failed, did testing halt immediately with results reported?
7. **Reset Performed**: Was the reset step called internally after tests completed (or after early termination)?
**Review Process**:
1. Once you believe your work is complete, spawn a sub-agent using Haiku to review your work against the quality criteria above
2. The sub-agent should examine your outputs and verify each criterion is met
3. If the sub-agent identifies valid issues, fix them
4. Have the sub-agent review again until all valid feedback has been addressed
5. Only mark the step complete when the sub-agent confirms all criteria are satisfied

## On Completion

1. Verify outputs are created
2. Inform user: "run_all step 2/4 complete, outputs: not_fire_results"
3. **Continue workflow**: Use Skill tool to invoke `/manual_tests.run_fire_tests`

---

**Reference files**: `.deepwork/jobs/manual_tests/job.yml`, `.deepwork/jobs/manual_tests/steps/run_not_fire_tests.md`