---
name: sprint-plan
description: Create comprehensive sprint plans by intelligently grouping estimated user stories based on velocity, dependencies, priorities, and risk. This skill should be used during sprint planning ceremonies to transform backlog into actionable sprint commitments.
acceptance:
  - velocity_respected: "Total story points ≤ team velocity with 15% buffer"
  - dependencies_satisfied: "All story dependencies respected in sprint ordering"
  - priorities_honored: "P0 stories prioritized over P1/P2/P3"
  - sprint_plan_generated: "Sprint plan file created with goals, stories, risks, and metrics"
inputs:
  sprint_name:
    type: string
    required: true
    description: "Name of sprint (e.g., 'Sprint 1', 'Q1 Sprint 3')"
  velocity:
    type: number
    required: true
    description: "Team velocity in story points (historical or estimated)"
  plan_ahead:
    type: number
    default: 1
    description: "Number of sprints to plan (1-4)"
  stories:
    type: array
    required: false
    description: "Specific story IDs to include (default: auto-select from backlog)"
  buffer:
    type: number
    default: 0.15
    description: "Reserve buffer percentage (default: 15% of velocity)"
outputs:
  sprint_plan:
    type: object
    description: "Sprint plan with goals, stories, capacity, risks"
  commitment:
    type: number
    description: "Total story points committed"
  utilization:
    type: number
    description: "Percentage of velocity utilized"
  sprint_plan_file:
    type: string
    description: "Path to generated sprint plan file"
telemetry:
  emit: "skill.sprint-plan.completed"
  track:
    - sprint_name
    - velocity
    - duration_ms
    - stories_count
    - commitment_points
    - utilization_percent
    - p0_stories_count
    - dependencies_count
---

# Sprint Planning

Create comprehensive sprint plans by intelligently grouping estimated user stories based on team velocity, dependencies, priorities, and risk mitigation.

## Purpose

Transform backlog of estimated stories into actionable sprint commitments:
- Calculate effective capacity (velocity - buffer)
- Select stories respecting dependencies and priorities
- Balance workload and minimize risk
- Generate sprint plan with goals, metrics, and risk mitigation
- Support multi-sprint planning (roadmap view)

## When to Use This Skill

This skill should be used when:
- Starting a new sprint (during Sprint Planning ceremony)
- Re-planning mid-sprint due to significant changes
- Creating multi-sprint roadmap (2-4 sprints ahead)
- Evaluating sprint capacity and feasibility
- Balancing team workload across multiple teams

This skill should NOT be used when:
- Stories are not yet estimated (use estimate-stories first)
- Stories lack acceptance criteria (use refine-story first)
- No historical velocity data (establish velocity first with 1-2 sprints)

## Prerequisites

- Stories created (via breakdown-epic skill)
- Stories estimated (via estimate-stories skill)
- Clear team velocity (historical average or initial estimate)
- Dependencies identified (in story files or epic summaries)

## Sequential Sprint Planning Process

Execute steps in order - each builds on previous analysis:

### Step 0: Load Configuration and Sprint Context

**Purpose:** Gather all inputs needed for sprint planning.

**Actions:**

1. Validate sprint parameters:
   - Sprint name (must be unique)
   - Velocity (must be > 0)
   - Plan ahead (1-4 sprints)
   - Buffer percentage (default 15%)

2. Load all eligible stories from `.claude/stories/`:
   - Filter: Status = "Ready" or "Backlog"
   - Filter: Has story points estimated
   - Filter: Has acceptance criteria

3. Load dependencies:
   - From story files (Dependencies section)
   - From epic summaries (dependency graphs)
   - Build dependency map

4. Calculate effective capacity:
   ```
   Effective Capacity = Velocity × (1 - Buffer)
   Example: 20 points × (1 - 0.15) = 17 points available
   ```

**Output:** Sprint context loaded with velocity, buffer, effective capacity, eligible stories, dependencies identified

**See:** `references/templates.md#step-0-output` for complete format and `sprint-planning-mechanics.md` for capacity calculations

---

### Step 1: Prioritize and Sort Stories

**Purpose:** Create prioritized list respecting business value and dependencies.

**Sorting Criteria (in order):**

1. **Priority Level** (P0 > P1 > P2 > P3)
2. **Dependency Order** (blockers before blocked)
3. **Risk Score** (high-risk early for discovery)
4. **Story Points** (smaller stories for momentum)

**Output:** Stories prioritized and sorted by priority level, dependency order, risk score, story points

**See:** `references/templates.md#step-1-output` for complete sorted backlog example and `story-selection-algorithm.md` for sorting logic

---

### Step 2: Select Stories for Sprint

**Purpose:** Fill sprint capacity with highest-value stories respecting constraints.

**Selection Algorithm:**

1. Start with P0 stories in dependency order
2. Add story if:
   - All dependencies already in sprint OR completed
   - Points fit within remaining capacity
   - Doesn't create incomplete feature (orphaned dependencies)
3. Continue with P1, then P2 stories
4. Stop when capacity reached or no more valid stories

**Output:** Stories selected for sprint respecting capacity, dependencies, feature completeness | Total points, utilization percentage, remaining capacity

**See:** `references/templates.md#step-2-output` for complete selection example and `story-selection-algorithm.md` for selection rules

---

### Step 3: Validate Dependencies

**Purpose:** Ensure no broken dependencies in sprint plan.

**Validation Checks:**

1. **Blocker Check:** All blocking stories either:
   - Included in current sprint (before blocked story)
   - Already completed (status = Done)

2. **Feature Completeness:** Avoid partial features:
   - If story A blocks B and C, either include all or none
   - Don't leave dependent stories orphaned

3. **Cross-Sprint Dependencies:** For multi-sprint plans:
   - Dependencies can span sprints (A in Sprint 1, B in Sprint 2)
   - But must be in correct order

**Output:** Dependencies validated, all blocking relationships satisfied, no orphaned dependencies, feature completeness maintained

**See:** `references/templates.md#step-3-output` for complete validation examples including edge cases

---

### Step 4: Identify Risks and Mitigation

**Purpose:** Surface sprint risks and plan mitigation.

**Risk Categories:**

1. **Capacity Risk:** Sprint over/under-committed
   - Over: >95% utilization (no buffer for unknowns)
   - Under: <75% utilization (team under-utilized)

2. **Dependency Risk:** Critical path dependencies
   - Long chains (A → B → C → D)
   - Single blocker affecting many stories

3. **Technical Risk:** High-risk stories in sprint
   - Stories with risk score > 6 (from estimation)
   - Unproven technology or approach

4. **Scope Risk:** Too many P0 stories
   - Sprint becomes "all or nothing"
   - No flexibility for adjustments

**Output:** Sprint risks assessed by category (capacity/dependency/technical/scope), overall risk level, mitigation strategies identified

**See:** `references/templates.md#step-4-output` for detailed risk assessment example and `sprint-risk-assessment.md` for scoring methodology

---

### Step 5: Define Sprint Goal

**Purpose:** Articulate clear, measurable sprint goal.

**Sprint Goal Formula:**
```
[Action Verb] [Feature/Outcome] so that [Business Value]
```

**Examples:**
- "Implement core authentication so that users can securely access the platform"
- "Enable user profile management so that users can personalize their experience"
- "Complete payment integration so that customers can purchase products"

**Good Sprint Goals:**
- **Specific:** Clear what will be delivered
- **Measurable:** Can verify if goal achieved
- **Valuable:** Business value is clear
- **Achievable:** Realistic given velocity
- **Focused:** 1-2 main themes, not scattered

**Poor Sprint Goals:**
- ❌ "Complete as many stories as possible"
- ❌ "Work on authentication and profiles and settings and..."
- ❌ "Make progress on the backlog"

**Output:** Sprint goal defined following formula ([Action] [Feature] so that [Business Value]), success criteria specified, goal validated (specific/measurable/valuable/achievable/focused)

**See:** `references/templates.md#step-5-output` for complete goal examples and `sprint-goals-and-metrics.md` for goal patterns

---

### Step 6: Calculate Sprint Metrics

**Purpose:** Provide quantitative sprint health indicators.

**Key Metrics:**

1. **Commitment:** Total story points committed
2. **Utilization:** Percentage of velocity used
3. **P0 Coverage:** Percentage of P0 stories included
4. **Dependency Depth:** Longest dependency chain
5. **Risk Score:** Weighted average of story risks

**Output:** Sprint metrics calculated including capacity (velocity/buffer/commitment/utilization), stories (total/priority breakdown), dependencies (relationships/longest chain), risk (average score/high-risk count/overall level)

**See:** `references/templates.md#step-6-output` for complete metrics example with all fields

---

### Step 7: Generate Sprint Plan Document

**Purpose:** Create comprehensive sprint plan file.

**File:** `.claude/sprints/sprint-{sprint-name}-{date}.md`

**Output:** Sprint plan document generated with sections: Sprint Goal, Committed Stories table, Sprint Metrics, Risks and Mitigation, Sprint Schedule, Definition of Done

**File:** `.claude/sprints/sprint-{name}-{date}.md`

**See:** `references/templates.md#step-7-output` for complete sprint plan document template with all sections

---

### Step 8: Multi-Sprint Planning (Optional)

**Purpose:** Plan 2-4 sprints ahead for roadmap visibility.

**When to Use:**
- plan_ahead parameter > 1
- Creating quarterly roadmap
- Long-range feature planning

**Process:**
1. Plan Sprint 1 (as above)
2. Mark Sprint 1 stories as "allocated"
3. Repeat Steps 1-7 for Sprint 2 with remaining stories
4. Continue for Sprint 3, 4 as needed

**Output:** Multiple sprint plans generated, total roadmap points, stories distributed across sprints, files created for each sprint

**See:** `references/templates.md#step-8-output` for multi-sprint roadmap example and `sprint-planning-mechanics.md` for algorithm

---

### Step 9: Present Sprint Plan Summary

**Purpose:** Communicate sprint plan clearly to team.

**Output:** Sprint plan summary with sprint name/dates, commitment details (stories/points/utilization), sprint goal, top stories list, risk summary, sprint plan file path, next steps

**See:** `references/templates.md#step-9-output` for complete summary format

---

## Integration with Other Skills

**Before Sprint Planning:**
- `breakdown-epic` → Create stories from epics
- `refine-story` → Ensure stories are sprint-ready
- `estimate-stories` → Estimate story points

**After Sprint Planning:**
- `implement-feature` → Implement stories from sprint
- `review-task` → Quality check completed stories
- (Next sprint) → `sprint-plan` again with updated velocity

---

## Best Practices

Respect velocity (10-15% buffer) | Honor dependencies (never break chains) | Focus on value (P0/P1 first) | Balance risk (mix high/low risk stories) | Complete features (avoid half-done work) | Review and adapt (update velocity based on actuals)

**See:** `sprint-goals-and-metrics.md` for detailed planning best practices

---

## Reference Files

Detailed documentation in `references/`:

- **templates.md**: All output formats (Steps 0-9), complete sprint plan document template, multi-sprint roadmap examples, risk assessment examples, sprint goal examples, JSON output format

- **sprint-planning-mechanics.md**: Capacity calculation, multi-sprint algorithm, velocity tracking

- **story-selection-algorithm.md**: Sorting criteria, selection rules, edge cases

- **sprint-risk-assessment.md**: Risk categories, scoring methodology, mitigation strategies

- **sprint-goals-and-metrics.md**: Goal-setting patterns, metrics definitions, best practices
