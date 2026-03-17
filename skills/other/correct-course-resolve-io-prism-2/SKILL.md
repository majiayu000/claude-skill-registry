---
name: correct-course
description: Use when handling sprint changes or scope adjustments. Analyzes change impacts, re-estimates affected stories, and adjusts sprint capacity using PRISM principles.
version: 1.0.0
---
<!-- Powered by PRISMâ„¢ Core -->

# Correct Course Task

## Quick Start

1. Acknowledge change trigger with user
2. Load current sprint stories and estimations
3. Calculate velocity impact using PRISM analysis
4. Re-estimate affected stories with PROBE method
5. Generate sprint change proposal
6. Update estimation history with lessons learned

## Purpose

Guide a structured response to change triggers using PRISM principles and PSP/TSP measurement:
- Analyze change impacts on epics, stories, and estimations
- Re-estimate affected stories using PROBE method
- Track velocity impact and adjust sprint capacity
- Maintain estimation accuracy through changes
- Document lessons learned for future estimation

## Instructions

### 1. Initial Setup & Impact Assessment

**Acknowledge Change & Measure Impact:**
- Confirm the change trigger with user
- Load current sprint stories and their estimations
- Calculate potential velocity impact
- Identify stories requiring re-estimation

**PSP/TSP Metrics to Consider:**
- Current sprint velocity vs planned
- Stories completed vs in-progress
- Estimation accuracy to date
- Team capacity remaining

### 2. Analyze Change Using PRISM Principles

**Predictability Impact:**
- How does change affect sprint predictability?
- What estimations become invalid?
- Which dependencies are affected?

**Resilience Considerations:**
- Can we absorb change without sprint failure?
- What's our contingency capacity?
- Are critical path items affected?

**Intentionality Check:**
- Is change aligned with sprint goals?
- Does it support product vision?
- Should we defer to next sprint?

**Sustainability Analysis:**
- Team capacity to handle change
- Technical debt implications
- Long-term velocity impact

**Maintainability Review:**
- Code quality impact of rushed changes
- Documentation update needs
- Test coverage considerations

### 3. Re-estimate Affected Stories

For each affected story:
```yaml
re_estimation:
  original_estimate:
    story_points: X
    size_category: Y
    hours: Z
  
  change_impact:
    scope_change: "+/-N%"
    complexity_change: "increased|decreased|same"
    risk_change: "higher|lower|same"
  
  new_estimate:
    story_points: X'
    size_category: Y'
    hours: Z'
    confidence: "high|medium|low"
  
  justification: "Clear explanation of estimate change"
```

### 4. Sprint Capacity Recalculation

```yaml
sprint_metrics:
  original:
    total_points: X
    total_hours: Y
    team_capacity: Z
  
  after_change:
    total_points: X'
    total_hours: Y'
    team_capacity: Z'
    
  options:
    - absorb: "Take the hit, extend hours"
    - defer: "Move stories to next sprint"
    - swap: "Replace with smaller stories"
    - descope: "Reduce story scope"
```

### 5. Generate Sprint Change Proposal

Create proposal document with:

**Executive Summary:**
- Change description and trigger
- Impact on sprint goals
- Recommended path forward

**Metrics Impact:**
- Velocity change: X â†’ Y points
- Capacity change: A â†’ B hours  
- Risk score change: Low â†’ Medium
- Confidence level: 85% â†’ 70%

**Story-Level Changes:**
For each affected story:
- Original estimation
- New estimation with rationale
- Dependencies affected
- Risk mitigation needed

**Team Considerations:**
- Role reassignments needed
- Skill gaps identified
- Additional resources required
- Quality gate adjustments

**Proposed Actions:**
1. Specific story changes
2. Sprint backlog adjustments
3. Team assignment updates
4. Timeline modifications

### 6. Update Estimation History

Record in estimation-history.yaml:
```yaml
change_events:
  - date: YYYY-MM-DD
    sprint: N
    trigger: "requirement change|bug|scope creep"
    stories_affected: [X.Y, X.Z]
    estimation_impact:
      total_points_change: +/-N
      accuracy_impact: "X%"
    lessons_learned: |
      - Specific insight about estimation
      - Pattern identified for future
    improvement_actions:
      - "Add buffer for similar changes"
      - "Update estimation proxies"
```

### 7. Team Communication

**Sprint Adjustment Meeting Agenda:**
1. Present change and impact (5 min)
2. Review estimation changes (10 min)
3. Discuss capacity options (10 min)
4. Team consensus on path (5 min)
5. Update assignments (5 min)

**Key Messages:**
- Data-driven decision making
- Transparency on impact
- Team empowerment to choose
- Learning opportunity captured

## Success Criteria

- [ ] All affected stories re-estimated
- [ ] Sprint capacity recalculated
- [ ] Team consensus achieved
- [ ] Estimation history updated
- [ ] Lessons learned documented
- [ ] Sprint plan adjusted and communicated

## Output Deliverables

**Primary:** Sprint Change Proposal (markdown)
- Executive summary with metrics
- Detailed estimation changes
- Recommended actions
- Updated sprint plan

**Secondary:** Updated Artifacts
- Stories with new estimations
- Sprint backlog adjustments
- Estimation history updates
- Team communication record
