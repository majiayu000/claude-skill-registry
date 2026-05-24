---
name: crank
description: 'Hands-free epic execution for Codex using wave-based sub-agents and lead-side validation. Triggers: "crank", "run epic", "execute epic", "run all tasks", "hands-free execution", "crank it".'
---

# $crank — Autonomous Epic Execution (Codex Tailoring)

This override captures the Codex-native execution model for multi-issue epic work.

## Core Model

- The lead agent owns wave planning, validation, and issue state transitions.
- Workers are spawned with `spawn_agent(...)`.
- Each worker gets a bounded task, explicit owned files, and validation steps.
- The lead agent uses `wait_agent(...)` only when integration is blocked on a worker result.

## Codex-Native Wave Loop

### Step 1: Select the wave

Use `bd ready --json` when available, or the current plan artifact when beads is unavailable. Only include unblocked work with disjoint file ownership in the same wave.

### Step 2: Prepare worker packets

For each issue, include:

- issue id and subject
- short implementation brief
- owned files
- validation commands
- reminder that the worker is not alone in the repo

### Step 3: Spawn workers

Use one `spawn_agent(...)` call per issue with `agent_type="worker"`.

### Step 4: Monitor and correct

Collect worker results with `wait_agent(...)`. If a worker needs rework, use `send_input(...)` with a focused correction or launch a new wave for the remaining work.

### Step 5: Validate centrally

The lead agent reviews the combined diff, runs repo-level validation, and only then closes issues or advances the wave.

### Step 6: Repeat

Continue until all children are closed or the epic is genuinely blocked.

## Constraints

1. Do not rely on batch-spawn, background-report, or timeout-specific wait APIs that are not present in Codex.
2. Do not let workers commit, push, or mutate issue state unless the task explicitly requires it.
3. Serialize overlapping file ownership into later waves instead of risking merge conflicts.
