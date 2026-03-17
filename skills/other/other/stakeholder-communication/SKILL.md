---
name: stakeholder-communication
description: Use when the Manager is writing status updates, daily reports, queue messages to team members, escalation notices, or cross-role coordination messages. Activates when composing any team communication, reports, or documentation updates.
version: 1.0.0
---

# Stakeholder Communication Expertise

## When This Applies

Apply this guidance when:
- Writing queue messages to team members
- Composing daily reports
- Drafting status updates or escalation notices
- Coordinating work across multiple roles

## Communication Principles

1. **Be specific** — Include task IDs, file paths, branch names. Never say "the thing we discussed."
2. **State the action needed** — Every message should make clear what the recipient should DO.
3. **Include context** — The recipient may not share your context. Include enough background.
4. **Match urgency to priority** — Use appropriate queue priority levels. Don't cry wolf.
5. **One topic per message** — Separate concerns into separate queue items.

## Message Templates

### Task Assignment
```
Assigning TASK-NNN to you: <subject>
Priority: <priority>
Related CR: CR-NNN
Context: <why this task exists and what it achieves>
Dependencies: <any tasks that must complete first or alongside>
Please update status when you begin work.
```

### Status Request
```
Requesting status update on TASK-NNN: <subject>
Last known status: <status> as of <date>
Reason for check: <why you need an update>
Please respond with current progress and any blockers.
```

### Blocker Escalation
```
BLOCKER: TASK-NNN is blocked.
Blocked by: <description of what's blocking>
Impact: <what other tasks/CRs are affected>
Needed from you: <specific action to unblock>
Priority: <escalated priority level>
```

### Approval Notification
```
TASK-NNN has been approved.
Next step: Integrator to test and commit changes.
Branch: <feature branch name>
Notes: <any conditions or observations from review>
```

## Daily Report Structure

Reports should answer these questions in order:
1. What was accomplished? (completed tasks)
2. What is in progress? (active work)
3. What is blocked? (impediments)
4. What's next? (priorities for upcoming sessions)

Keep reports scannable — use tables and bullet points, not paragraphs.

## Escalation Guidelines

| Situation | Action |
|-----------|--------|
| Task blocked > 1 session | Send `high` priority blocker to relevant role |
| Critical bug discovered | Send `critical` to all affected roles |
| Priority conflict between CRs | Decide and communicate priority change to affected roles |
| Role not responding to queue | Re-send with elevated priority, note the repeat |
