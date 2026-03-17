---
name: goal-tracker
description: Track goal progress, derive state from execution, identify gaps, trigger actions. Use for goal status checks, progress reviews, and operational goal management.
---

# Goal Tracker

Derive goal state from execution, track progress, identify gaps, trigger actions.

## Operating Model

Goals are the **primary** operating mode for LeanOS. Tracker maintains goal state.

```
PROACTIVE (primary):  Goal → Plan → Threads → Artifacts → Learning → Canvas
                                        ↑
                      goal-tracker derives state from here
```

**Goal-tracker reads:**
- Goal files (objectives, plans, success criteria)
- Threads (execution state, Stage 6 learning)
- Artifacts (deliverable verification)

**Goal-tracker writes:**
- Goal state section (metrics, trajectory, logs)
- Recommendations (gap-closing actions)

## Type Signature

```
GoalTracker : Goal × Threads × Time → UpdatedGoal × [Action]

Where:
  Goal         : strategy/goals/active/{id}.md
  Threads      : threads/{type}/{name}/ (linked to goal)
  Time         : Current date for trajectory calculation
  UpdatedGoal  : Goal with refreshed State section
  Action       : Recommended or auto-executed intervention
```

## When to Use

- Daily/periodic goal review
- After thread completion (update linked goal)
- User asks "How am I doing on {goal}?"
- Proactive gap detection
- Before planning sessions

## Core Operations

### 1. State Derivation

State is **computed**, not manually tracked. Derive from execution:

```
For goal G:
  1. Find linked threads:
     - Scan G.Plan.Subgoals[*].Threads
     - Load each thread's current state

  2. Aggregate execution metrics:
     threads_active = count(thread.status == "active")
     threads_completed = count(thread.status == "completed")
     threads_blocked = count(thread.status == "blocked")

  3. Extract outcome metrics:
     For each completed thread:
       Read Stage 6 (Learning) outcomes
       Map to goal success criteria

  4. Calculate derived metrics:
     For each success criterion:
       current = sum/count from thread outcomes
       gap = target - current
       trend = compare to previous state (↑↓→)
```

### 2. Subgoal Status Update

```
For each subgoal SG:
  If SG.Threads is empty:
    status = "pending"
  Else if any(thread.status == "active"):
    status = "in_progress"
  Else if all(thread.status == "completed") AND SG.Success met:
    status = "completed"
  Else if any(thread.status == "blocked"):
    status = "blocked"
```

### 3. Milestone Check

```
For each milestone M:
  If M.criterion is satisfied:
    Mark [x] completed
    Log completion date
```

### 4. Trajectory Projection

```
Given:
  current = current metric value
  target = target metric value
  start_date = goal.created
  deadline = goal.deadline
  today = current date

Calculate:
  elapsed = today - start_date
  remaining = deadline - today
  progress_rate = (current - initial) / elapsed
  projected_final = current + (progress_rate × remaining)

Determine:
  on_track = projected_final >= target
  projected_completion = start_date + ((target - initial) / progress_rate)

Risk level:
  Low = on_track AND remaining > 30 days
  Medium = on_track AND remaining <= 30 days
  High = NOT on_track
  Critical = NOT on_track AND remaining <= 14 days
```

### 5. Gap Analysis

```
For each success criterion:
  gap = target - current
  gap_percent = gap / target × 100

  If gap_percent > 50%:
    Flag: "Significant gap on {criterion}"

  If trend == "↓" AND gap_percent > 20%:
    Flag: "Declining metric: {criterion}"
```

### 6. Action Generation

Based on gaps and autonomy mode:

```
If gap detected AND goal.autonomy allows:

  For autonomy == "auto":
    Create thread directly
    Log: "Auto-created thread {id} to address {gap}"

  For autonomy == "ask":
    Generate recommendation
    Present to user with options

  For autonomy == "hybrid":
    Calculate action impact
    If impact < 0.5: auto-create
    If impact >= 0.5: ask user
```

**Action types:**
| Gap Type | Recommended Action |
|----------|-------------------|
| Pipeline gap | Create outbound campaign thread |
| Conversion gap | Create optimization thread |
| Content gap | Create content thread |
| Technical gap | Create engineering thread |
| Knowledge gap | Create learning thread |

## Output

### Updated Goal File

Update `strategy/goals/active/{goal-id}.md`:

```markdown
## State

### Metrics
| Metric | Current | Target | Gap | Trend |
|--------|---------|--------|-----|-------|
| MRR | $12,500 | $50,000 | $37,500 | ↑ |
| Customers | 6 | 10 | 4 | ↑ |
| Pipeline | 12 | 20 | 8 | → |

### Execution
- **Active threads:** 3 (campaign-q1, sales-process, content-linkedin)
- **Completed threads:** 5
- **Blocked:** 1 (waiting on legal review)

### Trajectory
- **On track:** No
- **Projected completion:** 2025-07-15 (15 days late)
- **Risk level:** Medium

## Log
- {previous entries}
- {today}: State updated. MRR +$2,500. Pipeline stalled. Risk: Medium.
```

### Progress Report (when requested)

```markdown
# Goal Progress: {Goal Title}

**Status:** {On Track | At Risk | Off Track}
**Progress:** {X}% toward objective
**Time remaining:** {N} days

## Metrics Summary
{Table of current vs target}

## What's Working
- {Positive trend 1}
- {Positive trend 2}

## Gaps Identified
- {Gap 1}: {Current} vs {Target} ({gap%} behind)
- {Gap 2}: {description}

## Recommended Actions
1. {Action 1} - addresses {gap}
2. {Action 2} - addresses {gap}

## Subgoal Status
- [x] SG1: {completed}
- [→] SG2: {in progress}
- [ ] SG3: {pending}

## Next Milestone
{Milestone description} - due {date} ({N} days)
```

## Workflows

### Snapshot (On-Demand)

```
Trigger: User asks for status, or periodic review

1. Load all active goals
2. For each goal:
   a. Derive current state
   b. Check trajectory
   c. Identify gaps and risks
3. Generate snapshot report (see Output section)
4. Present recommendations
5. Execute auto actions if autonomy allows
```

**No daily file generated.** Snapshot is computed on-demand, not stored.
Goals themselves are the persistent state - snapshot is a derived view.

### Thread Completion (Reactive)

```
Trigger: Thread reaches Stage 6 (Learning)

1. Find goal linked to thread
2. Update subgoal status
3. Extract metrics from thread learning
4. Update goal state
5. Check if goal completed
6. If completed: move to strategy/goals/completed/
```

### User Query

```
Trigger: User asks about goal progress

1. Load specified goal (or all if unspecified)
2. Derive current state
3. Generate progress report
4. Present with recommendations if gaps exist
```

### Goal Completion

```
Trigger: All success criteria met

1. Mark goal status: completed
2. Update all subgoals: completed
3. Mark remaining milestones
4. Add completion log entry
5. Move file to strategy/goals/completed/
6. Generate completion summary
7. Identify follow-on goals if any
```

## Integration

### With goal-setter
- Tracker operates on goals created by setter
- Tracker may recommend goal refinement → triggers setter

### With Threads (reasoning-causal)
- Threads execute goal subgoals via 6-stage causal flow
- Thread `meta.json` contains `goal_id` and `subgoal` reference
- Thread Stage 6 (Learning) notifies goal-tracker of completion
- Goal-tracker updates subgoal status and goal metrics
- Gap-closing actions create new goal-linked threads

### With Canvas
- Goal completion may validate Canvas assumptions
- Recommend Canvas updates based on learnings

## Autonomy Behavior

### Auto Mode
```
Gap detected → Create thread → Execute → Log
No user interaction unless error
```

### Ask Mode
```
Gap detected → Generate recommendation → Present options:
  [1] Create suggested thread
  [2] Modify recommendation
  [3] Ignore for now
  [4] Pause goal
```

### Hybrid Mode
```
Gap detected → Calculate impact:
  - Cost of action
  - Time commitment
  - Risk level

Impact < 0.5 → Auto mode
Impact >= 0.5 → Ask mode
```

## Constraints

### Update Frequency
- State derivation: On-demand or daily
- Trajectory calculation: Weekly minimum
- Full review: Before any planning session

### Data Freshness
- Thread data must be current (check updated timestamp)
- Stale data (>7 days) triggers warning

### Must NOT
- Modify goal objective or success criteria (that's goal-setter)
- Create threads without checking autonomy
- Mark goal complete without all criteria verified
- Delete or abandon goals without user confirmation

## Error Handling

**No linked threads:**
```
Warning: "Goal {id} has no execution threads.
         Subgoals defined but not activated.
         Recommend: Create initial threads for SG1."
```

**Stale goal (no updates >14 days):**
```
Warning: "Goal {id} has no activity for {N} days.
         Options: (1) Review and update, (2) Pause goal, (3) Abandon goal"
```

**Conflicting metrics:**
```
Warning: "Metric {name} has conflicting values from threads.
         Thread A: {value}, Thread B: {value}
         Using: {resolution strategy}"
```

**Goal deadline passed:**
```
Alert: "Goal {id} deadline was {date}.
        Status: {achieved | not achieved}
        Options: (1) Extend deadline, (2) Mark completed as-is, (3) Abandon"
```
