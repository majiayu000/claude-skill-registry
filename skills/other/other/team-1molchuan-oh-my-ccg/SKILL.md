---
name: team
description: 并行团队执行，N 个协调 Worker 协作
---

# oh-my-ccg Team Mode

Coordinate N parallel workers for independent tasks.

## Activation
Command: `/oh-my-ccg:team N "task description"` where N is worker count.
Or automatically triggered during impl phase when independent tasks detected.

## Workflow

1. **Analyze tasks**: Identify independent task groups from the plan
2. **Create team**: TeamCreate with task list
3. **Spawn workers**: Launch N executor agents
4. **Route tasks via MCP tools**:
   - Frontend tasks → workers call `ask_gemini(agent_role="designer")` for prototypes before implementing
   - Backend tasks → workers call `ask_codex(agent_role="architect")` for prototypes before implementing
   - General tasks → standard executor workers (no external model needed)
5. **Monitor**: Track completion via TaskList
6. **Verify**: Run verifier on all completed work
7. **Fix loop**: If issues found, assign fixes to available workers
8. **Cleanup**: Shutdown workers, delete team

## Worker MCP Access
Each worker can call the plugin's MCP tools:
- `ask_codex` / `ask_gemini` — for domain-specific prototypes and reviews
- `rpi_state_read` — to check current RPI progress
- Workers should use `background: false` for their MCP calls (each worker is already parallel)

## Task Distribution
- Each worker claims one task at a time
- Workers prefer tasks in ID order (lowest first)
- When a task completes, worker claims next available
- Blocked tasks wait for dependencies to resolve

## Parallel Guidelines
- Maximum 5 concurrent workers (configurable)
- Each worker gets its own executor agent
- Workers share state via task list
- Workers must not modify same files simultaneously

## Cancellation
/oh-my-ccg:cancel sends shutdown to all workers.
