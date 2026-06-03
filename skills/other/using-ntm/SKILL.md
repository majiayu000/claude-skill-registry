---
name: using-ntm
description: 'Use NTM as the out-of-session substrate: spawn Claude/Codex panes running /rpi and /evolve over a bead queue, then tend the swarm to convergence.'
practices:
- team-topologies
- agile-manifesto
- mythical-man-month
hexagonal_role: supporting
consumes: []
produces:
- documentation
context_rel:
- kind: customer-of
  with: swarm
skill_api_version: 1
user-invocable: true
context:
  window: isolated
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
    - INTEL
  intel_scope: none
metadata:
  tier: orchestration
  dependencies: []
output_contract: 'stdout: NTM-substrate operating guide'
---

# Using NTM as the Out-of-Session Substrate

AgentOps 3.0 runs its loops **in session** and ships **no** daemon, scheduler, or
overnight runner. To run the loop **unattended** — always-on, scheduled,
queue-driven — you hand it to an orchestration **substrate**. The reference
substrate is **NTM + MCP + managed-agents**; this skill covers the **NTM leg**:
a local [Named Tmux Manager](https://github.com/) swarm of Claude/Codex agent
panes. NTM is an adopted external tool (`ntm` on `PATH`), **not** an
AgentOps-owned surface — AgentOps adopts it, it does not vendor it.

> **Skills are the runtime, not the CLI.** The substrate dispatches a *whole
> loop* by spawning an agent that **runs the `/rpi` or `/evolve` skill** — it
> does **not** shell out to retired RPI/evolve CLI subprocesses. The loop
> lives as a skill an agent executes. The seam is
> **NTM pane → agent → `/rpi <bead>` skill**, one bead dispatched as one
> invocable unit.

## When to use this skill / when to skip

**Use it when:** you want a bead queue worked unattended out of session; you're
standing up or tending an NTM swarm that runs AgentOps loops; a pane is stuck,
rate-limited, or wedged; you need to know whether the swarm has converged.

**Skip it when:** the work fits a single in-session run (just run `/rpi` or
`/evolve` yourself); you want in-session parallel fan-out across worktrees (use
[`/swarm`](../swarm/SKILL.md)); you're choosing between automation shapes at all
(start at [`/automation-shape-routing`](../automation-shape-routing/SKILL.md),
which routes Workflow vs NTM swarm vs plain skill).

This skill does **not** re-document the full `ntm` command surface — run
`ntm help` for that. It covers the **AgentOps substrate contract**: how to
dispatch and tend AgentOps loops on an NTM swarm.

## The dispatch contract

1. **One bead = one whole-loop skill invocation.** A pane's agent runs
   `/rpi <bead> --auto` (one cycle) or `/evolve --auto` (the outer loop). The
   substrate never decomposes the loop into per-phase steps — whoever owns the
   loop owns its invariants, and AgentOps owns the loop. Re-expressing `/rpi` as
   substrate-side steps duplicates the loop shape and pits the substrate's retry
   machinery against the ratchet rules. Dispatch the skill; don't reimplement it.
2. **Agents inherit the skills via overlay.** Each pane is a Claude or Codex
   agent with the AgentOps skills installed, so `/rpi`, `/evolve`, `/validation`,
   etc. resolve in-pane.
3. **The bead queue is the work source.** A lead (operator or a lead pane) runs
   `bd ready`, picks the next bead, and dispatches it to a free worker pane.
4. **Green CI is the merge gate.** Each worker drives its bead to a green PR from
   a per-bead worktree (orchestrator-merge model); the operator stays *on* the
   loop (intent + stop), not *in* it (per-PR approval).

## Quick start

```bash
# 1. Spawn a swarm of agent panes against the repo (2 Claude + 1 Codex worker).
ntm spawn agentops --cc=2 --cod=1

# 2. Dispatch a whole loop to a pane — the SKILL, not a CLI subprocess.
ntm send agentops --pane=1 "/rpi ag-1234 --auto"
ntm send agentops --pane=2 "/evolve --beads-only --auto"

# 3. Watch / attach.
ntm activity agentops          # per-pane agent state
ntm attach agentops            # drop into the swarm

# 4. Health + dependencies (run before a long unattended session).
ntm doctor                     # validate the NTM ecosystem
ntm deps                       # required agent CLIs present
```

Scheduled cadence (e.g. a nightly `/evolve` pass) is driven by host-OS timing (a
systemd user timer or cron) that runs `ntm send … "/evolve --auto"`, or by a
managed-agent driver — **not** an AgentOps daemon.

## Tending the swarm (operator loop)

Run one tick at a time; take the first action whose trigger fires:

- **A pane is rate-limited or auth-expired** → rotate the account / relaunch the
  pane, then re-send its in-flight bead. Do not let a dead pane look idle.
- **A pane is wedged** (no output, not at a prompt) → nudge it once; if still
  wedged, kill + relaunch and re-dispatch its bead.
- **A pane is context-saturated** (forgetting earlier instructions, repeating
  itself) → have it write a handoff, then relaunch fresh and re-dispatch.
- **A worker finished its bead** (PR merged, bead closed) → dispatch the next
  `bd ready` bead to it.
- **Many review beads open, few closing** → flip the swarm to review-only and
  drain the backlog before taking new feature work.
- **Otherwise** → observe; do not nudge a healthy working pane.

## Coordination (the MCP leg)

NTM panes coordinate through the other substrate legs, not bespoke glue:

- **Beads (`bd`)** is the shared work queue and the source of truth for state —
  `bd ready` to pick, `bd update --claim` to claim, `bd close` when merged.
- **MCP Agent Mail** (`ao mcp serve` exposes the AgentOps tool surface across the
  seam) carries cross-pane messages and **file reservations** — the swarm's
  defense against two panes editing the same path. Reserve before editing;
  release on commit.
- **Worktree-per-bead** is mandatory: no pane edits the shared checkout. See
  [../swarm/references/shared-checkout-discipline.md](../swarm/references/shared-checkout-discipline.md).

## Convergence + shutdown

The swarm is done when: `bd ready` is empty, no pane has an in-flight bead, and
the last few CI runs are green. Confirm with `ntm activity` (all panes idle) and
`bd ready` (empty) before tearing down with `ntm kill <session>`. Don't shut down
on a transient quiet patch — a rate-limited pane also looks idle.

## Anti-patterns

- ❌ **Shelling out to retired RPI/evolve CLI subprocesses.**
  Dispatch the `/rpi` / `/evolve` **skill** to an agent pane instead.
- ❌ **Decomposing the loop into substrate steps.** Dispatch the whole loop as
  one invocable unit; never re-express `/rpi`'s phases as NTM-side orchestration.
- ❌ **Editing the shared checkout from a pane.** Worktree-per-bead, always.
- ❌ **Treating NTM as AgentOps-owned.** It is an adopted external substrate; a
  managed-agents driver (`ao agent`) or a plain in-session run are equally valid
  legs. Choose via [`/automation-shape-routing`](../automation-shape-routing/SKILL.md).

## Related skills

- [`/automation-shape-routing`](../automation-shape-routing/SKILL.md) — decide Workflow vs NTM swarm vs plain skill *before* standing up a swarm.
- [`/swarm`](../swarm/SKILL.md) — in-session parallel fan-out across worktrees (the in-session sibling of this out-of-session substrate).
- [`/agent-native`](../agent-native/SKILL.md) — `ao agent bundle` produces the loop definition a managed-agents substrate runs (the managed-agents leg).
- [`/rpi`](../rpi/SKILL.md) · [`/evolve`](../evolve/SKILL.md) — the loops the substrate dispatches.
