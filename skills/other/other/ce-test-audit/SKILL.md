---
name: ce-test-audit
description: >
  Audit existing tests for ADR-030 anti-patterns, redundancy risk, and compliance
  with repository test standards.
---

# CE Test Audit

You are auditing the test suite for quality issues. This skill applies the
criteria from ADR-030, `tests/README.md`, and the test-quality-method docs.
Load these references before auditing:

- `references/adr-030-test-quality.md`
- `docs/improvement/test-quality-method/README.md`
- `docs/improvement/test-quality-method/anti_pattern_auditor.md`

## Focus option handling

- **Option A (Test-Focused):** run the full audit toolchain, including
  redundancy analysis.
- **Option B (Code-Focused):** run only hard-gate and anti-pattern checks needed
  to support source-focused remediation.
- **Option C (Full Cycle):** run Option A and then re-check hard gates after
  code-focused changes.

## Audit Toolchain

Choose the command set based on focus option.

### Option A / Option C (full test audit)

```bash
# 1. Anti-pattern scan (primary audit)
python scripts/anti-pattern-analysis/detect_test_anti_patterns.py

# 2. Private member usage scan (hard gate in CI)
python scripts/anti-pattern-analysis/scan_private_usage.py --check

# 3. Over-testing / redundant test density report
python scripts/over_testing/over_testing_report.py

# 4. Redundant test detection
python scripts/over_testing/detect_redundant_tests.py

# 5. Marker hygiene check
python scripts/quality/check_marker_hygiene.py --check

# 6. No test-helper export check (hard gate)
python scripts/quality/check_no_test_helper_exports.py
```

### Option B (code-focused support audit)

```bash
# 1. Anti-pattern scan
python scripts/anti-pattern-analysis/detect_test_anti_patterns.py

# 2. Private member usage scan (hard gate in CI)
python scripts/anti-pattern-analysis/scan_private_usage.py --check

# 3. No test-helper export check (hard gate)
python scripts/quality/check_no_test_helper_exports.py
```

Results from (3) and (4) are also published as CI artifacts under
`ci-main.yml`'s advisory over-testing job.

## Issue Classification (ADR-030 Priority Order)

### Priority 1 — Determinism (highest)
**Symptoms:** flaky tests, CI failures without code changes.
**Detection:** look for unpatched `datetime.now()`, `random`, network I/O,
unseeded NumPy/Python RNG, or `time.sleep`.
**Fix:** `monkeypatch`, `tmp_path`, `np.random.seed(42)`, mock network calls.

### Priority 2 — Private Member Usage
**Detection:** `scan_private_usage.py --check` output.
**Fix decision tree:**
```
Is the private helper a stable domain concept?
├── YES → Make it public (rename, add docstring, export, update tests)
└── NO  → Delete the direct test; test through the public caller instead
```

### Priority 3 — Assertion Strength
**Symptoms:** tests that only check `assert result is not None` or
`assert "key" in dict`.
**Fix:** Replace with semantic domain assertions:
```python
# BEFORE
assert "predict" in result

# AFTER
assert result['low'] <= result['predict'] <= result['high']
```

### Priority 4 — Layering / Test Scope
**Symptoms:** unit tests with heavy I/O, integration tests in `tests/unit/`,
missing `@pytest.mark.slow` on long-running tests.
**Detection:** `check_marker_hygiene.py --check` output; manual scope review.
**Fix:** move to correct directory, add markers.

### Priority 5 — Fixture Discipline
**Symptoms:** deeply chained fixtures (>3 levels), copying fixture code between
test files, anonymous fixtures.
**Fix:** consolidate in `conftest.py`; reduce fixture depth; name fixtures
clearly.

### Priority 6 — Semantic Redundancy (over-testing)
**Detection:** `over_testing_report.py` shows tests with zero unique lines;
`detect_redundant_tests.py` shows identical coverage fingerprints.
**Rule (ADR-030):** 0 tests with 0 unique lines are allowed unless:
1. It's a `@pytest.mark.parametrize` case with a meaningful variation.
2. It's a regression test for a tracked issue (`@pytest.mark.issue`).
**Fix:** delete or merge into a parametrized test.

## Fallback Chain Violations

Any test triggering a fallback warning (`UserWarning`) that does NOT use
`enable_fallbacks` is a violation. Symptoms in CI:
- `"Execution plugin error; legacy sequential fallback engaged"`
- `"Parallel failure; forced serial fallback engaged"`
- `"Cache backend fallback: using minimal in-package LRU/TTL implementation"`

**Fix:** either fix the underlying condition (preferred) or explicitly mark the
test with `enable_fallbacks` and add `pytest.warns(UserWarning)`.

## Reporting Template

When reporting audit findings, use this structure:

```
## Test Audit Report — <module or scope>

### P1 — Determinism Issues
- [ ] <test name>: <issue description> → <fix>

### P2 — Private Member Usage
- [ ] <test name>: <private symbol accessed> → <fix>

### P3 — Assertion Strength
- [ ] <test name>: assertion is execution-only → replace with <semantic assertion>

### P4 — Layering
- [ ] <test file>: scope mismatch → move to <target path>

### P5 — Fixture Discipline
- [ ] <fixture name>: depth <N> → simplify

### P6 — Redundancy
- [ ] <test name>: 0 unique lines / identical fingerprint to <other test> → delete or parametrize

### Hard Gate Violations (fix before PR merge)
- [ ] Private-member scan violations
- [ ] No-test-helper-export violations
- [ ] 90% coverage gate status
```

## Out of Scope

- Writing new tests from scratch (see `ce-test-author`).
- Auditing visualization tests (ADR-023 exemption; these are excluded from
  coverage gate — check their `# pragma: no cover` placement instead).

## Evaluation Checklist

- [ ] Selected focus-option command set run and output reviewed.
- [ ] Issues classified by ADR-030 priority.
- [ ] Hard gate violations flagged separately.
- [ ] Fallback chain violations identified.
- [ ] Recommendations are concrete (test name + fix action).
