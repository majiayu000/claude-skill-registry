---
name: sys-activating-goals
description: Creates execution threads for goals using the 6-stage causal flow pattern. Links threads to goals, initializes 1-input.md with goal context, and routes to appropriate agent for execution. Transforms defined goals into actionable work.
triggers: activate goal, start goal, execute goal, create thread for goal
allowed-tools: Read, Write, Glob, Grep
license: Complete terms in LICENSE.txt
---

# Goal Activating

Transform a defined goal into an active execution thread.

## Responsibility

Create an execution thread for a goal using the causal flow pattern. Link the thread to the goal and route to the appropriate agent.

## Quick Start

1. Read goal from `strategy/goals/active/{goal-id}.md`
2. Determine thread location based on goal category
3. Create thread directory with causal flow structure
4. Initialize `1-input.md` with goal context
5. Update goal file with thread link
6. Route to appropriate agent

## Causal Flow Structure

Every execution thread follows this structure:

```
threads/{domain}/{thread-name}/
└── 1-input.md          # Goal context, constraints, success criteria
                        # Stages 2-6 created by sys-executing-threads when agents write output
```

## Thread Location Mapping

| Goal Category | Thread Domain | Agent |
|---------------|--------------|-------|
| revenue | revops | rop-allocator |
| activity | marketing or sales | mkt-campaign-manager or sls-outbound-manager |
| content | marketing | mkt-content-manager |
| efficiency | revops | rop-evaluator |
| retention | customer | cst-lifecycle-manager |

### Detailed Routing

```
Revenue Goals:
├── Pipeline target → threads/revops/ → rop-allocator
├── Bookings target → threads/sales/ → sls-strategist
└── Expansion target → threads/customer/ → cst-growth-manager

Activity Goals:
├── Meeting target → threads/sales/ → sls-outbound-manager
├── Outreach target → threads/sales/ → sls-outbound-manager
├── MQL target → threads/marketing/ → mkt-inbound-manager
└── Demo target → threads/sales/ → sls-outbound-manager

Content Goals:
├── Production target → threads/marketing/ → mkt-content-manager
├── Traffic target → threads/marketing/ → mkt-campaign-manager
└── SEO target → threads/marketing/ → mkt-content-manager

Efficiency Goals:
├── Conversion rate → threads/revops/ → rop-calibrator
├── Cycle time → threads/sales/ → sls-strategist
└── CAC optimization → threads/revops/ → rop-evaluator

Retention Goals:
├── Churn reduction → threads/customer/ → cst-lifecycle-manager
├── NRR target → threads/customer/ → cst-growth-manager
└── Renewal rate → threads/customer/ → cst-lifecycle-manager
```

## Thread Naming

Format: `{goal-metric}_{period-short}`

Examples:
- `pipeline_2026q1`
- `meetings_2026m01`
- `content-production_2026q1`
- `churn-reduction_2026q1`

## Output Structure

### Thread Directory

```
threads/{domain}/{thread-name}/
└── 1-input.md    # Only file created by this skill
                  # 2-6 created by sys-executing-threads
```

### 1-input.md Format

```markdown
---
thread_id: {domain}_{thread-name}
goal_id: {linked goal id}
created: {YYYY-MM-DD}
owner: {agent name}
status: active
---

# {Goal Name} Execution

## Goal Link

**Goal:** strategy/goals/active/{goal-id}.md
**Target:** {target_value} {unit}
**Deadline:** {period_end}
**Gap:** {current gap to close}

## Context

### Current State

{baseline_value} {unit} as of {baseline_date}

### Constraints

| Constraint | Value |
|------------|-------|
| Budget | {amount or "None"} |
| Headcount | {count or "None"} |
| Capacity | {description or "None"} |

### Assumptions

| Assumption | Value | Source |
|------------|-------|--------|
| {name} | {value} | {source} |

## Success Criteria

| Metric | Target | Current | Gap |
|--------|--------|---------|-----|
| {primary metric} | {target} | {current} | {gap} |

## Milestones

| Date | Target | Status |
|------|--------|--------|
| {date_1} | {value_1} | pending |
| {date_2} | {value_2} | pending |

## Dependencies

### Requires

- {upstream goals or resources}

### Enables

- {downstream goals}

## Risk Factors

- {risk_1}
- {risk_2}

## Routing

**Assigned Agent:** {agent-name}
**Reason:** {category-based routing logic}
```

### Stages 2-6

Templates for stages 2-6 are defined in `sys-executing-threads`. This skill does NOT create them. Agents produce output, then call `sys-executing-threads` to write the stage files.

## Process

### Step 1: Read Goal

```
Read: strategy/goals/active/{goal-id}.md
Extract:
  - goal_id
  - name
  - category
  - target_value, target_unit
  - period_start, period_end
  - baseline_value
  - constraints
  - assumptions
  - risk_factors
  - milestones
```

### Step 2: Determine Thread Location

```
1. Map category to domain
2. Check if parent goal has thread (coordinate)
3. Generate thread name from metric + period
4. Full path: threads/{domain}/{thread-name}/
```

### Step 3: Create Thread Directory

```
1. Create directory if not exists
2. Create 1-input.md (populated with goal context)
   - Stages 2-6 are NOT created here
   - They are created by sys-executing-threads when agents write output
```

### Step 4: Populate 1-input.md

```
1. Copy goal context into 1-input.md frontmatter
2. Format success criteria from goal targets
3. Include constraints and assumptions
4. List milestones as checkpoints
5. Note dependencies and risks
6. Assign agent based on routing
```

### Step 5: Update Goal File

```
Add thread link to goal frontmatter:
  thread: threads/{domain}/{thread-name}

Update status:
  status: activated
```

### Step 6: Route to Agent

```
Return activation context:
  thread_path: threads/{domain}/{thread-name}
  assigned_agent: {agent-name}
  goal_id: {goal-id}
  priority: {from goal urgency}
```

## Batch Activation

For decomposed goal hierarchies:

```
1. Identify leaf goals (no children)
2. Sort by dependency order
3. Activate each leaf goal
4. Parent goals activate when children complete
```

### Activation Priority

| Condition | Priority |
|-----------|----------|
| Deadline < 7 days | critical |
| Deadline < 14 days | high |
| Deadline < 30 days | medium |
| Deadline > 30 days | low |
| Blocking other goals | +1 level |

## Workflow

```
1. RECEIVE goal_id to activate

2. READ goal file
   └── Parse frontmatter and body
   └── Extract all goal attributes

3. CHECK activation readiness
   └── Goal status must be "active"
   └── Goal must not already have thread
   └── Dependencies should be met (or flag)

4. DETERMINE thread location
   └── Map category → domain
   └── Generate thread name
   └── Create full path

5. CREATE thread structure
   └── Make directory
   └── Write 1-input.md with goal context
   └── Stages 2-6 created later by sys-executing-threads

6. UPDATE goal file
   └── Add thread link
   └── Update status to "activated"

7. RETURN activation context
   └── thread_path
   └── assigned_agent
   └── priority
```

## Integration

### Upstream

- `sys-defining-goals`: Provides goal to activate
- `sys-decomposing-goals`: Provides leaf goals to activate

### Downstream

- Assigned agent receives thread for execution
- `sys-tracking-goals`: Monitors thread progress against goal

### With Agents

The assigned agent:
1. Reads `1-input.md`
2. Fills `2-hypothesis.md` with approach
3. Derives `3-implication.md`
4. Makes `4-decision.md`
5. Executes `5-actions.md`
6. Records `6-learning.md`

Agents write to stage files via `sys-executing-threads` skill, which handles frontmatter updates and completion tracking.

## Boundaries

**This skill provides:**
- Thread creation for goals
- Causal flow structure initialization
- Goal-thread linking
- Agent routing

**This skill does NOT:**
- Define goals (use `sys-defining-goals`)
- Decompose goals (use `sys-decomposing-goals`)
- Execute the work (agents do)
- Track progress (use `sys-tracking-goals`)

## Example

### Input

Goal: `goal_activity_meetings_2026q1`
- Category: activity
- Target: 100 meetings
- Period: Q1 2026
- Baseline: 0 (new quarter)

### Process

1. Read goal file
2. Map: activity → sales domain
3. Route: meetings → sls-outbound-manager
4. Thread path: `threads/sales/meetings_2026q1/`
5. Create directory and files
6. Populate 1-input.md with goal context
7. Update goal: `thread: threads/sales/meetings_2026q1`

### Output

Directory created:
```
threads/sales/meetings_2026q1/
└── 1-input.md      # Populated with goal context
```

Goal updated:
```yaml
thread: threads/sales/meetings_2026q1
status: activated
```

Activation context returned:
```
thread_path: threads/sales/meetings_2026q1
assigned_agent: sls-outbound-manager
goal_id: goal_activity_meetings_2026q1
priority: medium
```