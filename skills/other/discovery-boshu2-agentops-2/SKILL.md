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
