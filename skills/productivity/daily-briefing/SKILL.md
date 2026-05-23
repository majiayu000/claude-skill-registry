---
name: daily-briefing
description: |
  Generate daily briefing with priorities, progress, and alerts. Used as part of session-start or when user asks "what's on today". Internal skill supporting the marvin skill.
license: MIT
compatibility: marvin
metadata:
  marvin-category: session
  user-invocable: false
  slash-command: null
  model: default
  proactive: false
---

# Daily Briefing Skill

Generate comprehensive daily briefing with priorities, progress, and alerts.

## When to Use

- Part of `marvin` skill (session start)
- User asks "what's on today" or "daily briefing"
- Morning check-in requests

## Process

### Step 1: Calendar Overview (if available)
- Today's events with times
- Tomorrow's events (preview)
- Next 7 days: any important deadlines

### Step 2: Task Status
From `state/current.md`:
- Active priorities
- Overdue items
- Due today
- Open threads needing attention

### Step 3: Progress Check
For current month from `state/goals.md`:
- Progress against each goal
- Days remaining in month

If behind pace, flag it.

### Step 4: Open Threads
From `state/current.md`:
- Anything waiting on follow-up
- Stale threads (no update > 5 days)

### Step 5: Proactive Suggestions
Based on patterns:
- "You haven't made progress on {goal} this week"
- "Deadline for {item} is in 3 days"
- "Monthly review coming up — want to schedule?"

## Output Format

Keep concise. Structure as:
```
## {Day}, {Date}

**Today**: {summary}

**Alerts**:
- {any urgent items}

**Progress**: {goal status summary}

**Focus**: {top 1-2 priorities}
```

Offer to expand any section on request.

---

*Skill created: 2026-01-22*
