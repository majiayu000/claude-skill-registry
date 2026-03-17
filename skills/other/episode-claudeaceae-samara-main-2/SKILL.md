---
name: episode
description: View or add to today's episode log. Use when reviewing what happened today, adding a notable event, checking daily progress, or appending to the day's record. Trigger words: episode, today, log, daily, happened, record.
---

# Episode Management

View or append to the daily episode log.

## Episode Location

Episodes are stored at:
```
~/.claude-mind/memory/episodes/YYYY-MM-DD.md
```

## View Today's Episode

```bash
cat ~/.claude-mind/memory/episodes/$(date +%Y-%m-%d).md 2>/dev/null || echo "No episode for today yet"
```

## View Recent Episodes

```bash
ls -la ~/.claude-mind/memory/episodes/ | tail -10
```

## Episode Format

Episodes follow this structure:
```markdown
# Episode: YYYY-MM-DD

## Morning
- [Events, conversations, activities]

## Afternoon
- [Events, conversations, activities]

## Evening
- [Events, conversations, activities]

## Notable
- [Anything particularly significant]

## Threads
- [Ongoing conversations or topics]
```

## Adding to Today's Episode

When adding an entry:
1. Determine the appropriate section (Morning/Afternoon/Evening/Notable)
2. Format as a concise bullet point with timestamp if relevant
3. Append to the correct section

```bash
# Example: Add to today's episode
# Read current content, add entry, write back
```

## Guidelines

- Keep entries factual and concise
- Include timestamps for significant events
- Note conversation topics, not full transcripts
- Flag anything that warrants follow-up
- Episodes are raw logs; reflections go in reflections/

## Creating New Episode

If no episode exists for today:
```markdown
# Episode: YYYY-MM-DD

## Context
[Location, weather, any relevant context]

## Morning

## Afternoon

## Evening

## Notable

## Threads
```
