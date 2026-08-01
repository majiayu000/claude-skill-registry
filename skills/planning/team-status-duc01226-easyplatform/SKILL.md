---
name: team-status
description: Generate project/sprint status reports with metrics.
---

---
name: team-status
description: "[Team] Generate status reports for sprints or projects. Use when creating status reports, checking progress, or summarizing sprint metrics. Triggers on keywords like "status report", "sprint status", "progress", "how are we doing"."
argument-hint: sprint | project | feature-{name}
allowed-tools: Read, Write, Grep, Glob, Bash, TodoWrite
infer: true
---

# Status Report

Generate project/sprint status reports with metrics.

## Pre-Workflow

### Activate Skills

- Activate `project-manager` skill for status reporting and metrics analysis

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

#### Progress Summary
| Metric  | Planned | Actual | Status |
| ------- | ------- | ------ | ------ |
| Stories | X       | Y      | 🟢🟡🔴    |
| Points  | X       | Y      |        |

#### Completed
| Item | Owner |
| ---- | ----- |
|      |       |

#### In Progress
| Item | Status | Blocker |
| ---- | ------ | ------- |
|      |        |         |

#### Blockers
| Blocker | Impact | Action |
| ------- | ------ | ------ |
|         |        |        |

#### Risks
| Risk | Probability | Impact |
| ---- | ----------- | ------ |
|      |             |        |
```

**Status Indicators:** Use 🟢 (on track), 🟡 (at risk), 🔴 (blocked) for visual status.

### Output
- **Path:** `plans/reports/{YYMMDD}-status-{scope}.md`

### Related
- **Role Skill:** `project-manager`
- **Command:** `/team-status`

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
