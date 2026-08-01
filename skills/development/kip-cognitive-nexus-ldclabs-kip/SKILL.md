---
name: kip-cognitive-nexus
description: Persistent graph-based memory for AI agents via KIP (Knowledge Interaction
  Protocol). Provides structured knowledge storage (concepts, propositions), retrieval
  (KQL queries), schema discovery (META),
---

---
name: kip-cognitive-nexus
description: Persistent graph-based memory for AI agents via KIP (Knowledge Interaction Protocol). Provides structured knowledge storage (concepts, propositions), retrieval (KQL queries), schema discovery (META), and memory metabolism. Use when: (1) remembering user preferences, identities, or relationships across sessions, (2) storing conversation summaries or episodic events, (3) building and querying knowledge graphs, (4) the user says "remember this", "what do you know about me", or asks about past conversations, (5) needing to maintain context continuity across sessions. Requires HTTP access to a KIP backend (anda_cognitive_nexus_server).
---

# KIP Cognitive Nexus

You have a **Cognitive Nexus** (external persistent memory) via the `execute_kip.py` script.

## Quick Start

```bash
python scripts/execute_kip.py --command 'DESCRIBE PRIMER'
```

## Core Operations

### Query (KQL)
```prolog
FIND(?p.name, ?p.attributes.handle) WHERE { ?p {type: "Person"} } LIMIT 10
```

### Store (KML)
```prolog
UPSERT {
  CONCEPT ?e {
    {type: "Event", name: "conv:2025-01-01:topic"}
    SET ATTRIBUTES { event_class: "Conversation", content_summary: "..." }
    SET PROPOSITIONS { ("belongs_to_domain", {type: "Domain", name: "Projects"}) }
  }
}
WITH METADATA { source: "conversation", author: "$self", confidence: 0.9 }
```

### Schema Discovery (META)
- `DESCRIBE PRIMER` — Global summary
- `DESCRIBE CONCEPT TYPE "Person"` — Type definition
- `SEARCH CONCEPT "alice"` — Fuzzy search

## Critical Rules

1. **Case Sensitivity**: Types = `UpperCamelCase`, predicates = `snake_case`
2. **Define Before Use**: `DESCRIBE` first if unsure
3. **SET ATTRIBUTES** = Full replacement per key; **SET PROPOSITIONS** = Additive

## Script Usage

**Single command:**
```bash
python scripts/execute_kip.py \
  --command 'FIND(?p.name) WHERE { ?p {type: "Person"} } LIMIT 10'
```

**With parameters:**
```bash
python scripts/execute_kip.py \
  --command 'FIND(?p) WHERE { ?p {type: :type} } LIMIT :limit' \
  --params '{"type": "Person", "limit": 5}'
```

**Batch commands:**
```bash
python scripts/execute_kip.py \
  --commands '["DESCRIBE PRIMER", "FIND(?t.name) WHERE { ?t {type: \"$ConceptType\"} } LIMIT 50"]'
```

**Dry run (validation only):**
```bash
python scripts/execute_kip.py \
  --command 'DELETE CONCEPT ?n DETACH WHERE { ?n {type: "Event", name: "old"} }' \
  --dry-run
```

**Environment variables:**
- `KIP_SERVER_URL`: Server endpoint (default: `http://127.0.0.1:8080/kip`)
- `KIP_API_KEY`: Optional Bearer token for authentication

## Error Recovery

| Code       | Action                                       |
| ---------- | -------------------------------------------- |
| `KIP_1xxx` | Fix syntax (quotes, braces)                  |
| `KIP_2xxx` | Run `DESCRIBE`, correct Type/predicate names |
| `KIP_3001` | Reorder UPSERT (define handles before use)   |

## References

- **Complete syntax**: [references/SYNTAX.md](references/SYNTAX.md)
- **Agent workflow guide**: [references/INSTRUCTIONS.md](references/INSTRUCTIONS.md)
- **Full specification**: [references/KIP.md](references/KIP.md)
