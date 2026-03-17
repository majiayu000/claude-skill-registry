---
name: sys-defining-goals
description: Transforms business strategy (canvas) or natural language into a single measurable goal. Classifies input, extracts intent, derives target using formulas, writes goal file. Does NOT decompose - use sys-decomposing-goals for hierarchy.
triggers: define goal, create goal, set target, establish objective
allowed-tools: Read, Write, Glob, Grep
license: Complete terms in LICENSE.txt
---

# Goal Defining

Transform a single strategic intent into a measurable, actionable goal file.

## Responsibility

Define ONE goal. For goal hierarchies, invoke `sys-decomposing-goals` after.

## Quick Start

1. Classify input (canvas, natural language, hybrid)
2. Extract strategic intent
3. Identify canvas gaps (prompt if blocking)
4. Derive target using formulas
5. Create goal directory and write `strategy/goals/active/{goal-dir}/goal.md`

## Input Classification

### Canvas Input

Indicators:
- References `strategy/canvas/*.md` files
- Contains structured frontmatter
- Uses canvas terminology (mode, segments, GTM)
- Contains metric targets from canvas

Action: Read referenced files → extract values → derive target

### Natural Language Input

Indicators:
- Conversational phrasing ("I want to...", "We need to...")
- Vague quantifiers ("more", "better", "increase")
- Missing time bounds or baselines
- No canvas file references

Action: Extract intent → map to category → ask clarifying questions → derive target

### Hybrid Input

Indicators:
- References canvas with verbal context
- Partial data with narrative
- Mode awareness with conversational goals

Action: Extract structured first → supplement with intent

## Intent Extraction

### From Natural Language

| User Says | Intent | Category |
|-----------|--------|----------|
| "grow revenue" | increase_arr | revenue |
| "more customers" | acquire_customers | revenue |
| "book more meetings" | increase_meetings | activity |
| "generate leads" | increase_mqls | activity |
| "publish more content" | increase_content | content |
| "speed up sales" | reduce_cycle_time | efficiency |
| "reduce CAC" | optimize_cac | efficiency |
| "keep customers" | improve_retention | retention |

### From Canvas

| Section | Extractable Data |
|---------|-----------------|
| `00.mode.md` | Metric framework (MRR vs ARR) |
| `04.segments.md` | ICP-specific targets |
| `08.pricing.md` | ARPU for revenue calculations |
| `13.metrics.md` | Current baseline values |
| `15.gtm.md` | Channel-specific capacity |

## Canvas Dependencies

### Required (blocking if missing)

| File | Purpose |
|------|---------|
| `strategy/canvas/00.mode.md` | Determines metric framework |
| `strategy/canvas/13.metrics.md` | Provides baseline values |

### Recommended (use defaults if missing)

| File | Default If Missing |
|------|-------------------|
| `strategy/canvas/08.pricing.md` | $50K avg deal |
| `strategy/canvas/07.uvp.md` | 25% win rate |
| `strategy/canvas/15.gtm.md` | Equal channel distribution |

## Target Derivation

### Revenue Targets

Pipeline from revenue:
- Formula: `target_revenue / win_rate`
- Default win_rate: 0.25
- Example: $1M / 0.25 = $4M pipeline

Meetings from pipeline:
- Formula: `pipeline / (opp_rate × avg_deal_size)`
- Default opp_rate: 0.30, avg_deal: $50K
- Example: $4M / (0.30 × $50K) = 267 meetings

### Activity Targets

Outreach from meetings:
- Formula: `meetings / meeting_rate`
- Default meeting_rate: 0.02
- Example: 267 / 0.02 = 13,350 touches

MQLs from SQLs:
- Formula: `sql_target / mql_to_sql_rate`
- Default mql_to_sql: 0.40

### Efficiency Targets

Conversion improvement:
- Formula: `current_rate + improvement_target`
- Default improvement: 5 percentage points

Cycle time reduction:
- Formula: `current_days × (1 - reduction_pct)`
- Default reduction: 15%

## Output

### Directory Structure

Each goal gets its own directory under `strategy/goals/active/`:

```
strategy/goals/active/{goal-dir}/
└── goal.md          # Parent goal definition
```

Subgoals (created by `sys-decomposing-goals`) are added as numbered files in the same directory.

### Goal Directory and ID Format

`{short-name}-{period}`

The goal_id in frontmatter matches the directory name. Use concise, descriptive names.

Examples:
- `ea-revenue-q1` → `strategy/goals/active/ea-revenue-q1/goal.md`
- `distribution-q1` → `strategy/goals/active/distribution-q1/goal.md`
- `conversion-q1` → `strategy/goals/active/conversion-q1/goal.md`

### File Structure

```markdown
---
goal_id: {goal_id}
name: {human readable name}
category: {revenue|activity|content|efficiency|retention}
target_value: {number}
target_unit: {currency|count|percentage|days}
target_direction: {maximize|minimize}
period_start: {YYYY-MM-DD}
period_end: {YYYY-MM-DD}
period_type: {quarterly|monthly|weekly|annual}
baseline_value: {number}
baseline_source: {file path or "user_provided"}
baseline_date: {YYYY-MM-DD}
parent_goal: {goal_id|null}
child_goals: []
thread: null
derivation_formula: {formula name}
derivation_assumptions: [{name}: {value}]
ownership_accountable: {role}
ownership_contributors: [{roles}]
constraints_budget: {number|null}
constraints_headcount: {number|null}
constraints_capacity: {description|null}
confidence_score: {0.0-1.0}
status: active
created: {YYYY-MM-DD}
---

# {Goal Name}

## Target

{target_value} {unit} by {period_end}

## Current State

{baseline_value} {unit} as of {baseline_date}

## Gap Analysis

- **Absolute Gap:** {target - baseline} {unit}
- **Relative Gap:** {gap_percentage}%
- **Required Pace:** {daily_required} {unit}/day

## Derivation

**Source:** {parent_goal or "Direct input"}
**Formula:** {formula_description}

### Assumptions

| Assumption | Value | Source |
|------------|-------|--------|
| {name} | {value} | {canvas section or default} |

## Milestones

| Date | Target | Status |
|------|--------|--------|
| {milestone_1_date} | {value} | pending |
| {milestone_2_date} | {value} | pending |
| {milestone_3_date} | {value} | pending |

## Risk Factors

- {risk_1}
- {risk_2}

## Constraints

- **Budget:** {amount or "None"}
- **Headcount:** {count or "None"}
- **Capacity:** {description or "None"}
```

## Milestone Generation

### Linear Distribution

Even split across period:
- Formula: `baseline + (gap × milestone_fraction)`
- Use when: Steady-state activity

### Front-Loaded

More progress early:
- Distribution: [40%, 30%, 30%]
- Use when: Building momentum

### Back-Loaded

Acceleration expected:
- Distribution: [20%, 30%, 50%]
- Use when: Ramp-up required

## Workflow

```
1. RECEIVE input (canvas reference, NL, or hybrid)

2. CLASSIFY input type
   └── Canvas: Read files, extract structured values
   └── NL: Extract intent, ask clarifying questions
   └── Hybrid: Extract structured first, supplement

3. CHECK canvas dependencies
   └── Required missing: STOP, prompt user
   └── Recommended missing: Use defaults, flag

4. DERIVE target
   └── Apply appropriate formula
   └── Record assumptions used

5. CALCULATE milestones
   └── Determine distribution pattern
   └── Generate milestone dates and values

6. WRITE goal file
   └── Create directory: strategy/goals/active/{goal-dir}/
   └── Write: strategy/goals/active/{goal-dir}/goal.md
   └── Format: Frontmatter + prose (no inline YAML)

7. UPDATE index
   └── Add to strategy/goals/index.md

8. RETURN goal_id for downstream use
```

## Integration

### Upstream

- Human input (conversational or structured)
- Canvas files for baseline data

### Downstream

- `sys-decomposing-goals`: Break into subgoals
- `sys-activating-goals`: Create execution thread
- `sys-tracking-goals`: Monitor progress

## Boundaries

**This skill provides:**
- Input classification
- Intent extraction
- Canvas gap detection
- Single goal derivation
- Goal file generation

**This skill does NOT:**
- Decompose goals into subgoals (use `sys-decomposing-goals`)
- Create execution threads (use `sys-activating-goals`)
- Track progress (use `sys-tracking-goals`)
- Modify canvas sections

## Examples

### Example 1: Canvas Input

Input:
```
Set Q1 revenue goal based on strategy/canvas/13.metrics.md
```

Process:
1. Read 13.metrics.md → current_arr: $650K
2. Read 00.mode.md → VENTURE mode, ARR focus
3. Apply 30% growth default → target: $845K
4. Create directory and write goal file

Output:
```
strategy/goals/active/arr-q1/
└── goal.md
```

### Example 2: Natural Language Input

Input:
```
I want to hit $1M ARR by end of Q1
```

Process:
1. Extract: intent=target_arr, value=$1M, period=Q1
2. Ask: "What's your current ARR baseline?"
3. User: "$650K"
4. Calculate gap: $350K (35%)
5. Create directory and write goal file

Output:
```
strategy/goals/active/arr-q1/
└── goal.md
```

### Example 3: Hybrid Input

Input:
```
Based on our bootstrap mode and current metrics,
I want to add 50 new customers this quarter
```

Process:
1. Read 00.mode.md → BOOTSTRAP confirmed
2. Read 13.metrics.md → current_customers: 120
3. Target: 170 customers (+50)
4. Create directory and write goal file

Output:
```
strategy/goals/active/customers-q1/
└── goal.md
```