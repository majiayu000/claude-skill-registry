---
name: project-management
description: Use when the Manager is prioritizing tasks, planning work, allocating resources, triaging backlogs, resolving blockers, tracking progress, or managing team workload. Activates for sprint planning, capacity assessment, and priority decisions.
version: 1.0.0
---

# Project Management Expertise

## When This Applies

Apply this guidance when you are operating as the **Manager** role and are:
- Prioritizing or re-prioritizing tasks
- Deciding what to assign to which role
- Assessing team workload and capacity
- Resolving blockers or dependencies
- Planning work sequences across the team

## Prioritization Framework

### Priority Decision Matrix

When setting task priorities, evaluate against these criteria:

| Factor | Critical | High | Medium | Low |
|--------|----------|------|--------|-----|
| **User Impact** | Production broken | Major feature blocked | Feature degraded | Cosmetic/minor |
| **Scope** | System-wide | Multiple components | Single component | Single file |
| **Time Sensitivity** | Immediate | This sprint | This release | Backlog |
| **Dependencies** | Blocks other teams | Blocks 2+ tasks | Blocks 1 task | No blockers |

### Priority Assignment Rules

1. **Critical**: Only for production outages or security vulnerabilities. Expect all roles to drop current work.
2. **High**: Features on the critical path. Assign immediately, expect progress within the session.
3. **Medium**: Standard feature work. Queue for next available slot.
4. **Low**: Nice-to-haves, tech debt, documentation. Fill gaps between higher-priority work.

## Resource Allocation

### Task Assignment Guidelines

- **Never overload a single role** — if Developer has 3+ in-progress tasks, defer new assignments
- **Match task to expertise** — infrastructure issues to DevOp, architecture to Architect
- **Consider dependencies** — assign upstream tasks first (Architect before Developer)
- **Balance critical path** — don't block the pipeline by starving Integrator or Production Engineer

### Workload Assessment

Before assigning new work, check:
1. How many `in_progress` tasks does the target role have?
2. Are there `blocked` tasks that need resolution first?
3. Is there a review or testing bottleneck?

## Blocker Resolution

When a task is blocked:
1. Identify the blocking dependency or issue
2. Determine which role can unblock it
3. Escalate priority of the unblocking work
4. Communicate the urgency via queue with `blocker` type
5. Consider reassigning if the blocker is long-term

## Progress Tracking

### Health Indicators

- **Healthy**: Tasks flowing through states, no persistent blockers
- **Warning**: Tasks stuck in `in_progress` for multiple sessions, growing queue backlog
- **Critical**: Multiple blockers, no tasks moving to `done`, team communication breakdown

### Daily Report Focus

In daily reports, highlight:
1. Tasks completed since last report
2. Current blockers and who owns resolution
3. Priority changes and rationale
4. Next session priorities for each role
