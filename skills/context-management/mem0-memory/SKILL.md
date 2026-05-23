---
name: mem0-memory
description: Long-term semantic memory across sessions using Mem0. Use when you need to remember, recall, or forget information across sessions, or when referencing what we discussed last time or in a previous session.
context: fork
agent: any
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Mem0 Memory Management

Persist and retrieve semantic memories across Claude sessions.

## Memory Scopes

Organize memories by scope for efficient retrieval:

| Scope | Purpose | Examples |
|-------|---------|----------|
| `project-decisions` | Architecture and design decisions | "Use PostgreSQL with pgvector for RAG" |
| `project-patterns` | Code patterns and conventions | "Components use kebab-case filenames" |
| `project-continuity` | Session handoff context | "Working on auth refactor, PR #123 pending" |

## Core Operations

### Adding Memories

```python
# mcp__mem0__add_memory
await mcp.mem0.add_memory(
    content="Decided to use FastAPI over Flask for async support",
    metadata={
        "scope": "project-decisions",
        "category": "backend",
        "date": "2026-01-12"
    }
)
```

**Best practices for adding:**
- Be specific and actionable
- Include rationale ("because...")
- Add scope and category metadata
- Timestamp important decisions

### Searching Memories

```python
# mcp__mem0__search_memories
results = await mcp.mem0.search_memories(
    query="authentication approach",
    limit=5
)
```

**Search tips:**
- Use natural language queries
- Search by topic, not exact phrases
- Combine with scope filters when available

### Listing Memories

```python
# mcp__mem0__get_memories
all_memories = await mcp.mem0.get_memories(
    user_id="project-skillforge",
    limit=100
)
```

### Deleting Memories

```python
# mcp__mem0__delete_memory
await mcp.mem0.delete_memory(memory_id="mem_abc123")
```

**When to delete:**
- Outdated decisions that were reversed
- Incorrect information
- Duplicate or redundant entries

## What to Remember

**Good candidates:**
- Architecture decisions with rationale
- API contracts and interfaces
- Naming conventions adopted
- Technical debt acknowledged
- Blockers and their resolutions
- User preferences and style

**Avoid storing:**
- Temporary debugging context
- Large code blocks (use Git)
- Secrets or credentials
- Highly volatile information

## Memory Patterns

### Decision Memory
```
"Decision: Use cursor-based pagination for all list endpoints.
Rationale: Better performance for large datasets, consistent UX.
Date: 2026-01-12. Scope: API design."
```

### Pattern Memory
```
"Pattern: All React components export default function.
Convention: Use named exports only for utilities.
Applies to: frontend/src/components/**"
```

### Continuity Memory
```
"Session handoff: Completed hybrid search implementation.
Next steps: Add metadata boosting, write integration tests.
PR #456 ready for review. Blocked on: DB migration approval."
```

## Integration with SkillForge

Use memories to maintain context across plugin sessions:

```python
# At session start - recall project context
memories = await mcp.mem0.search_memories(
    query="current sprint priorities"
)

# During work - persist decisions
await mcp.mem0.add_memory(
    content=f"Implemented {feature} using {approach} because {reason}",
    metadata={"scope": "project-decisions"}
)

# At session end - save continuity
await mcp.mem0.add_memory(
    content=f"Session end: {summary}. Next: {next_steps}",
    metadata={"scope": "project-continuity"}
)
```

## MCP Requirements

This skill requires the Mem0 MCP server configured in Claude Desktop:

```json
{
  "mcpServers": {
    "mem0": {
      "command": "npx",
      "args": ["-y", "@mem0/mcp-server"],
      "env": {
        "MEM0_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Related Skills

- `semantic-caching` - Semantic caching patterns that complement long-term memory
- `embeddings` - Embedding strategies used by Mem0 for semantic search
- `langgraph-checkpoints` - State persistence patterns for workflow continuity
- `context-compression` - Compress context when memory retrieval adds too many tokens

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Memory scope | project-decisions, project-patterns, project-continuity | Clear separation of memory types |
| Storage format | Natural language with metadata | Semantic search works best with descriptive text |
| MCP integration | Mem0 MCP server | Native Claude Desktop integration |
| What to avoid | Secrets, large code blocks, volatile info | Keep memories clean and safe |

## Capability Details

### memory-add
**Keywords:** add memory, remember, store, persist, save context
**Solves:**
- How do I save information for later sessions?
- Persist a decision or pattern
- Store project context across sessions

### memory-search
**Keywords:** search memory, recall, find, retrieve, what did we
**Solves:**
- How do I find previous decisions?
- Recall context from past sessions
- Search for specific patterns or conventions

### memory-list
**Keywords:** list memories, show all, get memories, view stored
**Solves:**
- How do I see all stored memories?
- List project decisions
- Review stored patterns

### memory-delete
**Keywords:** delete memory, forget, remove, clear
**Solves:**
- How do I remove outdated memories?
- Delete incorrect information
- Clean up duplicate entries