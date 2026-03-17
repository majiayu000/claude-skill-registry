---
name: retrospective
description: "Generates a sprint or milestone retrospective by analyzing completed work, velocity, blockers, and patterns. Produces actionable insights for the next iteration."
argument-hint: "[sprint-N|milestone-name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
context: |
  !git log --oneline --since="2 weeks ago" 2>/dev/null
---

When this skill is invoked:

1. **Read the argument** to determine whether this is a sprint retrospective
   (`sprint-N`) or a milestone retrospective (`milestone-name`).

2. **Read the sprint or milestone plan** from the appropriate location:
   - Sprint plans: `production/sprints/`
   - Milestone definitions: `production/milestones/`

   Extract: planned tasks, estimated effort, owners, and goals.

3. **Read the git log** for the period covered by the sprint or milestone to
   understand what was actually committed and when.

4. **Scan for completed and incomplete tasks** by comparing the plan against
   actual deliverables. Check for:
   - Tasks completed as planned
   - Tasks completed but modified from the plan
   - Tasks carried over (not completed)
   - Tasks added mid-sprint (unplanned work)
   - Tasks removed or descoped

5. **Scan the codebase for TODO/FIXME trends**:
   - Count current TODO/FIXME/HACK comments
   - Compare to previous sprint counts if available (check previous
     retrospectives)
   - Note whether technical debt is growing or shrinking

6. **Read previous retrospectives** (if any) from `production/sprints/` or
   `production/milestones/` to check:
   - Were previous action items addressed?
   - Are the same problems recurring?
   - How has velocity trended?

7. **Generate the retrospective**:

```markdown
## Retrospective: [Sprint N / Milestone Name]
Period: [Start Date] -- [End Date]
Generated: [Date]

### Metrics

| Metric | Planned | Actual | Delta |
|--------|---------|--------|-------|
| Tasks | [X] | [Y] | [+/- Z] |
| Completion Rate | -- | [Z%] | -- |
| Story Points / Effort Days | [X] | [Y] | [+/- Z] |
| Bugs Found | -- | [N] | -- |
| Bugs Fixed | -- | [N] | -- |
| Unplanned Tasks Added | -- | [N] | -- |
| Commits | -- | [N] | -- |

### Velocity Trend

| Sprint | Planned | Completed | Rate |
|--------|---------|-----------|------|
| [N-2] | [X] | [Y] | [Z%] |
| [N-1] | [X] | [Y] | [Z%] |
| [N] (current) | [X] | [Y] | [Z%] |

**Trend**: [Increasing / Stable / Decreasing]
[One sentence explaining the trend]

### What Went Well
- [Observation backed by specific data or examples]
- [Another positive observation]
- [Recognize specific contributions or decisions that paid off]

### What Went Poorly
- [Specific issue with measurable impact -- e.g., "Feature X took 5 days
  instead of estimated 2, blocking tasks Y and Z"]
- [Another issue with impact]
- [Do not assign blame -- focus on systemic causes]

### Blockers Encountered

| Blocker | Duration | Resolution | Prevention |
|---------|----------|------------|------------|
| [What blocked progress] | [How long] | [How it was resolved] | [How to prevent recurrence] |

### Estimation Accuracy

| Task | Estimated | Actual | Variance | Likely Cause |
|------|-----------|--------|----------|--------------|
| [Most overestimated task] | [X] | [Y] | [+Z] | [Why] |
| [Most underestimated task] | [X] | [Y] | [-Z] | [Why] |

**Overall estimation accuracy**: [X%] of tasks within +/- 20% of estimate

[Analysis: Are we consistently over- or under-estimating? For which types of
tasks? What adjustment should we apply?]

### Carryover Analysis

| Task | Original Sprint | Times Carried | Reason | Action |
|------|----------------|---------------|--------|--------|
| [Task that was not completed] | [Sprint N-X] | [N] | [Why] | [Complete / Descope / Redesign] |

### Technical Debt Status
- Current TODO count: [N] (previous: [N])
- Current FIXME count: [N] (previous: [N])
- Current HACK count: [N] (previous: [N])
- Trend: [Growing / Stable / Shrinking]
- [Note any areas of concern]

### Previous Action Items Follow-Up

| Action Item (from Sprint N-1) | Status | Notes |
|-------------------------------|--------|-------|
| [Previous action] | [Done / In Progress / Not Started] | [Context] |

### Action Items for Next Iteration

| # | Action | Owner | Priority | Deadline |
|---|--------|-------|----------|----------|
| 1 | [Specific, measurable action] | [Who] | [High/Med/Low] | [When] |
| 2 | [Another action] | [Who] | [Priority] | [When] |

### Process Improvements
- [Specific change to how we work, with expected benefit]
- [Another improvement -- keep it to 2-3 actionable items, not a wish list]

### Summary
[2-3 sentence overall assessment: Was this a good sprint/milestone? What is
the single most important thing to change going forward?]
```

8. **Save the retrospective** to the appropriate location:
   - Sprint: `production/sprints/sprint-[N]-retrospective.md`
   - Milestone: `production/milestones/[milestone-name]-retrospective.md`

   Create the directory if it does not exist.

9. **Output a summary** to the user with: completion rate, velocity trend
   direction, top blocker, and the most important action item.

### Guidelines

- Be honest and specific. Vague retrospectives ("communication could be
  better") produce vague improvements. Use data and examples.
- Focus on systemic issues, not individual blame.
- Limit action items to 3-5. More than that dilutes focus.
- Every action item must have an owner and a deadline.
- Check whether previous action items were completed. Recurring unaddressed
  items are a process smell.
- If this is a milestone retrospective, also evaluate whether the milestone
  goals were achieved and what that means for the overall project timeline.
