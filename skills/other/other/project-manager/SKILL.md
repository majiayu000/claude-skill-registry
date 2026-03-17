---
name: project-manager
version: 1.1.0
description: '[Project Management] Generate project status reports, track dependencies, manage risk registers, and facilitate team sync meetings. Triggers: project status, sprint tracking, risk assessment, project timeline, blocker report, meeting agenda.'
allowed-tools: Read, Write, Edit, Grep, Glob, TaskCreate, WebSearch
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Generate project status reports, track dependencies, manage risks, and facilitate team sync meetings.

**Workflow:**

1. **Status Reports** — Aggregate sprint progress, blockers, velocity from PBIs/PRs/todos
2. **Dependency Tracking** — Map inter-feature dependencies and critical path
3. **Risk Management** — Score probability x impact (1-9), define mitigations
4. **Team Sync** — Generate meeting agendas, track action items and decisions

**Key Rules:**

- MUST READ `references/report-templates.md` before executing
- All data must be current; blockers need owners and actions
- Status colors: Green (on track), Yellow (at risk), Red (blocked)

# Project Manager Assistant

Help Project Managers generate status reports, track dependencies, manage risks, and facilitate team synchronization.

---

## Prerequisites

**⚠️ MUST READ** `references/report-templates.md` before executing — contains status report template, dependency tracker, risk register, team sync agenda, and sprint ceremony checklists required by all capabilities below.

## Core Capabilities

| Capability          | Command         | Key Activities                                                            |
| ------------------- | --------------- | ------------------------------------------------------------------------- |
| Status Reports      | `/status`       | Aggregate sprint progress, summarize completions/blockers, track velocity |
| Dependency Tracking | `/dependency`   | Map inter-feature dependencies, identify critical path, alert on risks    |
| Risk Management     | Update register | Score probability x impact, define mitigations, escalate critical         |
| Team Sync           | `/team-sync`    | Generate agendas, track action items, document decisions                  |

---

## Status Report Generation

**Command:** `/status`

Generate from:

1. PBIs in `team-artifacts/pbis/` with `in_progress` status
2. Recent PRs and commits
3. Open blockers in todo lists
4. Quality gate reports

**⚠️ MUST READ:** `references/report-templates.md` for full status report template.

---

## Dependency Tracking

**Command:** `/dependency`

Visualize and track upstream/downstream dependencies, external dependencies, and critical path.

**⚠️ MUST READ:** `references/report-templates.md` for dependency matrix and tracker template.

---

## Risk Management

Maintain risk register with probability x impact scoring (1-9 scale).

| Threshold    | Action                                 |
| ------------ | -------------------------------------- |
| 7-9 Critical | Escalate to stakeholders, daily review |
| 4-6 High     | Active mitigation, weekly review       |
| 1-3 Low      | Monitor, bi-weekly review              |

**⚠️ MUST READ:** `references/report-templates.md` for risk register template and scoring matrix.

---

## Team Sync Facilitation

**Command:** `/team-sync`

Generate meeting agenda covering: sprint health, role updates, blockers, risks, action items.

**⚠️ MUST READ:** `references/report-templates.md` for agenda template and sprint ceremonies checklists.

---

## Output Conventions

### File Naming

```
{YYMMDD}-pm-status-sprint-{n}.md
{YYMMDD}-pm-dependency-{feature}.md
{YYMMDD}-pm-risk-register.md
{YYMMDD}-pm-sync-{date}.md
```

### Status Colors

- Green: On Track
- Yellow: At Risk
- Red: Blocked/Critical

---

## Integration Points

| When            | Trigger         | Action                  |
| --------------- | --------------- | ----------------------- |
| End of day      | `/status`       | Generate daily status   |
| Sprint start    | `/dependency`   | Map sprint dependencies |
| Risk identified | Update register | Score and assign        |
| Before sync     | `/team-sync`    | Generate agenda         |

---

## Quality Checklist

- [ ] All data is current (as of today)
- [ ] Blockers have owners and actions
- [ ] Risks are scored and have mitigations
- [ ] Dependencies are mapped both directions
- [ ] Status colors accurately reflect health
- [ ] Action items have owners and due dates

## Related

- `product-owner`
- `planning`

## References

| File                             | Contents                                                                                       |
| -------------------------------- | ---------------------------------------------------------------------------------------------- |
| `references/report-templates.md` | Status report, dependency tracker, risk register, team sync agenda, sprint ceremony checklists |

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
