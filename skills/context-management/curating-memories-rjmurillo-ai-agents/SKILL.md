---
name: curating-memories
description: Guidance for maintaining memory quality through curation. Covers updating outdated memories, marking obsolete content, and linking related knowledge. Use when memories need modification, when new information supersedes old, or when building knowledge graph connections.
license: MIT
metadata:
version: 1.0.0
model: claude-sonnet-4-5
---

# Curating Memories

Active curation keeps the knowledge base accurate and connected. Outdated memories pollute search results and reduce effectiveness.

## When to Update a Memory

Use `update_memory` when:

- Information needs correction or clarification
- Importance level changes (more/less relevant than thought)
- Content needs refinement
- Links to projects/artifacts/documents change

```javascript
execute_forgetful_tool("update_memory", {
  "memory_id": <id>,
  "content": "Updated content...",
  "importance": 8
})
```

Only specified fields are changed (PATCH semantics).

## When to Mark Obsolete

Use `mark_memory_obsolete` when:

- Memory is outdated or contradicted by newer information
- Decision has been reversed or superseded
- Referenced code/feature no longer exists
- Memory was created in error

```javascript
execute_forgetful_tool("mark_memory_obsolete", {
  "memory_id": <id>,
  "reason": "Superseded by new architecture decision",
  "superseded_by": <new_memory_id>  // optional
})
```

Obsolete memories are soft-deleted (preserved for audit, hidden from queries).

## When to Link Memories

Use `link_memories` when:

- Concepts are related but not caught by auto-linking
- Building explicit knowledge graph structure
- Connecting decisions to their implementations
- Relating patterns across projects

```javascript
execute_forgetful_tool("link_memories", {
  "memory_id": <source_id>,
  "related_ids": [<target_id_1>, <target_id_2>]
})
```

Links are bidirectional (A↔B created automatically).

## Curation Workflow

When creating new memories, check impact on existing knowledge:

### Step 1: Query Related Memories

```javascript
execute_forgetful_tool("query_memory", {
  "query": "<topic of new memory>",
  "query_context": "Checking for memories that may need curation",
  "k": 5
})
```

### Step 2: Analyze Each Result

For each existing memory, determine action:

| Situation | Action |
|-----------|--------|
| Existing memory is still accurate | Link to it |
| Existing memory has minor gaps | Update it |
| Existing memory is now wrong | Mark obsolete, create new |
| Existing memory is partially valid | Create new, link both |

### Step 3: Execute Curation Plan

Present plan to user before executing:

```text
Curation plan:
- Create: "New authentication approach" (importance: 8)
- Mark obsolete: #42 "Old auth pattern" (superseded)
- Link: New memory ↔ #38 "Security requirements"

Proceed? (y/n)
```

### Step 4: Execute and Report

After user confirms:

1. Create new memory
2. Mark obsolete memories
3. Create links
4. Report results with all changes made

## Signs of Poor Curation

Watch for these indicators:

- Multiple similar memories on same topic (deduplicate)
- Memories referencing deleted code (mark obsolete)
- Contradictory memories (resolve conflict)
- Low-importance memories (importance < 6) accumulating
- Orphaned memories with no links (consider linking or removing)

## Auto-Linking

Forgetful auto-links semantically similar memories (similarity >= 0.7) during creation. Manual linking is for:

- Explicit relationships auto-linking missed
- Cross-project connections
- Non-obvious conceptual links

Check `similar_memories` in create response to see what was auto-linked.
