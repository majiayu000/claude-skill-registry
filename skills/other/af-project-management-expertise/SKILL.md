---
name: af-project-management-expertise
description: Use when planning weekly work cycles, managing team capacity, prioritizing backlogs, or scheduling issues into Linear cycles. Covers capacity budgets, prioritization rules, cycle management, and estimation quality checks.

# AgentFlow documentation fields
title: Project Management Expertise
created: 2026-02-08
updated: 2026-02-08
last_checked: 2026-02-08
tags: [skill, expertise, project-management, planning, cycles, capacity]
parent: ../README.md
related:
  - ../af-estimation-expertise/SKILL.md
  - ../af-work-management-expertise/SKILL.md
  - ../af-linear-api-expertise/SKILL.md
  - ../af-discovery-process/SKILL.md
  - ../af-refinement-process/SKILL.md
---

# Project Management Expertise

## When to Use This Skill

Load this skill when you need to:
- Plan a weekly work cycle for a team
- Prioritize backlog issues for scheduling
- Manage team capacity budgets
- Assign issues to Linear cycles
- Review estimation quality across a backlog

**Common triggers:**
- `/pm:plan-week` command invoked
- PM asks "what should we work on this week?"
- Sprint/cycle planning sessions
- Backlog grooming and prioritization

## Quick Reference

### Capacity Constants

| Parameter | Value |
|-----------|-------|
| Productive hours per day | 6 |
| Hours per story point | 3 |
| Story points per week per team | Project-specific (see project CLAUDE.md) |

**Note:** Capacity varies by team size and composition. Define your team's weekly capacity in the project's CLAUDE.md (e.g., `Team capacity: 50 pts/week`).

### Issue Status Types

| Status | Type | Planning Relevance |
|--------|------|-------------------|
| Discovered | backlog | Lowest priority for scheduling; may need Discovery Estimate |
| Approved | unstarted | Highest priority for scheduling; should have Refined Estimate from Refinement phase |

### Prioritization Order

Issues are scheduled in this order:
1. **Approved** issues (approved and estimated, ready to start)
2. **Discovered** issues with estimates (backlog items with Discovery Estimates)
3. **Discovered** issues without estimates (need estimation before scheduling)

Within each group, sort by:
1. Priority field (1=Urgent, 2=High, 3=Normal, 4=Low)
2. Estimate size (smaller issues first — complete more work)
3. Age (older issues first — prevent stagnation)

---

## Core Concepts

### Per-Team Planning

The PM agent plans for **one team at a time**. Each team has its own:
- Capacity budget (defined per project, see CLAUDE.md)
- Cycle (weekly time-box)
- Backlog of issues in Discovered/Approved states

The agent is scoped to the team it's installed in. If installed in the Agentview team, it only plans for Agentview issues.


### Cycles (Not Milestones)

Linear cycles are the scheduling container:
- **Team-scoped** — each team manages its own cycles
- **Time-boxed** — weekly or biweekly duration
- **Auto-rollover** — incomplete work rolls to the next cycle automatically
- **No auto-advance** — adding an issue to a cycle does NOT change its status
- **Independent of status** — cycle assignment and issue status are separate concerns

### Estimation Quality Tiers

The estimation skill (`af-estimation-expertise`) defines two tiers:

| Tier | When | Confidence | Tagged As |
|------|------|-----------|-----------|
| Discovery Estimate | During Discovery phase | Low/Medium | `[Discovery Estimate]` in Linear comment |
| Refined Estimate | During Refinement phase | Medium/High | `[Refined Estimate]` in Linear comment |

**For planning purposes:**
- Issues with Refined Estimates → schedule with high confidence
- Issues with Discovery Estimates → schedule with medium confidence (pad 20%)
- Issues with no estimate → estimate first using `af-estimation-expertise`, then schedule

### Checking Estimation Status

To determine if an issue has been estimated and at what quality:

1. **Has estimate?** Check `estimate` field on the Linear issue (non-null = has story points)
2. **What quality?** Search the issue's comments for `[Discovery Estimate]` or `[Refined Estimate]` tags
3. **No estimate?** Load `af-estimation-expertise` and run a Discovery Estimate (quick heuristic)

---

## Linear Hierarchy Model

### The Hierarchy

AgentFlow uses Linear constructs as follows:

| Linear Construct | AgentFlow Meaning | Created When | Notes |
|------------------|-------------------|--------------|-------|
| **Team** | Product/organisational boundary | Setup | Your biggest unit of organisation |
| **Project** | Optional — only for "super-epics" | As needed | Bundles of milestones; rarely used |
| **Milestone** | Delivery goal (replaces "Epic" concept) | Discovery or Planning | Groups issues that ship together (e.g., "Auth MVP") |
| **Issue (Parent)** | Deliverable capability | Discovery | Gets branch, PR, implementation |
| **Sub-issue** | Specification artifact | Refinement | [Behaviour] or [UX] work; own cycle/assignee |
| **Cycle** | Weekly time-box | Ongoing | For both refinement and delivery |

### Key Insight: Sub-issues Are Full Issues

Linear sub-issues have their own:
- Assignee (QA for Behaviour, UX for Storybook)
- Cycle (can differ from parent)
- Estimate (part of parent total, not additional)
- Status (tracked independently)

This enables scheduling spec work into refinement cycles before the parent's delivery cycle.

### Milestone Usage

Milestones serve the role that "Epics" previously filled — grouping related issues toward a delivery goal:

- **"Auth MVP"** — Login + Registration + Session Management
- **"v1.0 Release"** — Core feature set for first release
- **"Q2 Delivery"** — Time-boxed quarterly goal

**When to create Milestones:**
- During Discovery (for capability areas)
- During Planning (for release groupings)

**Milestones vs Projects:**
- **Milestones** — For most delivery goals (recommended)
- **Projects** — Only for "super-epics" spanning multiple milestones (rare)

---

## Scheduling Spec Work (Refinement Cycles)

### The Pattern

Specification sub-issues ([Behaviour], [UX]) should be scheduled into cycles **before** their parent's delivery cycle.

**Example:**
- Cycle 12 (refinement): [Behaviour] and [UX] sub-issues for Login Flow
- Cycle 13 (delivery): Login Flow parent issue

This ensures specs are complete and approved before implementation begins.

### Capacity Planning with Mixed Work

When planning a cycle, include both:
- **Delivery work** — Parent issues in Approved status
- **Refinement work** — Spec sub-issues in Approved status

Both consume capacity. A typical split:
- 60-70% delivery work
- 20-30% refinement work
- 10% buffer for unplanned work

### Checking Readiness for Delivery

Before scheduling a parent issue into a delivery cycle:
1. Check that its [Behaviour] sub-issue is Done
2. Check that its [UX] sub-issue is Done
3. If specs aren't complete, schedule the sub-issues first

**Issues ready for delivery:** Status = Approved AND all sub-issues have status = Done

---

## Standing Housekeeping Issues

### The Pattern

Each cycle should have a standing "Housekeeping" parent issue for batching trivial work.

**Create at cycle start:**
```
Title: Housekeeping — Week of {date}
Estimate: 2-3 points (collective)
Cycle: Current cycle
```

**During the cycle:** Add trivial items as sub-issues (titles only, no individual estimates):
- Typo fixes
- Config tweaks
- Unused import removal
- Small copy changes

**Benefits:**
- Trivial items don't inflate velocity individually
- Aggregate effort is tracked
- Nothing falls through the cracks

---

## Workflow: Plan a Weekly Cycle

### Step 1: Gather the Backlog

Query all schedulable issues for the team:

```
Using Linear MCP tools:
1. list_issues(team: "TeamName", state: "Approved")
2. list_issues(team: "TeamName", state: "Discovered")
```

For each issue, note:
- `identifier` (e.g., AGV-34)
- `title`
- `estimate` (story points, may be null)
- `priority` (1-4)
- `createdAt` (for age sorting)
- `labels` (for context)

### Step 2: Assess Estimation Coverage

Group issues by estimation status:

| Group | Criteria | Action |
|-------|----------|--------|
| **Ready** | Has estimate + Refined Estimate comment | Schedule directly |
| **Usable** | Has estimate + Discovery Estimate comment | Schedule with 20% padding |
| **Needs estimation** | No estimate (null) | Estimate using af-estimation-expertise heuristics |

For unestimated issues:
1. Load `af-estimation-expertise`
2. Use the **Estimation Heuristics** section (by change type) for quick estimates
3. Set story points on the issue
4. Post a `[Discovery Estimate]` comment

### Step 3: Prioritize and Fill the Cycle

With the team's weekly capacity budget (defined in project CLAUDE.md):

1. **Start with Approved issues** — these are committed work
2. **Add Discovered issues with estimates** — by priority, then size, then age
3. **Add Discovered issues with estimates** — if capacity remains
4. **Include refinement work** — spec sub-issues ([Behaviour], [UX]) consume capacity too
5. **Leave buffer** — aim for 80-90% of capacity (uncertainty margin)

**Capacity rules:**
- Never exceed the team's weekly capacity in a single cycle
- Leave 10-20% buffer for unplanned work
- If a single issue exceeds remaining capacity, skip it (don't split)
- Flag issues over 21 points — suggest decomposition

### Step 4: Present the Plan

Before making any changes, present the proposed cycle to the human:

```markdown
## Weekly Cycle Plan: [Team] — Week of [Date]

**Capacity:** 50 points | **Planned:** X points | **Buffer:** Y points

### Scheduled Issues (X points)

| # | Issue | Title | Points | Priority | Est. Quality |
|---|-------|-------|--------|----------|-------------|
| 1 | AGV-XX | Title | 5 | High | Refined |
| 2 | AGV-YY | Title | 3 | Normal | Discovery |
| ... | | | | | |

### Newly Estimated (Z issues)

| Issue | Title | Points | Basis |
|-------|-------|--------|-------|
| AGV-ZZ | Title | 3 | Heuristic: new UI component |

### Not Scheduled (Remaining Backlog)

| Issue | Title | Points | Reason |
|-------|-------|--------|--------|
| AGV-AA | Title | 21 | Exceeds remaining capacity |
| AGV-BB | Title | null | Needs detailed estimation |

### Recommendations
- [Any issues that should be decomposed]
- [Any estimation quality concerns]
- [Suggested focus areas]
```

### Step 5: Execute on Approval

After human approves:

1. **Get or create the current cycle** for the team:
   ```
   list_cycles(teamId: "team-uuid", type: "current")
   ```
   If no current cycle exists, note this and inform the human.

2. **Assign issues to the cycle:**
   ```
   update_issue(id: "AGV-XX", cycle: "cycle-name-or-id")
   ```

3. **Set newly estimated story points:**
   ```
   update_issue(id: "AGV-ZZ", estimate: 3)
   ```

4. **Post estimation comments** for any issues that were estimated during planning.

5. **Post summary to Zulip** with the final plan.

---

## Workflow: Review Estimation Quality

When reviewing a backlog for estimation health:

### Metrics to Report

| Metric | Healthy | Warning | Action |
|--------|---------|---------|--------|
| % issues with estimates | >80% | <50% | Batch estimate unestimated issues |
| % with Refined Estimates | >60% | <30% | Move issues through Refinement |
| Avg points per issue | 3-8 | >13 | Suggest decomposition |
| Issues over 21 points | 0 | >2 | Flag for decomposition |

### Report Format

```markdown
## Estimation Health: [Team]

**Total backlog:** X issues
**Estimated:** Y (Z%)
**Refined:** A (B% of estimated)
**Avg points:** C

### Issues Needing Attention
- [AGV-XX] No estimate — needs at least Discovery Estimate
- [AGV-YY] 34 points — should be decomposed into sub-issues
- [AGV-ZZ] Discovery Estimate only, in Approved status — needs Refined Estimate
```

---

## Integration Points

**Estimation skill** (`af-estimation-expertise`):
- Load for any estimation work (Discovery or Refined)
- Use heuristics table for quick batch estimates
- Follow structured output format for Linear comments

**Work management** (`af-work-management-expertise`):
- Linear status flow: Discovered → Refining → Approved → In Progress
- Issue updates via `linearis` CLI or Linear MCP tools
- Current-task.md for tracking planning sessions

**Process skills:**
- `af-discovery-process` — Features should get Discovery Estimates during Phase 4
- `af-refinement-process` — Features should get Refined Estimates before approval
- `af-delivery-process` — Story points must be set before starting implementation

**Linear MCP tools:**
- `list_issues` — Query backlog by team and state
- `list_cycles` — Get current/next cycles
- `update_issue` — Assign to cycle, set estimates
- `create_comment` — Post estimation breakdowns

---

## Duplicate and Overlap Detection

Before scheduling, scan the backlog for duplicate or overlapping issues:

### When to Check

- During cycle planning (Step 2.5 — after gathering backlog, before scheduling)
- After batch issue creation (new issues often overlap existing ones)
- When the backlog exceeds 50 issues (overlap probability increases with size)

### Detection Method

1. **Theme clustering.** Group issues by keywords (e.g., "cloud", "migration", "health", "costs", "activity"). Any theme with 3+ issues warrants review.
2. **Parent-child overlap.** Check if Epic/parent issues carry their own estimates when children already carry the work — this causes double-counting.
3. **Entity vs. deep link overlap.** An entity issue (e.g., "Environment Entity") may subsume a smaller issue (e.g., "Deep Links: Environments"). Make the smaller one a sub-issue or mark as duplicate.
4. **API + UI refactor pairs.** Verify that paired refactor issues (API Refactor + UI Rethink) don't overlap with a broader parent issue covering the same scope.
5. **Description cross-reference.** If an issue's description says "likely overlaps with X" or "see also Y", investigate immediately.

### Resolution Actions

| Finding | Action |
|---------|--------|
| True duplicate (identical scope) | Mark as `Duplicate` of the richer issue |
| Parent carries estimate but children do too | Zero the parent's estimate |
| Smaller issue subsumed by larger | Make it a sub-issue of the larger |
| Overlapping scope but distinct work | Add `relatedTo` link, note overlap in descriptions |

### Impact on Totals

After resolving duplicates, recalculate project totals. Report the delta:
- "Removed X pts of double-counting (was Y, now Z)"

---

## Cycle Lifecycle Management

### Verify Cycles Exist Before Assigning

Before assigning issues to cycles, always verify the target cycle exists in Linear:

```
list_cycles(teamId: "team-uuid")
```

If a cycle doesn't exist, **create it first** using the Linear GraphQL API:

```graphql
mutation {
  cycleCreate(input: {
    teamId: "team-uuid",
    startsAt: "YYYY-MM-DD",
    endsAt: "YYYY-MM-DD"
  }) {
    cycle { id number }
  }
}
```

**Never "plan" cycles conceptually without creating them in Linear.** Cycle assignments will silently fail if the cycle doesn't exist, and issues will appear unscheduled despite being "planned."

### Cycle Naming Convention

Cycles are numbered sequentially per team. When creating future cycles, continue the sequence from the last existing cycle.

---

## Common Pitfalls

1. **Over-scheduling.** Don't fill 100% of capacity. Leave 5-10 points for unplanned work and interruptions.
2. **Ignoring estimation quality.** A Discovery Estimate for a Discovered issue is fine. A Discovery Estimate for an Approved issue means Refinement didn't complete properly.
3. **Scheduling unestimated work.** Never add an unestimated issue to a cycle — estimate it first, even if just a heuristic.
4. **Ignoring dependencies.** Check parent/child relationships. Don't schedule a sub-issue if its parent isn't ready.
5. **Planning across teams.** Each team has its own capacity. Don't mix team budgets.
6. **Double-counting Epic parents.** If an issue has the "Epic" label and its children carry estimates, the parent should have estimate = 0. Otherwise totals are inflated.
7. **Forgetting to create cycles.** Always verify cycles exist in Linear before assigning issues. Conceptual planning without cycle creation leads to silent failures.
8. **Missing delivery by-products.** Issues created during delivery (follow-on work, "what's left" breakdowns) bypass the estimation workflow. Run an estimation sweep after each delivery cycle.

---

**Remember:**
1. Capacity is project-specific — check project CLAUDE.md for the team's weekly budget
2. Plan for one team at a time — the team the agent is installed in
3. Prioritize: Approved > Discovered
4. Always present the plan before executing
5. Leave capacity buffer for unplanned work (10-20%)
6. Estimate unestimated issues before scheduling them
7. Schedule spec sub-issues ([Behaviour], [UX]) into refinement cycles before parent delivery cycles
8. Create a standing Housekeeping issue each cycle for trivial work
9. Scan for duplicates and overlaps before finalizing cycle plans
10. Verify cycles exist in Linear before assigning issues to them
