---
name: memory-keeper
description: Capture discoveries, fixes, solutions, and patterns into a searchable knowledge graph for future reference
category: Core Universal
---

# Skill: memory-keeper

## What I do

I systematically capture problem-solution pairs, patterns discovered, and common mistakes into a knowledge graph. This creates searchable institutional memory that prevents repeating debugging work.

## When to use me

- After solving a difficult bug or problem (capture solution)
- When discovering a new pattern or technique (capture insight)
- After investigating a complex issue (capture findings)
- When learning something that took significant time (prevent repeat learning)

## Core principles

1. Capture context and why, not just the what
2. Make findings searchable with clear terminology
3. Verify accuracy before storing (no false memories)
4. Link related discoveries to see patterns emerge
5. Search memory before investigating (read before write)

## Decision triggers

- Always-active: load with every session to capture learnings
- Load with `pre-action` to decide what's worth capturing
- Load with `epistemic-rigor` to verify accuracy before storing
- For knowledge graph structure and schema, refer to Obsidian vault

## Retrieval patterns

**Search memory BEFORE investigating** — avoid re-discovering what's already known.

Search by topic or problem description:
```typescript
mcp_memory_search_nodes({ query: "topic or error description" })
```

Open specific known entities by name:
```typescript
mcp_memory_open_nodes({ names: ["EntityName", "AnotherEntity"] })
```

Query the Obsidian vault via RAG for KB docs and notes:
```typescript
mcp_vault-rag_query_vault({ vault: "baphled", question: "your question here", top_k: 5 })
```

**Lookup order:**
1. Search memory graph first (fastest, session-persistent)
2. Query vault-rag for KB docs (broader, covers all documented knowledge)
3. Read specific KB files directly if you know the path
4. Only investigate the codebase if none of the above answers the question

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Core-Universal/Memory Keeper.md`

## Related skills

- `knowledge-base` — Patterns for querying vault-rag and KB docs
- `pre-action` — Decide what's worth capturing before storing
- `epistemic-rigor` — Verify accuracy before storing (no false memories)
