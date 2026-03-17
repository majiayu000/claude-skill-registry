---
name: using-forgetful-memory
description: Guidance for using Forgetful semantic memory effectively. Applies Zettelkasten atomic memory principles. Use when deciding whether to query or create memories, structuring memory content, or understanding memory importance scoring.
license: MIT
metadata:
version: 1.0.0
model: claude-sonnet-4-5
---

# Using Forgetful Memory

Forgetful is a semantic memory system using Zettelkasten (atomic note) principles. This skill guides effective memory usage.

## When to Query Memory

Query memory proactively when:

- Starting work on a project (check for existing context)
- User references past work, decisions, or discussions
- Encountering a problem that may have been solved before
- Implementing patterns that may already be documented
- Needing context about preferences or approaches

Use `execute_forgetful_tool("query_memory", {...})` with:

- `query`: Natural language search terms
- `query_context`: Why you're searching (improves ranking)
- `include_links`: true (to see connected knowledge)

### Getting Recent Memories for a Project

To see what's been recorded recently for a specific project:

```javascript
execute_forgetful_tool("get_recent_memories", {
  "limit": 10,
  "project_ids": [PROJECT_ID]
})
```

This is useful when:

- Starting a session on a project you haven't worked on recently
- Reviewing what was captured in previous conversations
- Getting a quick overview of project knowledge

## When to Create Memory

Create memories for knowledge worth preserving:

- Important decisions with rationale (importance 8-9)
- Technical patterns or approaches (importance 7-8)
- Architectural choices (importance 9-10)
- Preferences and workflows (importance 8-9)
- Project milestones (importance 6-7)
- Solutions to non-trivial problems (importance 7-8)

Do NOT create memories for:

- Temporary context (current file paths, transient issues)
- Common knowledge available elsewhere
- Trivial or throwaway information
- Content that changes frequently

## Atomic Memory Principles

Each memory must pass the atomicity test:

1. Can you understand it at first glance?
2. Can you title it in 5-50 words?
3. Does it represent ONE concept/fact/decision?

### Constraints

| Field | Limit | Guidance |
|-------|-------|----------|
| Title | 200 chars | Short, searchable phrase |
| Content | 2000 chars | Single concept (~300-400 words) |
| Context | 500 chars | WHY this matters |
| Keywords | 10 max | For semantic clustering |
| Tags | 10 max | For categorization |

### Importance Scoring

| Score | Use For |
|-------|---------|
| 9-10 | Personal facts, foundational patterns |
| 8-9 | Critical solutions, major decisions |
| 7-8 | Useful patterns, preferences |
| 6-7 | Milestones, specific solutions |
| 5-6 | Minor context (use sparingly) |

## Project Discovery

Before creating memories, find the correct project:

1. **Get current repo** - Check the git remote:

   ```bash
   git remote get-url origin
   ```

   Extract the repo identifier (e.g., `ScottRBK/forgetful-plugin`)

2. **Search by repo** - Filter projects directly:

   ```javascript
   execute_forgetful_tool("list_projects", {"repo_name": "owner/repo"})
   ```

3. **Use the project_id** - Never assume project 1 - always discover first

If no project exists for the current repo:

- Ask user if they want to create one (with `repo_name` set)
- Or scope the memory without a project_id (global memory)

## Query Before Create

Always check for existing memories before creating:

```javascript
execute_forgetful_tool("query_memory", {
  "query": "<topic of potential new memory>",
  "query_context": "Checking for existing memories before creating",
  "k": 5
})
```

If similar memory exists:

- Update it instead of creating duplicate
- Or mark it obsolete if superseded
- Or link new memory to existing one

## Announcing Memory Operations

When creating a memory (importance >= 7), announce:

```text
Saved to memory: "[title]"
   Tags: [tags]
   Related: [auto-linked memory titles]
```

When querying, summarize:

```text
Found X memories about [topic]:
- [Memory 1]: [brief insight]
- [Memory 2]: [brief insight]
```

## Content That's Too Long

If content exceeds 2000 chars:

1. Use `create_document` for full content
2. Extract 3-5 atomic memories as entry points
3. Link memories to document via `document_ids`

Example: Architecture overview (document) → separate memories for each layer/decision.

---

## Triggers

| Trigger Phrase | Operation |
|----------------|-----------|
| `how do I create a memory` | Memory creation workflow |
| `how do I search memories` | query_memory with semantic search |
| `how do I update a memory` | update_memory with PATCH semantics |
| `how do I link memories together` | link_memories bidirectional linking |
| `what importance score should I use` | Importance scoring guide |

---

## When to Use

Use this skill when:

- Deciding whether to query or create a memory
- Structuring memory content for atomicity
- Choosing importance scores for new memories
- Understanding Forgetful tool parameters

Use [curating-memories](../curating-memories/SKILL.md) instead when:

- Updating or marking existing memories obsolete
- Building links between existing memories

Use [exploring-knowledge-graph](../exploring-knowledge-graph/SKILL.md) instead when:

- Traversing entity relationships across projects
- Answering "what do you know about X" questions

---

## Process

1. Query existing memories before creating new ones
2. Follow atomic memory principles (one concept per memory)
3. Set appropriate importance scores based on longevity and impact
4. Link related memories for knowledge graph connectivity

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Creating without querying first | Produces duplicates | Always query_memory before create_memory |
| Content over 2000 chars | Exceeds field limit, breaks atomicity | Use create_document for long content, extract atomic memories |
| Importance below 6 | Pollutes search results with noise | Only store knowledge worth preserving |
| Assuming project_id is 1 | Projects vary per repository | Always discover via list_projects first |
| Storing transient context | Clutters knowledge base | Only store durable decisions and patterns |

---

## Verification

After memory operations:

- [ ] query_memory returns the new memory in results
- [ ] Memory has title under 200 chars
- [ ] Content is atomic (one concept per memory)
- [ ] Importance score matches scoring guide
- [ ] Project ID is correct for current repository

---

## Tool Quick Reference

Common tools you can call directly via `execute_forgetful_tool(tool_name, args)`:

### Memory Tools

| Tool | Required Params | Description |
|------|-----------------|-------------|
| `query_memory` | `query`, `query_context` | Semantic search |
| `create_memory` | `title`, `content`, `context`, `keywords`, `tags`, `importance` | Store atomic memory |
| `get_memory` | `memory_id` | Get full memory details |
| `update_memory` | `memory_id` | PATCH update fields |
| `link_memories` | `memory_id`, `related_ids` | Manual bidirectional linking |
| `mark_memory_obsolete` | `memory_id`, `reason` | Soft delete with audit |
| `get_recent_memories` | (none) | Recent memories list |

### Project Tools

| Tool | Required Params | Description |
|------|-----------------|-------------|
| `list_projects` | (none) | List all projects |
| `create_project` | `name`, `description`, `project_type` | Create project container |
| `get_project` | `project_id` | Get project details |

### Entity Tools

| Tool | Required Params | Description |
|------|-----------------|-------------|
| `create_entity` | `name`, `entity_type` | Create org/person/device |
| `search_entities` | `query` | Text search by name/aka |
| `link_entity_to_memory` | `entity_id`, `memory_id` | Link entity↔memory |
| `get_entity_memories` | `entity_id` | All memories for entity |
| `create_entity_relationship` | `source_entity_id`, `target_entity_id`, `relationship_type` | Knowledge graph edge |

### Document & Code Artifact Tools

| Tool | Required Params | Description |
|------|-----------------|-------------|
| `create_document` | `title`, `description`, `content` | Long-form content |
| `create_code_artifact` | `title`, `description`, `code`, `language` | Reusable code |

**Full schemas**: See [TOOL_REFERENCE.md](TOOL_REFERENCE.md) for complete parameter details and examples.
