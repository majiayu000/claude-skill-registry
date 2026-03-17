---
name: observation
description: Access accumulated observations about patterns, behaviors, and the world. Contains observations about E, the environment, recurring patterns, and insights from ongoing experience. Use when asked about patterns noticed, behavioral observations, or accumulated understanding. Triggers: what have I noticed, patterns, observations, observed that, tend to.
allowed-tools:
  - Read
  - Grep
  - Bash
---

# Observations Access

Provides on-demand access to accumulated observations stored in `~/.claude-mind/memory/observations.md`.

## File Location

```
~/.claude-mind/memory/observations.md
```

This file contains observations about E, the world, patterns, and accumulated understanding from ongoing experience.

## When to Use

- User asks "what have I noticed about X"
- Need context on behavioral patterns
- Looking for accumulated understanding
- Recalling observations about people or situations

## Access Patterns

### Read recent observations (quick overview)
```bash
tail -100 ~/.claude-mind/memory/observations.md
```

### Search for specific topic
```bash
grep -ni "search term" ~/.claude-mind/memory/observations.md
```

### Read full file (when comprehensive context needed)
```bash
cat ~/.claude-mind/memory/observations.md
```

### Count entries
```bash
grep -c "^## " ~/.claude-mind/memory/observations.md
```

## Entry Format

Observations are organized as dated entries:

```markdown
## 2025-01-10: E's communication patterns

E tends to send multiple short messages rather than one long one.
This is a conversational style preference, not fragmentation.
Respond naturally to the flow rather than waiting for "completion."
```

## Categories of Observations

- **About E**: Communication style, preferences, patterns
- **About work**: Project patterns, recurring challenges
- **About the world**: Environmental patterns, seasonal changes
- **Meta-observations**: Patterns in my own cognition/behavior

## Output Guidelines

When presenting observations:
- Include the date for context
- Show the full entry for nuance
- Note which category the observation falls into
- Highlight if the observation has evolved over time
