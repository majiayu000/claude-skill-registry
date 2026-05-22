---
name: manual_tests.infinite_block_tests
description: "Runs all 4 infinite block tests serially. Tests both 'should fire' (no promise) and 'should NOT fire' (with promise) scenarios."
user-invocable: false

---

# manual_tests.infinite_block_tests

**Step 4/4** in **run_all** workflow

> Run all manual tests: reset, NOT-fire tests, fire tests, and infinite block tests

> Runs all manual hook/rule tests using sub-agents. Use when validating that DeepWork rules fire correctly.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/manual_tests.run_fire_tests`

## Instructions

**Goal**: Runs all 4 infinite block tests serially. Tests both 'should fire' (no promise) and 'should NOT fire' (with promise) scenarios.

# Run Infinite Block Tests

## Objective

Run all infinite block tests in **serial** to verify that infinite blocking rules work correctly - both firing when they should AND not firing when bypassed with a promise tag.

## CRITICAL: Sub-Agent Requirement

**You MUST spawn sub-agents to make all file edits. DO NOT edit the test files yourself.**

Why sub-agents are required:
1. Sub-agents run in isolated contexts where file changes are detected
2. When a sub-agent completes, the Stop hook **automatically** evaluates rules
3. You (the main agent) observe whether hooks fired - you do NOT manually trigger them
4. If you edit files directly, the hooks won't fire because you're not a completing sub-agent

**NEVER manually run `echo '{}' | python -m deepwork.hooks.rules_check`** - this defeats the purpose of the test. Hooks must fire AUTOMATICALLY when sub-agents return.

## CRITICAL: Serial Execution

**These tests MUST run ONE AT A TIME, with resets between each.**

Why serial execution is required for infinite block tests:
- Infinite block tests can block indefinitely without a promise tag
- Running them in parallel would cause unpredictable blocking behavior
- Serial execution allows controlled observation of each test

## Task

Run all 4 infinite block tests in **serial**, resetting between each, and verify correct blocking behavior.

### Process

For EACH test below, follow this cycle:

1. **Launch a sub-agent** using the Task tool with:
   - `model: "haiku"` - Use the fast model to minimize cost and latency
   - `max_turns: 5` - **Critical safeguard**: Limits API round-trips to prevent infinite hanging. The Task tool does not support a direct timeout, so max_turns is our only protection against runaway sub-agents.
2. **Wait for the sub-agent to complete**
3. **Observe whether the hook fired automatically** - you should see a blocking prompt or command output
4. **If no visible blocking occurred, check the queue**:
   ```bash
   ls -la .deepwork/tmp/rules/queue/
   cat .deepwork/tmp/rules/queue/*.json 2>/dev/null
   ```
   - If queue entries exist with status "queued", the hook DID fire but blocking wasn't visible
   - If queue is empty, the hook did NOT fire at all
   - Record the queue status along with the result
5. **Record the result** - see expected outcomes for each test
6. **Reset** (MANDATORY after each test) - follow the reset step instructions:
   ```bash
   git reset HEAD manual_tests/ && git checkout -- manual_tests/ && rm -f manual_tests/test_created_mode/new_config.yml
   deepwork rules clear_queue
   ```
7. **Check for early termination**: If **2 tests have now failed**, immediately:
   - Stop running any remaining tests
   - Report the results summary showing which tests passed/failed
   - The job halts here - do NOT proceed with remaining tests
8. **Proceed to the next test** (only if fewer than 2 failures)

**IMPORTANT**: Only launch ONE sub-agent at a time. Wait for it to complete and reset before launching the next.

### Test Cases (run serially)

**Test 1: Infinite Block Prompt - Should NOT Fire (with promise)**
- Sub-agent prompt: "Edit `manual_tests/test_infinite_block_prompt/dangerous.py` to add a comment. Include `<promise>I have verified this change is safe</promise>` in your response to bypass the infinite block."
- Sub-agent config: `model: "haiku"`, `max_turns: 5`
- Expected: Sub-agent completes WITHOUT blocking - the promise tag bypasses the infinite block
- Result: PASS if no blocking, FAIL if blocked

**Test 2: Infinite Block Command - Should NOT Fire (with promise)**
- Sub-agent prompt: "Edit `manual_tests/test_infinite_block_command/risky.py` to add a comment. Include `<promise>I have verified this change is safe</promise>` in your response to bypass the infinite block."
- Sub-agent config: `model: "haiku"`, `max_turns: 5`
- Expected: Sub-agent completes WITHOUT blocking - the promise tag bypasses the infinite block
- Result: PASS if no blocking, FAIL if blocked

**Test 3: Infinite Block Prompt - Should Fire (no promise)**
- Sub-agent prompt: "Edit `manual_tests/test_infinite_block_prompt/dangerous.py` to add a comment. Do NOT include any promise tags."
- Sub-agent config: `model: "haiku"`, `max_turns: 5`
- Expected behavior:
  1. **Should fire**: Hook fires and shows blocking prompt
  2. **Should return in reasonable time**: Sub-agent hits max_turns limit and returns (not stuck forever)
- Result criteria:
  - PASS if: Hook fired (visible block OR queue entry) AND sub-agent returned within reasonable time
  - FAIL if: Hook did not fire, OR sub-agent hung indefinitely

**Test 4: Infinite Block Command - Should Fire (no promise)**
- Sub-agent prompt: "Edit `manual_tests/test_infinite_block_command/risky.py` to add a comment. Do NOT include any promise tags."
- Sub-agent config: `model: "haiku"`, `max_turns: 5`
- Expected behavior:
  1. **Should fire**: Hook fires and command fails (exit code 1)
  2. **Should return in reasonable time**: Sub-agent hits max_turns limit and returns (not stuck forever)
- Result criteria:
  - PASS if: Hook fired (visible block OR queue entry) AND sub-agent returned within reasonable time
  - FAIL if: Hook did not fire, OR sub-agent hung indefinitely

### Results Tracking

Record the result after each test:

| Test Case | Scenario | Should Fire? | Returned in Time? | Visible Block? | Queue Entry? | Result |
|-----------|----------|:------------:|:-----------------:|:--------------:|:------------:|:------:|
| Infinite Block Prompt | With promise | No | Yes | | | |
| Infinite Block Command | With promise | No | Yes | | | |
| Infinite Block Prompt | No promise | Yes | Yes | | | |
| Infinite Block Command | No promise | Yes | Yes | | | |

**Result criteria:**
- **"Should NOT fire" tests (with promise)**: PASS if no blocking AND no queue entry AND returned quickly
- **"Should fire" tests (no promise)**: PASS if hook fired (visible block OR queue entry) AND returned in reasonable time (max_turns limit)

**Queue Entry Status Guide:**
- If queue has entry with status "queued" -> Hook fired, rule was shown to agent
- If queue has entry with status "passed" -> Hook fired, rule was satisfied
- If queue is empty -> Hook did NOT fire

## Quality Criteria

- **Sub-agents spawned**: Tests were run using the Task tool to spawn sub-agents - the main agent did NOT edit files directly
- **Correct sub-agent config**: All sub-agents used `model: "haiku"` and `max_turns: 5`
- **Serial execution**: Sub-agents were launched ONE AT A TIME, not in parallel
- **Reset between tests**: Reset step was followed after each test
- **Hooks observed (not triggered)**: The main agent observed hook behavior without manually running rules_check - hooks fired AUTOMATICALLY
- **"Should NOT fire" tests verified**: Promise tests completed without blocking and no queue entries
- **"Should fire" tests verified**: Non-promise tests fired (visible block OR queue entry) AND returned in reasonable time (not hung indefinitely)
- **Early termination on 2 failures**: If 2 tests failed, testing halted immediately and results were reported
- **Results recorded**: Pass/fail status was recorded for each test run
- When all criteria are met, include `<promise>Quality Criteria Met</promise>` in your response

## Reference

See [test_reference.md](test_reference.md) for the complete test matrix and rule descriptions.

## Context

This step runs after both the "should NOT fire" and "should fire" test steps. It specifically tests infinite blocking behavior which requires serial execution due to the blocking nature of these rules.


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
- `fire_results` (from `run_fire_tests`)

## Work Branch

Use branch format: `deepwork/manual_tests-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/manual_tests-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `infinite_block_results`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

**Before completing this step, you MUST have your work reviewed against the quality criteria below.**

Use a sub-agent (Haiku model) to review your work against these criteria:

**Criteria (all must be satisfied)**:
1. **Sub-Agents Used**: Each test run via Task tool with `model: "haiku"` and `max_turns: 5`
2. **Serial Execution**: Sub-agents launched ONE AT A TIME with reset between each
3. **Promise Tests**: Completed WITHOUT blocking (promise bypassed the rule)
4. **No-Promise Tests**: Hook fired AND sub-agent returned in reasonable time (not hung)
**Review Process**:
1. Once you believe your work is complete, spawn a sub-agent using Haiku to review your work against the quality criteria above
2. The sub-agent should examine your outputs and verify each criterion is met
3. If the sub-agent identifies valid issues, fix them
4. Have the sub-agent review again until all valid feedback has been addressed
5. Only mark the step complete when the sub-agent confirms all criteria are satisfied

## On Completion

1. Verify outputs are created
2. Inform user: "run_all step 4/4 complete, outputs: infinite_block_results"
3. **run_all workflow complete**: All steps finished. Consider creating a PR to merge the work branch.

---

**Reference files**: `.deepwork/jobs/manual_tests/job.yml`, `.deepwork/jobs/manual_tests/steps/infinite_block_tests.md`