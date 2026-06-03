---
name: eval-outcomes
description: Grade against Outcomes as a holdout-safe projection of the locked eval substrate — one bar, many runtimes.
skill_api_version: 1
practices:
- continuous-delivery
- ddd
hexagonal_role: supporting
consumes:
- validation
- ratchet
- council
produces:
- skills/council/schemas/verdict.json
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: execution
  dependencies: [validation, ratchet]
  stability: experimental
output_contract: "skills/council/schemas/verdict.json (one council verdict record)"
---

# /eval-outcomes — Outcomes as a Projection of the Locked Eval Substrate

Grade an agent's output through Anthropic **Outcomes** (or any model) without ever forking the bar: the rubric is *compiled from* the locked eval substrate (`~/.agents/evals/SCHEMA.md`), the grader runs holdout-safe, and the score is ingested back as the **one** council verdict record. Outcomes is a *projection*, never an alternate authority.

## Overview

Outcomes (Anthropic, May 2026) closes the loop "agent runs → grader scores against a rubric → agent retries." AgentOps already has a locked, council-reviewed eval substrate (Suites/Tasks, deterministic-or-LLM scorers, dev/holdout splits, a global Dolt-synced holdout burn ledger, validity gates 1–9, `judge_content_hash` drift detection). This skill makes Outcomes a **grading transport** for that substrate rather than a second bar:

- **`ao eval outcomes compile <input.json>`** — projects a locked Task + criteria into a holdout-safe Outcomes rubric payload. It **refuses** to emit any `target`/`ground_truth` field (Managed Agents are not ZDR).
- A grader runs the rubric against the candidate output — cloud Managed Agents in the bushido self-hosted sandbox (Claude path), or the local Inspect AI / llama.cpp Qwen grader (Codex/NTM path). Both grade against the *same* compiled rubric.
- **`ao eval outcomes ingest <score.json> --json`** — converts the returned score into one council verdict record (`skills/council/schemas/verdict.json` shape), closing the Outcomes → Knowledge Flywheel loop.

It **extends** two existing skills, rewriting neither:
- [validation](../validation/SKILL.md) — Outcomes is an additional grading transport for the existing per-criterion rubric; the verdict output stays the council verdict schema.
- [ratchet](../ratchet/SKILL.md) — Outcomes-derived deltas feed the same Brownian-Ratchet gate records; no new gate semantics.

## ⚠️ Critical Constraints

- **Managed Agents are NOT ZDR.** Never send a holdout `target`, `ground_truth`, or PII into an Outcomes payload. **Why:** any leak ships answers to Anthropic permanently and breaks holdout isolation — the load-bearing eval invariant. `ao eval outcomes compile` enforces deny-by-default (allowlist-only field copy + a re-parse guard + schema `additionalProperties:false`); a CI check verifies it, not a runtime hook.
- **SCHEMA.md is the authority; the rubric is a derived artifact.** **Why:** the compiled rubric carries `judge_content_hash`, so a stale cloud rubric self-invalidates exactly like a stale local judge (gate #2 parity). Never hand-edit a cloud rubric.
- **Every holdout grade registers a global Dolt burn.** **Why:** routing all holdout grades through `ao eval outcomes ingest` keeps gate #3 (the global burn ledger) unconditional — a cloud/Codex run against holdout cannot silently bypass quota.
- **Do not relitigate the locked substrate.** **Why:** this skill is a projection; changes to splits/scorers/gates belong to the `ao-evals-schema-v1` council process, not here.

## Workflow

### Phase 1: Compile a holdout-safe rubric

```bash
ao eval outcomes compile task-input.json > rubric.json
```

Projects the locked Task + per-criterion rubric into an Outcomes payload, stripping every holdout field. If a holdout value would leak, compile refuses with a non-zero exit.

**Checkpoint:** `rubric.json` carries `judge_content_hash` and contains no `target`/`ground_truth` keys.

### Phase 2: Grade against the rubric

- **Claude path:** submit the rubric + candidate output to a Managed Agents Session in the bushido sandbox (`100.109.17.108`); the grader sees criteria + candidate only, never the holdout target.
- **Codex/NTM path:** grade locally via the Inspect AI runner (dev split) or dispatch to the bushido llama.cpp Qwen grader over tailnet. Same rubric, byte-identical verdict.

**Checkpoint:** the score payload carries the same `judge_content_hash` as the rubric (parity), else discard it as stale.

### Phase 3: Ingest into the one verdict record

```bash
ao eval outcomes ingest score.json --json
```

Emits a council verdict record (PASS/WARN/FAIL + per-criterion breakdown) on the existing `eval-verdict-compiler` pipeline. A holdout grade registers a global Dolt burn here.

**Checkpoint:** the verdict matches `skills/council/schemas/verdict.json`, identical in shape to a local `ao eval run` verdict.

## Output Specification

**Format:** JSON. **Filename:** caller-chosen (`<run>.verdict.json`). **Structure:** one council verdict record — `result` (PASS|WARN|FAIL), `satisfaction_score`, per-criterion `breakdown`, `judge_content_hash`.

## Quality Rubric

- [ ] Compiled rubric contains zero `target`/`ground_truth` keys (deny-by-default held).
- [ ] Rubric + score share the same `judge_content_hash` (no stale-bar drift).
- [ ] Holdout grades registered a global Dolt burn via ingest.
- [ ] Ingested verdict matches the council verdict schema — one bar, not a fork.

## Examples

```bash
# Project a locked Task into a holdout-safe rubric, grade, then ingest the score
ao eval outcomes compile task-input.json > rubric.json
# (grade rubric.json against the candidate via cloud or local grader -> score.json)
ao eval outcomes ingest score.json --json
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `compile` exits non-zero "would leak into the rubric payload" | A holdout `target`/`ground_truth` reached the allowlist boundary | Working as intended — never bypass; grade against the dev split or fix the input shape |
| Verdict differs from a local `ao eval run` | Stale rubric (`judge_content_hash` mismatch) | Recompile from the current Task; discard the stale score |
| Holdout quota unexpectedly consumed | A cloud/Codex holdout grade registered a burn (correct) | Expected — gate #3 is unconditional; use the dev split for iteration |

## See Also

- [validation](../validation/SKILL.md) — the per-criterion rubric Outcomes transports
- [ratchet](../ratchet/SKILL.md) — gate records Outcomes deltas feed
- [council](../council/SKILL.md) — the verdict schema ingest emits
- [skill-auditor](../skill-auditor/SKILL.md) — audit this skill before declaring stable
