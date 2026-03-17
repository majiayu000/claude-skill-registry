---
name: team-team-sync
description: "[Team] Generate meeting agendas and facilitate team coordination. Use when preparing standups, sprint reviews, or team meetings. Triggers on keywords like "standup", "team sync", "meeting agenda", "daily", "sprint review"."
argument-hint: "daily | weekly | sprint-review | sprint-planning"
infer: true
allowed-tools: Read, Write, Grep, Glob, TodoWrite
---

# Team Sync

Generate meeting agendas and action item tracking.

## Summary

**Goal:** Generate structured meeting agendas and track action items for team coordination meetings.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Identify meeting type | Daily standup, weekly sync, sprint review, or sprint planning |
| 2 | Review previous items | Search `plans/reports/` for prior agendas and open action items |
| 3 | Gather current data | Recent git activity, artifacts, PBIs, blockers |
| 4 | Generate agenda | Use type-specific template with current data |
| 5 | Save output | `plans/reports/{YYMMDD}-{meeting-type}.md` |

**Key Principles:**
- Carry forward incomplete action items from previous meetings
- Use meeting-type-specific templates (standup, weekly, sprint review, planning)
- Include sprint metrics (velocity, commitment %) for review meetings

## When to Use
- Daily standup preparation
- Weekly team sync
- Sprint review/planning
- Retrospective facilitation

## Pre-Workflow

### Activate Skills

- Activate `project-manager` skill for meeting facilitation best practices

## Meeting Types

### Daily Standup
- What I did yesterday
- What I'll do today
- Any blockers

### Weekly Sync
- Progress highlights
- Cross-team dependencies
- Upcoming milestones

### Sprint Review
- Demo completed items
- Stakeholder feedback
- Velocity review

### Sprint Planning
- Capacity check
- Backlog prioritization
- Sprint goal setting

## Workflow
1. Identify meeting type
2. Review previous meeting action items (search `plans/reports/` for prior agendas)
3. Gather relevant data (recent git activity, artifacts, PBIs, blockers)
4. Check open blockers and pending handoffs
5. Track completion status of previous action items; carry incomplete items forward
6. Generate agenda template based on meeting type
7. Populate with current data
8. Save output to `plans/reports/{YYMMDD}-{meeting-type}.md`

## Detailed Templates

### Daily Standup Template
```markdown
## Daily Standup - {Date}

### Sprint Progress
- Day {N} of {Total}
- Points: {completed}/{planned}

### Yesterday
- {completed items}

### Today
- {planned items}

### Blockers
- {blockers}
```

### Weekly Sync Template
```markdown
## Weekly Team Sync - {Date}

### Sprint Progress (10 min)

### Cross-Role Updates (15 min)
| Role   | Update |
| ------ | ------ |
| PO     |        |
| BA     |        |
| Dev    |        |
| QA     |        |
| Design |        |

### Risks & Blockers (10 min)

### Action Items (5 min)
```

### Sprint Review Template
```markdown
## Sprint {N} Review - {Date}

### Demo Items
| Feature | Demo By |
| ------- | ------- |
|         |         |

### Sprint Goal: {goal}
- Status: {achieved/partial/not}

### Metrics
- Velocity: {points}
- Commitment: {%}

### Feedback
```

### Generic Agenda Template
```markdown
## {Meeting Type} - {Date}

### Attendees
- {names}

### Agenda
1. {item}

### Discussion Points
- {point}

### Action Items
- [ ] {action} - {owner}

### Next Meeting
{date/time}
```

## Example

```bash
/team-team-sync daily
/team-team-sync sprint-review
/team-team-sync sprint-planning
```

## Related
- **Role Skill:** `project-manager`
- **Command:** `/team-team-sync`

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
