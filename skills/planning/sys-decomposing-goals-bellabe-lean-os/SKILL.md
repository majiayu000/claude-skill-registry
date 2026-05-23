---
name: sys-decomposing-goals
description: Decomposes a goal into subgoals using top-down derivation formulas. Creates linked goal hierarchy with parent-child relationships. Recursively breaks business goals into system, operational, and tactical goals.
triggers: decompose goal, break down goal, create subgoals, goal hierarchy
allowed-tools: Read, Write, Glob, Grep
license: Complete terms in LICENSE.txt
---

# Goal Decomposing

Break a single goal into a hierarchy of actionable subgoals.

## Responsibility

Take ONE goal and decompose it into subgoals using derivation formulas. Creates multiple goal files with parent-child links.

## Quick Start

1. Read parent goal from `strategy/goals/active/{goal-dir}/goal.md`
2. Determine decomposition pattern based on category
3. Apply derivation formulas to create subgoals
4. Write subgoal files as `{n}.{name}.md` in the parent goal directory
5. Update parent `goal.md` with child links

## Decomposition Hierarchy

```
Level 1: Business Goal (leadership)
    │    "Achieve $10M ARR"
    │    Time horizon: Annual
    │
    ▼
Level 2: System Goal (RevOps)
    │    "Generate $40M pipeline"
    │    Time horizon: Quarterly
    │
    ▼
Level 3: Operational Goal (Team Leads)
    │    "Book 400 qualified meetings"
    │    Time horizon: Monthly
    │
    ▼
Level 4: Tactical Goal (Individual)
         "Complete 100 outreach touches/day"
         Time horizon: Weekly/Daily
```

## Decomposition Patterns

### Revenue Goal Decomposition

```
Revenue Target ($X ARR)
    │
    ├── Pipeline Target = Revenue / Win Rate
    │       │
    │       ├── Opportunities = Pipeline / Avg Deal Size
    │       │
    │       └── Meetings = Opportunities / Opp Rate
    │               │
    │               └── Outreach = Meetings / Meeting Rate
    │
    ├── Expansion Target = Existing ARR × Expansion Rate
    │       │
    │       └── Expansion Meetings = Target / Avg Expansion Deal
    │
    └── Retention Target = 100% - Churn Rate
            │
            └── At-Risk Interventions = Churn Risk Accounts × Save Rate
```

### Activity Goal Decomposition

```
Meeting Target (X meetings)
    │
    ├── Outbound Meetings = Total × Outbound Ratio
    │       │
    │       └── Outbound Touches = Meetings / Meeting Rate
    │
    └── Inbound Meetings = Total × Inbound Ratio
            │
            └── MQL Target = Meetings / MQL-to-Meeting Rate
                    │
                    └── Traffic Target = MQLs / Conversion Rate
```

### Content Goal Decomposition

```
Content Lead Target (X leads)
    │
    ├── Blog Leads = Total × Blog Attribution %
    │       │
    │       └── Blog Posts = Leads / Leads-per-Post
    │
    ├── Gated Content Leads = Total × Gated %
    │       │
    │       └── Ebooks/Guides = Leads / Leads-per-Asset
    │
    └── Traffic Target = Total / Conversion Rate
            │
            └── SEO Keywords = Traffic / Avg Traffic-per-Keyword
```

## Derivation Formulas

### Revenue Formulas

| From | To | Formula | Defaults |
|------|----|---------|---------| 
| Revenue | Pipeline | `revenue / win_rate` | win_rate: 0.25 |
| Pipeline | Opportunities | `pipeline / avg_deal` | avg_deal: $50K |
| Opportunities | Meetings | `opps / opp_rate` | opp_rate: 0.30 |
| Meetings | Outreach | `meetings / meeting_rate` | meeting_rate: 0.02 |
| Revenue | Expansion | `existing_arr × expansion_rate` | expansion_rate: 0.25 |
| Revenue | New Logo | `(target - existing × nrr) / arpu` | nrr: 1.0 |

### Activity Formulas

| From | To | Formula | Defaults |
|------|----|---------|----------|
| Meetings | MQLs | `meetings / mql_meeting_rate` | rate: 0.15 |
| MQLs | Traffic | `mqls / conversion_rate` | rate: 0.025 |
| Outreach | Emails | `outreach × email_ratio` | ratio: 0.60 |
| Outreach | Calls | `outreach × call_ratio` | ratio: 0.25 |
| Outreach | LinkedIn | `outreach × linkedin_ratio` | ratio: 0.15 |

### Efficiency Formulas

| From | To | Formula | Defaults |
|------|----|---------|----------|
| Win Rate | Stage Rates | `win_rate^(1/stages)` | stages: 4 |
| Cycle Time | Stage Times | `cycle / stages` | stages: 4 |
| CAC | Channel CAC | `cac × channel_weight` | by channel |

## Process

### Step 1: Read Parent Goal

```
Read: strategy/goals/active/{goal-dir}/goal.md
Extract:
  - goal_id (matches directory name, e.g. ea-revenue-q1)
  - category (determines pattern)
  - target_value, target_unit
  - period_start, period_end
  - baseline_value
  - assumptions
```

### Step 2: Determine Decomposition Pattern

```
if category == "revenue":
    if target > $1M:
        pattern = full_revenue_cascade
    else:
        pattern = simple_revenue_cascade
        
if category == "activity":
    pattern = activity_cascade
    
if category == "content":
    pattern = content_cascade
    
if category == "efficiency":
    pattern = efficiency_decomposition
    
if category == "retention":
    pattern = retention_decomposition
```

### Step 3: Apply Formulas

For each subgoal in pattern:
1. Calculate target using formula
2. Inherit period from parent (or subdivide)
3. Inherit constraints proportionally
4. Set parent_goal link
5. Generate goal_id

### Step 4: Write Subgoal Files

Location: Numbered files inside the parent goal directory.

```
strategy/goals/active/{goal-dir}/{n}.{name}.md
```

- `{n}` — sequential number (1, 2, 3...)
- `{name}` — short kebab-case metric name

Subgoal ID format: `{goal-dir}/{n}.{name}`

Examples:
- `ea-revenue-q1/1.launch-readiness`
- `ea-revenue-q1/2.feb-sales`
- `distribution-q1/1.github-organic`

### Step 5: Update Parent

Add child_goals list to parent `goal.md` frontmatter using subgoal IDs:

```yaml
child_goals:
  - ea-revenue-q1/1.launch-readiness
  - ea-revenue-q1/2.feb-sales
  - ea-revenue-q1/3.mar-sales
```

## Output Structure

### Directory Layout

Subgoals are numbered files inside the parent goal directory:

```
strategy/goals/active/{goal-dir}/
├── goal.md              # Parent goal (created by sys-defining-goals)
├── 1.{name}.md          # First subgoal
├── 2.{name}.md          # Second subgoal
└── 3.{name}.md          # Third subgoal
```

### Subgoal File Format

```markdown
---
goal_id: {goal-dir}/{n}.{name}
name: {descriptive name}
category: {inherited or derived}
target_value: {calculated}
target_unit: {inherited or derived}
target_direction: {inherited}
period_start: {inherited or subdivided}
period_end: {inherited or subdivided}
period_type: {inherited or derived}
baseline_value: {calculated or inherited}
baseline_source: derived_from_parent
baseline_date: {same as parent}
parent_goal: {goal-dir}
child_goals: []
thread: null
derivation_formula: {formula used}
derivation_assumptions: [{from parent + new}]
ownership_accountable: {derived from level}
ownership_contributors: []
constraints_budget: {proportional allocation}
constraints_headcount: {proportional allocation}
constraints_capacity: {inherited}
confidence_score: {parent × formula_confidence}
status: active
created: {today}
---

# {Subgoal Name}

## Target

{target_value} {unit} by {period_end}

## Derivation

**Parent Goal:** {goal-dir}/goal.md
**Formula:** {formula_description}

### Calculation

```
{parent_metric}: {parent_value}
{rate_name}: {rate_value}
Result: {parent_value} {operator} {rate_value} = {target_value}
```

## Current State

Baseline derived from parent goal derivation.

## Milestones

| Date | Target | Status |
|------|--------|--------|
| {date_1} | {value_1} | pending |
| {date_2} | {value_2} | pending |

## Dependencies

- **Requires:** {goal-dir}
- **Enables:** {child_goals if any}

## Constraints

Allocated from parent:
- **Budget:** {proportional_amount}
- **Headcount:** {proportional_count}
```

## Recursive Decomposition

For deep hierarchies, apply decomposition recursively:

```
1. Decompose business goal → system goals
2. For each system goal with target > threshold:
   └── Decompose → operational goals
3. For each operational goal with target > threshold:
   └── Decompose → tactical goals
4. Stop when:
   └── Target small enough for single owner
   └── Period is weekly or shorter
   └── No further decomposition formula exists
```

### Decomposition Thresholds

| Category | Level | Continue If |
|----------|-------|-------------|
| Revenue | System | target > $500K |
| Revenue | Operational | target > $100K |
| Activity | Operational | count > 100 |
| Activity | Tactical | count > 20/day |
| Content | Operational | pieces > 10 |

## Constraint Allocation

When parent has constraints, distribute to children:

### Budget Allocation

```
Method 1: Proportional to target
  child_budget = parent_budget × (child_target / total_child_targets)

Method 2: By category weights
  outbound_weight: 0.40
  inbound_weight: 0.35
  content_weight: 0.25
  
Method 3: Fixed allocation
  Some subgoals may have explicit budget assignments
```

### Headcount Allocation

```
If parent.headcount defined:
  - Outreach goals: AE/SDR count
  - Content goals: Writer count
  - Ops goals: Ops count
  
Calculate capacity per person:
  touches_per_sdr = 100/day
  posts_per_writer = 4/month
```

## Workflow

```
1. READ parent goal
   └── Parse frontmatter and body
   └── Extract target, category, period, constraints

2. DETERMINE decomposition pattern
   └── Match category to pattern
   └── Check thresholds for depth

3. CALCULATE subgoals
   └── Apply formulas for each level
   └── Validate against capacity constraints

4. WRITE subgoal files
   └── For each subgoal:
       └── Generate numbered filename: {n}.{name}.md
       └── Set goal_id: {goal-dir}/{n}.{name}
       └── Calculate target and milestones
       └── Write to strategy/goals/active/{goal-dir}/

5. UPDATE parent goal.md
   └── Add child_goals array to frontmatter
   └── Use subgoal IDs: [{goal-dir}/{n}.{name}]

6. RETURN subgoal list
   └── [{goal_id, target, relationship}]
```

## Validation

### Consistency Checks

```
1. Sum of child targets should derive parent target
   Example: If revenue needs $4M pipeline at 25% win rate,
   pipeline subgoal should be $4M (not arbitrary)

2. Time periods should align
   Children period ≤ parent period
   Quarterly parent → Monthly children OK
   Monthly parent → Quarterly children NOT OK

3. Constraints should not exceed parent
   sum(child_budgets) ≤ parent_budget
```

### Achievability Checks

```
1. Capacity validation
   If outreach target > team_capacity × days:
     Flag constraint, adjust or note

2. Historical benchmark
   If required rate > best_historical × 1.5:
     Flag stretch, note risk

3. Dependency check
   If child requires other goal not yet defined:
     Note dependency gap
```

## Integration

### Upstream

- `sys-defining-goals`: Provides parent goal to decompose

### Downstream

- `sys-activating-goals`: Creates threads for leaf goals
- `sys-tracking-goals`: Monitors all goals in hierarchy

### With RevOps

- `rop-calibrator`: Provides scoring models for conversion assumptions
- `rop-allocator`: May trigger decomposition for resource planning

## Boundaries

**This skill provides:**
- Hierarchical decomposition of goals
- Formula-based subgoal derivation
- Parent-child linking
- Constraint allocation

**This skill does NOT:**
- Define the initial parent goal (use `sys-defining-goals`)
- Create execution threads (use `sys-activating-goals`)
- Track progress (use `sys-tracking-goals`)
- Override parent constraints

## Example

### Input

Parent goal directory: `strategy/goals/active/arr-q1/goal.md`
- goal_id: `arr-q1`
- Target: $1,000,000 ARR
- Current: $650,000
- Period: Q1 2026
- Win rate assumption: 25%

### Output

```
strategy/goals/active/arr-q1/
├── goal.md                  # Parent (updated with child_goals)
├── 1.pipeline.md            # Target: $1,400,000 (gap $350K / 0.25)
├── 2.opportunities.md       # Target: 28 ($1.4M / $50K)
├── 3.meetings.md            # Target: 93 (28 / 0.30)
└── 4.outreach.md            # Target: 4,650 touches (93 / 0.02)
```

Parent `goal.md` updated with:
```yaml
child_goals: [arr-q1/1.pipeline, arr-q1/2.opportunities, arr-q1/3.meetings, arr-q1/4.outreach]
```

Each subgoal references `parent_goal: arr-q1` in frontmatter.