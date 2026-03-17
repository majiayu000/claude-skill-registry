---
name: sys-tracking-goals
description: Monitors active goals against current state. Calculates gaps, scores urgency, detects at-risk goals, generates alerts. Reads goals from strategy/goals/active/, computes progress from metrics, outputs prioritized alerts and updates goal status.
triggers: track goals, check progress, monitor goals, goal status, at-risk goals
allowed-tools: Read, Write, Glob, Grep
license: Complete terms in LICENSE.txt
---

# Goal Tracking

Monitor goals, calculate gaps, score urgency, generate alerts.

## Responsibility

Track progress of active goals, detect gaps and risks, generate prioritized alerts for action.

## Quick Start

1. Load active goals from `strategy/goals/active/`
2. Collect current metric values from sources
3. Calculate gaps (target - current)
4. Score urgency (gap × time pressure × impact)
5. Assess achievability
6. Rank and output prioritized alerts
7. Update goal status in files

## Process Overview

```
Goals (strategy/goals/active/)
        │
        ▼
    Load & Parse
        │
        ▼
Current Values (canvas, threads, external)
        │
        ▼
    Gap Calculation
        │
        ▼
    Urgency Scoring
        │
        ▼
    Achievability Assessment
        │
        ▼
    Priority Ranking
        │
        ▼
Alert Generation ──► Dashboard
        │
        ▼
Goal Status Updates
```

## Input Sources

### Goals

Location: `strategy/goals/active/*.md`

Read from frontmatter:
- goal_id
- target_value, target_unit, target_direction
- period_start, period_end
- baseline_value
- milestones
- parent_goal, child_goals
- ownership_accountable

### Current Values

| Source | Priority | Content |
|--------|----------|---------|
| `strategy/canvas/13.metrics.md` | Primary | Baseline metrics |
| `threads/*/5-actions.md` | Secondary | Execution progress |
| External data | Tertiary | Real-time values |

## Gap Calculation

### Absolute Gap

For maximize goals:
```
absolute_gap = target_value - current_value
```

For minimize goals:
```
absolute_gap = current_value - target_value
```

### Relative Gap

```
relative_gap = absolute_gap / target_value
```

Interpretation:
- 0.00: On target
- 0.01-0.20: Minor gap
- 0.21-0.40: Moderate gap
- 0.41-0.60: Significant gap
- 0.61+: Critical gap

### Trajectory Gap

Project where we'll end up at current pace:

```
days_elapsed = today - period_start
daily_velocity = (current - baseline) / days_elapsed
days_remaining = period_end - today
projected_end = current + (daily_velocity × days_remaining)
trajectory_gap = target - projected_end
```

### Pace Gap

Compare actual pace to required pace:

```
required_pace = (target - baseline) / total_days
actual_pace = (current - baseline) / days_elapsed
pace_ratio = actual_pace / required_pace
```

Interpretation:
- pace_ratio > 1.0: Ahead of pace
- pace_ratio = 1.0: On pace
- pace_ratio 0.8-1.0: Slightly behind
- pace_ratio 0.5-0.8: Significantly behind
- pace_ratio < 0.5: Critically behind

## Urgency Scoring

### Formula

```
urgency_score = relative_gap × time_pressure × impact_weight
```

### Time Pressure

```
time_pressure = min(1.0, 30 / days_remaining)
```

| Days Remaining | Time Pressure |
|----------------|---------------|
| 60+ | 0.5 |
| 30 | 1.0 |
| 14 | 1.0 (capped) |
| 7 | 1.0 (capped) |
| 1 | 1.0 (capped) |

### Impact Weight

From goal category or explicit weight:

| Category | Default Weight |
|----------|---------------|
| revenue | 1.0 |
| retention | 0.9 |
| activity | 0.7 |
| efficiency | 0.6 |
| content | 0.5 |

### Urgency Levels

| Level | Score Range | Criteria |
|-------|-------------|----------|
| critical | > 0.8 | gap > 50% AND days < 7 |
| high | 0.6 - 0.8 | gap > 30% AND days < 14 |
| medium | 0.3 - 0.6 | gap > 20% OR days < 30 |
| low | < 0.3 | gap < 20% AND days > 30 |

## Achievability Assessment

### Factors

| Factor | Weight | Source |
|--------|--------|--------|
| Historical performance | 0.40 | Past goal outcomes |
| Resource availability | 0.30 | Constraint analysis |
| Trajectory analysis | 0.20 | Current velocity |
| External factors | 0.10 | Risk factors |

### Achievability Score

| Score | Interpretation | Action |
|-------|----------------|--------|
| > 0.8 | Achievable | Proceed with plan |
| 0.5 - 0.8 | Stretch | Flag risk, proceed |
| < 0.5 | At risk | Recommend revision |

## Priority Ranking

### Formula

```
priority = (impact × 0.40) + (urgency × 0.35) + ((1 - achievability) × 0.25)
```

### Adjustments

| Condition | Adjustment |
|-----------|------------|
| Blocking other goals | +0.1 |
| Quick win (small gap, high achievability) | +0.1 |
| Resource constrained | -0.05 |

## Alert Generation

### Alert Types

| Type | Trigger | Content |
|------|---------|---------|
| gap_alert | Gap exceeds threshold | Goal, current, target, gap, urgency |
| trajectory_warning | Will miss target | Projected end, shortfall, recovery options |
| milestone_alert | Milestone approaching/missed | Milestone date, target, current |
| at_risk_alert | Achievability < 0.5 | Risk factors, revision options |
| achievement_alert | Target reached | Final value, days ahead/behind |

### Alert Routing

| Urgency | Destination | Escalation |
|---------|-------------|------------|
| critical | Immediate notification | Leadership if not acked |
| high | Daily digest | After 24h no action |
| medium | Weekly summary | None |
| low | Dashboard only | None |

## Output

### Alert File Format

Location: `artifacts/system/alerts/{alert-id}.md`

```markdown
---
alert_id: alert_{type}_{goal_id}_{timestamp}
alert_type: {gap|trajectory|milestone|at_risk|achievement}
goal_id: {goal_id}
urgency_level: {critical|high|medium|low}
generated_at: {YYYY-MM-DD HH:MM}
status: active
---

# Alert: {Goal Name}

## Status

| Metric | Value |
|--------|-------|
| Current | {current_value} |
| Target | {target_value} |
| Baseline | {baseline_value} |
| Gap | {gap_value} ({gap_pct}%) |

## Urgency

| Factor | Value |
|--------|-------|
| Level | {urgency_level} |
| Score | {urgency_score} |
| Days Remaining | {days} |
| Time Pressure | {pressure} |

## Achievability

| Factor | Score |
|--------|-------|
| Overall | {achievability_score} |
| Assessment | {achievable|stretch|at_risk} |

## Trajectory

At current pace: {projected_end} by deadline
Shortfall: {shortfall} ({shortfall_pct}%)

## Recommended Action

**Type:** {action_type}
**Description:** {action_description}
**Expected Impact:** {expected_impact}

## Routing

| Field | Value |
|-------|-------|
| Owner | {accountable} |
| Escalate To | {escalation_target} |
| Ack Deadline | {ack_deadline} |
```

### Goal Status Update

Updates goal file tracking section:

```markdown
## Tracking

| Field | Value |
|-------|-------|
| Last Checked | {datetime} |
| Current Value | {current} |
| Gap | {gap_value} ({gap_pct}%) |
| Urgency | {level} |
| Achievability | {score} |
| Status | {on_track|behind|at_risk|achieved} |

### Progress History

| Date | Value | Gap | Status |
|------|-------|-----|--------|
| {date_1} | {value_1} | {gap_1} | {status_1} |
| {date_2} | {value_2} | {gap_2} | {status_2} |
```

### Dashboard Summary

Location: `artifacts/system/goal-dashboard.md`

```markdown
---
generated_at: {YYYY-MM-DD HH:MM}
period: {current period}
---

# Goal Dashboard

## Summary

| Status | Count |
|--------|-------|
| Total Goals | {count} |
| On Track | {count} |
| Behind | {count} |
| At Risk | {count} |
| Achieved | {count} |

## By Category

| Category | Goals | Progress | Top Gap |
|----------|-------|----------|---------|
| Revenue | {n} | {pct}% | {goal_id} |
| Activity | {n} | {pct}% | {goal_id} |
| Content | {n} | {pct}% | {goal_id} |
| Efficiency | {n} | {pct}% | {goal_id} |
| Retention | {n} | {pct}% | {goal_id} |

## Critical Alerts

| Goal | Gap | Urgency | Action |
|------|-----|---------|--------|
| {name} | {gap}% | critical | {action} |

## Upcoming Milestones

| Goal | Date | Target | Current | Status |
|------|------|--------|---------|--------|
| {name} | {date} | {target} | {current} | {status} |
```

## Monitoring Cadence

### Real-Time

- Inbound lead flow
- Deal stage changes
- Revenue bookings
- Churn events

### Scheduled

| Frequency | Checks |
|-----------|--------|
| Hourly | Activity goal progress |
| Daily | All gap recalculation, urgency update |
| Weekly | Achievability reassessment, trend analysis |

## Workflow

```
1. LOAD goals
   └── Read strategy/goals/active/*.md
   └── Parse frontmatter

2. COLLECT current values
   └── Read strategy/canvas/13.metrics.md
   └── Read threads/*/5-actions.md for execution data
   └── Use provided values if external

3. CALCULATE gaps
   └── Absolute gap for each goal
   └── Relative gap (percentage)
   └── Trajectory gap (projected vs target)

4. SCORE urgency
   └── Apply formula: gap × time_pressure × impact
   └── Classify into urgency levels

5. ASSESS achievability
   └── Check historical performance
   └── Validate against constraints
   └── Factor in trajectory

6. RANK priorities
   └── Apply weighted formula
   └── Sort by priority score

7. GENERATE alerts
   └── Create alert files for gaps above threshold
   └── Write to artifacts/system/alerts/

8. UPDATE goals
   └── Add/update tracking section in each goal file

9. UPDATE dashboard
   └── Write summary to artifacts/system/goal-dashboard.md
```

## Integration

### Upstream

- `sys-defining-goals`: Creates goals to track
- `sys-decomposing-goals`: Creates goal hierarchies
- `sys-activating-goals`: Links goals to threads

### Downstream

- `rop-allocator`: Receives alerts for planning
- Agents: Receive alerts for their goals
- `meta-aggregating-learnings`: Receives outcome data

## Proactive Triggers

Beyond gap tracking, detect:

### Opportunity Triggers

| Trigger | Signal | Action |
|---------|--------|--------|
| New ICP match | High-fit prospect discovered | Add to prospecting |
| Champion identified | Advocate at target account | Accelerate outreach |
| Competitor vulnerability | Customer dissatisfaction signal | Targeted outreach |

### Decay Triggers

| Trigger | Signal | Action |
|---------|--------|--------|
| Deal stalled | No stage change > threshold | Nudge action |
| Lead cooling | Engagement declining | Re-engagement sequence |
| Relationship cooling | Customer touchpoints down | Health check |

### Resource Triggers

| Trigger | Signal | Action |
|---------|--------|--------|
| Rep bandwidth | Capacity below threshold | Assign more leads |
| Budget unspent | Spend rate below plan | Increase or reallocate |

## Boundaries

**This skill provides:**
- Gap calculation
- Urgency scoring
- Achievability assessment
- Priority ranking
- Alert generation
- Goal status updates
- Dashboard summaries

**This skill does NOT:**
- Create goals (use `sys-defining-goals`)
- Decompose goals (use `sys-decomposing-goals`)
- Create threads (use `sys-activating-goals`)
- Execute against goals (agents do)
- Modify targets without approval