---
name: eval-report
description: Generate evaluation report from session metrics, checkpoint evals, and pass@k data
disable-model-invocation: true
---

# Eval Report

Generate a dashboard of session effectiveness metrics.

## Arguments
- `--days N` — look back N days (default: 7)
- `--branch <name>` — filter by branch
- `--format table|json` — output format (default: table)

## Process

### 1. Read Metrics
Read `.claude/agent-memory/session-learnings/metrics.jsonl`

> **Guard:** If `metrics.jsonl` does not exist, output "No session metrics recorded yet. Run sessions with `evaluate-session.sh` enabled to populate." and skip to step 2.

Calculate:
- Total sessions in period
- Average commits per session
- Average tasks completed per session
- Average files changed per session
- Error rate (sessions with errors / total sessions)
- Average session duration (minutes)

### 2. Read Checkpoint Evals
Read `.claude/phases/output/eval-*.json`

Calculate:
- Phase transition pass rate
- Most common failure criteria
- Average attempts per transition

### 3. Read pass@k Data
Read `.claude/instincts/eval-tracker.jsonl`

Calculate:
- pass@1: (tasks succeeded on first attempt) / (total tasks)
- pass@3: (tasks succeeded within 3 attempts) / (total tasks)
- Average attempts to success

### 4. Skill Effectiveness Analysis

Read `.claude/instincts/eval-tracker.jsonl` and analyze `skill_context` field:

For each pattern ID that appears in any eval-tracker entry:
- Count tasks where this pattern was active
- Calculate pass@1 rate for tasks with this pattern
- Compare to overall pass@1 rate

Display:
```
| Pattern | Tasks | pass@1 (with) | pass@1 (overall) | Verdict |
|---------|-------|--------------|-----------------|---------|
| inst_abc123 | 5 | 80% | 60% | effective |
| inst_def456 | 3 | 33% | 60% | harmful |
```

Verdicts:
- "effective": pattern pass@1 > overall + 10%
- "neutral": within 10% of overall
- "harmful": pattern pass@1 < overall - 10%

Flag harmful patterns: "Consider reducing confidence or removing: <pattern-id>"

### 5. Output Report

Display as markdown table:

```
| Metric              | Value | Trend        |
|---------------------|-------|--------------|
| Sessions (7d)       | N     | -            |
| Commits/session     | N.N   | up/down/flat |
| Tasks/session       | N.N   | up/down/flat |
| Error rate          | N%    | up/down/flat |
| Avg duration (min)  | N     | up/down/flat |
| Phase pass rate     | N%    | up/down/flat |
| pass@1              | N%    | up/down/flat |
| pass@3              | N%    | up/down/flat |
```

Trend: compare current period to previous equivalent period.

## Data File Locations

- Metrics: `.claude/agent-memory/session-learnings/metrics.jsonl`
- Checkpoint evals: `.claude/phases/output/eval-*.json`
- pass@k tracker: `.claude/instincts/eval-tracker.jsonl`
