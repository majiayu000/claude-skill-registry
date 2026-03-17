---
name: tune-system
description: Review automation system operation and make conservative adjustments to cadences and thresholds when clearly warranted. Monthly maintenance task.
---

# Tune System

A meta-review skill that analyzes the automation system's own operation and makes conservative, evidence-based adjustments. Mirrors The Unfinishable Map's "Minimal Quantum Interaction" tenet: small, precise interventions with clear justification.

## When to Use

- **Monthly maintenance**: Runs on 30-day cadence (injected when 45 days overdue)
- **Post-milestone**: After reaching convergence milestones (50%, 75%, etc.)
- **Manual invocation**: When you notice operational issues
- **After significant failures**: If failed_tasks count exceeds 5 in a session

## Instructions

### 1. Load Data Sources

Read these files to gather operational data:

```
obsidian/workflow/evolution-state.yaml  # Primary metrics
obsidian/workflow/changelog.md          # Execution history
obsidian/workflow/todo.md               # Task patterns
obsidian/reviews/                       # Recent review outputs
obsidian/project/project-brief.md       # Project goals (reference)
```

### 2. Check Abort Conditions

**STOP and escalate to human if any of these are true:**
- More than 50% of recent tasks (last 10) failed
- Convergence has regressed for 3+ consecutive sessions
- `quality.critical_issues > 0`
- Any file read errors during analysis

If aborting, create a minimal report explaining why and skip to step 8.

### 3. Check Locked Settings

Read `evolution-state.yaml` for `locked_settings` section. These settings cannot be modified automatically—note them for the report.

### 4. Analyze Five Categories

#### A. Cadence Analysis

Compare `last_runs` timestamps against `cadences` settings:

- Calculate days between actual runs for each maintenance task
- Identify tasks frequently overdue (pattern: overdue in >60% of opportunities)
- Identify tasks never reaching cadence (always run early)

**Evidence required**: 5+ data points (sessions) showing consistent pattern

#### B. Failure Pattern Analysis

Examine `failed_tasks` and `recent_tasks`:

- Count failures by task type
- Look for common error patterns
- Identify environmental issues (missing files, API errors)

**Evidence required**: 3+ failures of same type or pattern

#### C. Queue Health Analysis

Examine `queue_status` and `replenishment_source_counts`:

- Compare task sources (chain, research, gap, staleness) to execution rates
- Check if certain sources produce tasks that never get executed
- Monitor P3 promotion rate

**Evidence required**: 5+ sessions of queue data

#### D. Review Finding Patterns

Scan recent files in `reviews/`:

- Identify issues raised multiple times but never addressed
- Track issue resolution rate
- Note recurring themes across pessimistic reviews

**Evidence required**: 3+ reviews showing same pattern

#### E. Convergence Progress

Analyze `progress` and `quality` metrics:

- Calculate convergence rate (% change per session)
- Identify stalled areas (no progress in 3+ sessions)
- Compare current state to `convergence_targets`

**Evidence required**: 5+ sessions of convergence data

### 5. Generate Findings

For each finding, determine the tier:

#### Tier 1 — Automatic Changes (max 3 per session)

Small, safe adjustments with clear evidence. Apply directly:

| Change Type | Limits | Example |
|-------------|--------|---------|
| Cadence adjustment | ±2 days | pessimistic-review: 7 → 5 days |
| Overdue threshold | ±2 days | validate-all overdue: 2 → 3 days |
| Replenishment weight | ±20% | chain source weight: 50 → 60 |

**Before applying, verify:**
- Setting is not in `locked_settings`
- Setting hasn't changed in last 60 days (check changelog)
- Clear directional pattern (not random variation)

#### Tier 2 — Recommendations (log for human approval)

Medium-impact changes:

- New task suggestions (add to todo.md as P3)
- Cadence changes >2 days
- Replenishment mode changes (conservative ↔ aggressive)
- Convergence target adjustments

#### Tier 3 — Report Only (never automatic)

Changes requiring human judgment:

- Skill instruction modifications
- New skill creation
- Tenet-related adjustments
- Removing vetoed task constraints
- Priority level promotions

### 6. Apply Tier 1 Changes

For each approved Tier 1 change:

1. Record the previous value
2. Apply the change to the appropriate file
3. Add a comment noting the change date and rationale

Example change to `evolution-state.yaml`:
```yaml
cadences:
  pessimistic-review: 5  # Changed from 7 by tune-system 2026-01-08 (overdue 4/5 sessions)
```

### 7. Update Evolution State

Add/update these fields in `evolution-state.yaml`:

```yaml
last_runs:
  tune-system: [current ISO timestamp]

# Track what was changed for cooldown enforcement
tune_system_history:
  last_run: [ISO timestamp]
  changes_applied:
    - setting: cadences.pessimistic-review
      old_value: 7
      new_value: 5
      date: [ISO date]
      rationale: "Overdue in 4 of 5 recent sessions"
```

### 8. Generate Report

Create report at `obsidian/reviews/system-tune-YYYY-MM-DD.md`:

```markdown
---
title: "System Tuning Report - YYYY-MM-DD"
created: YYYY-MM-DD
modified: YYYY-MM-DD
human_modified: null
ai_modified: [ISO timestamp]
draft: false
topics: []
concepts: []
related_articles:
  - "[[todo]]"
  - "[[changelog]]"
ai_contribution: 100
author: null
ai_system: [current model]
ai_generated_date: YYYY-MM-DD
last_curated: null
---

# System Tuning Report

**Date**: YYYY-MM-DD
**Sessions analyzed**: N (sessions X to Y)
**Period covered**: [date range]

## Executive Summary

[2-3 sentences on overall system health and key findings]

## Metrics Overview

| Metric | Current | Previous | Trend |
|--------|---------|----------|-------|
| Session count | N | N-X | +X |
| Avg tasks/session | X.X | X.X | ↑/↓/→ |
| Failure rate | X% | X% | ↑/↓/→ |
| Convergence | X% | X% | +X% |
| Queue depth (P0-P2) | X | X | ↑/↓/→ |

## Findings

### Cadence Analysis

[Findings with evidence and recommendations]

### Failure Pattern Analysis

[Findings with evidence and recommendations]

### Queue Health Analysis

[Findings with evidence and recommendations]

### Review Finding Patterns

[Findings with evidence and recommendations]

### Convergence Progress

[Findings with evidence and recommendations]

## Changes Applied (Tier 1)

| File | Setting | Old | New | Rationale |
|------|---------|-----|-----|-----------|
| evolution-state.yaml | cadences.X | Y | Z | [reason] |

*No changes applied* — if none were warranted

## Recommendations (Tier 2)

### [Recommendation Title]
- **Proposed change**: [specific change]
- **Rationale**: [why this helps]
- **Risk**: Low/Medium
- **To approve**: [how human can apply]

## Items for Human Review (Tier 3)

### [Item Title]
- **Issue observed**: [description]
- **Why human needed**: [explanation]
- **Suggested action**: [what human might do]

## Next Tuning Session

- **Recommended**: [date, 30 days out]
- **Focus areas**: [what to watch]
```

### 9. Log to Changelog

Prepend to `obsidian/workflow/changelog.md` (add immediately after frontmatter, before existing entries):

```markdown
## [current time from prompt] - tune-system
- **Status**: Success/Partial/Failed
- **Sessions analyzed**: N
- **Findings**: X cadence, Y failure, Z queue, W review, V convergence
- **Tier 1 changes**: N applied
- **Tier 2 recommendations**: N logged
- **Output**: [[reviews/system-tune-YYYY-MM-DD]]
```

## Safeguards

### Evidence Thresholds

| Analysis Type | Minimum Data Points |
|---------------|---------------------|
| Cadence patterns | 5 sessions |
| Failure patterns | 3 occurrences |
| Queue patterns | 5 sessions |
| Review patterns | 3 reviews |
| Convergence trends | 5 sessions |

### Change Cooldowns

After a Tier 1 change, that setting cannot be changed again for:
- 2 tune-system sessions, OR
- 60 days

Check `tune_system_history.changes_applied` before making any change.

### Magnitude Limits

- Cadence: ±2 days maximum
- Threshold: ±2 days maximum
- Weight: ±20 percentage points maximum
- Maximum 3 Tier 1 changes per session

### Locked Settings

Human can prevent automatic changes by adding to `evolution-state.yaml`:

```yaml
locked_settings:
  cadences.check-tenets: "Locked 2026-01-10 - monthly cadence is intentional"
```

## Important

**DO NOT:**
- Modify skill instruction files (SKILL.md files)
- Change priority levels (P0-P3) of existing tasks
- Remove items from vetoed tasks
- Modify anything related to tenets
- Make changes without clear evidence (no speculative "improvements")
- Exceed magnitude limits even if evidence seems strong
- Change locked settings
- Run more frequently than monthly (unless manually invoked)

**DO:**
- Be conservative — when in doubt, recommend rather than apply
- Document everything — all findings, all changes, all rationale
- Respect cooldowns — no rapid oscillation of settings
- Focus on operational parameters — cadences, thresholds, weights
- Generate actionable recommendations for Tier 2/3 items