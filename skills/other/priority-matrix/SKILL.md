---
name: priority-matrix
description: Applies Eisenhower matrix (urgent/important) to prioritize tasks. Use when prioritizing, reviewing tasks, or deciding what to work on next.
---

# Eisenhower Priority Matrix

Categorize tasks by urgency and importance.

## The Four Quadrants

```
                    URGENT              NOT URGENT
             ┌─────────────────┬─────────────────┐
             │                 │                 │
  IMPORTANT  │   DO FIRST      │   SCHEDULE      │
             │   (Q1)          │   (Q2)          │
             │                 │                 │
             ├─────────────────┼─────────────────┤
             │                 │                 │
NOT IMPORTANT│   DELEGATE      │   ELIMINATE     │
             │   (Q3)          │   (Q4)          │
             │                 │                 │
             └─────────────────┴─────────────────┘
```

## Quadrant Definitions

### Q1: Do First (Urgent + Important)
**Priority:** `!high`
**Action:** Do immediately, add to today.md

Signs of Q1 tasks:
- Deadlines today or tomorrow
- Blocking other people
- Production issues
- Client-facing problems
- Health/safety concerns

### Q2: Schedule (Not Urgent + Important)
**Priority:** `!medium`
**Action:** Add to backlog, schedule specific time

Signs of Q2 tasks:
- Long-term goals
- Skill development
- Relationship building
- Strategic planning
- Prevention and preparation

### Q3: Delegate (Urgent + Not Important)
**Priority:** `!low`
**Action:** Can someone else do this?

Signs of Q3 tasks:
- Interruptions
- Some meetings
- Some emails/messages
- Other people's priorities

### Q4: Eliminate (Not Urgent + Not Important)
**Priority:** Consider removing
**Action:** Delete or move to someday.md

Signs of Q4 tasks:
- Time wasters
- Pleasant but unproductive
- Busy work
- Outdated tasks

## Decision Tree

```
Is this task aligned with my goals?
├── No → ELIMINATE or SOMEDAY
└── Yes → Does it have a hard deadline within 48h?
    ├── Yes → Is it blocking others or high-impact?
    │   ├── Yes → DO FIRST (!high)
    │   └── No → DELEGATE if possible, else DO FIRST
    └── No → Is it important for long-term success?
        ├── Yes → SCHEDULE (!medium)
        └── No → DELEGATE or ELIMINATE (!low)
```

## Application Rules

1. **Daily limit:** Max 3 tasks in "Do First"
2. **Weekly balance:** 60% Q2, 30% Q1, 10% Q3
3. **Review trigger:** If Q1 > 5 tasks, something is wrong
4. **Q2 protection:** Block time for important-not-urgent work

## Reprioritization Triggers

Run `/prioritize` when:
- New urgent task arrives
- Deadline changes
- Blocked on current task
- End of day review
- Weekly review
