---
name: using-gc
description: Explain how to run AgentOps on the Gas City (gc) substrate.
practices:
- wiki-knowledge-surface
- twelve-factor-app
- agile-manifesto
hexagonal_role: generic
consumes: []
produces:
- documentation
context_rel: []
skill_api_version: 1
user-invocable: false
context:
  window: isolated
  intent:
    mode: none
  sections:
    exclude:
    - HISTORY
    - INTEL
    - TASK
  intel_scope: none
metadata:
  tier: meta
  dependencies: []
  internal: true
output_contract: 'stdout: gc operating guide'
---
# Running AgentOps on Gas City (gc)

> **This guide GUIDES agents on the `gc` CLI — exactly like the bd protocol guides them on `bd`.** `ao` does NOT wrap `gc`; `gc` is a guided out-of-session dependency. AgentOps is the *opinions* (the rpi/evolve loops, the ratchet rules, the skill corpus, the `.agents/` context compiler); Gas City is the *substrate* (controller/supervisor, Orders, the bead/dolt queue, the Event Bus, runtime providers, mayor/worker agents). The seam: `gc` (orchestration) invokes `ao` (the loop) as a subprocess.

**When to use gc.** In-session, you run the loop yourself (`/rpi`, `/evolve`) — you do not need gc. Reach for gc when you want the loop to run **out of session**: scheduled maintenance, autonomous bead drain, a long-lived team-lead agent that dispatches work and drives PRs to merge. The reference pack at [`packs/agentops/`](../../packs/agentops/) is the canonical AgentOps-on-GC config. North-star framing: [`docs/3.0.md`](../../docs/3.0.md).

## gc Availability Pattern

gc is an **optional, out-of-session** dependency. Skills must degrade gracefully when it is absent (see the [shared fallback table](../shared/SKILL.md)).

```bash
if command -v gc &>/dev/null; then
  # Out-of-session orchestration available — see the dispatch loop below.
else
  echo "Note: gc not installed. Run the loop in-session with /rpi or /evolve."
  # Fallback: drive the loop yourself; gc adds out-of-session orchestration only.
fi
```

## gc Primitives (the vocabulary)

| Primitive | What it is | AgentOps mapping |
|-----------|-----------|------------------|
| **City** / `city.toml` | The top-level deployment — workspace, daemon, bead/session/mail providers, pack imports | The reference City *is* `city.toml` + `[imports.agentops]`. Every other block is pure substrate consumption. See [references/reference-city.md](references/reference-city.md). |
| **Rig** | A code workspace the City manages (one repo / worktree root) | The repo whose beads get worked. `gc rig add <path>` registers it. |
| **Pack** | A bundle of agents + formulas + orders + overlay shipped into a City | [`packs/agentops/`](../../packs/agentops/) — the only opinion is two agents + thin orders. |
| **Agent** | A named, scheduled session (a template the supervisor spawns) | **mayor** (city-scoped, always-on team lead) + **refinery** (rig-scoped, on-demand worker). |
| **Order** | A trigger (cooldown / cron / event) that fires a formula or an exec command | Cron/exec maintenance Orders (`compile-corpus`, `maturity-scan`); the reference dispatch Order (`bead-dispatch`). |
| **Formula** | A multi-step workflow an Order or `gc sling` can route to a pool | THIN one-step dispatch formulas (`rpi-dispatch`, `evolve-dispatch`) — each step just runs ONE `ao` command. |
| **Mayor** | Team-lead agent: orchestrate / merge / notify, human on the loop | Owns the merge gate (CI-green is the signal); never owns the loop's insides. |
| **Refinery (worker)** | Rig-scoped worker the pool scales under bead pressure | Runs the WHOLE `ao rpi` loop on one bead as a single invocable unit. |

**THE governing boundary (THIN-SEAM).** GC dispatches the *whole* `ao rpi` loop; it never sees the loop's insides. The loop's internal steps (research → plan → implement → validate) and its ratchet rules (no-self-grade, fresh-agent-on-failure, knowledge→constraints) live INSIDE AgentOps, behind the single command `ao rpi`. There is deliberately no `mol-rpi-cycle` 4-step GC formula — that would duplicate the loop shape across the seam and pit GC's `check.max_attempts` retry against AgentOps's fresh-agent-on-failure invariant.

## The AgentOps-on-GC workflow (end to end)

### 1. Init the City

The reference City consumes the GC substrate and imports the AgentOps pack. Point gc at the City dir that holds `city.toml` and `packs/agentops/`:

```bash
gc start <path-to-city-dir>          # boots controller + supervisor + always-on mayor
gc rig add <path-to-your-repo>       # register the rig whose beads get worked
```

The City's `[beads] provider = "bd"` consumes the **same `bd`/dolt store** standalone `bd` uses — `gc bd` and `bd` share one tracker (one issue prefix per served DB). Do NOT import a dolt-managing pack: `provider` is pure client config, not a managed server (the 1,478-flap guard — see [references/reference-city.md](references/reference-city.md)).

### 2. The mayor-driven dispatch loop (the honest path today)

A long-lived **mayor** agent runs `bd ready`, slings the next bead to a **refinery** worker, and the worker runs `ao rpi <bead>`:

```bash
# Mayor (city-scoped, always-on): find ready work and route it to the worker pool.
gc bd ready --json
TARGET_RIG="${GC_RIG:-}"                                   # rig that owns the code
gc sling "${TARGET_RIG:+$TARGET_RIG/}refinery" <bead-id>   # route the RAW bead to a worker

# Refinery (rig-scoped worker): run the WHOLE loop — ONE command.
ao rpi <bead-id>                                           # research→plan→implement→validate

# When ao rpi lands green, the worker hands the bead back to the mayor for merge:
BRANCH=$(git rev-parse --abbrev-ref HEAD)
gc bd update <bead-id> --status=open --assignee="mayor" \
  --set-metadata branch="$BRANCH" --set-metadata verdict=PASS \
  --notes "ao rpi green — verdict under .agents/"
gc mail send mayor/ -s "READY-TO-MERGE <bead-id>" -m "rpi cycle green; ready to merge."
```

The mayor owns the merge gate: CI-green is the merge signal — it drives each PR to merge on `main` and triggers the knowledge-flywheel feedback. There is **no human merge gate in the autonomous loop**; the human is *on* the loop (approvals, strategy, escalations), not *in* it. Full dispatch walkthrough: [references/mayor-dispatch-loop.md](references/mayor-dispatch-loop.md).

### 3. The outer loop (evolve cadence)

On a cadence, the mayor runs `ao evolve` (the OUTER loop): it selects next-best work and drives a wave of `ao rpi` cycles toward a `GOALS.md` directive, then post-mortems at the session-scope threshold. evolve's *cadence* (recurrence) is GC orchestration (a cron Order → `evolve-dispatch`); evolve's *logic* (which bead next, N-cycles-toward-a-goal, post-mortem) stays inside `ao evolve`.

### 4. Cron `exec` Orders for maintenance

Deterministic, no-LLM-judgment maintenance runs as GC **exec** Orders (no agent context burned):

| Order | Trigger | Runs |
|-------|---------|------|
| `compile-corpus` | cooldown 6h | `ao compile` — recompile the `.agents/` corpus (Mine → Grow → Defrag → Lint) |
| `maturity-scan` | cron 07:00 | `ao maturity --scan` — refresh inject decay-ranking / find stale entries |

See [`packs/agentops/orders/`](../../packs/agentops/orders/) for the order definitions.

## HONEST gap: order-auto-dispatch is upstream-GC, not turnkey here (soc-5jwah)

**Be honest about what dispatches, and how.** The `bead-dispatch` cooldown Order CANNOT bind a ready bead to `rpi-dispatch` on its own: GC Orders have **no per-fire variable-binding mechanism**, so the formula's required `issue` var has no value and the order self-fails on every fire:

```text
order.failed  msg=variable validation failed: - variable "issue" is required
```

Proven against the real `gc` binary (Tier 3 RED). So:

- **Works today (proven):** the City is gc-parse-valid; the controller, supervisor, Order engine, and `agentops.mayor` come up; the skills overlay lands in the spawned workdir; `ao inject` / `ao validate --gate` run there with the corpus compounding. The seam-correct manual path — `gc sling <rig>/refinery <bead>` routing a RAW bead to a worker that runs `ao rpi <bead>` — succeeds. **The honest dispatch path is MAYOR-DRIVEN** (a mayor running `bd ready` then `gc sling`).
- **Not turnkey:** order-level *autonomous* dispatch needs the upstream GC var-binding / next-ready-resolution capability (an **upstream Gas City contribution**, soc-5jwah), not an AgentOps feature. `bead-dispatch.toml` ships as a labeled REFERENCE for the intended shape. Do NOT read "gc-parse-valid" as "autonomous-dispatch-functional."

**Operator posture:** accept what GC offers today and grow with it. Mayor-driven dispatch is the shipped capability; order-auto-dispatch arrives with the upstream GC work.

## References

- [references/reference-city.md](references/reference-city.md) — anatomy of the reference City (`city.toml` substrate consumption, the `[imports.agentops]` opinion seam, the dolt 1,478-flap guard, single-prefix posture) and the pack layout.
- [references/mayor-dispatch-loop.md](references/mayor-dispatch-loop.md) — the mayor↔refinery dispatch + merge handoff in full, the THIN-SEAM boundary, the outer evolve loop, and the order-auto-dispatch gap.
- [references/using-gc.feature](references/using-gc.feature) — executable spec: an agent runs the reference City end-to-end with guided gc commands.

## Issue Tracking (shared with gc)

gc consumes the same `bd`/dolt tracker, so the bead protocol is identical whether you call `bd` or `gc bd`:

```bash
gc bd ready              # unblocked issues (same store as `bd ready`)
gc bd update <id> ...    # claim / hand off / set merge metadata
gc bd prime              # protocol refresher inside a gc-spawned worker
```
