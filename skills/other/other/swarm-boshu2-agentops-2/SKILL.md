---
name: swarm
description: 'Spawn isolated Codex sub-agents for parallel task execution using the current runtime primitives. Triggers: "swarm", "spawn agents", "parallel work", "run in parallel", "parallel execution".'
---

# $swarm — Parallel Agent Execution (Codex Tailoring)

This override captures the Codex-native execution model for parallel work.

The active runtime primitives are:

- `spawn_agent`
- `send_input`
- `wait_agent`
- `close_agent`

Use `agent_type="explorer"` for read-only discovery and `agent_type="worker"` for implementation workers.

## Core Rules

1. Only parallelize tasks with disjoint file ownership.
2. Give every worker an explicit file manifest and validation command.
3. Tell each worker it is not alone in the repo and must not revert unrelated edits.
4. Wait sparingly. Keep the lead agent doing useful non-overlapping work.
5. The lead agent validates, integrates, and closes the loop.

## Codex-Native Flow

### Step 1: Prepare tasks

Each task must define:

- `id`
- `subject`
- `description`
- `files`
- `validation`

If file ownership is unknown, spawn `explorer` agents first to map the blast radius.

### Step 2: Conflict check

Do not run workers in the same wave if they claim overlapping files. Split them into sub-waves instead.

### Step 3: Spawn workers

Use one `spawn_agent(...)` call per worker with:

- `agent_type="worker"`
- a bounded task
- explicit owned files
- explicit validation steps

### Step 4: Monitor

Use `wait_agent(...)` only when the next integration step actually depends on the worker result. If a worker needs a correction, use `send_input(...)` with a focused follow-up.

### Step 5: Integrate

The lead agent reviews worker outputs, runs repo-level validation, and decides whether to launch another wave.

## Fallback

If sub-agents are unavailable, execute the same tasks sequentially in the lead session while keeping the same file-ownership and validation discipline.
