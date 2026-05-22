---
name: manual_tests.run_not_fire_tests
description: "Runs all 'should NOT fire' tests in parallel sub-agents. Use to verify rules don't fire when safety conditions are met."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Sub-Agents Used**: Did the main agent spawn sub-agents (using the Task tool) to make the file edits? The main agent must NOT edit the test files directly.
            2. **Parallel Execution**: Were multiple sub-agents launched in parallel (in a single message with multiple Task tool calls)?
            3. **Hooks Observed**: Did the main agent observe that no blocking hooks fired when the sub-agents returned? The hooks fire AUTOMATICALLY - the agent must NOT manually run the rules_check command.
            4. **All Tests Run**: Were all 8 'should NOT fire' tests executed (trigger/safety, set, pair forward, pair reverse, multi safety, infinite block prompt, infinite block command, created)?
            5. **Git Reverted**: Were changes reverted and queue cleared after tests completed using `git checkout -- manual_tests/` and `rm -rf .deepwork/tmp/rules/queue/*.json`?

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

            1. **Sub-Agents Used**: Did the main agent spawn sub-agents (using the Task tool) to make the file edits? The main agent must NOT edit the test files directly.
            2. **Parallel Execution**: Were multiple sub-agents launched in parallel (in a single message with multiple Task tool calls)?
            3. **Hooks Observed**: Did the main agent observe that no blocking hooks fired when the sub-agents returned? The hooks fire AUTOMATICALLY - the agent must NOT manually run the rules_check command.
            4. **All Tests Run**: Were all 8 'should NOT fire' tests executed (trigger/safety, set, pair forward, pair reverse, multi safety, infinite block prompt, infinite block command, created)?
            5. **Git Reverted**: Were changes reverted and queue cleared after tests completed using `git checkout -- manual_tests/` and `rm -rf .deepwork/tmp/rules/queue/*.json`?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
---

# manual_tests.run_not_fire_tests

**Step 1/2** in **manual_tests** workflow

> Runs all manual hook/rule tests using sub-agents. Use when validating that DeepWork rules fire correctly.


## Instructions

**Goal**: Runs all 'should NOT fire' tests in parallel sub-agents. Use to verify rules don't fire when safety conditions are met.

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

Run all 8 "should NOT fire" tests in **parallel** sub-agents, then verify no blocking hooks fired.

### Process

1. **Launch parallel sub-agents for all "should NOT fire" tests**

   Use the Task tool to spawn **ALL of the following sub-agents in a SINGLE message** (parallel execution). Each sub-agent should use a fast model like haiku.

   **Sub-agent prompts (launch all 8 in parallel):**

   a. **Trigger/Safety test** - "Edit `manual_tests/test_trigger_safety_mode/feature.py` to add a comment, AND edit `manual_tests/test_trigger_safety_mode/feature_doc.md` to add a note. Both files must be edited so the rule does NOT fire."

   b. **Set Mode test** - "Edit `manual_tests/test_set_mode/module_source.py` to add a comment, AND edit `manual_tests/test_set_mode/module_test.py` to add a test comment. Both files must be edited so the rule does NOT fire."

   c. **Pair Mode (forward) test** - "Edit `manual_tests/test_pair_mode/handler_trigger.py` to add a comment, AND edit `manual_tests/test_pair_mode/handler_expected.md` to add a note. Both files must be edited so the rule does NOT fire."

   d. **Pair Mode (reverse) test** - "Edit ONLY `manual_tests/test_pair_mode/handler_expected.md` to add a note. Only the expected file should be edited - this tests that the pair rule only fires in one direction."

   e. **Multi Safety test** - "Edit `manual_tests/test_multi_safety/core.py` to add a comment, AND edit `manual_tests/test_multi_safety/core_safety_a.md` to add a note. Both files must be edited so the rule does NOT fire."

   f. **Infinite Block Prompt test** - "Edit `manual_tests/test_infinite_block_prompt/dangerous.py` to add a comment. Include `<promise>I have verified this change is safe</promise>` in your response to bypass the infinite block."

   g. **Infinite Block Command test** - "Edit `manual_tests/test_infinite_block_command/risky.py` to add a comment. Include `<promise>I have verified this change is safe</promise>` in your response to bypass the infinite block."

   h. **Created Mode test** - "Modify the EXISTING file `manual_tests/test_created_mode/existing.yml` by adding a comment. Do NOT create a new file - only modify the existing one. The created mode rule should NOT fire for modifications."

2. **Observe the results**

   When each sub-agent returns:
   - **If no blocking hook fired**: The test PASSED - the rule correctly did NOT fire
   - **If a blocking hook fired**: The test FAILED - investigate why the rule fired when it shouldn't have

   **Remember**: You are OBSERVING whether hooks fired automatically. Do NOT run any verification commands manually.

3. **Record the results**

   Track which tests passed and which failed:

   | Test Case | Should NOT Fire | Result |
   |-----------|:---------------:|:------:|
   | Trigger/Safety | Edit both files | |
   | Set Mode | Edit both files | |
   | Pair Mode (forward) | Edit both files | |
   | Pair Mode (reverse) | Edit expected only | |
   | Multi Safety | Edit both files | |
   | Infinite Block Prompt | Promise tag | |
   | Infinite Block Command | Promise tag | |
   | Created Mode | Modify existing | |

4. **Revert all changes and clear queue**

   After all tests complete, run:
   ```bash
   git checkout -- manual_tests/
   rm -rf .deepwork/tmp/rules/queue/*.json 2>/dev/null || true
   ```

   This cleans up the test files AND clears the rules queue before the "should fire" tests run. The queue must be cleared because rules that have already been shown to the agent (status=QUEUED) won't fire again until the queue is cleared.

## Quality Criteria

- **Sub-agents spawned**: All 8 tests were run using the Task tool to spawn sub-agents - the main agent did NOT edit files directly
- **Parallel execution**: All 8 sub-agents were launched in a single message (parallel)
- **Hooks observed (not triggered)**: The main agent observed hook behavior without manually running rules_check
- **No unexpected blocks**: All tests passed - no blocking hooks fired
- **Changes reverted and queue cleared**: `git checkout -- manual_tests/` and `rm -rf .deepwork/tmp/rules/queue/*.json` was run after tests completed
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Reference

See [test_reference.md](test_reference.md) for the complete test matrix and rule descriptions.

## Context

This step runs first and tests that rules correctly do NOT fire when safety conditions are met. The "should fire" tests run after these complete and the working directory is reverted.


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

Stop hooks will automatically validate your work. The loop continues until all criteria pass.

**Criteria (all must be satisfied)**:
1. **Sub-Agents Used**: Did the main agent spawn sub-agents (using the Task tool) to make the file edits? The main agent must NOT edit the test files directly.
2. **Parallel Execution**: Were multiple sub-agents launched in parallel (in a single message with multiple Task tool calls)?
3. **Hooks Observed**: Did the main agent observe that no blocking hooks fired when the sub-agents returned? The hooks fire AUTOMATICALLY - the agent must NOT manually run the rules_check command.
4. **All Tests Run**: Were all 8 'should NOT fire' tests executed (trigger/safety, set, pair forward, pair reverse, multi safety, infinite block prompt, infinite block command, created)?
5. **Git Reverted**: Were changes reverted and queue cleared after tests completed using `git checkout -- manual_tests/` and `rm -rf .deepwork/tmp/rules/queue/*.json`?


**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "Step 1/2 complete, outputs: not_fire_results"
3. **Continue workflow**: Use Skill tool to invoke `/manual_tests.run_fire_tests`

---

**Reference files**: `.deepwork/jobs/manual_tests/job.yml`, `.deepwork/jobs/manual_tests/steps/run_not_fire_tests.md`