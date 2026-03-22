---
name: rifts
description: Workgraph + Rifts (aka Driftdriver orchestrator: Speedrift + optional Specrift/UXrift) autopilot workflow for starting/resuming a repo, creating an end-to-end Workgraph plan with dependencies, and keeping code/spec/intent drift under control via advisory checks and follow-up tasks (no hard blocks). Use when working with workgraph (`wg`), Driftdriver, Speedrift, Specrift, UXrift, drift control, task contracts (`wg-contract`), or when the user wants agents to “plan everything in Workgraph and get to work”.
---

# Rifts (Workgraph Autopilot)

Rifts is the umbrella workflow: **Speedrift** (drift + contracts) plus optional **Specrift** (spec/doc drift) and optional **UXrift** (UX checks), integrated into **Workgraph**.

## Start / Resume (Repo Bootstrap)

Run these from the repo root:

```bash
# Ensure wrappers + executor guidance exist (idempotent)
/Users/braydon/projects/experiments/driftdriver/bin/driftdriver install

# Ensure every open/in-progress task has a `wg-contract` block (idempotent)
./.workgraph/speedrift ensure-contracts --apply

# Optional: snapshot drift into wg logs + spawn follow-ups
./.workgraph/speedrift scan --write-log --create-followups
```

Optional (only if you plan to do UX work in this repo):

```bash
/Users/braydon/projects/experiments/driftdriver/bin/driftdriver install --with-uxrift
```

Specrift is lightweight and is installed automatically when found; it runs only for tasks that declare a `specrift` block.

Then start “hands-off” execution:

```bash
# Workgraph daemon: auto-spawn agents for ready tasks (uses .workgraph/config.toml executor/model)
wg service start
```

Optional pit-wall telemetry (continuous drift monitor+redirect):

```bash
./.workgraph/rifts orchestrate --write-log --create-followups
```

## Planning: Turn “Do The Project” Into Workgraph Tasks

When asked to “create an end-to-end plan with dependencies in Workgraph”:

1. Create a short **root** task (the why/what).
2. Decompose into executable leaf tasks with stable IDs.
3. Encode dependencies with `wg add --blocked-by ...`.
4. Put a `wg-contract` block at the top of every task description.
5. Add a `uxrift` block only for tasks that need UX checks (so `rifts` will run UXrift automatically).
6. Add a `specrift` block for tasks that must keep docs/specs in sync (so `rifts` will run Specrift automatically).

Useful commands:

```bash
wg add "Kickoff: plan + execute" --id kickoff -d "..."
wg add "Implement X" --id implement-x --blocked-by kickoff -d "..."
wg add "Test X" --id test-x --blocked-by implement-x -d "..."
wg add "UX check flow" --id ux-check --blocked-by implement-x -d $'```uxrift\nschema=1\nurl=\"...\"\n...\n```'
wg ready
```

## Per-Task Protocol (What Agents Must Do)

Always pass a task id (avoids ambiguity when multiple tasks are in progress):

```bash
./.workgraph/rifts check --task <task_id> --write-log --create-followups
```

Use it:
- Once at task start (before edits)
- Once just before marking done/submitting

Interpretation:
- Exit `0`: clean
- Exit `3`: findings exist (non-blocking; act via follow-ups / contract edits)

## Handling Drift Without Slowing Down

Speedrift is advisory. Preferred responses:

- If scope changed: update the contract touch set (don’t silently expand scope).
  ```bash
  ./.workgraph/speedrift contract set-touch --task <task_id> src/** tests/**
  ```
- If `hardening_in_core`: don’t add retries/fallbacks/guardrails in the core task.
  Do the `harden:` follow-up task instead (or create one if missing).
- Let follow-up tasks carry the drift (keeps the main task focused, preserves velocity).

## Choosing Contract Mode

- `mode = "core"`: strict drift checks (scope/deps/churn + “hardening in core” signals). Default.
- `mode = "harden"`: use when the objective is explicitly guardrails/retries/timeouts (expect to add “hardening”).
- `mode = "explore"`: use for research/data analysis spikes where broad exploration is expected.
