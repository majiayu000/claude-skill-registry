---
name: status
version: 1.0.0
description: "[Project Management] Generate status reports for sprints or projects. Use when creating status reports, checking progress, or summarizing sprint metrics. Triggers on keywords like "status report", "sprint status", "progress", "how are we doing", "what's done", "project status"."
allowed-tools: Read, Write, Grep, Glob, Bash, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Generate a project status report covering progress, blockers, and next steps.

**Workflow:**
1. **Gather** -- Collect data from git, tasks, plans, and recent activity
2. **Analyze** -- Assess progress against goals, identify blockers
3. **Report** -- Write structured status report with metrics

**Key Rules:**
- Include: completed items, in-progress work, blockers, next steps
- Quantify where possible (files changed, tests passing, coverage)
- Save report to plans/reports/ with standard naming

# Status Report

Generate project/sprint status reports with metrics.

## When to Use

- Sprint status needed
- Project progress report
- Stakeholder update

## Quick Reference

### Workflow

1. Read PBIs in scope
2. Check git log for recent commits
3. Find open issues/PRs
4. Calculate metrics
5. Generate report
6. Save to `plans/reports/`

### Metrics

- Completed vs Planned
- Velocity (if sprint)
- Bug count
- Blocker count

### Report Structure

```markdown
## Status Report - {Date}

### Sprint: {Name} | Day {N}/{Total}

#### Progress

| Metric | Planned | Actual | Status |
| ------ | ------- | ------ | ------ |

#### Completed

| Item | Owner |

#### In Progress

| Item | Status | Blocker |

#### Blockers

| Blocker | Impact | Action |

#### Risks

| Risk | Probability | Impact |
```

### Output

- **Path:** `plans/reports/{YYMMDD}-status-{scope}.md`

### Related

- **Role Skill:** `project-manager`
- **Command:** `/status`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
