---
name: using-atm
description: 'Use ATM as the out-of-session substrate: spawn Claude/Codex panes running /rpi and /evolve over a bead queue, then tend the swarm to convergence.'
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
output_contract: 'stdout: ATM-substrate operating guide'
---

# Using ATM as the Out-of-Session Substrate

AgentOps 3.0 runs its loops **in session** and ships **no** daemon, scheduler, or
overnight runner. To run the loop **unattended** — always-on, scheduled,
queue-driven — you hand it to an orchestration **substrate**. The reference
substrate is **ATM + Agent Mail (`am`) + managed-agents**; this skill covers the **ATM leg**:
a local [Named Tmux Manager](https://github.com/) swarm of Claude/Codex agent
panes. ATM is an adopted external tool (`atm` on `PATH`), **not** an
AgentOps-owned surface — AgentOps adopts it, it does not vendor it.
ATM is Bo's fork/alias of upstream NTM: `atm` points at
`~/dev/ntm/dist/atm-darwin-arm64` and keeps the upstream `ntm` command surface.

> **Skills are the runtime, not the CLI.** The substrate dispatches a *whole
> loop* by spawning an agent that **runs the `rpi` or `evolve` skill** — it
> does **not** shell out to retired RPI/evolve CLI subprocesses. The loop
> lives as a skill an agent executes. The seam is
> **ATM pane → agent → `/rpi <bead>` skill**, one bead dispatched as one
> invocable unit.

## When to use this skill / when to skip

**Use it when:** you want a bead queue worked unattended out of session; you're
standing up or tending an ATM swarm that runs AgentOps loops; a pane is stuck,
rate-limited, or wedged; you need to know whether the swarm has converged.

**Skip it when:** the work fits a single in-session run (just run `rpi` or
`evolve` yourself); you want in-session parallel fan-out across worktrees (use
[`/swarm`](../swarm/SKILL.md)); you're choosing between automation shapes at all
(start at [`/automation-shape-routing`](../automation-shape-routing/SKILL.md),
which routes Workflow vs ATM swarm vs plain skill).

This skill does **not** re-document the full `atm` command surface — run
`atm help` for that. It covers the **AgentOps substrate contract**: how to
dispatch and tend AgentOps loops on an ATM swarm.

## The dispatch contract

1. **One bead = one whole-loop skill invocation.** A pane's agent runs
   `/rpi <bead> --auto` (one cycle) or `/evolve --auto` (the outer loop). The
   substrate never decomposes the loop into per-phase steps — whoever owns the
   loop owns its invariants, and AgentOps owns the loop. Re-expressing `rpi` as
   substrate-side steps duplicates the loop shape and pits the substrate's retry
   machinery against the ratchet rules. Dispatch the skill; don't reimplement it.
2. **Agents inherit the skills via overlay.** Each pane is a Claude or Codex
   agent with the AgentOps skills installed, so `rpi`, `evolve`, `/validate`,
   etc. resolve in-pane.
3. **The bead queue is the work source.** A lead (operator or a lead pane) runs
   `bd ready`, picks the next bead, and dispatches it to a free worker pane.
4. **Green CI is the merge gate.** Each worker drives its bead to a green PR from
   a per-bead worktree (orchestrator-merge model); the operator stays *on* the
   loop (intent + stop), not *in* it (per-PR approval).

## Quick start

```bash
# 1. Spawn a swarm of agent panes against the repo (2 Claude + 1 Codex worker).
atm spawn agentops --cc=2 --cod=1

# 2. Dispatch a whole loop to a pane — the SKILL, not a CLI subprocess.
atm send agentops --pane=1 "/rpi ag-1234 --auto"
atm send agentops --pane=2 "/evolve --beads-only --auto"

# 3. Watch / attach.
atm activity agentops          # per-pane agent state
atm attach agentops            # drop into the swarm

# 4. Health + dependencies (run before a long unattended session).
atm doctor                     # validate the ATM ecosystem
atm deps                       # required agent CLIs present
```

Scheduled cadence (e.g. a nightly `evolve` pass) is driven by host-OS timing (a
systemd user timer or cron) that runs `atm send … "/evolve --auto"`, or by a
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

## Coordination (the Agent Mail leg)

ATM panes coordinate through the other substrate legs, not bespoke glue:

- **Beads (`bd`)** is the shared work queue and the source of truth for state —
  `bd ready` to pick, `bd update --claim` to claim, `bd close` when merged.
- **Agent Mail (`am`)** (its own daemon at `127.0.0.1:8765` — the `am` CLI,
  **not** an `ao` subcommand) carries cross-pane **messages** and
  **file reservations** — the swarm's defense against two panes editing the same
  path. Each pane registers once with `am macros start-session`, reserves before
  editing (`am file_reservations reserve <proj> <agent> "<path>"`), releases on
  commit, and **messages other panes with `am mail send --from <me> --to <agent> --subject … --body …`**
  (read with `am mail inbox`). The CLI form works from any shell even when the
  MCP tool surface (`send_message` etc.) isn't wired into the session. **Trap:**
  the verb is `am mail send`, **not** `am send` (which doesn't exist), and the
  `mail` group isn't in `am --help` — see br cp-jgcl. List addressable agents
  with `am robot agents --project <proj>`.
- **Worktree-per-bead** is mandatory: no pane edits the shared checkout. See
  [../swarm/references/shared-checkout-discipline.md](../swarm/references/shared-checkout-discipline.md).

## Convergence + shutdown

The swarm is done when: `bd ready` is empty, no pane has an in-flight bead, and
the last few CI runs are green. Confirm with `atm activity` (all panes idle) and
`bd ready` (empty) before tearing down with `atm kill <session>`. Don't shut down
on a transient quiet patch — a rate-limited pane also looks idle.

## Single-writer + merged-before-close (cards 17–18, cp-4gj6; POLICY → gate cp-hxp6)

For assurance-close contexts, the gate cp-hxp6 enforces: a bead is durable only
when its branch is **merged to trunk** and the commit is visible on the canonical
store. A pane that closes a bead before merging puts protection OFF — the split-brain
incident of 2026-06-09 was caused by an unmerged trio. The fix is not behavioral:
the gate enforces it structurally.

**Read canonical, not shared main.** Every reader of bead/verdict state must target
the canonical store (the bead's worktree branch or the trunk after merge). `main`
in a shared checkout is stale relative to in-flight worktree branches. A reader that
declares "stuck" or "closed" based on a stale `main` read is reporting on phantom
state. Verify bead state on the bead's branch or via `br show` against the live
server; do not declare convergence from a stale checkout.

## Anti-patterns

- ❌ **Shelling out to retired RPI/evolve CLI subprocesses.**
  Dispatch the `rpi` / `evolve` **skill** to an agent pane instead.
- ❌ **Decomposing the loop into substrate steps.** Dispatch the whole loop as
  one invocable unit; never re-express `rpi`'s phases as ATM-side orchestration.
- ❌ **Editing the shared checkout from a pane.** Worktree-per-bead, always.
- ❌ **Treating ATM as AgentOps-owned.** It is an adopted external substrate; a
  managed-agents driver (`ao agent`) or a plain in-session run are equally valid
  legs. Choose via [`/automation-shape-routing`](../automation-shape-routing/SKILL.md).
- ❌ **Closing a bead before the branch is merged.** Closed-but-unmerged is
  protection-off. Require merge confirmation before `bd close`.
- ❌ **Reading state from a stale shared `main`.** Read canonical from the bead's
  worktree branch or after merge; stale reads are the other half of the split-brain.

## Related skills

- [`/automation-shape-routing`](../automation-shape-routing/SKILL.md) — decide Workflow vs ATM swarm vs plain skill *before* standing up a swarm.
- [`/swarm`](../swarm/SKILL.md) — in-session parallel fan-out across worktrees (the in-session sibling of this out-of-session substrate).
- [`/agent-native`](../agent-native/SKILL.md) — `ao agent bundle` produces the loop definition a managed-agents substrate runs (the managed-agents leg).
- [`rpi`](../rpi/SKILL.md) · [`evolve`](../evolve/SKILL.md) — the loops the substrate dispatches.
