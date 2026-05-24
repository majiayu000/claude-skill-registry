---
name: error-guard
description: >
  System safety and control-plane skill that prevents agent deadlocks and freezes.
  Provides non-LLM control commands to inspect task state, flush message queues,
  cancel long-running work, and recover safely without restarting the container.
  Use when implementing or operating long-running tasks, sub-agents, benchmarks,
  background monitors (e.g., Moltbook, PNR checks), or when the system becomes
  unresponsive and needs immediate recovery controls.
---

# error-guard

⚠️ **System‑level skill (Advanced users)**

This skill defines the **control‑plane safety primitives** for OpenClaw.
It is intentionally minimal, non‑blocking, and designed to prevent agent freezes, deadlocks, and unrecoverable states when running long‑lived or high‑risk workloads.

## Design Principles

> **Warning:** This skill operates at the agent control‑plane level.
> It should be installed only by users who understand OpenClaw’s execution model and are running workloads that can block, hang, or run for extended periods.

- **Main agent never blocks**: no long exec, no external I/O, no LLM calls.
- **Event-driven**: workers emit events; the control plane listens.
- **Fail-safe first**: recovery commands must always respond.
- **Minimal state**: track only task metadata (never payloads).

## Command Surface (Phase 1)

### /status

Report current system health and task registry state.

Returns:
- Active tasks (taskId, type, state)
- Start time and last heartbeat
- Flags for stalled or overdue tasks

Constraints:
- Must run in constant time
- Must not call any model or external API

### /flush

Emergency stop.

Immediately:
- Cancel all active tasks
- Kill active exec/process sessions
- Clear pending message queue
- Reset in-memory task registry

Constraints:
- Must always respond
- No waiting on workers
- No model calls

### /recover

Safe recovery sequence.

Steps:
1. Execute `/flush`
2. Reset control-plane state
3. Optionally reload skills/state (no container restart)

## Future Extensions (Not Implemented Yet)

- Sub-agent runner helper (event-driven)
- Task watchdogs with TTL and silence detection
- Structured event protocol (task.started, task.heartbeat, task.completed, ...)
- Back-pressure and task classes (interactive / batch / background)

## Security & Privacy

- This skill **does not** store payloads, prompts, messages, or model outputs
- Only minimal task metadata is persisted (taskId, timestamps, state)
- No API keys, credentials, or user data are read or written
- Safe to publish and share publicly

## Non-Goals

- No business logic
- No background polling loops
- No user-facing features
- No LLM reasoning paths

This skill is the **last line of defense**. Keep it small, fast, and reliable.
