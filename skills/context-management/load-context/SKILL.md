---
name: load-context
description: Auto-load relevant memories at session start from both mem0 and graph. Use when you need session context restored or preloaded.
tags: [memory, mem0, graph, session, context, continuity, auto-load]
user-invocable: true
auto-invoke: session-start
context: inherit
agent: null
version: 1.0.0
allowed-tools: [Read, mcp__mem0__search_memories, mcp__mem0__get_memories, mcp__memory__search_nodes, mcp__memory__read_graph]
author: SkillForge
---

# Load Context - Memory Fabric Initialization

Auto-load relevant memories at session start from both Mem0 semantic memory and the knowledge graph for seamless session continuity.

**CC 2.1.6 Context-Aware:** Loading adapts based on `context_window.used_percentage`.

## Overview

- **Automatically**: Invoked at session start via `auto-invoke: session-start`
- **Manually**: Run `/load-context` to reload memories mid-session
- **After MCP reconnect**: Refresh context if MCP servers were restarted

## Context-Aware Loading Tiers

Memory Fabric adjusts how much context to load based on current context pressure:

| Context Usage | Decisions | Blockers | Entities | Behavior |
|---------------|-----------|----------|----------|----------|
| 0-40% (Green) | 5 | 3 | 5 | Full context load |
| 40-70% (Yellow) | 3 | 1 | 3 | Reduced context |
| 70-90% (Orange) | 1 | critical only | 0 | Minimal context |
| >90% (Red) | 0 | 0 | 0 | Skip, show hint only |

## Workflow

### 1. Check Context Pressure

```
If context_window.used_percentage > 90%:
  → Output: "[Memory Fabric] Skipping - context at {X}%"
  → Exit early

If > 70%: Use minimal tier (1 decision, critical blockers only)
If > 40%: Use reduced tier (3 decisions, 1 blocker, 3 entities)
```

### 2. Query Recent Sessions (Mem0)

Call `mcp__mem0__search_memories`:

```json
{
  "query": "session context blockers next steps",
  "filters": {
    "AND": [
      { "user_id": "{project}-continuity" },
      { "created_at": { "gte": "7 days ago" } }
    ]
  },
  "limit": 3,
  "enable_graph": true
}
```

### 3. Query Recent Decisions (Mem0)

Call `mcp__mem0__get_memories`:

```json
{
  "filters": {
    "AND": [{ "user_id": "{project}-decisions" }]
  },
  "page_size": 5
}
```

### 4. Query Graph Entities

Call `mcp__memory__search_nodes`:

```json
{
  "query": "recent decisions patterns"
}
```

### 5. Format Output

```
[Memory Fabric Loaded]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recent Decisions ({count}):
  - [{time ago}] {decision_text}

Unresolved Blockers ({count}):
  - {blocker_text} (session {date})

Active Entities ({count}):
  - {entity} -> {relation} -> {entity}

Next Steps from Last Session:
  - {step_1}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Error Handling

### MCP Unavailable

Show configuration hints and continue without that source:

```
[Memory Fabric]
Mem0 MCP server unavailable. Run /configure to enable.
Continuing without semantic memory...
```

### No Memories Found

```
[Memory Fabric Loaded]
No memories found for this project.
This is normal for new projects. Use /remember to start building memory.
```

## Related Skills

- `mem0-sync` - Save context at session end
- `remember` - Store decisions and patterns manually
- `recall` - Search memories on-demand

## Arguments

- No arguments: Load context using default settings
- `--refresh`: Force reload even if recently loaded
- `--verbose`: Show detailed MCP query results
