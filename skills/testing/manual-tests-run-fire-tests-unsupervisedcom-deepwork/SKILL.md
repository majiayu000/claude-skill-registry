---
name: manual_tests.run_fire_tests
description: "Runs all 'should fire' tests serially with git reverts between each. Use after NOT-fire tests to verify rules fire correctly."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Sub-Agents Used**: Did the main agent spawn a sub-agent (using the Task tool) for EACH test? The main agent must NOT edit the test files directly.
            2. **Serial Execution**: Were sub-agents launched ONE AT A TIME (not in parallel) to prevent cross-contamination?
            3. **Hooks Fired Automatically**: Did the main agent observe the blocking hooks firing automatically when each sub-agent returned? The agent must NOT manually run the rules_check command.
            4. **Git Reverted Between Tests**: Was `git checkout -- manual_tests/` and `rm -rf .deepwork/tmp/rules/queue/*.json` run between each test to prevent cross-contamination?
            5. **All Tests Run**: Were all 8 'should fire' tests executed (trigger/safety, set, pair, command action, multi safety, infinite block prompt, infinite block command, created)?
            6. **Results Recorded**: Did the main agent track pass/fail status for each test case?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
  SubagentStop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Sub-Agents Used**: Did the main agent spawn a sub-agent (using the Task tool) for EACH test? The main agent must NOT edit the test files directly.
            2. **Serial Execution**: Were sub-agents launched ONE AT A TIME (not in parallel) to prevent cross-contamination?
            3. **Hooks Fired Automatically**: Did the main agent observe the blocking hooks firing automatically when each sub-agent returned? The agent must NOT manually run the rules_check command.
            4. **Git Reverted Between Tests**: Was `git checkout -- manual_tests/` and `rm -rf .deepwork/tmp/rules/queue/*.json` run between each test to prevent cross-contamination?
            5. **All Tests Run**: Were all 8 'should fire' tests executed (trigger/safety, set, pair, command action, multi safety, infinite block prompt, infinite block command, created)?
            6. **Results Recorded**: Did the main agent track pass/fail status for each test case?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
---

# manual_tests.run_fire_tests

**Step 2/2** in **manual_tests** workflow

> Runs all manual hook/rule tests using sub-agents. Use when validating that DeepWork rules fire correctly.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/manual_tests.run_not_fire_tests`

## Instructions

**Goal**: Runs all 'should fire' tests serially with git reverts between each. Use after NOT-fire tests to verify rules fire correctly.

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

**These tests MUST run ONE AT A TIME, with git reverts between each.**

Why serial execution is required:
- These tests edit ONLY the trigger file (not the safety)
- If multiple sub-agents run in parallel, sub-agent A's hook will see changes from sub-agent B
- This causes cross-contamination: A gets blocked by rules triggered by B's changes
- Run one test, observe the hook, revert, then run the next

## Task

Run all 8 "should fire" tests in **serial** sub-agents, reverting between each, and verify that blocking hooks fire automatically.

### Process

For EACH test below, follow this cycle:

1. **Launch a sub-agent** using the Task tool (use a fast model like haiku)
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
6. **Revert changes and clear queue**:
   ```bash
   git checkout -- manual_tests/
   rm -rf .deepwork/tmp/rules/queue/*.json 2>/dev/null || true
   ```
   The queue must be cleared because rules that have been shown (status=QUEUED) won't fire again until cleared.
7. **Proceed to the next test**

**IMPORTANT**: Only launch ONE sub-agent at a time. Wait for it to complete and revert before launching the next.

### Test Cases (run serially)

**Test 1: Trigger/Safety**
- Sub-agent prompt: "Edit ONLY `manual_tests/test_trigger_safety_mode/feature.py` to add a comment. Do NOT edit the `_doc.md` file."
- Expected: Hook fires with prompt about updating documentation

**Test 2: Set Mode**
- Sub-agent prompt: "Edit ONLY `manual_tests/test_set_mode/module_source.py` to add a comment. Do NOT edit the `_test.py` file."
- Expected: Hook fires with prompt about updating tests

**Test 3: Pair Mode**
- Sub-agent prompt: "Edit ONLY `manual_tests/test_pair_mode/handler_trigger.py` to add a comment. Do NOT edit the `_expected.md` file."
- Expected: Hook fires with prompt about updating expected output

**Test 4: Command Action**
- Sub-agent prompt: "Edit `manual_tests/test_command_action/input.txt` to add some text."
- Expected: Command runs automatically, appending to the log file (this rule always runs, no safety condition)

**Test 5: Multi Safety**
- Sub-agent prompt: "Edit ONLY `manual_tests/test_multi_safety/core.py` to add a comment. Do NOT edit any of the safety files (`_safety_a.md`, `_safety_b.md`, or `_safety_c.md`)."
- Expected: Hook fires with prompt about updating safety documentation

**Test 6: Infinite Block Prompt**
- Sub-agent prompt: "Edit `manual_tests/test_infinite_block_prompt/dangerous.py` to add a comment. Do NOT include any promise tags."
- Expected: Hook fires and BLOCKS with infinite prompt - sub-agent cannot complete until promise is provided

**Test 7: Infinite Block Command**
- Sub-agent prompt: "Edit `manual_tests/test_infinite_block_command/risky.py` to add a comment. Do NOT include any promise tags."
- Expected: Hook fires and command fails - sub-agent cannot complete until promise is provided

**Test 8: Created Mode**
- Sub-agent prompt: "Create a NEW file `manual_tests/test_created_mode/new_config.yml` with some YAML content. This must be a NEW file, not a modification."
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
| Infinite Block Prompt | Edit .py (no promise) | | | |
| Infinite Block Command | Edit .py (no promise) | | | |
| Created Mode | Create NEW .yml | | | |

**Queue Entry Status Guide:**
- If queue has entry with status "queued" → Hook fired, rule was shown to agent
- If queue has entry with status "passed" → Hook fired, rule was satisfied
- If queue is empty → Hook did NOT fire

## Quality Criteria

- **Sub-agents spawned**: All 8 tests were run using the Task tool to spawn sub-agents - the main agent did NOT edit files directly
- **Serial execution**: Sub-agents were launched ONE AT A TIME, not in parallel
- **Git reverted and queue cleared between tests**: `git checkout -- manual_tests/` and `rm -rf .deepwork/tmp/rules/queue/*.json` was run after each test
- **Hooks observed (not triggered)**: The main agent observed hook behavior without manually running rules_check - hooks fired AUTOMATICALLY
- **Blocking behavior verified**: For each test, the appropriate blocking hook fired automatically when the sub-agent returned
- **Results recorded**: Pass/fail status was recorded for each test
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Reference

See [test_reference.md](test_reference.md) for the complete test matrix and rule descriptions.

## Context

This step runs after the "should NOT fire" tests. These tests verify that rules correctly fire when trigger conditions are met without safety conditions. The serial execution with reverts is essential to prevent cross-contamination between tests.


### Job Context

A workflow for running manual tests that validate DeepWork rules/hooks fire correctly.

This job tests that rules fire when they should AND do not fire when they shouldn't.
Each test is run in a SUB-AGENT (not the main agent) because:
1. Sub-agents run in isolated contexts where file changes can be detected
2. The Stop hook automatically evaluates rules when each sub-agent completes
3. The main agent can observe whether hooks fired without triggering them manually

CRITICAL: All tests MUST run in sub-agents. The main agent MUST NOT make the file
edits itself - it spawns sub-agents to make edits, then observes whether the hooks
fired automatically when those sub-agents returned.

Steps:
1. run_not_fire_tests - Run all "should NOT fire" tests in PARALLEL sub-agents
2. run_fire_tests - Run all "should fire" tests in SERIAL sub-agents with reverts between

Test types covered:
- Trigger/Safety mode
- Set mode (bidirectional)
- Pair mode (directional)
- Command action
- Multi safety
- Infinite block (prompt and command)
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

Stop hooks will automatically validate your work. The loop continues until all criteria pass.

**Criteria (all must be satisfied)**:
1. **Sub-Agents Used**: Did the main agent spawn a sub-agent (using the Task tool) for EACH test? The main agent must NOT edit the test files directly.
2. **Serial Execution**: Were sub-agents launched ONE AT A TIME (not in parallel) to prevent cross-contamination?
3. **Hooks Fired Automatically**: Did the main agent observe the blocking hooks firing automatically when each sub-agent returned? The agent must NOT manually run the rules_check command.
4. **Git Reverted Between Tests**: Was `git checkout -- manual_tests/` and `rm -rf .deepwork/tmp/rules/queue/*.json` run between each test to prevent cross-contamination?
5. **All Tests Run**: Were all 8 'should fire' tests executed (trigger/safety, set, pair, command action, multi safety, infinite block prompt, infinite block command, created)?
6. **Results Recorded**: Did the main agent track pass/fail status for each test case?


**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "Step 2/2 complete, outputs: fire_results"
3. **Workflow complete**: All steps finished. Consider creating a PR to merge the work branch.

---

**Reference files**: `.deepwork/jobs/manual_tests/job.yml`, `.deepwork/jobs/manual_tests/steps/run_fire_tests.md`