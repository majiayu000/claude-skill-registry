---
name: manual_tests
description: "Runs all manual hook/rule tests using sub-agents. Use when validating that DeepWork rules fire correctly."
---

# manual_tests

**Multi-step workflow**: Runs all manual hook/rule tests using sub-agents. Use when validating that DeepWork rules fire correctly.

> **CRITICAL**: Always invoke steps using the Skill tool. Never copy/paste step instructions directly.

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


## Available Steps

1. **run_not_fire_tests** - Runs all 'should NOT fire' tests in parallel sub-agents. Use to verify rules don't fire when safety conditions are met.
2. **run_fire_tests** - Runs all 'should fire' tests serially with git reverts between each. Use after NOT-fire tests to verify rules fire correctly. (requires: run_not_fire_tests)

## Execution Instructions

### Step 1: Analyze Intent

Parse any text following `/manual_tests` to determine user intent:
- "run_not_fire_tests" or related terms → start at `manual_tests.run_not_fire_tests`
- "run_fire_tests" or related terms → start at `manual_tests.run_fire_tests`

### Step 2: Invoke Starting Step

Use the Skill tool to invoke the identified starting step:
```
Skill tool: manual_tests.run_not_fire_tests
```

### Step 3: Continue Workflow Automatically

After each step completes:
1. Check if there's a next step in the sequence
2. Invoke the next step using the Skill tool
3. Repeat until workflow is complete or user intervenes

### Handling Ambiguous Intent

If user intent is unclear, use AskUserQuestion to clarify:
- Present available steps as numbered options
- Let user select the starting point

## Guardrails

- Do NOT copy/paste step instructions directly; always use the Skill tool to invoke steps
- Do NOT skip steps in the workflow unless the user explicitly requests it
- Do NOT proceed to the next step if the current step's outputs are incomplete
- Do NOT make assumptions about user intent; ask for clarification when ambiguous

## Context Files

- Job definition: `.deepwork/jobs/manual_tests/job.yml`