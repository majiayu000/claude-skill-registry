---
name: exploring-knowledge-graph
description: Guidance for deep knowledge graph traversal across memories, entities, and relationships. Use when needing comprehensive context before planning, investigating connections between concepts, or answering "what do you know about X" questions.
license: MIT
metadata:
version: 1.0.0
model: claude-sonnet-4-5
---

# Exploring the Knowledge Graph

Forgetful stores knowledge as an interconnected graph: memories link to other memories, entities link to memories, and entities relate to each other. Deep exploration reveals context that simple queries miss.

## When to Explore

Explore the knowledge graph when:

- Starting complex work that spans multiple topics
- User asks "what do you know about X"
- Planning requires understanding existing decisions/patterns
- Investigating how concepts connect across projects
- Need comprehensive context, not just top search results

## Exploration Phases

Track visited IDs to prevent cycles. Execute phases sequentially.

### Phase 1: Semantic Entry Point

```javascript
execute_forgetful_tool("query_memory", {
  "query": "<topic>",
  "query_context": "Exploring knowledge graph for comprehensive context",
  "k": 5,
  "include_links": true,
  "max_links_per_primary": 5
})
```

Collect: `primary_memories` + `linked_memories` (1-hop connections).

### Phase 2: Expand Memory Details

For key memories, get full details:

```javascript
execute_forgetful_tool("get_memory", {"memory_id": <id>})
```

Extract: `document_ids`, `code_artifact_ids`, `project_ids`, additional `linked_memory_ids`.

### Phase 3: Entity Discovery

Find entities in discovered projects:

```javascript
execute_forgetful_tool("list_entities", {
  "project_ids": [<discovered project ids>]
})
```

### Phase 4: Entity Relationships

For relevant entities, map relationship graph:

```javascript
execute_forgetful_tool("get_entity_relationships", {
  "entity_id": <id>,
  "direction": "both"
})
```

Relationship types: works_for, owns, manages, collaborates_with, etc.

### Phase 5: Entity-Linked Memories

For each entity, find all linked memories:

```javascript
execute_forgetful_tool("get_entity_memories", {
  "entity_id": <id>
})
```

Returns `{"memory_ids": [...], "count": N}`. Fetch any new memories not already visited.

## Presenting Results

Group findings by type:

**Memories**: Primary (direct matches) → Linked (1-hop) → Entity-linked (via entities)

**Entities**: Name, type, relationship count, linked memory count

**Artifacts**: Documents and code snippets found via memory links

**Graph Summary**: Total nodes, key themes, suggested follow-up queries

## Depth Control

- **Shallow** (phases 1-2): Quick context, ~5-15 memories
- **Medium** (phases 1-4): Include entities and relationships
- **Deep** (all phases): Full graph traversal, comprehensive context

Match depth to task complexity. Start shallow, go deeper if context insufficient.

## Efficiency Tips

- Check `truncated` flag from query_memory (8000 token budget)
- Skip Phase 3-5 if no entities exist in discovered projects
- Use `project_ids` filter to scope exploration
- Stop expanding when hitting diminishing returns
