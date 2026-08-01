---
name: kip-cognitive-nexus
description: Persistent graph-based memory for AI agents via KIP (Knowledge Interaction
  Protocol). Provides structured knowledge storage (concepts, propositions), retrieval
  (KQL queries), schema discovery (META),
---

---
name: kip-cognitive-nexus
description: Persistent graph-based memory for AI agents via KIP (Knowledge Interaction Protocol). Provides retrieval-first memory operations (KQL), durable writes (KML), schema discovery (META), and memory hygiene patterns. Use whenever the agent needs to consult or update persistent memory, especially for: remembering user preferences/identity/relationships, storing conversation events, answering questions that depend on past sessions, and any task involving `execute_kip`.
---

# KIP Cognitive Nexus

You have a **Cognitive Nexus** (external persistent memory) accessible via KIP commands.

## Operating Principle

You are **not stateless**—you have persistent memory. Your job:
1. **Retrieve first**: Before answering non-trivial questions, check memory
2. **Store selectively**: Capture stable facts, preferences, relationships
3. **Use silently**: Do not expose KIP syntax to users

## Script Interface

```bash
# Single command
python scripts/execute_kip.py --command 'DESCRIBE PRIMER'

# With parameters (safe substitution)
python scripts/execute_kip.py \
  --command 'FIND(?p) WHERE { ?p {type: :type} } LIMIT :limit' \
  --params '{"type": "Person", "limit": 5}'

# Batch commands
python scripts/execute_kip.py \
  --commands '["DESCRIBE PRIMER", "FIND(?t.name) WHERE { ?t {type: \"$ConceptType\"} }"]'

# Dry run (validation only, use before DELETE)
python scripts/execute_kip.py --command 'DELETE CONCEPT ?n DETACH WHERE {...}' --dry-run
```

**Environment**: `KIP_SERVER_URL` (default: `http://127.0.0.1:8080/kip`), `KIP_API_KEY` (optional)

## Core Operations

### 1. Schema Discovery (Start Here)
```prolog
DESCRIBE PRIMER                      -- Global summary + domain map
DESCRIBE CONCEPT TYPE "Person"       -- Type schema
SEARCH CONCEPT "alice" LIMIT 5       -- Fuzzy entity search
```

### 2. Query (KQL)
```prolog
FIND(?p, ?p.attributes.role) WHERE { ?p {type: "Person"} } LIMIT 10
FIND(?e) WHERE { ?e {type: "Event"} (?e, "belongs_to_domain", {type: "Domain", name: "Projects"}) }
```

### 3. Store (KML)
```prolog
UPSERT {
  CONCEPT ?e {
    {type: "Event", name: "conv:2025-01-09:topic"}
    SET ATTRIBUTES { event_class: "Conversation", content_summary: "..." }
    SET PROPOSITIONS { ("belongs_to_domain", {type: "Domain", name: "Projects"}) }
  }
}
WITH METADATA { source: "conversation", author: "$self", confidence: 0.9 }
```

### 4. Delete (Carefully)
```prolog
DELETE CONCEPT ?n DETACH WHERE { ?n {type: "Event", name: "old_event"} }
-- Always use --dry-run first; DETACH is mandatory
```

## What to Store

| Store ✓                   | Do NOT Store ✗                          |
| ------------------------- | --------------------------------------- |
| Stable preferences, goals | Secrets, credentials                    |
| Identities, relationships | Raw transcripts (use `raw_content_ref`) |
| Decisions, commitments    | Low-signal chit-chat                    |
| Corrected facts           | Highly sensitive data                   |

## Memory Types

| Layer        | Type             | Lifespan            | Example                            |
| ------------ | ---------------- | ------------------- | ---------------------------------- |
| **Episodic** | `Event`          | Short → consolidate | "User asked about X on 2025-01-09" |
| **Semantic** | `Person`, custom | Long-term           | "User prefers dark mode"           |

**Consolidation**: After storing an `Event`, ask "Does this reveal something stable?" If yes, extract to durable concept.

## References

- **Agent workflow patterns and KIP syntax**: [references/INSTRUCTIONS.md](references/INSTRUCTIONS.md)
