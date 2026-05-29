---
name: team-sync
description: Generate meeting agendas and facilitate team coordination. Use when preparing standups, sprint reviews, or team meetings. Triggers on keywords like "standup", "team sync", "meeting agenda", "daily", "sprint review".
allowed-tools: Read, Write, Grep, Glob, TodoWrite
---

# Team Sync

Generate meeting agendas and action item tracking.

## When to Use
- Daily standup preparation
- Weekly team sync
- Sprint review/planning
- Retrospective facilitation

## Quick Reference

### Meeting Types

#### Daily Standup
- What I did yesterday
- What I'll do today
- Any blockers

#### Weekly Sync
- Progress highlights
- Cross-team dependencies
- Upcoming milestones

#### Sprint Review
- Demo completed items
- Stakeholder feedback
- Velocity review

#### Sprint Planning
- Capacity check
- Backlog prioritization
- Sprint goal setting

### Workflow
1. Identify meeting type
2. Gather relevant data (PBIs, blockers)
3. Generate agenda template
4. Populate with current data
5. Output agenda

### Agenda Template
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

### Related
- **Role Skill:** `project-manager`
- **Command:** `/team-sync`

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
