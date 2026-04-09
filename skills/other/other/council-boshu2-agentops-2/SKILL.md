---
name: council
description: 'Multi-perspective review for Codex using the current sub-agent runtime. Triggers: "council", "get consensus", "multi-model review", "multi-perspective review", "council validate", "council brainstorm", "council research".'
---

# $council — Consensus Review (Codex Tailoring)

This override captures the Codex-native execution model for council-style judging.

## Modes

- `--quick`: inline review, no sub-agents
- default: 2 judges via `spawn_agent(...)`
- `--deep`: 3 judges via `spawn_agent(...)`

## Codex-Native Flow

### Step 1: Build the review packet

Collect the target files, diff, plan, or report the judges need to review. Keep the packet concise and give each judge one perspective such as correctness, completeness, or edge cases.

### Step 2: Spawn judges

Use one `spawn_agent(...)` call per judge. Use `agent_type="default"` unless the task is purely exploratory, in which case `agent_type="explorer"` is acceptable.

Each judge prompt should include:

- the review target
- the assigned perspective
- the expected verdict vocabulary
- where to write a detailed report if the task is large

### Step 3: Wait and follow up

Use `wait_agent(...)` to collect judge results. If one judge needs clarification, use `send_input(...)` with a narrow follow-up question rather than restarting the council.

### Step 4: Consolidate inline

The lead agent reads the judge outputs and produces the final consensus:

- `PASS` when no judge finds a ship blocker
- `WARN` when concerns exist but no hard blocker exists
- `FAIL` when any judge finds a blocking defect

### Step 5: Close sub-agents

Use `close_agent(...)` on finished judges once their outputs are integrated.

## Constraints

1. Do not assume batch-spawn or worker-report APIs that are not present in this runtime.
2. Keep judge outputs small in the lead context; large analysis should live in files.
3. Prefer stable judge perspectives over decorative personas.
