---
name: codex-goals
user-invocable: false
description: |-
  Use when using Codex Goals to define an objective once and let Codex iterate until done.
  Triggers:
practices:
- agile-manifesto
- continuous-delivery
hexagonal_role: driving-adapter
consumes: []
produces:
- codex-goal-state
context_rel: []
skill_api_version: 1
user-invocable: true
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: orchestration
  dependencies: [caam, ntm]
  stability: stable
output_contract: A running/converged Codex Goals session; operator reports the goal id, final status, and the converged artifact (diff, closed beads, or green gate).
---

# Codex Goals

Use Codex's **Goals** feature (stable, `goals = true`) as the Codex-native operating loop: declare the objective once and Codex owns the iterate-until-done cycle, instead of a hand-rolled `codex exec` re-prompt wrapper.

## Overview / When to Use

The flywheel's loop control historically meant a bash `while` re-invoking `codex exec` per tick. Codex now ships **Goals** as a *stable* first-class feature: a durable objective Codex tracks across turns, driving its own iterate → self-check → continue cycle until the stated done-condition is met. This is the Codex analog of AUTODEV/`operating-loop` — the harness owns the loop, not your shell.

Reach for this skill when an operator (you, an NTM pane, or a spawned `codex exec` worker) needs a Codex worker to converge on a stated outcome with minimal re-prompting.

Ground truth (verified `codex-cli 0.137.0`):
- `codex features list` → `goals    stable    true` — it is a stable, on-by-default feature.
- State is durable: `~/.codex/goals_1.sqlite` (confirmed via `codex doctor` → "goals DB … integrity ok"). Goals survive across turns and resumed sessions.
- Surfaced **in-session** (the `/goals` slash command inside interactive `codex`), not as a top-level `codex goals` subcommand. You set the objective from the session, and Codex carries it.
- Toggle: `codex features enable goals` / `codex features disable goals`, or `-c goals=true` per-invocation. It writes to `~/.codex/config.toml`.

## ⚠️ Critical Constraints

- **Operator-side only.** This drives flywheel binaries/harness. Codex, Goals, AUTODEV, and the loop vocabulary **never** reach client-facing surfaces. **Why:** the backstage-stays-backstage rule is load-bearing for the AI Partner product; announcing the machinery breaks it.
- **Never `claude -p` to spawn the worker.** Goals is a *Codex* loop. Drive it with `codex exec` (Codex Pro sub) or interactive `codex` in an NTM pane. **Why:** `claude -p` bills per-token against the API, not the Max sub — banned for worker dispatch (memory: never-claude-p-for-workers).
- **A goal MUST have a done-condition.** Define termination (tests green, spec met, beads closed, file exists) before starting. **Why:** Goals iterates until done — with no done-condition it loops indefinitely and burns budget.
- **Sandbox must be explicit for unattended runs; approval flags differ by form.** For `codex exec` use `-s workspace-write` (exec is non-interactive — failures return to the model with no per-call approval, so `-a` is **not** an `exec` flag and will error `unexpected argument '-a'`). The `-a never` / `--ask-for-approval never` flag belongs to *interactive* `codex` only; to force it inside `exec` use `-c approval_policy=never`. Use `--dangerously-bypass-approvals-and-sandbox` only inside an externally-sandboxed box. **Why:** passing `-a` to `exec` aborts the launch outright; an over-broad sandbox on an unsandboxed host is destructive.
- **Goals state is host-local SQLite.** `~/.codex/goals_1.sqlite` does not sync across the fleet. **Why:** a goal set on Mac is invisible on bushido; treat the worker host as the source of truth and report status out, don't assume cross-host visibility.
- **Publish on convergence.** When the goal converges, the worker must push to shared state (commit, close beads, Agent Mail summary). **Why:** a live Codex session is unreadable to other agents — only the published compression makes the work visible (memory: cross-agent-awareness).

## Workflow / Methodology

### Phase 1: Confirm the feature is live
```bash
codex features list | grep '^goals'        # expect: goals    stable    true
codex doctor | grep -i 'goals DB'          # expect: integrity ok
```
If disabled: `codex features enable goals` (persists to `~/.codex/config.toml`), or pass `-c goals=true` for one run.

**Checkpoint:** `goals` shows `true` and the DB reports `integrity ok` before defining any objective.

### Phase 2: Write the objective + done-condition
Draft a single, testable objective. State the loop contract inline so Codex owns iteration:
- **Objective:** one sentence — what "done" produces.
- **Done-condition:** the machine-checkable gate (e.g. `bd ready` empty, `pytest` green, file present, lint clean).
- **Guardrails:** files/dirs in scope, what not to touch.

**Checkpoint:** the done-condition is something a command can verify — not a vibe. If you cannot name the check, stop and tighten the objective.

### Phase 3: Launch Codex with the objective
Interactive (you supervise; set the goal via `/goals` in-session):
```bash
codex -C /path/to/repo -a never   # interactive codex DOES take -a/--ask-for-approval
                                  # then inside the TUI: /goals → state objective + done-condition
```
Unattended worker (background / NTM pane / spawned job):
```bash
codex exec -C /path/to/repo \
  -s workspace-write \
  -o /tmp/codex-goal-result.md \
  "GOAL: <objective>. ITERATE UNTIL DONE. Done-condition: <machine-checkable gate>. \
   Guardrails: only touch <paths>. On convergence: commit + close beads + write summary."
```
Notes: `codex exec` is already non-interactive — it returns command failures to the model instead of prompting, so **no approval flag is needed** (and `-a` is rejected by `exec`). To pin the policy explicitly, add `-c approval_policy=never`. `--json` emits JSONL events for a watcher; `-o`/`--output-last-message` captures the final report. Use `-p <profile>` / `caam` to pin the right Codex Pro lane.

**Checkpoint:** the process is iterating without an approval stall (no pending prompt in the pane / no hang on stdin).

### Phase 4: Monitor + resume
- Tail JSONL (`--json`) or the pane for the iterate→check→continue cycle.
- Resume an interrupted goal: `codex exec resume --last "continue toward the goal"` (Goals state is durable in SQLite, so the objective is preserved).

**Checkpoint:** each tick makes contact with the done-condition (the gate is being re-run), not just producing motion.

### Phase 5: Converge + publish
On the done-condition passing, verify independently, then publish: `git commit`, close beads (`bd close`), and post an Agent Mail / `.agents` summary.

**Checkpoint:** the done-condition command passes when YOU run it (not just Codex's self-report), and the result is committed/announced to shared state.

## Output Specification

**Format:** terminal report (operator) — no artifact file is written by this skill itself; Codex writes its own (diff, commits, `--output-last-message` file).
**Filename:** if capturing the final message, `--output-last-message <path>` (e.g. `/tmp/codex-goal-result.md`); JSONL stream via `--json`.
**Structure:** report back exactly three things —
1. **Goal:** the objective + done-condition as launched.
2. **Status:** `converged` | `iterating` | `stalled` | `failed`, with the resolved session/goal id.
3. **Artifact:** the converged proof — commit SHA / closed bead ids / the green gate command + its passing output.

## Quality Rubric

- [ ] Confirmed `goals` is `stable true` via `codex features list` before relying on it (no assuming from memory).
- [ ] Objective has a single machine-checkable done-condition, written down before launch.
- [ ] Worker dispatched via `codex exec` / interactive `codex` — never `claude -p`.
- [ ] Unattended `codex exec` runs set an explicit `-s` sandbox (and `-c approval_policy=never` if pinning policy); `-a` is NOT passed to `exec`. No approval stall possible.
- [ ] Convergence verified independently (operator re-runs the gate), not taken from Codex's self-report.
- [ ] Result published to shared state (commit + beads + summary) before calling it done.
- [ ] No Codex/Goals/AUTODEV jargon leaked toward any client-facing surface.

## Examples

**Operating loop on a repo (unattended):**
```bash
codex exec -C ~/dev/agentops -s workspace-write --json \
  "GOAL: make the test suite green. ITERATE UNTIL DONE. \
   Done-condition: 'pytest -q' exits 0. Guardrails: edit src/ and tests/ only. \
   On convergence: git commit -m 'fix: green suite' and stop."
```

**Drain ready beads as a goal:**
```bash
codex exec -C ~/dev/<repo> -s workspace-write \
  "GOAL: close all ready beads. ITERATE UNTIL DONE. \
   Done-condition: 'bd ready' returns no items. Per bead: implement, verify, bd close. \
   On convergence: git push and write an Agent Mail summary."
```

**Interactive, supervised:** `codex -C ~/dev/<repo>` → `/goals` → type the objective + done-condition; watch it iterate.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `goals` shows `false` in `features list` | Disabled in config | `codex features enable goals`, or `-c goals=true` per run |
| `error: unexpected argument '-a' found` | Passed `-a`/`--ask-for-approval` to `codex exec` (interactive-only flag) | Drop `-a` from `exec`; it's already non-interactive. Pin policy with `-c approval_policy=never` if needed |
| Loop hangs, no progress | Interactive `codex` waiting on an approval prompt | Use `codex exec` (non-interactive) for unattended loops, or launch interactive `codex -a never`; for sandboxed boxes add `--dangerously-bypass-approvals-and-sandbox` |
| Goal "lost" after a crash | Looked on the wrong host | Goals live in host-local `~/.codex/goals_1.sqlite`; resume on the SAME host with `codex exec resume --last` |
| Iterates forever, never stops | No real done-condition | Rewrite the objective with a machine-checkable gate; kill and relaunch |
| Worker burned API credits | Spawned with `claude -p` | Banned — re-dispatch with `codex exec` (Pro sub) or an NTM Claude pane (OAuth) |
| `goals DB … integrity` error in `codex doctor` | Corrupt SQLite | Stop sessions, back up/remove `~/.codex/goals_1.sqlite`, restart Codex to recreate |

## See Also / References

- `caam` — pin the right Codex Pro account lane for the worker.
- `ntm` / `vibing-with-ntm` — run Goals workers as panes in a swarm.
- `agentops:autodev`, `operating-loop` — the AgentOps loop contract this is the Codex-native equivalent of.
- `codex --help`, `codex exec --help`, `codex features list` — authoritative command surface (verified `codex-cli 0.137.0`).
- Memory: never-`claude -p`-for-workers; cross-agent-awareness = published compressions.
