---
name: context
description: |
  Context window management. Use when:
  - User asks about "context window", "context usage", "context limit"
  - User mentions "running out of context", "context full"
  - User wants to "compact", "clear context", "optimize context"
  - Context is getting full and needs management
---

# Context Window Management

Monitor and manage Claude Code context window usage.

## Check Context Usage

Run `/context` in Claude Code to see current usage.

## Context Thresholds

Thresholds scale with your context window size:

### Default Context (~200K tokens)
| Level | Usage | Action |
|-------|-------|--------|
| Notice | 70% (~140K) | Consider handoff at next stopping point |
| Warning | 80% (~160K) | Create handoff, prepare to compact |
| Critical | 90% (~180K) | Create handoff NOW, then compact |

## Managing Context

### Create Handoff Before Compacting
```
/create-handoff
```

This saves:
- Current task state
- Key decisions made
- Files modified
- Next steps

### Compact Context
```
/compact
```

Reduces context by summarizing earlier conversation.

### Resume After Compact
```
/resume-handoff
```

Restores context from handoff file.

## Tips for Reducing Context

1. **Use `context: fork`** - Skills that fork don't bloat main context
2. **Delegate exploration** - Let agents handle research
3. **Clean summaries** - Agents return summaries, not raw output
4. **Avoid large file reads** - Use TLDR for token-efficient analysis

## When Context is Full

1. **Don't panic** - Your work isn't lost
2. **Create handoff** - Save current state
3. **Compact** - Let Claude summarize
4. **Resume** - Pick up where you left off

## Automatic Protection

The setup includes:
- Warning at 70%, 80%, 90% thresholds
- Auto-handoff before compaction (PreCompact hook)
- Session start recalls relevant learnings

## Output

Report:
- **Current usage**: X% of context
- **Recommendation**: Action to take
- **Next steps**: What to do
