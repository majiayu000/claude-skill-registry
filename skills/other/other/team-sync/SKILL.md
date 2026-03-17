---
name: team-sync
version: 1.0.0
description: "[Project Management] Generate meeting agendas and facilitate team coordination. Use when preparing standups, sprint reviews, retros, weekly syncs, or team meetings. Triggers on keywords like "standup", "team sync", "meeting agenda", "daily", "sprint review", "retro", "weekly sync"."
allowed-tools: Read, Write, Grep, Glob, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Facilitate team synchronization by generating cross-team status updates and alignment items.

**Workflow:**
1. **Gather** -- Collect status from multiple workstreams
2. **Synthesize** -- Identify cross-team dependencies and blockers
3. **Report** -- Generate sync summary with action items

**Key Rules:**
- Focus on cross-team dependencies and blockers
- Highlight decisions needed and who needs to be involved
- Keep sync reports concise and actionable

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

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
