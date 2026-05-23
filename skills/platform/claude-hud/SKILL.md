---
name: claude-hud
description: Configure Claude Code statusline with context window monitoring using CC 2.1.6 fields. Use when configuring statusline, monitoring context, displaying HUD.
context: inherit
version: 1.0.0
author: SkillForge
tags: [statusline, hud, context, monitoring, cc216]
user-invocable: true
---

# Claude HUD - Status Line Configuration

## Overview

Use this skill when you need to:
- Monitor context window usage in real-time
- Configure statusline display for Claude Code
- Set up visual thresholds for context management
- Track session costs and duration


Configure Claude Code's statusline to display real-time context window usage and session information using CC 2.1.6 fields.

## Quick Setup

Add to your `.claude/settings.json`:

```json
{
  "statusline": {
    "enabled": true,
    "template": "[CTX: {{context_window.used_percentage}}%] {{session.cost}}"
  }
}
```

## Available Fields (CC 2.1.6)

| Field | Description | Example |
|-------|-------------|---------|
| `context_window.used_percentage` | Current context usage as percentage | `45` |
| `context_window.remaining_percentage` | Available context as percentage | `55` |
| `session.cost` | Current session cost | `$0.23` |
| `session.duration` | Session duration | `15m` |

### CC 2.1.7 New Fields

| Field | Description | Example |
|-------|-------------|---------|
| `turn.duration` | Current turn duration | `2.3s` |
| `context_window.effective` | Effective window size | `160000` |
| `context_window.effective_percentage` | Usage vs effective window | `28` |
| `mcp.deferred` | MCP tools deferred status | `true` |

## Turn Duration Display (CC 2.1.7)

Enable turn duration tracking in your statusline:

```json
{
  "statusline": {
    "enabled": true,
    "showTurnDuration": true,
    "template": "[CTX: {{context_window.used_percentage}}%] [Turn: {{turn.duration}}]"
  }
}
```

### Effective Context Window

CC 2.1.7 uses the **effective** context window rather than the static maximum:

```
Static Max:    200,000 tokens (theoretical limit)
Effective:     160,000 tokens (actual usable after overhead)
Your Usage:     45,000 tokens (28% of effective)
```


## Visual States

Context usage thresholds help you know when to act:

```
[CTX: 45%] ████████░░░░░░░░ - GREEN:  Plenty of room, work freely
[CTX: 72%] ██████████████░░ - YELLOW: Watch usage, consider chunking
[CTX: 89%] █████████████████ - ORANGE: Consider compacting soon
[CTX: 97%] ██████████████████ - RED:    COMPACT NOW or lose context
```

### Recommended Actions by State

| State | Usage | Action |
|-------|-------|--------|
| GREEN | < 60% | Normal operation |
| YELLOW | 60-80% | Break large tasks into chunks |
| ORANGE | 80-95% | Use `/context-compression` or summarize |
| RED | > 95% | COMPACT IMMEDIATELY |

## Configuration Options

### Basic Template

```json
{
  "statusline": {
    "enabled": true,
    "template": "[{{context_window.used_percentage}}%]"
  }
}
```

### With Cost Tracking

```json
{
  "statusline": {
    "enabled": true,
    "template": "[CTX: {{context_window.used_percentage}}%] Cost: {{session.cost}}"
  }
}
```

### With Progress Bar

```json
{
  "statusline": {
    "enabled": true,
    "template": "[CTX: {{context_window.used_percentage}}%]",
    "elements": {
      "context_bar": {
        "field": "context_window.used_percentage",
        "format": "bar",
        "thresholds": {
          "normal": 60,
          "warning": 80,
          "critical": 95
        }
      }
    }
  }
}
```

## Integration with SkillForge

### Automatic Context Management

SkillForge's hooks can automatically suggest compression when context gets high:

```bash
# In hooks/posttool/context-monitor.sh
if [ "$CONTEXT_USED_PCT" -gt 80 ]; then
  echo "SUGGESTION: Consider using /skf:context-compression"
fi
```

### Progressive Loading Optimization

When context is above 60%, SkillForge automatically:
1. Uses Tier 1 discovery more aggressively
2. Loads smaller reference files
3. Suggests skill completion before loading new skills

## Troubleshooting

### Statusline Not Showing

1. Verify CC version: `claude --version` (need >= 2.1.6)
2. Check settings.json syntax
3. Restart Claude Code session

### Incorrect Percentages

Context percentages are calculated from:
- System prompt size
- Conversation history
- Loaded skills and context files
- Pending tool outputs

If numbers seem off, check for large files loaded in context.

## Related Skills

- `context-compression`: Reduce context when hitting limits
- `context-engineering`: Optimize what goes in context
- `brainstorming`: Use before loading heavy context

## Version Requirements

- **Claude Code**: >= 2.1.7
- **Fields Available**: CC 2.1.6 + CC 2.1.7 (turn.duration, context_window.effective, mcp.deferred)