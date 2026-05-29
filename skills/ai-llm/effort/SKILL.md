---
name: effort
description: |
  Dynamic effort level management. Use when:
  - User mentions "think harder", "be thorough", "quick fix", "max effort"
  - Task complexity changes mid-session
  - Need to optimize for speed vs depth
  - User says "slow down", "speed up", "think more"
allowed-tools:
  - Bash
argument-hint: "[low|medium|high|max]"
---

# Effort Level Management

Adjust Claude's adaptive thinking depth based on task complexity.

## Effort Levels

| Level | When to Use | Thinking Behavior |
|-------|-------------|-------------------|
| `low` | Simple edits, formatting, renaming | Minimal -- fast responses |
| `medium` | Standard implementation, exploration | Balanced depth |
| `high` | Complex logic, multi-file changes (DEFAULT) | Deep analysis |
| `max` | Architecture decisions, security reviews, hard bugs | Maximum depth, no constraints |

## Auto-Scaling Recommendations

| Task Type | Recommended Effort |
|-----------|-------------------|
| Security-sensitive code | `max` |
| Architecture decisions | `max` |
| Complex debugging | `max` |
| Standard implementation | `high` |
| File exploration | `medium` |
| Boilerplate generation | `low` |
| Simple renaming/formatting | `low` |

## Setting Effort

Environment variable: `CLAUDE_CODE_EFFORT_LEVEL`
Interactive: `/model` then use arrow keys to adjust

Current effort level: Check `$CLAUDE_CODE_EFFORT_LEVEL`

If the user provided an argument, acknowledge the level change and explain what it means for the current session.
