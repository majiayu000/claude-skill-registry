---
name: migration-ready-schema
description: Data-model rules that make a schema importable from day one, so the migration-import-engineer is never blocked on missing columns. Every SMB Product-Builder product must let a customer bring their data from an incumbent (ServiceTitan/Toast/Mindbody/Shopify) — that requires provenance (source_ref) and rollback (import_batch_id) on importable entities, and modelling real-world actors as entities rather than inline fields. Applied by architect when writing the data model in ARCH-{slug}.md, and checked by migration-import-engineer. One cheap rule set prevents the migration↔architecture seam gap from recurring across all 40 products.
when_to_use: |
  Apply when:
  - architect writes the Data contracts / data model section of ARCH-{slug}.md
  - migration-import-engineer verifies the destination schema can satisfy its
    idempotency + rollback invariants
  - any new entity is added that could be populated from an import or a third-party sync
  Do NOT apply to purely ephemeral / derived tables (caches, materialized views) that are
  never imported into.
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/migration/**"
---

# Migration-ready schema — importable from day one

Every SMB product's wedge is **low switching cost** — the customer brings their data from
the incumbent. If the schema can't receive that data idempotently and reversibly, the
`migration-import-engineer` blocks and the wedge is a slogan. These rules are cheap at
design time and impossible to retrofit cleanly. **Apply them to the data model in ARCH,
before any import is designed.**

## The three rules (the ones that actually block imports)

### 1. Importable entities carry `source_ref` (provenance)
Any entity that can be populated from an incumbent export or a third-party sync gets a
nullable, **unique** `source_ref` column:

```
source_ref  text  UNIQUE NULL   -- e.g. "servicetitan:pricebook:8842"
```

- It is the **dedup key** for idempotent re-import (re-running an export never duplicates).
- Namespaced `{source}:{type}:{id}` so two incumbents can't collide.
- Nullable because natively-created rows have no source.

### 2. Importable entities carry `import_batch_id` (rollback)
```
import_batch_id  uuid  NULL  -- tags every row written by one import run
```
Rollback = delete where `import_batch_id = ?`. Without it there is no undo, and an import
with no undo is one a user will never trust enough to run.

### 3. Model real-world actors as entities, not inline fields
A customer, contact, vendor, member, or tenant is an **entity with its own table**, even if
v1 only stores a name + phone. Reason: imports populate these **before** the dependent
records (quotes, orders, bookings) exist — an inline `customer_name` field on `Quote` has
**nowhere to land** an imported customer. Inline-actor is the single most common migration
blocker.

```
-- WRONG (blocks import):  Quote(... customer_contact text)
-- RIGHT:                   CustomerContact(id, ..., source_ref, import_batch_id)
                            Quote(... customer_contact_id → CustomerContact.id)
```

## Supporting rules (cheap, prevent silent data loss)

- **Money in integer minor units** (`*_cents`), never float — incumbent exports carry exact
  amounts; floats corrupt them.
- **Timestamps carry the source timezone** (store UTC + offset, or tz-aware) — exports use
  local times; ambiguous `MM/DD` and naive datetimes lose data.
- **Infra tables for integration bookkeeping exist in the model**: `outbound_message`
  (idempotent send guard), `processed_webhook_events` (event dedup). The
  integrations-engineer relies on them; enumerate them so they aren't a surprise.

## Checklist (architect runs this before finalizing the data model)

```
For each entity in the data model:
- [ ] Can it be imported from an incumbent or third-party? If yes → has source_ref + import_batch_id
- [ ] Is it a real-world actor (customer/contact/vendor/member)? If yes → it is its own entity, not an inline field
- [ ] Money fields integer minor units? Timestamps tz-aware?
- [ ] Listed the infra tables (outbound_message, processed_webhook_events) the integrations layer needs?
```

A data model that passes this checklist hands `migration-import-engineer` a destination it
can import into idempotently and reversibly — no blocked seam.
