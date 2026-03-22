---
name: ce-deadcode-hunter
description: >
  Identify unreachable or non-contributing source code and separate true dead code
  from merely untested reachable paths, with Test Quality Method Option A/B/C
  routing.
---

# CE Dead-Code Hunter

This skill implements the **Dead-Code Hunter** role from ADR-030 and mirrors
the prompt in `docs/improvement/test-quality-method/deadcode_hunter.md`.

## Required references

- `docs/improvement/test-quality-method/README.md` (canonical method + options)
- `docs/improvement/test-quality-method/deadcode_hunter.md` (full role prompt)

## Use this skill when

- Proposing source removals.
- Investigating code only exercised by tests.
- Reducing maintenance surface without behavioral regressions.

## Focus option handling

- **Option A (Test-Focused):** limit analysis to source paths implicated by
  pruning and overlap findings.
- **Option B (Code-Focused):** run the full dead-code reachability audit.
- **Option C (Full Cycle):** run full audit and reconcile with Option A test
  proposals before classifying removals.

## Core missions

1. Identify truly unreachable code paths.
2. Distinguish dead code from untested but reachable code.
3. Produce evidence-backed removal candidates with risk labels.

## Workflow

1. Confirm the selected focus option (`A`, `B`, or `C`).
2. Start with structural evidence:

```bash
python scripts/anti-pattern-analysis/analyze_private_methods.py
```

3. Cross-check coverage artifacts:
- `reports/over_testing/gaps.csv`
- `reports/over_testing/line_coverage_counts.csv`

4. Validate dynamic reachability:
- lazy imports in `src/calibrated_explanations/__init__.py`
- plugin registration/entry points
- environment-specific branches

5. Classify each candidate:
- `Dead`: unreachable from any supported runtime path.
- `Untested`: reachable but not covered.
- `Needs investigation`: dynamic/conditional path not yet proven.

## Output contract

For each candidate provide:

- location (`file:line`)
- reachability evidence
- category (`Dead`, `Untested`, `Needs investigation`)
- recommended action (remove, keep + test, or defer)
- selected focus option (`A`, `B`, or `C`) and why this candidate is in-scope

## Constraints

- Analysis-first skill; no bulk deletions without explicit approval.
- Prefer conservative classification when dynamic reachability is uncertain.
- Coordinate with `ce-test-pruning-expert` when tests are the only callers.
