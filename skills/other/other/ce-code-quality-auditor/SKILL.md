---
name: ce-code-quality-auditor
description: >
  Audit source and tests for ADR-030 anti-patterns, determinism failures,
  API-boundary violations, and test-helper leakage with Option A/B/C handling
  from the Test Quality Method.
---

# CE Code Quality Auditor

This skill combines the **Code Quality Auditor** and **Anti-Pattern Auditor**
roles from ADR-030.

## Required references

- `docs/improvement/test-quality-method/README.md` (canonical method + options)
- `docs/improvement/test-quality-method/code_quality_auditor.md` (code-quality prompt)
- `docs/improvement/test-quality-method/anti_pattern_auditor.md` (anti-pattern prompt)

## Use this skill when

- Reviewing overall source/test quality before cleanup.
- Producing a findings-first anti-pattern report.
- Prioritizing quality issues by risk and blocker level.

## Focus option handling

- **Option A (Test-Focused):** prioritize test anti-pattern analysis; run
  source-quality checks only when they explain test failures.
- **Option B (Code-Focused):** run the full code-quality gate pack and
  dead/private helper audits.
- **Option C (Full Cycle):** run Option A evidence pass and Option B gate pass,
  then combine results into one ranked proposal.

## Core principles

1. Determinism first: no unsilenced `random`, `time`, or network dependencies.
2. Public-contract tests only: private-member access requires explicit allowlist.
3. Assertion strength: favor behavioral assertions over shape/type-only checks.
4. Marker/layer hygiene: test markers and suite placement must match behavior.
5. No production test-helper exports from `src/`.

## Audit workflow

1. Confirm the selected focus option (`A`, `B`, or `C`).
2. Run anti-pattern detection:

```bash
python scripts/anti-pattern-analysis/detect_test_anti_patterns.py
python scripts/anti-pattern-analysis/scan_private_usage.py --check
python scripts/quality/check_no_test_helper_exports.py
```

3. Run source-quality checks:

```bash
python scripts/quality/check_import_graph.py
python scripts/quality/check_docstring_coverage.py
python scripts/anti-pattern-analysis/analyze_private_methods.py
```

4. Validate deprecation compliance:

```bash
$env:CE_DEPRECATIONS='error'
pytest tests/unit -m "not viz" -q
```

5. Classify each finding:
- Severity: blocker/high/medium/low.
- Scope: source/test/docs/process.
- Action: remove/refactor/rewrite/test-add/update-allowlist.

## Output contract

Report findings in this order:

1. Blockers (must-fix now).
2. High-risk defects.
3. Medium/low hygiene improvements.

For each finding include:
- file path + line
- violated rule/ADR
- concrete remediation proposal
- selected focus option (`A`, `B`, or `C`) and why the finding is in-scope

## Constraints

- Analysis and planning focus; do not silently auto-fix large areas.
- Preserve CE-first boundaries (ADR-001 layering and public API policy).
