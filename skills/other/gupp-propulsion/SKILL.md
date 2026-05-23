---
name: gupp-propulsion
description: Interrupt controller converting polled to proactive agent execution. Per-runtime strategies, configurable thresholds, Deacon heartbeat supervision. Fights LLM passivity bias.
format: 2025-10-02
version: 1.0.0
status: ACTIVE
updated: 2026-04-25
triggers:
  - agent has work assigned to its hook and is not yet executing
  - stall detection identifies an agent with hooked work that has gone idle
  - new agent is spawned and needs GUPP enforcement injected into its context
  - runtime-specific GUPP strategy selection is needed
  - heartbeat supervision needs to be configured for active agents
references_subdir: true
word_budget: 800
---

# GUPP Propulsion

The Gas Town Universal Propulsion Principle: **If there is work on your hook, YOU MUST RUN IT.**

GUPP is the interrupt controller of the Gastown chipset. In a real processor, the interrupt controller converts external events (keyboard press, network packet, timer tick) into CPU interrupts that force immediate handling. GUPP does the same for AI coding agents: it converts the polled model (agent checks periodically, waits for user input) into an interrupt-driven model (work appears on hook, agent executes immediately).

## Why GUPP Exists

RLHF-trained LLM assistants have a strong bias toward *waiting for the user* — asking clarifying questions, seeking confirmation, pausing for feedback. This is appropriate in interactive chat but catastrophic for autonomous multi-agent orchestration, where every moment of idle waiting stalls the pipeline. Gastown discovered this empirically: agents spawned with a work item would introduce themselves, summarize the task, and *wait*, asking "Shall I proceed?" when the answer was already on their hook. GUPP overrides this trained passivity with an explicit, non-negotiable execution mandate: if you have hooked work, you do not wait, do not ask for confirmation, do not pause for feedback. You begin immediately. This is physics, not politeness.

## Activation Triggers

This skill activates when:

- An agent has work assigned to its hook and is not yet executing
- Stall detection identifies an agent with hooked work that has gone idle
- A new agent is spawned and needs GUPP enforcement injected into its context
- Runtime-specific GUPP strategy selection is needed
- Heartbeat supervision needs to be configured for active agents
- An agent has been nudged but remains stalled

## Enforcement at a Glance

GUPP enforcement adapts to each runtime via the Runtime HAL. The HAL exposes `getGUPPStrategy()` which returns one of:

- `hook_injection` — Claude Code (SessionStart hook, highest fidelity)
- `startup_fallback` — Codex (tmux `gt prime`, medium fidelity)
- `polling` — Gemini / Cursor / unknown (prompt preamble + state polling)

A Deacon heartbeat loop runs inside the witness-observer at the configured `nudge_interval`, detecting agents that received hooks but stalled. After `restart_threshold`, the watchdog requests a session restart. Per-runtime strategy tables, configurable thresholds, and the full heartbeat protocol are in [`references/runtime-strategies.md`](references/runtime-strategies.md).

## Safety Boundaries

**These safety rules MUST remain in effect at all times — they are not advisory.**

### GUPP Is Advisory in GSD

GUPP enforcement is ADVISORY within GSD's structured workflow. The GSD orchestrator's phase gates, verification steps, and checkpoint protocols take precedence over GUPP urgency. If a GSD checkpoint requires human verification, GUPP does not override it. If a phase gate blocks progress pending approval, GUPP does not force execution past the gate.

The hierarchy is:

```
GSD orchestrator (highest authority)
  -> Phase gates and checkpoints
  -> GUPP propulsion (execution enforcement)
  -> Agent autonomy (lowest -- must obey all above)
```

GUPP operates between the orchestrator's structural gates. Within a phase, within an approved plan, within a committed task — GUPP demands immediate execution. But it never overrides the orchestrator's decision about *what* to execute or *when* a phase is complete.

### Restart Limits

The watchdog restart mechanism has strict limits to prevent infinite restart loops:

| Limit | Value |
|-------|-------|
| Max restart threshold | 1800s (30 min, hard cap) |
| Max restarts per bead | 3 |
| Restart cooldown | 60s minimum between consecutive restarts |

After 3 restarts for the same work item, escalation to human is mandatory.

### Human Escalation

After 3 restarts for the same bead without resolution, GUPP stops attempting automated recovery and escalates to a human operator via durable mail to the mayor. The mayor surfaces this through whatever channel the human is monitoring. GUPP does not attempt a fourth restart.

### No Data Destruction

GUPP enforcement never destroys work in progress. Restarts preserve the agent's branch and commits. Nudges are non-destructive signals. Escalations are informational. At no point does GUPP delete files, reset branches, or discard uncommitted changes.

## Integration with Other Gastown Skills

Reads runtime capabilities from `runtime-hal` (`getGUPPStrategy()`, thresholds, restart support). Targets `polecat-worker` (the primary enforcement target). Runs inside `witness-observer` (Deacon heartbeat). Sends nudges via `nudge-sync` and escalations via `mail-async`. Reads agent activity timestamps from `beads-state` and hook status from `hook-persistence`. `mayor-coordinator` receives escalations. `sling-dispatch` sets hooks that activate GUPP enforcement.

## References

Implementation detail moved to:

- [`references/runtime-strategies.md`](references/runtime-strategies.md) — per-runtime enforcement tables (Claude Code, Codex, Gemini, Cursor), threshold reference, Deacon heartbeat pattern.
- [`references/boundaries.md`](references/boundaries.md) — full Safety Boundaries detail (advisory-in-GSD hierarchy, restart limits, escalation, no-data-destruction).
- [`references/metrics-and-learning.md`](references/metrics-and-learning.md) — observable metrics (response time, nudge effectiveness, strategy success, stall frequency) and the learning feedback loop.
- [`references/gastown-origin.md`](references/gastown-origin.md) — the GUPP principle from Gastown, how it fights model training bias.
- [`heartbeat.md`](heartbeat.md) — Deacon heartbeat supervision pattern and integration points.
