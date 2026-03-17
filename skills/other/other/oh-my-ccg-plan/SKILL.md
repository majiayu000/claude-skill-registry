---
name: oh-my-ccg-plan
description: RPI 计划阶段 — 约束集转化为零决策可执行计划
---

# oh-my-ccg Plan Phase

You are executing the RPI Plan phase. Transform constraints into a zero-decision executable plan.

## Prerequisites
- RPI state must be in RESEARCH phase (or resuming PLAN)
- Constraints must be defined in state

## Workflow

### Step 1: Restore State
Use the **oh-my-ccg-tools** MCP server's `rpi_state_read` tool.
Load constraints, decisions, and artifacts from the persisted state.

### Step 2: Multi-Model Analysis (PARALLEL)
Launch both models **simultaneously in a single message** using MCP tools:

**Codex** (planner role) — use `ask_codex` tool:
- `agent_role`: "planner"
- `prompt`: Include all constraints, ask for implementation approach and risk analysis
- `context_files`: Key architecture files
- `background`: true

**Gemini** (designer role) — use `ask_gemini` tool:
- `agent_role`: "designer"
- `prompt`: Include all constraints, ask for frontend decomposition and UX risks
- `files`: Key UI/component files
- `background`: true

Then use `check_job_status` for both job IDs to collect results.

### Step 3: Task Decomposition
Using the `planner` agent, decompose into ordered tasks:
- Each task must be mechanical (zero decisions)
- Specify exact files, functions, tests
- Mark dependencies between tasks
- Route each task: frontend / backend / fullstack

### Step 4: PBT Property Extraction
For each requirement/constraint, extract testable properties:
- Define invariants
- Specify property-based tests where applicable

### Step 5: Ambiguity Elimination
Audit the plan for any remaining decisions:
- If ambiguities found → use AskUserQuestion to resolve
- Iterate until zero ambiguities remain

### Step 6: Generate Artifacts
- Write specs/ documents using the Write tool (in OpenSpec change dir if available)
- Write design/ documents using the Write tool
- Write tasks.md with full task list
- Use `rpi_state_write` MCP tool to update state with:
  - Phase transition to "plan"
  - Artifacts list
  - PBT properties
  - Task list

### Step 7: Transition
Report: task count, PBT properties, estimated scope.
Instruct user to `/clear` then `/oh-my-ccg:impl`.
