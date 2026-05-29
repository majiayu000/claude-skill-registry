---
name: oh-my-ccg-impl
description: RPI 实施阶段 — 按零决策计划机械执行
---

# oh-my-ccg Implementation Phase

You are executing the RPI Impl phase. Execute the plan mechanically.

## Prerequisites
- RPI state must be in PLAN phase (or resuming IMPL)
- Tasks must be defined in state/artifacts

## Workflow

### Step 1: Restore State
Use the **oh-my-ccg-tools** MCP server's `rpi_state_read` tool.
Load the task list and current progress.

### Step 2: Assess Parallelism
Check task dependencies:
- If multiple independent tasks exist → use Team mode for parallel execution
- If tasks are sequential → execute one by one with executor agent

### Step 3: Execute Tasks
For each task (or batch of parallel tasks):

1. **Route to appropriate model for prototype** (via MCP tools):
   - Frontend tasks → call `ask_gemini(agent_role="designer")` for prototype, then executor rewrites to production
   - Backend tasks → call `ask_codex(agent_role="architect")` for prototype, then executor rewrites to production
   - General tasks → executor implements directly (no external model needed)

2. **Executor implements**:
   - Read task spec completely
   - Explore existing code patterns
   - Rewrite prototype to production quality (NEVER apply external model output directly)
   - Run type checks and tests

3. **Side-effect review** (MANDATORY before moving to next task):
   - Verify changes stay within task scope
   - Check no unintended dependencies affected
   - Confirm interfaces match expectations

### Step 4: Cross-Review
After all tasks complete, run dual-model cross-review using MCP tools **in parallel**:

- `ask_codex(agent_role="code-reviewer", background=true)` — reviews logic/security
- `ask_gemini(agent_role="designer", background=true)` — reviews patterns/maintainability

Collect both results via `check_job_status`, then:
- Fix any Critical findings immediately
- Log Warnings for review phase

### Step 5: Verify
Run verifier agent:
- All tests pass
- Build succeeds
- No type errors
- Constraints satisfied

### Step 6: Update State
Use `rpi_state_write` MCP tool to:
- Mark tasks complete in state
- Transition phase to "impl"
- If all tasks done → prompt for `/oh-my-ccg:review`

### Ralph Integration
If ralph mode is active:
- Execute → Verify → Pass? → Complete
- Execute → Verify → Fail? → Fix → Repeat (up to max iterations)
