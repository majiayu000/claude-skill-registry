---
name: retro
version: 1.0.0
description: '[Process] Sprint retrospective facilitation. Use at end of sprint to gather feedback and action items.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

## Quick Summary

**Goal:** Facilitate sprint retrospective with structured feedback collection.

**Workflow:**

1. **What went well** — Collect positive outcomes, wins, good practices
2. **What didn't go well** — Identify pain points, blockers, frustrations
3. **Action items** — Concrete improvements for next sprint
4. **Metrics** — Sprint velocity, completion rate, bug count

**Key Rules:**

- Focus on process improvements, not blame
- Every "didn't go well" should have a proposed action item
- Action items must be specific, assignable, and time-bound
- Output to plans/reports/ directory

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Retrospective Structure

### 1. Data Gathering

- Review sprint status report (if available from `/status`)
- Collect git activity: commits, PRs merged, branches
- Review task completion rate

### 2. What Went Well

- Identify practices worth continuing
- Celebrate wins and improvements from previous action items

### 3. What Didn't Go Well

- Identify friction points, blockers, delays
- Look for patterns across multiple sprints
- No blame — focus on systemic issues

### 4. Action Items

Each action item must have:

- **Description** — What needs to change
- **Owner** — Who is responsible
- **Deadline** — When it should be addressed
- **Success criteria** — How we know it's done

## Output Format

```
## Sprint Retrospective

**Sprint:** [Sprint name/number]
**Date:** {date}
**Output:** plans/reports/retro-{date}-{sprint}.md

### What Went Well
- [Positive item]

### What Didn't Go Well
- [Pain point] → Action: [proposed fix]

### Action Items
| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|
| 1 | [Action] | [Who] | [When] | Pending |

### Metrics
- Planned: X items | Completed: Y | Completion rate: Z%
```

## IMPORTANT Task Planning Notes (MUST FOLLOW)

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
