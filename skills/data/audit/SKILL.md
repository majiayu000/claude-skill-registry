---
# VERSION: 2.43.0
name: audit
description: "Generate usage report for MiniMax and token optimization Use when: (1) /audit is invoked, (2) task relates to audit functionality."
user-invocable: true
context: fork
---

# /audit

Generate usage and cost optimization report.

## What it shows
- Total queries by model (MiniMax M2.1, lightning, Claude)
- Estimated cost savings from MiniMax usage
- Usage trends (daily/weekly)
- Optimization recommendations

## Execution
```bash
# View stats
mmc --stats

# Detailed audit report
ralph audit
```

## Cost Calculation
- Claude Sonnet: $3.00/$15.00 per 1M tokens (input/output)
- MiniMax M2.1: $0.30/$1.20 per 1M tokens (~92% savings)
- MiniMax-lightning: $0.15/$0.60 per 1M tokens (~96% savings)

## Example Output
```
=== MiniMax Usage Audit ===
Period: Last 7 days

Model Distribution:
  MiniMax M2.1:     45 queries (60%)
  MiniMax-lightning: 20 queries (27%)
  Claude Sonnet:    10 queries (13%)

Estimated Savings:
  If all queries used Claude: ~$X.XX
  Actual cost with MiniMax:   ~$X.XX
  Savings:                    ~XX%
```
