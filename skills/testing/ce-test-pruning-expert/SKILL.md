---
name: ce-test-pruning-expert
description: >
  Identify redundant or low-value tests using unique-lines and overlap evidence
  while preserving behavior coverage, with Option A/B/C routing from the Test
  Quality Method.
---

# CE Test Pruning Expert

This skill implements the **Pruner** role from ADR-030 and mirrors the prompt
in `docs/improvement/test-quality-method/pruner.md`.

## Required references

- `docs/improvement/test-quality-method/README.md` (canonical method + options)
- `docs/improvement/test-quality-method/pruner.md` (full role prompt)

## Use this skill when

- Triaging over-testing reports.
- Reducing redundant generated tests.
- Consolidating near-duplicate tests into parameterized suites.

## Focus option handling

- **Option A (Test-Focused):** run the full pruning workflow.
- **Option B (Code-Focused):** skip pruning by default; only process explicit
  test-removal requests.
- **Option C (Full Cycle):** run Option A and pass risk-marked removals to
  code-quality and dead-code reviewers before implementation.

## Core principles

1. Zero-unique-line tests are candidates, not automatic removals.
2. Identical coverage fingerprints indicate redundancy risk.
3. Behavioral uniqueness can justify retention even with low line uniqueness.

## Workflow

1. Confirm the selected focus option (`A`, `B`, or `C`).
2. Gather evidence:

```bash
python scripts/over_testing/detect_redundant_tests.py
python scripts/over_testing/estimator.py --recommend
```

3. Review primary artifacts:
- `reports/over_testing/per_test_summary.csv`
- `reports/over_testing/redundant_tests.csv`

4. Classify each test:
- `Remove`: redundant and behaviorally duplicative.
- `Refactor`: preserve behavior but merge/parameterize.
- `Keep`: unique behavioral guardrail.

5. Validate removal safety:
- no sole-provider line coverage loss
- no regression-specific or issue-tagged protection removed

## Output contract

For each candidate include:
- test id/path
- evidence (unique lines, overlap fingerprint, assertion profile)
- recommendation (`Remove`, `Refactor`, `Keep`)
- risk note and required follow-up
- selected focus option (`A`, `B`, or `C`) and why pruning is in-scope

## Constraints

- Never remove without evidence-backed safety analysis.
- Coordinate with `ce-deadcode-hunter` if only tests touch a code path.
- Submit final pruning batches to `ce-devils-advocate`.
