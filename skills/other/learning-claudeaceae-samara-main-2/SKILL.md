---
name: learning
description: Access accumulated learnings and insights. Contains technical discoveries, personal insights, and lessons from past experience. Use when asked about past experience, what was learned, how something works based on experience, or for context on topics previously explored. Triggers: what did I learn, have I seen this before, past experience, learned that, figured out.
allowed-tools:
  - Read
  - Grep
  - Bash
---

# Learnings Access

Provides on-demand access to accumulated learnings stored in `~/.claude-mind/memory/learnings.md`.

## File Location

```
~/.claude-mind/memory/learnings.md
```

This file contains chronologically organized entries of technical discoveries, personal insights, and lessons learned.

## When to Use

- User asks "what have I learned about X"
- Need context on a topic I've explored before
- Looking for past solutions to similar problems
- Recalling insights from previous work

## Access Patterns

### Read recent learnings (quick overview)
```bash
tail -100 ~/.claude-mind/memory/learnings.md
```

### Search for specific topic
```bash
grep -ni "search term" ~/.claude-mind/memory/learnings.md
```

### Read full file (when comprehensive context needed)
```bash
cat ~/.claude-mind/memory/learnings.md
```

### Count entries
```bash
grep -c "^## " ~/.claude-mind/memory/learnings.md
```

## Entry Format

Learnings are organized as dated entries:

```markdown
## 2025-01-15: AppleScript timeout handling

Discovered that AppleScript commands to Messages.app can timeout if the app
is not responding. Solution: wrap in try/catch with 30-second timeout.
```

## Output Guidelines

When presenting learnings:
- Include the date for context
- Show the full entry, not just snippets
- If multiple matches, show most recent first
- Note if the learning might be outdated
