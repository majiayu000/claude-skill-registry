---
name: dora-metrics
description: Computes DORA delivery-performance metrics from git and GitHub API. Use when assessing deployment frequency, lead time, or change failure rate.
alwaysApply: false
category: governance
tags:
- dora
- metrics
- delivery
- engineering-management
- github
dependencies: []
tools: []
provides:
  governance:
  - dora-tier
  - delivery-bottleneck
  reporting:
  - dora-report
  - tier-classification
usage_patterns:
- delivery-retro
- agentic-pipeline-audit
- release-health-input
complexity: intermediate
model_hint: standard
estimated_tokens: 800
progressive_loading: true
modules:
- modules/thresholds.md
- modules/agentic-workflow-signals.md
---

# DORA Metrics

## Purpose

Compute the four DORA delivery-performance metrics (Deployment
Frequency, Lead Time for Changes, Change Failure Rate, and Time to
Restore Service) from local git history and the GitHub API. Classify
each metric into Elite, High, Medium, or Low using thresholds from
DORA's State of DevOps research, and surface the single weakest
dimension as the next improvement target.

## When to Use

- Engineering management retrospectives and quarterly reviews.
- Auditing whether agentic workflows (AI-assisted PRs, automated
  deploys) improve velocity and stability or quietly regress them.
- Feeding a tier signal into `minister:release-health-gates`.

## When Not to Use

- Single-team velocity tracking that needs story-point burndowns
  rather than delivery-performance evidence.
- Repositories without a clear production branch or release cadence;
  DORA assumes one.

## Workflow

1. Run the helper script with the desired window:

   ```bash
   python3 -m minister.dora_metrics --window 30 --branch main
   ```

2. Read the output: per-metric value, tier classification, and the
   bottleneck pointer.

3. For agentic-workflow audits, run the same window twice. Once
   filtering to AI-authored PRs (e.g., `--failure-label ai-bug`),
   once across all PRs. Compare the CFR delta. See
   `modules/agentic-workflow-signals.md`.

4. Optionally pipe `--json` into the tracker so trend data persists
   alongside `release-health-gates` snapshots.

5. Optionally render trend charts with kuva when reviewing multiple
   windows or comparing before/after an agentic-workflow change:

   ```bash
   # Collect weekly snapshots into a TSV, then plot all four metrics
   # week<TAB>metric<TAB>value
   kuva line trends.tsv --x week --y value --color-by metric \
       --title "DORA trends (30-day windows)" -o dora-trends.svg

   # Quick terminal preview without writing a file
   kuva line trends.tsv --x week --y value --color-by metric --terminal
   ```

   kuva reads TSV/CSV from stdin or a file path. Install once:
   `cargo install kuva --features cli`. No project source changes
   required. See [kuva](https://github.com/Psy-Fer/kuva) for the
   full plot-type reference.

## Inputs

| Flag | Default | Meaning |
|------|---------|---------|
| `--window` | 30 | Measurement window in days |
| `--branch` | HEAD | Production branch |
| `--failure-label` | bug | GitHub label marking prod failures |
| `--json` | off | Emit JSON instead of human-readable |
| `--repo-path` | cwd | Repository directory |

## Outputs

A short text report or JSON payload with:

- Per-metric numeric value (e.g., `4.2/day`, `2.1 hours`, `8%`).
- Per-metric tier (Elite, High, Medium, Low).
- Overall tier (the weakest of the four).
- Bottleneck key, identifying which metric to focus improvement on.

## Tier Thresholds

See `modules/thresholds.md` for the complete table. Brief summary:

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| DF | >= 1/day | >= 1/week | >= 1/month | < 1/month |
| LT | <= 1 day | <= 1 week | <= 1 month | > 1 month |
| CFR | <= 15% | <= 30% | <= 45% | > 45% |
| TRS | < 1 hour | < 1 day | < 1 week | >= 1 week |

## Verification

Confirm a DORA report is real by re-running the script over a
narrower window and checking that DF and LT scale predictably. For
CFR and TRS, sample two or three of the contributing GitHub issues
and verify the `bug` (or chosen) label is correct on each.

## Testing

Unit tests live in
`plugins/minister/tests/unit/test_dora_metrics.py`. Each tier
boundary is exercised at the threshold, so future contributors who
adjust an inequality (`>` vs `>=`) trigger a failure rather than a
silent regression. Add new tests at the threshold when extending
classification logic.

## Exit Criteria

- [ ] DORA report generated for the requested window.
- [ ] All four metrics classified into a tier.
- [ ] Bottleneck dimension surfaced.
- [ ] Output is readable in a terminal or as a PR comment.
