---
name: ai-release
description: "Use when preparing a release: aggregated GO/NO-GO gate checking coverage, security, tests, lint, and dependency vulnerabilities against manifest thresholds."
effort: medium
argument-hint: "[version]|--check-only"
tags: [quality, release, gate, go-no-go, delivery]
---


# Release Gate

Aggregated GO/NO-GO release readiness gate. Checks every quality dimension against `manifest.yml` thresholds and produces a verdict with evidence. Run before version tagging or merge-to-main.

## When to Use

- Pre-release milestone, version tagging, merge-to-main decision.
- NOT for code quality only -- use `/ai-quality`.
- NOT for security only -- use `/ai-security`.

## Process

### Phase 1: Gate Dimensions

1. **Coverage** -- verify test coverage meets threshold.
   - Run `pytest tests/ --cov --cov-report=term-missing`.
   - Gate: coverage >= threshold from `manifest.yml` (default 80%).

2. **Security** -- verify zero medium+ findings.
   - Run `gitleaks protect --staged`, `semgrep scan --config auto .`, `pip-audit`.
   - Gate: zero critical/high findings. Medium findings documented.

3. **Tests** -- verify all tests pass.
   - Run `pytest tests/ -v`.
   - Gate: 100% pass rate. Zero skipped governance tests.

4. **Lint** -- verify clean lint and format.
   - Run `ruff check .`, `ruff format --check .`.
   - Gate: zero unfixable lint errors.

5. **Dependency vulnerabilities** -- verify clean dependency tree.
   - Run `pip-audit --strict`.
   - Gate: zero known vulnerabilities. Accepted risks must be in `decision-store.json`.

6. **Type checking** -- verify type correctness.
   - Run `ty check src/`.
   - Gate: zero errors.

7. **Documentation coherence** -- verify docs are current.
   - CHANGELOG.md has `[Unreleased]` entries or versioned section.
   - README.md reflects current features.

8. **Packaging integrity** -- verify distribution builds.
   - Run `uv build` or equivalent.
   - Gate: wheel builds cleanly, no missing files.

### Phase 2: Aggregate Verdict

9. **Determine verdict**:
   - **GO**: all dimensions pass.
   - **CONDITIONAL GO**: all pass except non-critical items with risk acceptance in `decision-store.json`.
   - **NO-GO**: one or more blocking issues without risk acceptance.

10. **Produce closure path** (for NO-GO):
    - List specific blockers with fix suggestions.
    - Prioritize by blocking severity.
    - Estimate effort per fix.

## Output Contract

```markdown
## Release Readiness: [version]

### Verdict: GO | CONDITIONAL GO | NO-GO

| Dimension | Status | Detail |
|-----------|--------|--------|
| Coverage | PASS 87% (>= 80%) | -- |
| Security | PASS | 0 findings |
| Tests | PASS | 142/142 pass |
| Lint | PASS | 0 errors |
| Dependencies | PASS | 0 vulns |
| Types | PASS | 0 errors |
| Docs | PASS | CHANGELOG current |
| Packaging | PASS | wheel builds |

### Blockers (if NO-GO)
- [Issue, severity, fix suggestion]

### Residual Risk
- [Risk acceptances from decision-store.json]
```

## Quick Reference

```
/ai-release              # full GO/NO-GO gate
/ai-release v2.0.0       # gate for specific version
/ai-release --check-only # report without blocking
```

## Common Mistakes

- Running release gate on a dirty working tree -- commit first.
- Ignoring CONDITIONAL GO risks -- each must have a `decision-store.json` entry.
- Skipping packaging integrity -- wheel build failures are release blockers.

## Integration

- Aggregates results from `/ai-security`, `/ai-quality`, `/ai-test`.
- Reads thresholds from `manifest.yml`.
- Risk acceptances from `state/decision-store.json`.

## References

- `.claude/skills/ai-security/SKILL.md` -- security gate.
- `.claude/skills/ai-governance/SKILL.md` -- compliance and risk.
- `.ai-engineering/manifest.yml` -- quality thresholds.
$ARGUMENTS
