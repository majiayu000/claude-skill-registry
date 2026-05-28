---
name: discovery
description: Create dense execution packets.
practices:
- adr
- lean-startup
- mythical-man-month
hexagonal_role: domain
consumes:
- brainstorm
- design
- plan
- pre-mortem
- research
- shared
produces:
- .agents/plans/*.md
- bd-issue
- execution-packet.json
context_rel:
- kind: shared-kernel
  with: standards
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: full
metadata:
  tier: meta
  dependencies:
  - brainstorm
  - design
  - research
  - plan
  - pre-mortem
  - shared
output_contract: .agents/plans/YYYY-MM-DD-*.md, beads, epic-id
---
# /discovery - Dense Discovery Phase Adapter

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

> **Loop position:** move 1 (shape intent as BDD) plus the seed for move 3
> (slice candidates) of the [operating loop](../../docs/architecture/operating-loop.md).
> Discovery turns a goal plus delegated child artifacts into one dense execution
> packet for `/crank` and `/validation`.

## Strict Delegation Contract (default)

Discovery delegates to `/brainstorm` (conditional), `/design` (conditional),
`/research`, `/plan`, and `/pre-mortem` via declared skill invocations.
Strict delegation is the **default**.

**Anti-pattern to reject:** inlining `/research` work (grep + read + synthesize), collapsing `/plan` into an inline decomposition, skipping `/pre-mortem`. See [`../shared/references/strict-delegation-contract.md`](../shared/references/strict-delegation-contract.md) for the full contract and supported compression escapes (`--quick`, `--skip-brainstorm`, `--interactive`/`--auto`, `--no-scaffold`).

See [`docs/learnings/orchestrator-compression-anti-pattern.md`](../../docs/learnings/orchestrator-compression-anti-pattern.md) for the live compression signature.
See [`references/isolation-contract.md`](references/isolation-contract.md) for the mechanical four-lever model and the compression patterns flagged by `scripts/check-skill-isolation.sh`. See [`references/best-practices.md`](references/best-practices.md) for the lifecycle principle + anti-pattern citation table.

## Narrow Waist

Discovery does not carry raw child-skill output forward. It records artifact
paths, verdicts, the `hexagon:` boundary block from
[`docs/architecture/intent-to-loop-hexagon.md`](../../docs/architecture/intent-to-loop-hexagon.md),
and the six Context Density Rule fields:

| Field | Meaning |
|-------|---------|
| `intent` | Behavior or capability to produce |
| `boundary` | Bounded context, non-goals, write scope |
| `evidence` | Acceptance examples, tests, gates, verdicts |
| `decision` | Why this plan shape was chosen |
| `constraint` | Safety, runtime, token, and process limits |
| `next_action` | Exact `/crank` or follow-up command |

Everything else stays in child artifacts and is linked by path.

## Discovery To Plan Port

Use the [Skill Ports and Adapters](../../docs/contracts/skill-ports-and-adapters.md)
vocabulary and the [Intent-to-Loop Hexagon](../../docs/architecture/intent-to-loop-hexagon.md)
for the boundary between Discovery and Plan:

| Boundary piece | Discovery contract |
|---|---|
| Inbound port | `shape_intent` from operator goal or BDD intent |
| Outbound port | `plan_slices` into `/plan` |
| Driving adapter | `/discovery` skill invocation |
| Driven adapter | `/plan` skill invocation plus bd/file persistence |
| Context packet | density block, artifact links, acceptance examples, non-goals, constraints |
| Guard adapter | `/pre-mortem` verdict before packet handoff |

Executable acceptance: [references/discovery.feature](references/discovery.feature) — Discovery hands dense intent across the `plan_slices` port (promoted from inline; soc-qk4b.2).

## Open-Ended Path (generate-winnow → operationalize → refine)

> **Additive to the default flow — it does not replace the strict-delegation contract or the artifact-first DAG.** This path activates for open-ended "improve the project"-style goals (`"improve the project"`, `"what should we build next"`, `"make X more robust"`) OR when `--ideate` is passed. For a specific goal, the default flow (brainstorm-clarify → research → plan → pre-mortem) is unchanged.

On the open-ended path, Discovery prepends the generate-winnow methodology before research/plan and adds two steps after planning. Full detail lives in [`../brainstorm/references/bead-operationalization.md`](../brainstorm/references/bead-operationalization.md) and [`../brainstorm/references/ideation-mode.md`](../brainstorm/references/ideation-mode.md).

1. **Ideate (delegate to `/brainstorm --ideate`).** Invoke `/brainstorm` in **ideation mode** (a real skill invocation — strict delegation still applies; do NOT inline the 30-idea generation). It returns a ranked portfolio of **15** ideas (top 5 + next 10) with how/perceive/implement notes, rubric scores, and red-team findings.
2. **Research + Plan + Pre-mortem.** Run the normal artifact-first DAG over the selected portfolio, scoped to the winnowed ideas rather than a single goal.
3. **Operationalize.** Turn the ranked portfolio into a comprehensive, granular set of **self-documenting `bd` beads** — tasks, subtasks, dependency structure (`bd dep add`), and **explicit test tasks** (unit + e2e with detailed logging). Each bead carries what/why/how/risks/success so the original plan markdown never needs to be consulted again. Overlap-check against existing beads (`bd list --json`) before creating — merge, don't duplicate.
4. **Refine in plan space (4-5 passes).** Before handing the packet to `/crank`, run **4-5 refinement passes** over the bead set. Each pass: **re-read AGENTS.md** (especially after compaction), check every bead for sense and optimality, and **DO NOT OVERSIMPLIFY / DO NOT LOSE FEATURES OR FUNCTIONALITY**. Validate between passes (no dependency cycles; every leaf actionable via `bd ready`).

> Tracking is **`bd`**, never `br`/`bv` — this is AgentOps. The operationalize and refine steps consume `/brainstorm`'s ideation output; see [`../brainstorm/references/bead-operationalization.md`](../brainstorm/references/bead-operationalization.md).

Executable acceptance for this path: [references/discovery.feature](references/discovery.feature) (ideation/operationalize/refine scenarios, ag-yw0).

## Execution

Run the artifact-first DAG in [references/dag.md](references/dag.md). That
file owns the executable workflow, state shape, gate detail, per-step detail,
and the acceptance-criteria YAML contract.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--auto` | on | Fully autonomous (no human gates). Inverse of `--interactive`. Passed through to `/research` and `/plan`. |
| `--interactive` | off | Human gates in research and plan (STEP 3, STEP 4). Does NOT affect pre-mortem gate. |
| `--skip-brainstorm` | auto | Skip STEP 1 brainstorm when goal is already specific |
| `--ideate` | auto | Force the open-ended generate-winnow path: delegate to `/brainstorm --ideate` (30→5→15), then operationalize into self-documenting `bd` beads and refine 4-5x in plan space. Auto-on for open-ended goals. See [Open-Ended Path](#open-ended-path-generate-winnow--operationalize--refine). |
| `--complexity=<level>` | auto | Force complexity level (`fast` / `standard` / `full`) |
| `--no-budget` | off | Disable phase time budgets |
| `--no-scaffold` | off | Skip scaffold auto-invocation in STEP 4.5 (canonical name) |
| `--no-lifecycle` | off | **DEPRECATED ALIAS** for `--no-scaffold`. Honored through v2.40.0 for transition. When both flags are passed, they are equivalent. |

> **Deprecation note:** When Claude encounters `--no-lifecycle` on `/discovery`, treat it as `--no-scaffold` and mention the deprecation inline in the phase summary (e.g., `"used deprecated --no-lifecycle, prefer --no-scaffold"`). This surfaces guidance in the RPI output without a runtime parser.

## Quick Start

```bash
/discovery "add user authentication"              # full discovery
/discovery --interactive "refactor payment module" # human gates in research + plan
/discovery --skip-brainstorm "fix login bug"       # skip brainstorm for specific goals
/discovery --complexity=full "migrate to v2 API"   # force full council ceremony
```

## Output Specification

**Format:** compact markdown phase summary to stdout plus JSON execution packet
on disk.

**Files written:**

- `.agents/research/<topic-slug>.md` - research artifact path only
- `.agents/plans/YYYY-MM-DD-<goal-slug>.md` - plan document path only
- `.agents/council/YYYY-MM-DD-pre-mortem-<topic>.md` - pre-mortem verdict path only
- `.agents/rpi/execution-packet.json` - latest dense packet
- `.agents/rpi/runs/<run-id>/execution-packet.json` - per-run archive when `run_id` is set
- `.agents/rpi/phase-1-summary-YYYY-MM-DD-<goal-slug>.md` - compact discovery summary

**Exit signal:** completion marker (`<promise>DONE</promise>` or `<promise>BLOCKED</promise>`) — see Completion Markers below.

## Completion Markers

```
<promise>DONE</promise>      # Discovery complete, epic-id + execution-packet ready
<promise>BLOCKED</promise>   # Pre-mortem failed 3x, manual intervention needed
```

## Troubleshooting

Read `references/troubleshooting.md` for common problems and solutions.

## Reference Documents

- [references/dag.md](references/dag.md) — executable workflow, state shape, gate detail, per-step detail, acceptance-criteria YAML contract
- [references/complexity-auto-detect.md](references/complexity-auto-detect.md) — precedence contract for keyword vs issue-count classification
- [references/idempotency-and-resume.md](references/idempotency-and-resume.md) — re-run safety and resume behavior
- [references/phase-budgets.md](references/phase-budgets.md) — time budgets per complexity level
- [references/troubleshooting.md](references/troubleshooting.md) — common problems and solutions
- [references/output-templates.md](references/output-templates.md) — execution packet and phase summary formats
- [references/phase-data-contracts.md](references/phase-data-contracts.md) — phase artifact data contracts (cited from references/isolation-contract.md)

**See also:** [brainstorm](../brainstorm/SKILL.md), [design](../design/SKILL.md), [research](../research/SKILL.md), [plan](../plan/SKILL.md), [pre-mortem](../pre-mortem/SKILL.md), [crank](../crank/SKILL.md), [rpi](../rpi/SKILL.md), [scaffold](../scaffold/SKILL.md)
