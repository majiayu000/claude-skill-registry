---
id: scoring
title: Audit Scoring Skill
category: methodology
difficulty: intermediate
triggers:
  - audit score
  - quality metrics
  - scoring framework
  - audit quality
  - performance metrics
related_skills:
  - severity/SKILL.md
  - methodology/SKILL.md
  - report-writer/SKILL.md
tags:
  - scoring
  - metrics
  - quality
  - methodology
last_updated: 2026-02-26
description: >-
  Quantitative scoring framework for measuring audit quality with
  objective metrics to evaluate performance, track improvement over
  time, and identify areas needing attention. Use when benchmarking
  audit thoroughness, comparing engagement quality, or building
  quality gates into CI pipelines.
---

# Audit Scoring

## Purpose

This directory provides the quantitative scoring framework for measuring audit quality. Use these metrics to objectively evaluate performance, track improvement over time, and identify areas needing attention.

## Available Files

| File | Description |
|------|-------------|
| [AUDIT_SCORING.md](AUDIT_SCORING.md) | Complete scoring system — detection, precision, severity accuracy, coverage, efficiency metrics, composite score formula, reward schema, tracking templates, and industry benchmarks |

## Core Metrics at a Glance

| Metric | Weight | What It Measures |
|--------|--------|-----------------|
| Detection Score | 35% | Vulnerabilities correctly identified vs. total real vulnerabilities |
| Precision Score | 25% | Valid findings vs. total findings submitted (false positive rate) |
| Severity Accuracy | 15% | Correct severity classification vs. total findings |
| Coverage Score | 15% | Functions/entry points audited vs. total codebase |
| Efficiency Score | 10% | Weighted findings produced per hour spent |

> **Composite Score** = `(0.35 × Detection) + (0.25 × Precision) + (0.15 × Severity) + (0.15 × Coverage) + (0.10 × Efficiency)`

## Severity Weights for Efficiency Scoring

These weights connect the scoring system to the [severity classification](../severity/):

| Severity | Points | Reference |
|----------|--------|-----------|
| Critical | 10 | Escalation required (not in standard severity files) |
| High | 5 | [high-severity.md](../severity/high-severity.md) |
| Medium | 2 | [medium-severity.md](../severity/medium-severity.md) |
| Low | 1 | [low-severity.md](../severity/low-severity.md) |
| Informational | 0.5 | Best-practice suggestions |
| Gas | 0 | [gas-optimizations.md](../severity/gas-optimizations.md) |

## How to Use

1. **After an audit** → Fill out the Score Card Template in [AUDIT_SCORING.md](AUDIT_SCORING.md)
2. **Classify findings** → Use [severity/](../severity/) files + [severity-scoring decision tree](../patterns/severity-scoring.md)
3. **Track monthly** → Use the Monthly Score Tracking template
4. **Identify gaps** → Category-specific scores highlight weak areas
5. **Improve** → Low category scores → update [checklists](../checklists/) and [patterns](../patterns/)

## Related Skills

- [Severity Classification](../severity/) — HIGH / MEDIUM / LOW / GAS finding databases
- [Severity Scoring Decision Tree](../patterns/severity-scoring.md) — How to assign severity levels
- [Feedback Loop](../audit-feedback/FEEDBACK_LOOP.md) — Scores feed back into skill improvement
- [Audit Report Templates](../methodology/audit-report-templates.md) — Report structure with severity sections
- [Prompt Evolution](../methodology/prompt-evolution.md) — Higher-scoring prompts get promoted
## Prerequisites

Scoring requires completed audit findings with severity classifications. The [Severity Classification](../severity/) skill MUST be applied before scoring.

## Validation

To verify scoring accuracy, compare computed composite scores against known benchmarks:

```python
# Example composite score calculation
detection = 0.85   # 85% of real vulns found
precision = 0.80   # 80% valid findings
severity_acc = 0.90 # 90% correct severity
coverage = 0.75    # 75% codebase covered
efficiency = 0.70  # Weighted findings per hour

composite = (0.35 * detection + 0.25 * precision + 0.15 * severity_acc + 0.15 * coverage + 0.10 * efficiency)
print(f"Composite Score: {composite:.2f}")  # Expected: 0.81
```

```yaml
# Score thresholds for audit quality tiers
tiers:
  elite: 0.90+       # Top-tier competitive auditor
  proficient: 0.75+  # Solid professional auditor
  developing: 0.60+  # Learning auditor
  needs_work: <0.60  # Consider additional training
```

```bash
# Validate scoring data integrity
python scripts/quality-check.py skills/scoring/SKILL.md
```

## Behavior Guidelines

- Detection and Precision scores are **required** for every engagement
- Coverage tracking is **optional** for quick scans but MUST be included in full audits
- Efficiency scoring should be used for self-improvement, never to rush audits

## References

- [Scoring References](references/README.md) - Industry benchmarks and calibration data