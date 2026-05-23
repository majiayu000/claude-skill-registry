---
name: openmemory
description: Persistent long-term agent memory for storing and querying past work, patterns, and learnings.
agents: [blaze, rex, nova, tap, spark, grizz, bolt, cleo, cipher, tess, morgan, atlas, stitch]
triggers: [memory, remember, store, recall, past work, similar, previous]
---

# OpenMemory (Persistent Agent Memory)

You have access to **OpenMemory** for persistent long-term memory across sessions.

## Memory Tools

| Tool | Purpose |
|------|---------|
| `openmemory_query` | Semantic search across memories by similarity |
| `openmemory_store` | Store new memories with sector classification |
| `openmemory_list` | List recent memories for a user/agent |
| `openmemory_get` | Retrieve specific memory by ID |
| `openmemory_reinforce` | Boost salience of important memories |

## Memory Sectors

Memories are classified into sectors:

| Sector | Use Case | Example |
|--------|----------|---------|
| **episodic** | Events, task history | "Implemented auth flow for project X" |
| **semantic** | Facts, learned patterns | "Always add Context7 lookup before Rust implementation" |
| **procedural** | How-to knowledge | "Steps to deploy with ArgoCD" |

## Usage Patterns

**Before starting a task:**
```
openmemory_query({ query: "similar implementations", sector: "episodic" })
```

**After completing a task:**
```
openmemory_store({ 
  content: "Implemented OAuth2 with PKCE for React app using Effect",
  sector: "episodic",
  tags: ["auth", "react", "effect"]
})
```

**For important learnings:**
```
openmemory_reinforce({ memory_id: "mem_xyz", boost: 1.5 })
```

## Best Practices

1. **Query before implementing** - Check for similar past work
2. **Store after completing** - Save successful patterns and solutions
3. **Reinforce important memories** - Boost salience of critical learnings
4. **Tag memories well** - Include relevant technologies and patterns
