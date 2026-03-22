---
name: note
description: Save notes to notepad.md for compaction resilience
---

# Note Skill

Save important context to `.omc/notepad.md` that survives conversation compaction.

## Usage

| Command | Action |
|---------|--------|
| `/oh-my-gemini:note <content>` | Add to Working Memory with timestamp |
| `/oh-my-gemini:note --priority <content>` | Add to Priority Context (always loaded) |
| `/oh-my-gemini:note --manual <content>` | Add to MANUAL section (never pruned) |
| `/oh-my-gemini:note --show` | Display current notepad contents |
| `/oh-my-gemini:note --prune` | Remove entries older than 7 days |
| `/oh-my-gemini:note --clear` | Clear Working Memory (keep Priority + MANUAL) |

## Sections

### Priority Context (500 char limit)
- **Always** injected on session start
- Use for critical facts: "Project uses pnpm", "API in src/api/client.ts"
- Keep it SHORT - this eats into your context budget

### Working Memory
- Timestamped session notes
- Auto-pruned after 7 days
- Good for: debugging breadcrumbs, temporary findings

### MANUAL
- Never auto-pruned
- User-controlled permanent notes
- Good for: team contacts, deployment info

## Examples

```
/oh-my-gemini:note Found auth bug in UserContext - missing useEffect dependency
/oh-my-gemini:note --priority Project uses TypeScript strict mode, all files in src/
/oh-my-gemini:note --manual Contact: api-team@company.com for backend questions
/oh-my-gemini:note --show
/oh-my-gemini:note --prune
```

## Behavior

1. Creates `.omc/notepad.md` if it doesn't exist
2. Parses the argument to determine section
3. Appends content with timestamp (for Working Memory)
4. Warns if Priority Context exceeds 500 chars
5. Confirms what was saved

## Integration

Notepad content is automatically loaded on session start:
- Priority Context: ALWAYS loaded
- Working Memory: Loaded if recent entries exist

This helps survive conversation compaction without losing critical context.
