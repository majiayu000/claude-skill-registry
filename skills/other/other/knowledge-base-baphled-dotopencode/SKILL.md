---
name: knowledge-base
description: Query memory graph, vault-rag, and Obsidian KB docs to find existing knowledge before investigating
category: Session Knowledge
---

# Skill: knowledge-base

## What I do

I teach agents how to access the three knowledge systems available in this setup: the memory graph (MCP), the Obsidian vault via RAG, and direct KB doc navigation. I prevent re-discovering what's already documented.

## When to use me

- Before starting any investigation — check what's already known
- When a skill's `## KB Reference` points to a KB doc you need to read
- When searching for past decisions, patterns, or solutions
- When you need context about a codebase, agent, skill, or workflow

## The three knowledge systems

| System | What it holds | Best for |
|---|---|---|
| Memory graph | Problem-solution pairs, session discoveries, entity relations | Fast lookup of specific known things |
| Vault-RAG | All Obsidian vault notes, KB docs, skill docs, ADRs | Broad semantic search across all documentation |
| KB docs (direct) | Structured reference docs in `~/vaults/baphled/` | Deep reading when you know the exact topic |

## Patterns & examples

**Search memory graph** (fastest — check first):
```typescript
mcp_memory_search_nodes({ query: "describe the problem or topic" })
mcp_memory_open_nodes({ names: ["KnownEntityName"] })
```

**Query vault via RAG** (semantic search across all docs):
```typescript
mcp_vault-rag_query_vault({
  vault: "baphled",
  question: "what is the pattern for X?",
  top_k: 5
})
```

**Read KB doc directly** (when you know the path):
```
~/vaults/baphled/3. Resources/Knowledge Base/Skills/{Category}/{Name}.md
~/vaults/baphled/3. Resources/Tech/OpenCode/
~/vaults/baphled/3. Resources/Knowledge Base/Agents/{Name}.md
```

## Lookup order

1. **Memory graph** — search_nodes for the topic
2. **Vault-RAG** — query_vault if memory has nothing
3. **Direct KB read** — if you know the exact doc path
4. **Codebase investigation** — only if none of the above answers it

## Anti-patterns to avoid

- ❌ Investigating the codebase before checking memory/vault
- ❌ Asking the user for context that's already in the KB
- ❌ Ignoring `## KB Reference` sections in skills — they point to deeper coverage
- ❌ Storing to memory without searching first (creates duplicates)

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Core-Universal/Knowledge Base.md`

## Related skills

- `memory-keeper` — Capturing and retrieving from the memory graph
- `obsidian-structure` — PARA structure for navigating the vault
- `investigation` — Systematic codebase investigation when KB has no answer
