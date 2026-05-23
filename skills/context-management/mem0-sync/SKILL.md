---
name: mem0-sync
description: Auto-sync session context, decisions, and patterns to Mem0 for cross-session continuity
tags: [mem0, sync, session, memory, continuity, persistence]
user-invocable: true
auto-invoke: session-end
context: inherit
---

# Mem0 Auto-Sync

Automatically synchronize session context to Mem0 for seamless cross-session continuity. This skill executes MCP calls to persist decisions, patterns, and session summaries.

## When to Use

- **Automatically**: Invoked at session end by `mem0-pre-compaction-sync.sh` hook
- **Manually**: Run `/mem0-sync` to force sync mid-session
- **After major decisions**: Sync important architectural decisions immediately

## Quick Sync

Execute these MCP calls based on the sync context provided:

### 1. Session Summary (Always)

```
mcp__mem0__add_memory({
  text: "Session Summary: {task_summary}",
  user_id: "{project}-continuity",
  metadata: {
    type: "session_summary",
    status: "{status}",
    has_blockers: {has_blockers},
    has_next_steps: {has_next_steps}
  },
  enable_graph: true
})
```

### 2. Pending Decisions (If Any)

For each decision in the decision log that hasn't been synced:

```
mcp__mem0__add_memory({
  text: "{decision_content}",
  user_id: "{project}-decisions",
  metadata: {
    category: "{category}",
    outcome: "success"
  },
  enable_graph: true
})
```

### 3. Agent Patterns (If Any)

For each agent pattern that was learned:

```
mcp__mem0__add_memory({
  text: "{pattern_description}",
  user_id: "{project}-agents",
  agent_id: "skf:{agent_type}",
  metadata: {
    category: "{category}",
    outcome: "{success|failed}"
  },
  enable_graph: true
})
```

### 4. Best Practices (If Generalizable)

For patterns that apply across projects:

```
mcp__mem0__add_memory({
  text: "{best_practice}",
  user_id: "skillforge-global-best-practices",
  metadata: {
    project: "{project}",
    category: "{category}",
    outcome: "success"
  },
  enable_graph: true
})
```

## Sync Protocol

1. **Check availability**: Verify Mem0 MCP is configured
2. **Read sync state**: Load `.claude/coordination/.decision-sync-state.json`
3. **Execute MCP calls**: Run add_memory for each item
4. **Update sync state**: Mark synced items to prevent duplicates
5. **Confirm completion**: Output sync summary

## Key Patterns

### Idempotent Sync
- Track synced decision IDs in sync state file
- Skip already-synced items
- Handle partial failures gracefully

### Graph Memory
- Always use `enable_graph: true` for relationship extraction
- Mem0 automatically creates entity/relation graphs
- Enables semantic search across related concepts

### Scoped User IDs
- `{project}-continuity`: Session summaries
- `{project}-decisions`: Architectural decisions
- `{project}-agents`: Agent-specific patterns
- `skillforge-global-best-practices`: Cross-project patterns

## Related Skills

- `recall` - Search and retrieve from Mem0
- `context-compression` - Compress context before sync
- `brainstorming` - Generate decisions worth syncing
