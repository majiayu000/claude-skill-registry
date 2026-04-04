---
id: e3e99cfa-ae89-46cc-820e-35e2456d802b
title: Memory Router Skill
created: 2025-12-13T00:00:00
updated: 2025-12-13T00:00:00
project: dotfiles
scope: ai
type: reference
status: ✅ active
publish: false
tags:
  - claude
aliases:
  - Memory Router Skill
  - Memory Router Skill Reference
related: []
---

# Memory Router Skill

Route memory operations to appropriate backends (Graphiti for knowledge, AgentDB for coordination).

## Activation Triggers

- "remember this"
- "store this knowledge"
- "save for later"
- "search memory"
- "recall"
- "what do we know about"
- "memory"
- "knowledge graph"
- "agent context"

## Memory Channels

This skill manages four memory channels:

| Channel | Backend | Use For |
|---------|---------|---------|
| **long-term** | Graphiti | Architecture, patterns, permanent knowledge |
| **sprint** | Graphiti | Current feature work, research, WIP decisions |
| **team** | AgentDB | Agent coordination, task handoffs, shared state |
| **short-term** | Context | Immediate task, scratchpad (automatic) |

## Instructions

### When Storing Information

1. **Determine the appropriate channel** based on content type:

   - **Long-term** (permanent project knowledge):
     - Architecture decisions (ADRs)
     - Code patterns and conventions
     - API schemas and contracts
     - Domain entity definitions
     - Team standards

   - **Sprint** (current work context):
     - Feature research and findings
     - WIP design decisions
     - Investigation results
     - Temporary workarounds
     - Sprint-specific patterns

   - **Team** (agent coordination):
     - Task assignments and status
     - Handoff context between agents
     - Shared variables and flags
     - Agent capabilities and availability

2. **Use the appropriate MCP tool**:

   For Graphiti (long-term and sprint channels):
   ```
   Use: mcp__graphiti__add_episode
   Parameters:
   - name: Descriptive name for the knowledge
   - episode_body: The content to store
   - source: Origin of the knowledge (e.g., "user_conversation", "code_analysis")
   - episode_type: "message" | "json" | "text"
   ```

   For AgentDB (team channel):
   ```
   Use: mcp__claude-flow__agent_set_state or mcp__claude-flow__shared_state_set
   Parameters vary by operation type
   ```

3. **Add appropriate metadata**:
   - `channel`: The target channel
   - `content_type`: Specific type (adr, pattern, research, task_assignment, etc.)
   - `related_entities`: Links to related knowledge
   - `temporal_context`: When this knowledge is valid

### When Searching/Recalling

1. **Determine which channels to search**:
   - For architectural questions: `["long_term"]`
   - For current work context: `["sprint", "long_term"]`
   - For agent coordination: `["team"]`
   - For comprehensive search: `["long_term", "sprint", "team"]`

2. **Use federated search**:

   For Graphiti:
   ```
   Use: mcp__graphiti__search
   Parameters:
   - query: Natural language search query
   - num_results: Number of results (default: 10)
   ```

   For AgentDB:
   ```
   Use: mcp__claude-flow__memory_search
   Parameters:
   - query: Search query
   - limit: Number of results
   ```

3. **Merge and present results** by relevance, noting the source channel.

### Content Type Classification

When the user doesn't specify a channel, classify content automatically:

| Content Pattern | Channel | Content Type |
|-----------------|---------|--------------|
| "ADR", "architecture decision" | long_term | adr |
| "pattern", "convention", "standard" | long_term | pattern |
| "schema", "API contract" | long_term | schema |
| "researching", "investigating" | sprint | research |
| "for this feature", "current work" | sprint | feature_spec |
| "WIP", "temporary", "for now" | sprint | wip_decision |
| "agent status", "task update" | team | agent_status |
| "hand off to", "coordinate with" | team | handoff |

### Promotion Operations

When sprint knowledge becomes permanent:

1. Confirm with user: "This appears to be stable knowledge. Promote to long-term memory?"
2. If confirmed, copy from sprint to long-term with provenance metadata
3. Optionally archive the sprint version

### Example Interactions

**User**: "Remember that we decided to use JWT for authentication"
**Action**: Store in `long_term` channel as `pattern` content type

**User**: "Save my research on the rate limiting options"
**Action**: Store in `sprint` channel as `research` content type

**User**: "What do we know about the UserService?"
**Action**: Search `long_term` and `sprint` channels for "UserService"

**User**: "Update the backend worker that the API integration is complete"
**Action**: Update `team` channel with agent handoff context

**User**: "This workaround for the caching issue should be documented permanently"
**Action**: Promote from `sprint` to `long_term` with promotion metadata

## MCP Tools Used

### Graphiti MCP Server
- `mcp__graphiti__add_episode` - Store knowledge
- `mcp__graphiti__search` - Semantic search
- `mcp__graphiti__get_entity` - Retrieve specific entity
- `mcp__graphiti__get_entity_edge` - Get relationships

### claude-flow MCP Server
- `mcp__claude-flow__memory_store` - Store in AgentDB
- `mcp__claude-flow__memory_search` - Search AgentDB
- `mcp__claude-flow__shared_state_set` - Set shared state
- `mcp__claude-flow__shared_state_get` - Get shared state
- `mcp__claude-flow__agent_set_state` - Update agent state

## Configuration

Ensure both MCP servers are configured:

```json
{
  "mcpServers": {
    "graphiti": {
      "command": "graphiti-mcp-server",
      "args": ["--falkordb-url", "redis://localhost:6379"]
    },
    "claude-flow": {
      "command": "npx",
      "args": ["claude-flow@alpha", "mcp", "start"]
    }
  }
}
```

## Fallback Behavior

If a backend is unavailable:

1. **Graphiti unavailable**: Fall back to AgentDB for all storage (with warning)
2. **AgentDB unavailable**: Fall back to Graphiti for team coordination (with warning)
3. **Both unavailable**: Use context window only, warn user about persistence loss

## Related Documentation

- [[adr-memory-channel-architecture]] - Full architecture decision
- [[adr-agent-framework-strategy]] - Agent framework strategy
- [Graphiti Docs](https://docs.falkordb.com/agentic-memory/graphiti.html)
- [claude-flow Docs](https://github.com/ruvnet/claude-flow)
