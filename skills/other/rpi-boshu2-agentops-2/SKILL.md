---
name: rpi
description: Run discovery, crank, validation.
practices:
- bdd-gherkin
- ddd-bounded-context
- hexagonal-architecture
- tdd
- continuous-delivery
- dora-metrics
- agile-manifesto
- pragmatic-programmer
hexagonal_role: supporting
consumes:
- crank
- discovery
- domain
- ratchet
- validation
produces:
- .agents/rpi/*.md
context_rel:
- kind: customer-of
  with: crank
- kind: customer-of
  with: discovery
- kind: customer-of
  with: validation
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
  - domain
  - discovery
  - crank
  - validation
  - ratchet
  internal: false
output_contract: .agents/rpi/YYYY-MM-DD-*.md
---

# /rpi - Full Lifecycle Orchestrator

> Quick ref: `/discovery` -> `/crank` -> `/validation`, then report.

**Execute this workflow. Do not only describe it.** RPI is autonomous unless
`--interactive` is set. The user touchpoint is after validation, or after a
real blocked state exhausts retries. Read
[references/autonomous-execution.md](references/autonomous-execution.md) when
you need the full autonomy contract.

When an external executor fails but the code surface may still be valid, read
[references/codex-executor.md](references/codex-executor.md) and recover through
Codex direct checks before declaring a source-level regression.

## Loop position

`/rpi` is the orchestrator across **every move** of the [operating loop](../../docs/architecture/operating-loop.md): BDD intent → vertical slices → conflict-free wave → bead acceptance → evidence + learning capture. It delegates each move to the skill that owns it (`/discovery`, `/plan`, `/crank`, `/validation`, `/forge`/`/retro`), and enforces three loop-level invariants:

- **No move-skipping.** Strict delegation is on by default; phases never compress, and validation cannot be skipped. The lifecycle objective is preserved across the whole loop.
- **The first failing test is the bead's contract.** With `--test-first` on (the default), `/crank` is invoked with the TDD-per-slice discipline; `--no-test-first` is an explicit opt-out, not a fast path.
- **Acceptance examples close the bead, not activity.** Validation FAIL re-cranks on the same objective up to 3 attempts; DONE requires the acceptance roll-up in the [slice-validation template](../../docs/templates/slice-validation.md) to be fully green.
- **Ports stay visible.** Preserve the
  [Intent-to-Loop Hexagon](../../docs/architecture/intent-to-loop-hexagon.md)
  boundary as the objective crosses `shape_intent`, `persist_intent`,
  `plan_slices`, `execute_wave`, `validate_acceptance`, and `record_evidence`.
- **Context density survives phase boundaries.** Apply the [Context Density Rule](../domain/references/context-density-rule.md) to every phase handoff and final report: keep intent, boundary, evidence, decision, constraint, and next action; omit or link anything else.

## Core Contract

RPI delegates via `Skill(skill="discovery", ...)`,
`Skill(skill="crank", ...)`, and `Skill(skill="validation", ...)` as separate
tool invocations. Keep strict delegation on by default; do not compress phases,
replace phase skills with direct agent spawns, or skip validation. Read
[../shared/references/strict-delegation-contract.md](../shared/references/strict-delegation-contract.md)
for the full anti-compression contract.
See [references/isolation-contract.md](references/isolation-contract.md) for
the four-lever model, phase-isolated skill transport, and the compression
patterns `scripts/check-skill-isolation.sh` flags. See
[references/best-practices.md](references/best-practices.md) for the principle
and anti-pattern citation table.

When the runtime supports phase isolation, keep `/rpi` visible in the main
session and run each phase contract through isolated transport: phase skill
name in, bounded handoff artifact in, phase artifact/verdict/next action out.
The transport may be a daemon job, process runner, or subagent wrapper, but it
must execute the declared phase skill contract rather than doing phase work
directly.

RPI owns one lifecycle objective across all phases. Preserve the discovered
`epic_id` when present; otherwise preserve the original goal and execution
packet objective. A child bead or one ready slice is context, not a replacement
objective. `<promise>PARTIAL</promise>` from `/crank` means retry Phase 2 on the
same objective.

## Route And Classify

1. Create `.agents/rpi/`.
2. Resolve `--from`:
   - default, `research`, `plan`, `pre-mortem`, `brainstorm` -> discovery
   - `implementation` or `crank` -> implementation
   - `validation`, `vibe`, or `post-mortem` -> validation
3. If the input is a bead and `--from` is absent, resolve it with `bd show`:
   - epic -> implementation with that epic
   - child with parent -> implementation with the parent epic
4. Classify complexity:
   - `fast`: short/simple goal or `--fast-path`
   - `standard`: medium goal or one scope keyword
   - `full`: `--deep`, complex-operation keyword, 2+ scope keywords, or >120 chars
5. Log `RPI mode: rpi-phased (complexity: <level>)`.

Track state compactly:

```text
rpi_state = {
  goal: "<goal string>",
  epic_id: null,
  phase: "<discovery|implementation|validation>",
  complexity: "<fast|standard|full>",
  test_first: <true by default; false only when --no-test-first>,
  cycle: 1,
  verdicts: {}
}
```

Complex-operation keywords include `refactor`, `migrate`, `rewrite`,
`redesign`, `rearchitect`, `overhaul`, `decouple`, `deprecate`, `split`,
`extract module`, and `port`. Scope keywords include `all`, `entire`, `across`,
`everywhere`, `every file`, `system-wide`, `global`, and `codebase`.

## Phase DAG

Enter at the routed phase and run every phase after it.

1. **Discovery:** invoke `/discovery <goal> [--interactive] --complexity=<level>`
   directly or through phase-isolated skill transport.
   On DONE, read `.agents/rpi/execution-packet.json` or the run archive and
   preserve its objective spine. On BLOCKED, stop with the discovery verdict.
2. **Implementation:** invoke `/crank <epic-id>` when the packet has `epic_id`;
   otherwise invoke `/crank .agents/rpi/execution-packet.json`, directly or
   through phase-isolated skill transport. Pass `--test-first` or
   `--no-test-first` through. On DONE, record `ao ratchet record implement
   2>/dev/null || true` and continue. On PARTIAL or BLOCKED, retry the same
   objective up to 3 total attempts.
3. **Validation:** invoke `/validation <epic-id> --complexity=<level>` when an
   epic exists; otherwise invoke `/validation --complexity=<level>`, directly
   or through phase-isolated skill transport. Add `--strict-surfaces` when
   `--quality` is set. On FAIL, extract findings, re-run `/crank` on the same
   objective, then re-run `/validation`, up to 3 total validation attempts. On
   DONE, record `ao ratchet record vibe 2>/dev/null || true`.
4. **Report:** summarize phase verdicts and epic status using
   [references/report-template.md](references/report-template.md). With
   `--loop`, restart from discovery on FAIL while `cycle < max_cycles`. With
   `--spawn-next`, read `.agents/rpi/next-work.jsonl` and suggest the next
   command without invoking it. Before emitting the report, apply the Context
   Density Rule: every line should carry intent, boundary, evidence, decision,
   constraint, or next action.

## Phase Data Contract

The execution packet carries the repo execution profile through
`contract_surfaces`, `done_criteria`, and queue claim/finalize metadata. Keep
the latest alias at `.agents/rpi/execution-packet.json` and read
[references/phase-data-contracts.md](references/phase-data-contracts.md) for
schemas and archive paths.

## Complexity-Scaled Gates

### Pre-mortem
- `complexity == "low"` or `"fast"`: inline review, no spawning (`--quick`)
- `complexity == "medium"` or `"standard"`: inline fast default (`--quick`)
- `complexity == "high"` or `"full"`: full council, 2-judge minimum; max 3 total attempts

### Final Vibe
- `complexity == "low"` or `"fast"`: inline review, no spawning (`--quick`)
- `complexity == "medium"` or `"standard"`: inline fast default (`--quick`)
- `complexity == "high"` or `"full"`: full council, 2-judge minimum; max 3 total attempts

### Post-mortem (STEP 2)
- `complexity == "low"` or `"fast"`: inline review, no spawning (`--quick`)
- `complexity == "medium"` or `"standard"`: inline fast default (`--quick`)
- `complexity == "high"` or `"full"`: full council, 2-judge minimum; max 3 total attempts

## Flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--from=<phase>` | discovery | Start at discovery, implementation, or validation |
| `--discovery-artifact=<path>` | unset | With implementation start, convert an existing artifact into the handoff packet |
| `--interactive` | off | Human gates in discovery/validation |
| `--auto` | on | Fully autonomous default |
| `--loop --max-cycles=<n>` | off / 3 | Iterate when validation fails |
| `--spawn-next` | off | Surface follow-up work after reporting |
| `--test-first` | on | Pass strict-quality preference to `/crank` |
| `--no-test-first` | off | Explicitly opt out of strict-quality |
| `--fast-path` / `--deep` | auto | Force fast or full complexity |
| `--quality` | off | Make validation strict surfaces blocking |
| `--dry-run` / `--no-budget` | off | Report only, or disable phase time budgets |

## Examples

**User says:** `/rpi "add user authentication"`
Run discovery, implementation, validation, then report.

**User says:** `/rpi --from=implementation ag-23k`
Resolve the bead scope, run implementation and validation, then report.

**User says:** `/rpi --deep "refactor payment module"`
Use full council gates across the lifecycle.

Read [references/examples.md](references/examples.md) for resume,
interactive, loop, and artifact-mode examples.

## Troubleshooting

| Problem | Response |
|---------|----------|
| Discovery BLOCKED | Stop and report discovery's manual-intervention reason |
| `/crank` returns PARTIAL | Retry `/crank` on the same objective; do not narrow to a child slice |
| Validation FAIL | Re-crank with findings, then re-validate, up to 3 total attempts |
| Packet shape unclear | Read [references/phase-data-contracts.md](references/phase-data-contracts.md) |
| External executor fails | Read [references/codex-executor.md](references/codex-executor.md), run direct Codex validation, and only create follow-up work for reproducible source failures |

## Reference Documents

- [references/orchestrator-compression-anti-pattern.md](references/orchestrator-compression-anti-pattern.md) — Phase-skipping failure mode; rationalizations to reject
- [references/autonomous-execution.md](references/autonomous-execution.md)
- [references/installed-plugin-version-not-repo-head.md](references/installed-plugin-version-not-repo-head.md) — `/rpi` loads from `~/.claude/plugins/cache/`, not the repo working tree; verify which version is active before measuring
- [references/complexity-scaling.md](references/complexity-scaling.md)
- [references/context-windowing.md](references/context-windowing.md) — OPT-IN large-repo mode (`--large-repo`); NOT part of the default RPI path. Default discovery/research does not generate `.agents/rpi/context-shards/latest.json`.
- [references/codex-executor.md](references/codex-executor.md)
- [references/discovery-artifact-mode.md](references/discovery-artifact-mode.md)
- [references/error-handling.md](references/error-handling.md)
- [references/examples.md](references/examples.md)
- [references/gate-retry-logic.md](references/gate-retry-logic.md)
- [references/gate4-loop-and-spawn.md](references/gate4-loop-and-spawn.md)
- [references/phase-budgets.md](references/phase-budgets.md)
- [references/phase-data-contracts.md](references/phase-data-contracts.md)
- [references/report-template.md](references/report-template.md)
- [references/troubleshooting.md](references/troubleshooting.md)
