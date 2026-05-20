---
name: ce-test-quality-method
description: >
  Orchestrate end-to-end ADR-030 test-quality remediation by routing work across
  specialist skills (ce-test-pruning-expert, ce-test-creator, ce-test-audit,
  ce-code-quality-auditor, ce-deadcode-hunter, ce-devils-advocate) using the Test
  Quality Method with Option A/B/C focus selection.
---

# CE Test Quality Method

This skill is the ADR-030 integrator. It combines implementer and process
architect responsibilities and must align with the test-quality-method docs and
agent prompts.

## Required references

- `docs/improvement/test-quality-method/README.md` (canonical method + options)
- `docs/improvement/test-quality-method/implementer.md` (execution prompt)
- `docs/improvement/test-quality-method/process_architect.md` (workflow prompt)

## Specialist skill to prompt mapping

- `ce-test-pruning-expert` -> `docs/improvement/test-quality-method/pruner.md`
- `ce-test-creator` -> `docs/improvement/test-quality-method/test_creator.md`
- `ce-test-audit` -> `docs/improvement/test-quality-method/anti_pattern_auditor.md`
- `ce-code-quality-auditor` -> `docs/improvement/test-quality-method/code_quality_auditor.md`
- `ce-deadcode-hunter` -> `docs/improvement/test-quality-method/deadcode_hunter.md`
- `ce-devils-advocate` -> `docs/improvement/test-quality-method/devils_advocate.md`

## Use this skill when

- Running end-to-end test quality remediation.
- Reconciling outputs from specialist skills into one execution plan.
- Sequencing over-testing reduction with safety checks.

## Focus option handling

- **Option A (Test-Focused):** run coverage-context and redundancy analysis,
  prioritize `ce-test-pruning-expert`, `ce-test-creator`, and `ce-test-audit`.
- **Option B (Code-Focused):** run code-quality and dead-code loop, prioritize
  `ce-code-quality-auditor` and `ce-deadcode-hunter`; run `ce-test-audit` only
  for hard-gate checks.
- **Option C (Full Cycle):** run Option A then Option B and reconcile combined
  coverage, redundancy, and maintainability tradeoffs before execution.

## Specialist inputs

- `ce-test-pruning-expert`
- `ce-deadcode-hunter`
- `ce-test-creator`
- `ce-code-quality-auditor`
- `ce-test-audit`
- `ce-devils-advocate`

## Consolidation workflow

1. Select focus option (`A`, `B`, or `C`) from `README.md` and state it in the plan header.
2. Collect specialist reports from `reports/over_testing/`.
3. Validate data freshness (`metadata.json`, coverage-context provenance).
4. Cross-check proposal conflicts (e.g., remove test vs keep behavior guardrail).
5. Produce `final_remedy_plan.md` with:
- findings summary
- phased action list
- rollback points
- coverage-risk checkpoints

## Execution workflow

1. Execute low-risk batches first (small, reversible changes).
2. Re-run relevant verification gates for the selected focus option after each batch.
3. Stop and remediate immediately if coverage or behavior regresses.

## Output contract

Return:

1. Consolidated remedy plan with selected focus option (`A`, `B`, or `C`).
2. Ordered execution phases with risk level.
3. Validation evidence per phase.

## Constraints

- Never drop below enforced coverage gates.
- Never delete sole-provider tests without replacement behavior coverage.
- Keep decisions evidence-based and traceable to ADR-030 priorities.
