---
name: soloism
description: Use when two or more concurrent subagents are running and one finishing should immediately drive the next, or when spawned subagents go idle unnoticed, linger as stale processes the human must poll or hand-kill, or leave dependent work stalled behind them. Triggers on eager parallel dispatch, subagents that need reaping, poll-only fan-outs that never wake the orchestrator.
---

Drive concurrent soloterm subagents as one eager wake/reap loop. A child's completion wakes you the instant it lands — nothing goes stale, leaks, or waits on a barrier.

- Learn tools on demand, never from memory: `help(topic="timers")`, `help(topic="spawning")`, `help(topic="inspection")`.
- First call: `whoami` must return your `process_id`. No soloterm → stop and say so.
- Keep a private map of each task ↔ its `process_id`.

## The loop

### 1. Dispatch

- `spawn_agent(agent_tool_id=N, extra_args=["--ax-screen-reader"])` per task; `send_input(process_id=pid, input=<prompt>)` with the returned `agent_instructions` prepended. Record task ↔ pid.
- Arm one wake over the live pids: `timer_fire_when_idle_any([pid…], guard_ms, body)`. `_any`, never `_all`.
- Pack `body` with the live pids, the map, and "run the wake step".

### 2. Wake

Idle ≠ done — idle only means look.

- `get_process_output(process_id=pid)`. From its output decide:
  - **finished** → step 3.
  - **still working** → `send_input` the reply or nudge; re-arm (step 4).
  - **stuck / errored** → reap; surface to the human.

### 3. Reap + advance

- `close_process(process_id=pid)`.
- Dispatch whatever this completion unblocks — back through step 1. Don't wait for siblings.
- Report the live children and what just finished. Never pause for approval.

### 4. Re-arm

`timer_fire_when_idle_any` over the still-live pids. Repeat until none are live.

## Exit

Sweep: `close_process` every pid in your map, `timer_cancel` every pending timer. Leave zero live children.
