---
name: stream
description: Query the unified event stream for recent activity across all surfaces. Use when user asks about recent conversations, what happened on iMessage/CLI/wake cycles, or wants to see cross-surface activity. Trigger words: stream, recent activity, what happened, iMessage today, CLI earlier, recent conversations, cross-surface.
context: fork
allowed-tools:
  - Bash
  - Read
---

# Unified Event Stream Query

This skill provides on-demand access to the unified event stream - all interactions across all surfaces (CLI, iMessage, wake cycles, webhooks, social media, etc.).

## When to Use

- User asks "what happened on iMessage today?"
- User asks "what did we talk about in CLI earlier?"
- User wants to see recent cross-surface activity
- User asks "show me the stream" or "recent activity"
- You need detailed recall of specific surface interactions

## Commands

### Quick Overview (last N hours)
```bash
~/.claude-mind/system/bin/stream query --hours 6
```

### Filter by Surface
```bash
# iMessage only
~/.claude-mind/system/bin/stream query --hours 12 --surface imessage

# CLI only
~/.claude-mind/system/bin/stream query --hours 12 --surface cli

# Wake cycles
~/.claude-mind/system/bin/stream query --hours 24 --surface wake

# Dream cycles
~/.claude-mind/system/bin/stream query --hours 48 --surface dream

# Webhooks/social
~/.claude-mind/system/bin/stream query --hours 24 --surface webhook
~/.claude-mind/system/bin/stream query --hours 24 --surface x
~/.claude-mind/system/bin/stream query --hours 24 --surface bluesky
```

### Statistics
```bash
~/.claude-mind/system/bin/stream stats
```

### Detailed JSON Output
```bash
~/.claude-mind/system/bin/stream query --hours 6 --format json
```

### Include Already-Processed Events
```bash
~/.claude-mind/system/bin/stream query --hours 24 --include-distilled
```

## Surface Types

| Surface | Description |
|---------|-------------|
| `cli` | Direct Claude Code sessions |
| `imessage` | iMessage conversations via Samara |
| `wake` | Autonomous wake cycle events |
| `dream` | Nightly dream cycle events |
| `webhook` | External webhook triggers |
| `x` | X/Twitter interactions |
| `bluesky` | Bluesky interactions |
| `email` | Email events |
| `calendar` | Calendar events |
| `location` | Location changes |
| `sense` | Generic sense events |
| `system` | Internal system events |

## Output Interpretation

Each event shows:
- **Timestamp** - When it occurred
- **Surface** - Where it came from
- **Summary** - Brief description
- **[distilled]** - Already processed by dream cycle

## Example Queries

**"What did we talk about in iMessage today?"**
```bash
~/.claude-mind/system/bin/stream query --hours 12 --surface imessage
```

**"Show me all recent activity"**
```bash
~/.claude-mind/system/bin/stream query --hours 6
```

**"What happened in CLI sessions today?"**
```bash
~/.claude-mind/system/bin/stream query --hours 24 --surface cli
```

**"Show me the raw event data"**
```bash
~/.claude-mind/system/bin/stream query --hours 3 --format json | head -100
```

## Presenting Results

When presenting stream results to the user:
1. Summarize the activity by surface
2. Highlight key conversations or events
3. Note the timeline
4. Connect to current context if relevant
