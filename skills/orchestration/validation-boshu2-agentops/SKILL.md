---
name: validation
description: Run post-implementation validation.
practices:
- llm-eval-harness
- dora-metrics
- sre
hexagonal_role: domain
consumes:
- forge
- post-mortem
- retro
- shared
- vibe
produces:
- .agents/research/*.md
- result.json
- verdict.json
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
  - vibe
  - post-mortem
  - retro
  - forge
  - shared
output_contract: skills/council/schemas/verdict.json
---
# /validation — Full Validation Phase Orchestrator

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

> **Loop position:** moves 6 (slice acceptance) + bead acceptance roll-up of the [operating loop](../../docs/architecture/operating-loop.md). Consumes wave outputs; produces a [slice-validation roll-up](../../docs/templates/slice-validation.md): every Given/When/Then from the intent issue must map to a passing test. Activity logs do not close beads.

## Strict Delegation Contract (default)

Validation delegates to `/vibe`, `/post-mortem`, `/retro`, and `/forge` (plus lifecycle skills `/test`, `/deps`, `/review`, `/perf`) via `Skill(skill="<name>", ...)` calls — **separate tool invocations**. Strict delegation is the **default**.

**Anti-pattern to reject:** spawning judges via `Agent()` in place of `/vibe`, inlining post-mortem analysis, skipping `/forge`. See [`../shared/references/strict-delegation-contract.md`](../shared/references/strict-delegation-contract.md) for the full contract and supported compression escapes (`--quick`, `--no-retro`, `--no-forge`, `--no-lifecycle`, `--no-behavioral`, `--allow-critical-deps`).

See [`docs/learnings/orchestrator-compression-anti-pattern.md`](../../docs/learnings/orchestrator-compression-anti-pattern.md) for the live compression signature.
See [`references/isolation-contract.md`](references/isolation-contract.md) for the four-lever model and the compression patterns `scripts/check-skill-isolation.sh` flags in phase-skill SKILL.md bodies. See [`references/best-practices.md`](references/best-practices.md) for the lifecycle principle + anti-pattern citation table.

Validation owns the `validate_acceptance` port in the
[Intent-to-Loop Hexagon](../../docs/architecture/intent-to-loop-hexagon.md).
The roll-up must preserve bounded context, context packet, guard adapters, done
state, and fresh proof for each accepted scenario. Apply the
[Completion-Claim Kernel](../shared/validation-contract.md#completion-claim-kernel)
before accepting DONE/closed/green claims.

## Execution

Run the DAG in [references/dag.md](references/dag.md) — STEP 1 (vibe) → 1.5 (four-surface closure) → 1.6 (test pyramid) → 1.6b (validation-lane budget guard) → 1.7 (lifecycle: test/deps/review/perf) → 1.8 (behavioral) → 2 (post-mortem) → 3 (retro) → 4 (forge) → 5 (phase summary), no stopping between steps. That file owns the executable workflow, gate detail, blocking conditions, phase summary format, phase budgets, and the expensive-command policy.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--complexity=<level>` | auto | Force complexity level (`fast` / `standard` / `full`). Matches `/rpi` and `/discovery` syntax. |
| `--interactive` | off | Human gates in validation report review (before writing summary). Does NOT override `/vibe` council autonomy. |
| `--no-lifecycle` | off | Skip ALL lifecycle checks in STEP 1.7 (test, deps, review, perf) |
| `--lifecycle=<tier>` | matches complexity | Controls which lifecycle skills fire: `minimal` (test only), `standard` (+deps, +review), `full` (+perf) |
| `--no-retro` | off | Skip retro step only |
| `--no-forge` | off | Skip forge step only |
| `--no-budget` | off | Disable phase time budgets |
| `--strict-surfaces` | off | Make all 4 surface failures blocking (FAIL instead of WARN). Passed automatically by `/rpi --quality`. |
| `--allow-critical-deps` | off | Allow shipping with CVSS >= 9.0 vulnerabilities (acknowledged risk acceptance) |

See [references/flags.md](references/flags.md) for flag interactions, precedence, and combined-flag examples.

## Expensive Command Policy

Routine validation is targeted by default. Broad proof commands such as
`go test -race`, `go test -shuffle`, `go test -count=N` with `N > 1`, eval
runners, retrieval bench, headless runtime smoke, and release gates require
explicit operator/release/acceptance-criteria context. If one is run, record the
reason and timeout in the phase summary.

When validating release-bound work, see [references/release-readiness-gates.md](references/release-readiness-gates.md) for the additional gates that must pass before shipping.

## Quick Start

```bash
/validation ag-5k2                        # validate epic with full close-out
/validation                               # validate recent work (no epic)
/validation --complexity=full ag-5k2      # force full council ceremony
/validation --no-retro ag-5k2             # skip retro only
/validation --no-forge ag-5k2             # skip forge only
```

## Output Specification

**Format:** markdown summary to stdout + on-disk artifacts. Files written: `.agents/rpi/phase-3-summary-YYYY-MM-DD-validation.md` (phase summary), `.agents/post-mortems/YYYY-MM-DD-<topic>.md`, `.agents/learnings/<slug>.md`, `.agents/findings/registry.jsonl` (appended), `.agents/ratchet/state.json`. **Exit signal:** completion marker — see below.

## Completion Markers

```
<promise>DONE</promise>    # Validation passed, learnings captured
<promise>FAIL</promise>    # Vibe failed, re-implementation needed (findings attached)
```

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md).

## Reference Documents

- [references/validation.feature](references/validation.feature) — Executable spec: criterion→test roll-up, strict delegation, verdict.json, strict-surface blocking (soc-qk4b.2)
- [references/dag.md](references/dag.md) — executable workflow, gate detail, blocking conditions, phase summary format, phase budgets, expensive-command policy
- [references/per-criterion-rubric.md](references/per-criterion-rubric.md) — per-criterion verdict rubric and runner contract
- [references/step-1.8-behavioral-validation.md](references/step-1.8-behavioral-validation.md) — STEP 1.8 holdout + agent-spec evaluator council
- [references/four-surface-closure.md](references/four-surface-closure.md) — four-surface closure validation (code + docs + examples + proof)
- [references/forge-scope.md](references/forge-scope.md) and [references/idempotency-and-resume.md](references/idempotency-and-resume.md) — forge scoping, rerun behavior, standalone mode
- [references/remote-and-multi-repo-validation.md](references/remote-and-multi-repo-validation.md)
- [references/phase-data-contracts.md](references/phase-data-contracts.md) — phase artifact data contracts (cited from references/isolation-contract.md)
