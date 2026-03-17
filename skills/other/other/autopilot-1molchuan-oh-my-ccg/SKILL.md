---
name: autopilot
description: 全自动 RPI 执行 — 从想法到可运行代码
---

# oh-my-ccg Autopilot

Full automatic RPI cycle: research → plan → impl → review.

## Activation
Trigger: "autopilot", "auto" + requirement description

## Workflow

### Phase 1: Initialize
- Use `rpi_state_write` MCP tool to create RPI state with requirement
- Verify Codex + Gemini availability via `ask_codex(prompt="ping")` and `ask_gemini(prompt="ping")` MCP calls
- Use `mode_state_write` MCP tool to start autopilot state tracking

### Phase 2: Auto-Research
- Run explore agent for codebase context
- Launch multi-model exploration **in parallel via MCP tools**:
  - `ask_codex(agent_role="analyst", background=true)` — backend constraints
  - `ask_gemini(agent_role="designer", background=true)` — frontend constraints
- Collect results via `check_job_status`
- Synthesize constraints automatically
- Present constraint summary to user for quick confirmation

### Phase 3: Auto-Plan
- Suggest /clear if context > 80%
- Run planner agent with constraints
- Cross-validate with dual-model **parallel MCP calls**:
  - `ask_codex(agent_role="planner", background=true)` — plan validation
  - `ask_gemini(agent_role="designer", background=true)` — frontend validation
- Generate zero-decision task list
- Update state via `rpi_state_write` MCP tool

### Phase 4: Auto-Impl
- Suggest /clear if context > 80%
- Route tasks via MCP tools:
  - Frontend tasks → `ask_gemini` for prototype, then executor rewrites
  - Backend tasks → `ask_codex` for prototype, then executor rewrites
- Use Team mode if multiple independent tasks
- Use Ralph mode for each task (execute→verify→fix)
- Continue until all tasks pass verification
- Update state via `rpi_state_write` MCP tool after each task

### Phase 5: Auto-Review
- Run dual-model cross-review via **parallel MCP calls**:
  - `ask_codex(agent_role="code-reviewer", background=true)`
  - `ask_gemini(agent_role="designer", background=true)`
- Fix Critical findings automatically
- Present final report to user

## Context Management
- Monitor context usage after each phase
- Prompt user for /clear when approaching 80%
- State persists in .oh-my-ccg/state/ across /clear (managed via MCP tools)

## Cancellation
Use /oh-my-ccg:cancel to stop autopilot at any point.
