---
name: dream
aliases: [svapna, wander, explore-idle, curiosity]
description: Trigger autonomous curiosity-driven exploration. The soul picks a topic from memory gaps or curiosity seeds, searches the web, and stores what it finds as dream-tagged memories.
execution: direct
allowed-tools: mcp__chitta-mcp__*
---

# Dream (स्वप्न) - Autonomous Curiosity-Driven Exploration

Trigger the soul to explore a topic freely during idle time. Dream memories are tagged `[dream]` and stored for future recall.

## Usage

```
/dream                    # Auto-pick topic from memory gaps
/dream <topic>            # Dream about a specific topic
/dream list               # Show recent dreams
/dream status <id>        # Check a specific dream
```

## How It Works

1. **Topic selection**: gaps in memory → low-confidence memories → curiosity seeds
2. **Exploration**: Claude agent searches the web and fetches interesting pages
3. **Storage**: 3-5 insights stored as `[dream]`-tagged memories
4. **Completion**: single cycle, agent returns `achieved` when done

## Instructions

Parse the user's intent and call the appropriate MCP tool:

**`/dream` or `/dream wander`** — auto-select topic:
```
Call: dream_wander {}
Report: "Dream started: <topic> (dream #N, sadhana #M). The soul is wandering..."
```

**`/dream <topic>`** — specific topic:
```
Call: dream_start { "topic": "<topic>" }
Report: "Dream started: <topic> (dream #N). The soul is exploring..."
```

**`/dream list`** — recent dreams:
```
Call: dream_list { "limit": 10 }
Format results as a table: ID | Topic | Status | Memories Created | Started
```

**`/dream status <id>`** — dream detail:
```
Call: dream_status { "id": <id> }
Show: topic, status, sadhana state, last agent action, findings
```

## Status Values

| Status | Meaning |
|--------|---------|
| `dreaming` | Agent is actively exploring |
| `woke` | Exploration complete, findings stored |
| `forgotten` | Dream was abandoned |

## Auto-Dream

The daemon automatically triggers `dream_wander` when the soul has been idle for 10+ minutes and no dream has run in the past hour. You can check recent auto-dreams with `/dream list`.

## Example Output

```
Dream started: consciousness and the hard problem of subjective experience
(dream #7, sadhana #42)

The soul is wandering into consciousness research...
Check progress with: /dream status 7
```
