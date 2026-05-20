---
name: aidd-loop
description: Enforces loop-mode discipline for implement/review/qa (packs, scope, no questions). Use when loop stages require bounded scope and retry policy.
lang: en
model: inherit
user-invocable: false
---

Follow `feature-dev-aidd:aidd-core` for output contract and DocOps.

## Loop discipline
1. Read order: loop pack -> review pack (if any) -> fix_plan.json when verdict=REVISE -> rolling context pack.
2. Excerpt-first: do not read full PRD/plan/tasklist/spec when the loop pack excerpt covers Goal/DoD/Boundaries/Expected paths/Size budget/Tests/Acceptance.
3. No questions in loop-mode; record blockers/handoff instead.
4. REVISE: reuse the same scope, follow fix_plan.json, and do not widen boundaries.
5. Scope guard: out-of-scope -> WARN + handoff; forbidden -> BLOCKED. Never expand boundaries yourself.
6. Tests: follow loop pack or reviewer policy; do not invent new test requirements.
7. No large logs/diffs in chat; link to `aidd/reports/**`.
8. Block policy: `strict` fail-fast on any blocked step; `ralph` uses policy matrix v2 (`hard_block|recoverable_retry|warn_continue`) with bounded retries for recoverable reasons.
9. For recoverable blocked retries, emit observability fields: `recoverable_blocked`, `recovery_path`, `retry_attempt`.

## Preload matrix v2
- Roles: `implementer`, `reviewer`, `qa`.
- This skill must not be preloaded for other subagents.

## Canonical shared Python entrypoints
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-loop/runtime/loop_pack.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-loop/runtime/loop_step.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-loop/runtime/loop_run.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-loop/runtime/preflight_result_validate.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-loop/runtime/output_contract.py`
- Preflight preparation is stage-chain-internal and not an operator command.

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-loop/runtime/loop_pack.py`
- When to run: before loop stage execution to assemble bounded evidence input.
- Inputs: ticket/scope context and available stage artifacts (`readmap`, `review pack`, context pack).
- Outputs: deterministic loop pack summary for implement/review/qa orchestration.
- Failure mode: non-zero exit when required upstream artifacts are missing or malformed.
- Next action: repair missing prerequisites and rerun pack generation.

### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-loop/runtime/loop_run.py`
- When to run: stage-chain-orchestrated loop execution for bounded stage retries.
- Inputs: loop mode/profile, ticket/scope context, and stage-specific payloads.
- Outputs: loop execution status with deterministic retry/blocked metadata.
- Failure mode: non-zero exit on invalid loop payload, policy violation, or unrecoverable blocked condition.
- Next action: apply fix plan or handoff policy action, then rerun with unchanged scope.

## Additional resources
- Loop stage-chain reference: [reference.md](reference.md) (when: stage-chain path/fallback behavior needs clarification; why: confirm canonical chain and bounded recovery policy).
- Loop pack template source: [templates/loop-pack.template.md](templates/loop-pack.template.md) (when: loop pack format is unclear; why: confirm canonical sections seeded by init/runtime).
