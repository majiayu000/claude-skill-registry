---
id: severity
title: Severity Classification Skill
category: methodology
difficulty: beginner
triggers:
  - classify severity
  - severity level
  - critical finding
  - high finding
  - medium finding
  - low finding
  - informational finding
related_skills:
  - report-writer/SKILL.md
  - scoring/SKILL.md
  - methodology/SKILL.md
tags:
  - severity
  - classification
  - findings
  - methodology
last_updated: 2026-02-26
description: >-
  Data-driven severity classification for smart contract audit findings
  with statistical breakdowns and 30 representative examples per level
  from top audit firms. Use when assigning severity to findings, justifying
  classifications with historical data, or calibrating severity judgment
  against Code4rena, Sherlock, and Cyfrin benchmarks.
---

# Severity Classification

## Purpose

This directory provides data-driven severity classification for smart contract audit findings. Each file contains statistical breakdowns of real vulnerability types at that severity level, plus 30 representative examples from top audit firms (Code4rena, Cyfrin, Spearbit, Pashov, MixBytes, Shieldify, OtterSec, Quantstamp).

## Severity Levels

| Level | File | Finding Count | % of All | Scoring Weight |
|-------|------|---------------|----------|----------------|
| HIGH | [high-severity.md](high-severity.md) | 8,022 | 15.88% | 5 points |
| MEDIUM | [medium-severity.md](medium-severity.md) | 13,814 | 27.34% | 2 points |
| LOW | [low-severity.md](low-severity.md) | 25,272 | 50.01% | 1 point |
| GAS | [gas-optimizations.md](gas-optimizations.md) | 3,422 | 6.77% | 0 points |

> Scoring weights reference the [Audit Scoring System](../scoring/AUDIT_SCORING.md) efficiency metric.

## How to Use

1. **Classifying a finding** → Use the [Severity Scoring Decision Tree](../patterns/severity-scoring.md) to determine the correct level
2. **Validating severity** → Compare your finding against the top vulnerability types table in each file
3. **Writing the report** → Reference representative examples for formatting and depth expectations
4. **Scoring the audit** → Apply severity weights from [AUDIT_SCORING.md](../scoring/AUDIT_SCORING.md) to calculate composite scores

## Quick Severity Decision Tree

```
Is there direct fund loss possible?
├── YES → Is it unconditional (anyone can exploit)?
│   ├── YES → CRITICAL (not in this dataset — escalate)
│   └── NO (needs conditions) → HIGH
└── NO → Is there indirect fund loss or protocol damage?
    ├── YES → Is the attack practical?
    │   ├── YES → HIGH
    │   └── NO (theoretical) → MEDIUM
    └── NO → Is there any functional impact?
        ├── YES → LOW
        └── NO → GAS / INFORMATIONAL
```

> Full decision tree with scoring matrix: [patterns/severity-scoring.md](../patterns/severity-scoring.md)

## Cross-Severity Vulnerability Migration

Some vulnerability types appear across multiple severity levels depending on conditions. Key crossovers:

| Vulnerability Type | HIGH Count | MEDIUM Count | LOW Count | Notes |
|---|---|---|---|---|
| Business Logic | 100 | 127 | 7 | Most common at every level |
| Validation | 52 | 75 | — | Severity depends on what's unvalidated |
| Reentrancy | 39 | 20 | — | HIGH when funds at risk, MEDIUM when state-only |
| Oracle | 24 | 34 | — | HIGH for price manipulation, MEDIUM for staleness |
| Access Control | 27 | 19 | 2 | HIGH for privilege escalation, LOW for missing events |
| Front-Running | 39 | 67 | — | MEDIUM unless sandwich causes fund loss |
| DOS | 23 | 43 | — | HIGH for permanent, MEDIUM for temporary |
| Overflow/Underflow | 21 | 22 | — | Severity = magnitude of miscalculation |

## Related Skills

- [Audit Scoring System](../scoring/AUDIT_SCORING.md) — Composite scoring using severity weights
- [Severity Scoring Decision Tree](../patterns/severity-scoring.md) — AI-optimized classification guide
- [Audit Report Templates](../methodology/audit-report-templates.md) — How to write findings at each severity
- [PoC Writing Guide](../methodology/poc-writing-guide.md) — Proving exploitability strengthens severity claims
- [Checklists](../checklists/) — Protocol-specific vulnerability checklists
## Prerequisites

Severity classification requires understanding of the [Severity Scoring Decision Tree](../patterns/severity-scoring.md). The decision tree MUST be consulted before assigning final severity.

## Validation

To verify severity classification consistency, compare against historical benchmarks:

```python
# Validate severity distribution against expected ranges
def test_severity_distribution(findings):
    high_pct = len([f for f in findings if f.severity == 'HIGH']) / len(findings)
    assert 0.10 <= high_pct <= 0.25, f"HIGH findings at {high_pct:.0%} (expected 10-25%)"
    print(f"Severity distribution validated: {high_pct:.0%} HIGH")
```

```yaml
# Expected severity distribution benchmarks
benchmarks:
  high: 15.88%    # 8,022 of 50,530 findings
  medium: 27.34%  # 13,814 findings
  low: 50.01%     # 25,272 findings
  gas: 6.77%      # 3,422 findings
```

```bash
# Verify severity files are complete
for f in high-severity.md medium-severity.md low-severity.md gas-optimizations.md; do
  echo "Checking $f: $(wc -l < $f) lines"
done
```

## Behavior Guidelines

- Every finding MUST have a severity classification before submission
- The decision tree is **required** for borderline HIGH/MEDIUM cases
- Auditors may optionally include a severity justification paragraph for contested findings
- GAS findings ALWAYS have 0 scoring weight in composite metrics

## References

- [Severity References](references/README.md) - Historical distribution data and calibration benchmarks