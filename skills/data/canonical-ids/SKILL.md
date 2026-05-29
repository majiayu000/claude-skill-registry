---
name: canonical-ids
description: Create or reference entities with canonical IDs. Every entity must have a globally unique, traceable ID.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Canonical IDs Skill

## Core Principle

**Every entity must have a canonical ID that is globally unique and traceable.**

---

## ID Format

| Entity | Format | Example |
|--------|--------|---------|
| Product | `ptc_prod_{uuid}` | `ptc_prod_a1b2c3d4-...` |
| Item | `ptc_item_{uuid}` | `ptc_item_f9e8d7c6-...` |
| Listing | `ptc_list_{uuid}` | `ptc_list_12345678-...` |
| Participant | `ptc_part_{uuid}` | `ptc_part_abcdef12-...` |
| Event | `ptc_evt_{uuid}` | `ptc_evt_98765432-...` |
| Campaign | `ptc_camp_{uuid}` | `ptc_camp_11223344-...` |

---

## Generator

```javascript
const PREFIXES = {
  product: "ptc_prod",
  item: "ptc_item",
  listing: "ptc_list",
  participant: "ptc_part",
  event: "ptc_evt",
};

export function generateCanonicalId(entityType) {
  return `${PREFIXES[entityType]}_${crypto.randomUUID()}`;
}

export function isValidCanonicalId(id, expectedType = null) {
  const pattern = /^ptc_(prod|item|list|part|evt)_[0-9a-f-]{36}$/;
  if (!pattern.test(id)) return false;
  if (expectedType) return id.startsWith(PREFIXES[expectedType]);
  return true;
}
```

---

## Legacy ID Mapping

```sql
CREATE TABLE id_mappings (
  canonical_id TEXT PRIMARY KEY,
  entity_type TEXT NOT NULL,
  source_system TEXT NOT NULL,
  source_id TEXT NOT NULL,
  UNIQUE(source_system, source_id, entity_type)
);
```

```javascript
export async function resolveToCanonical(env, sourceSystem, sourceId, entityType) {
  const mapping = await env.DB.prepare(
    "SELECT canonical_id FROM id_mappings WHERE source_system = ? AND source_id = ?"
  ).bind(sourceSystem, sourceId).first();

  if (mapping) return mapping.canonical_id;

  const canonicalId = generateCanonicalId(entityType);
  await env.DB.prepare(
    "INSERT INTO id_mappings VALUES (?, ?, ?, ?)"
  ).bind(canonicalId, entityType, sourceSystem, sourceId).run();

  return canonicalId;
}
```

---

## Source IDs in Records

```javascript
const record = {
  identity: {
    canonical_id: "ptc_item_a1b2c3d4-...",
    source_ids: {
      "consumer-wallet": "wallet_12345",
      "ebay": "ebay_item_98765",
    },
  },
};
```

---

## Anti-Patterns

- Using auto-increment IDs as references
- UUIDs without prefix
- Different ID formats per service
- Changing canonical IDs after creation
- Nullable canonical_id on core entities
