---
name: using-kodex
description: Use when project knowledge could help - queries Kodex topics and flags outdated information
user-invocable: false
allowed-tools:
  - mcp__plugin_mermaid-collab_mermaid__kodex_query_topic
  - mcp__plugin_mermaid-collab_mermaid__kodex_list_topics
  - mcp__plugin_mermaid-collab_mermaid__kodex_flag_topic
---

# Using Kodex

Query and maintain the project knowledge base.

## When to Query Kodex

Use judgment to query Kodex when project knowledge could help:

- Starting work on a feature that may have established patterns
- Investigating code that follows project conventions
- Making architectural decisions that should align with existing patterns

**Don't query for:** Trivial tasks, unrelated work, or when you already have sufficient context.

## How to Query

### Topic Inference

Infer topic names from your current context:

1. Extract key concepts from the task (e.g., "authentication", "error-handling")
2. Try variations: `{concept}`, `{concept}-patterns`, `{concept}-conventions`

### Example

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_query_topic
Args: {
  "project": "<absolute-path-to-cwd>",
  "name": "authentication"
}
```

### Handling Results

- **Topic found:** Display content as context for your work
- **Topic not found:** Try alternative names or continue without
- **Error:** Log and continue (non-blocking)

## When to Flag Topics

Flag a topic when it contradicts actual code **after verification**:

1. Query a topic and notice potential discrepancy
2. Read the actual source files to verify
3. Confirm the topic is genuinely outdated/incorrect
4. Flag with specific details

### Flagging Example

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_flag_topic
Args: {
  "project": "<absolute-path-to-cwd>",
  "name": "authentication",
  "type": "outdated",
  "description": "Topic says JWT tokens expire in 1 hour, but code shows 24 hours (see src/auth/config.ts:15)"
}
```

**Never flag without verifying against actual code.**

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `kodex_query_topic` | Query a topic by name |
| `kodex_list_topics` | List all available topics |
| `kodex_flag_topic` | Flag outdated/incorrect topic |
| `kodex_dashboard` | View Kodex stats |
| `kodex_list_flags` | View flagged topics |

**Note:** Topic creation and updates are human-driven. Claude should flag issues, not directly modify topics.
