---
name: synthesize
description: >-
  Merge, deduplicate, rank, and format research findings
  from multiple channels into a coherent report. Use after
  research agents return their results.
version: 1.9.3
alwaysApply: false
category: synthesis
tags:
  - merge
  - rank
  - format
  - report
estimated_tokens: 150
model_hint: standard
---
# Finding Synthesis

## When To Use

- After research agents return results from multiple channels
- Producing a final ranked report from raw findings

## When NOT To Use

- No research session is active (run `/tome:research` first)
- Refining a single channel (use `/tome:dig` instead)

Merge findings from all channels into a ranked report.

## Workflow

1. Merge: `tome.synthesis.merger.merge_findings()`
2. Rank: `tome.synthesis.ranker.rank_findings()`
3. Group: `tome.synthesis.ranker.group_by_theme()`
4. Format: `tome.output.report.format_report()`

## Output Formats

- **report**: Full sectioned markdown
- **brief**: Condensed 1-2 pages
- **transcript**: Raw session log
