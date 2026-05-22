---
name: manual_tests.run_fire_tests
description: "Runs all 6 'should fire' tests serially with resets between each. Use after NOT-fire tests to verify rules fire correctly."
user-invocable: false

---

# manual_tests.run_fire_tests

**Step 3/4** in **run_all** workflow

> Run all manual tests: reset, NOT-fire tests, fire tests, and infinite block tests

> Runs all manual hook/rule tests using sub-agents. Use when validating that DeepWork rules fire correctly.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/manual_tests.run_not_fire_tests`

## Instructions

**Goal**: Runs all 6 'should fire' tests serially with resets between each. Use after NOT-fire tests to verify rules fire correctly.

# Run Should-Fire Tests

## Objective

Run all "should fire" tests in **serial** sub-agents to verify that rules fire correctly when their trigger conditions are met without safety conditions.

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

Why serial execution is required:
- These tests edit ONLY the trigger file (not the safety)
- If multiple sub-agents run in parallel, sub-agent A's hook will see changes from sub-agent B
- This causes cross-contamination: A gets blocked by rules triggered by B's changes
- Run one test, observe the hook, reset, then run the next

## Task

Run all 6 "should fire" tests in **serial** sub-agents, resetting between each, and verify that blocking hooks fire automatically.

### Process

For EACH test below, follow this cycle:

1. **Launch a sub-agent** using the Task tool with:
   - `model: "haiku"` - Use the fast model to minimize cost and latency
   - `max_turns: 5` - Prevent sub-agents from hanging indefinitely
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
5. **Record the result** - pass if hook fired (visible block OR queue entry), fail if neither
6. **Reset** (MANDATORY after each test) - follow the reset step instructions:
   ```bash
   git reset HEAD manual_tests/ && git checkout -- manual_tests/ && rm -f manual_tests/test_created_mode/new_config.yml
   deepwork rules clear_queue
   ```
   See [reset.md](reset.md) for detailed explanation of these commands.
7. **Check for early termination**: If **2 tests have now failed**, immediately:
   - Stop running any remaining tests
   - Report the results summary showing which tests passed/failed
   - The job halts here - do NOT proceed with remaining tests
8. **Proceed to the next test** (only if fewer than 2 failures)

**IMPORTANT**: Only launch ONE sub-agent at a time. Wait for it to complete and reset before launching the next.

### Test Cases (run serially)

**Test 1: Trigger/Safety**
- Sub-agent prompt: "Edit ONLY `manual_tests/test_trigger_safety_mode/feature.py` to add a comment. Do NOT edit the `_doc.md` file."
- Sub-agent config: `model: "haiku"`, `max_turns: 5`
- Expected: Hook fires with prompt about updating documentation

**Test 2: Set Mode**
- Sub-agent prompt: "Edit ONLY `manual_tests/test_set_mode/module_source.py` to add a comment. Do NOT edit the `_test.py` file."
- Sub-agent config: `model: "haiku"`, `max_turns: 5`
- Expected: Hook fires with prompt about updating tests

**Test 3: Pair Mode**
- Sub-agent prompt: "Edit ONLY `manual_tests/test_pair_mode/handler_trigger.py` to add a comment. Do NOT edit the `_expected.md` file."
- Sub-agent config: `model: "haiku"`, `max_turns: 5`
- Expected: Hook fires with prompt about updating expected output

**Test 4: Command Action**
- Sub-agent prompt: "Edit `manual_tests/test_command_action/input.txt` to add some text."
- Sub-agent config: `model: "haiku"`, `max_turns: 5`
- Expected: Command runs automatically, appending to the log file (this rule always runs, no safety condition)

**Test 5: Multi Safety**
- Sub-agent prompt: "Edit ONLY `manual_tests/test_multi_safety/core.py` to add a comment. Do NOT edit any of the safety files (`_safety_a.md`, `_safety_b.md`, or `_safety_c.md`)."
- Sub-agent config: `model: "haiku"`, `max_turns: 5`
- Expected: Hook fires with prompt about updating safety documentation

**Test 6: Created Mode**
- Sub-agent prompt: "Create a NEW file `manual_tests/test_created_mode/new_config.yml` with some YAML content. This must be a NEW file, not a modification."
- Sub-agent config: `model: "haiku"`, `max_turns: 5`
- Expected: Hook fires with prompt about new configuration files

### Results Tracking

Record the result after each test:

| Test Case | Should Fire | Visible Block? | Queue Entry? | Result |
|-----------|-------------|:--------------:|:------------:|:------:|
| Trigger/Safety | Edit .py only | | | |
| Set Mode | Edit _source.py only | | | |
| Pair Mode | Edit _trigger.py only | | | |
| Command Action | Edit .txt | | | |
| Multi Safety | Edit .py only | | | |
| Created Mode | Create NEW .yml | | | |

**Queue Entry Status Guide:**
- If queue has entry with status "queued" -> Hook fired, rule was shown to agent
- If queue has entry with status "passed" -> Hook fired, rule was satisfied
- If queue is empty -> Hook did NOT fire

## Quality Criteria

- **Sub-agents spawned**: Tests were run using the Task tool to spawn sub-agents - the main agent did NOT edit files directly
- **Correct sub-agent config**: All sub-agents used `model: "haiku"` and `max_turns: 5`
- **Serial execution**: Sub-agents were launched ONE AT A TIME, not in parallel
- **Reset between tests**: Reset step was followed after each test
- **Hooks fired automatically**: The main agent observed the blocking hooks firing automatically when each sub-agent returned - the agent did NOT manually run rules_check
- **Early termination on 2 failures**: If 2 tests failed, testing halted immediately and results were reported
- **Results recorded**: Pass/fail status was recorded for each test case
- When all criteria are met, include `<promise>Quality Criteria Met</promise>` in your response

## Reference

See [test_reference.md](test_reference.md) for the complete test matrix and rule descriptions.

## Context

This step runs after the "should NOT fire" tests. These tests verify that rules correctly fire when trigger conditions are met without safety conditions. The serial execution with resets is essential to prevent cross-contamination between tests. Infinite block tests are handled in a separate step.


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
- `not_fire_results` (from `run_not_fire_tests`)

## Work Branch

Use branch format: `deepwork/manual_tests-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/manual_tests-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `fire_results`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

**Before completing this step, you MUST have your work reviewed against the quality criteria below.**

Use a sub-agent (Haiku model) to review your work against these criteria:

**Criteria (all must be satisfied)**:
1. **Sub-Agents Used**: Did the main agent spawn a sub-agent (using the Task tool) for EACH test? The main agent must NOT edit the test files directly.
2. **Sub-Agent Config**: Did all sub-agents use `model: "haiku"` and `max_turns: 5`?
3. **Serial Execution**: Were sub-agents launched ONE AT A TIME (not in parallel) to prevent cross-contamination?
4. **Hooks Fired Automatically**: Did the main agent observe the blocking hooks firing automatically when each sub-agent returned? The agent must NOT manually run the rules_check command.
5. **Reset Between Tests**: Was the reset step called internally after each test to revert files and prevent cross-contamination?
6. **Early Termination**: If 2 tests failed, did testing halt immediately with results reported?
7. **Results Recorded**: Did the main agent track pass/fail status for each test case?
**Review Process**:
1. Once you believe your work is complete, spawn a sub-agent using Haiku to review your work against the quality criteria above
2. The sub-agent should examine your outputs and verify each criterion is met
3. If the sub-agent identifies valid issues, fix them
4. Have the sub-agent review again until all valid feedback has been addressed
5. Only mark the step complete when the sub-agent confirms all criteria are satisfied

## On Completion

1. Verify outputs are created
2. Inform user: "run_all step 3/4 complete, outputs: fire_results"
3. **Continue workflow**: Use Skill tool to invoke `/manual_tests.infinite_block_tests`

---

**Reference files**: `.deepwork/jobs/manual_tests/job.yml`, `.deepwork/jobs/manual_tests/steps/run_fire_tests.md`