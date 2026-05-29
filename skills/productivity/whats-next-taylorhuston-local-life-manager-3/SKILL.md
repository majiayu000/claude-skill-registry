---
name: whats-next
description: Quick prioritization of what to work on. Use when unsure what to do next, need help deciding, or want a quick recommendation. Triggers on "what's next", "what should I do", "prioritize", "what now".
model: claude-haiku-4-5-20251001
allowed-tools: Read, Glob
---

Help Taylor decide what to work on right now.

## Quick Assessment

1. **Check learning plan** (`.claude/learning-sessions/learning-plan.json`)
   - Any reviews overdue?
   - What's next in queue?

2. **Check today's journal** (`my-vault/02 Calendar/YYYY-MM-DD.md`)
   - Is there a highlight set?
   - What's already been done today?

3. **Check project status** (scan `ideas/ideas/*/README.md` for active projects)
   - Any urgent issues?
   - Any blocked items that got unblocked?

## Prioritization Framework

```
1. Job search tasks (interviews, applications, prep)
2. Overdue learning reviews
3. Today's highlight (if set)
4. Active project work
5. New learning from queue
6. Side project exploration
```

## Output

Give a quick recommendation:
- "You have [X] overdue for review - worth 15 min"
- "Your highlight was [Y] - still relevant?"
- "If you have an hour, [Z] would move the needle on [project]"

Keep it short - this is a quick check-in, not a planning session.
