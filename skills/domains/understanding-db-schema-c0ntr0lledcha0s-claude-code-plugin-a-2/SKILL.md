---
name: understanding-db-schema
version: 1.0.0
description: >
  Deep expertise in Logseq's Datascript database schema. Auto-invokes when users ask about
  Logseq DB schema, Datascript attributes, built-in classes, property types, entity relationships,
  schema validation, or the node/block/page data model. Provides authoritative knowledge of
  the DB graph architecture.
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# Understanding Logseq DB Schema

## When to Use This Skill

This skill auto-invokes when:
- User asks about Logseq's database schema or Datascript
- Questions about built-in classes (Tag, Page, Task, Property, etc.)
- Property type system questions (:default, :number, :date, :checkbox, etc.)
- Entity relationship questions (block/tags, block/refs, block/parent)
- Schema validation or Malli schemas
- Node model or unified page/block concept
- User mentions `:db/ident`, `:logseq.class/*`, or `:logseq.property/*`

**Reference Material**: See `{baseDir}/references/built-in-classes.md` for complete class hierarchy.

You have expert knowledge of Logseq's database schema architecture.

## Datascript Foundation

Logseq DB graphs are built on **Datascript**, a Clojure/ClojureScript in-memory database that supports:
- Entity-Attribute-Value (EAV) data model
- Datalog queries
- Schema-driven attribute definitions

### Attribute Types

```clojure
;; Value types
:db.type/ref      ; References to other entities
:db.type/string   ; Text values
:db.type/long     ; Integer numbers
:db.type/double   ; Floating point numbers
:db.type/boolean  ; True/false
:db.type/instant  ; Timestamps
:db.type/keyword  ; Clojure keywords
:db.type/uuid     ; UUIDs

;; Cardinality
:db.cardinality/one   ; Single value
:db.cardinality/many  ; Multiple values (set)
```

### Core Reference Attributes

```clojure
:block/tags    ; Classes/tags assigned to the entity
:block/refs    ; Outgoing references to other entities
:block/alias   ; Alternative names for a page
:block/parent  ; Parent block in hierarchy
:block/page    ; Page containing this block
```

## Built-in Classes Hierarchy

```
:logseq.class/Root
├── :logseq.class/Page
├── :logseq.class/Tag (classes themselves)
├── :logseq.class/Property
├── :logseq.class/Task
│   └── Status, Priority, Deadline, Scheduled
├── :logseq.class/Query
├── :logseq.class/Asset
├── :logseq.class/Code-block
└── :logseq.class/Template
```

All non-Root classes extend `:logseq.class/Root` via `:logseq.property.class/extends`.

## Property Type System

| Type | Validator | Closed Values | Use Case |
|------|-----------|---------------|----------|
| `:default` | `text-entity?` | ✅ | Text blocks with titles |
| `:number` | `number-entity?` | ✅ | Numeric values |
| `:date` | `date?` | ❌ | Journal page entities |
| `:datetime` | `datetime?` | ❌ | Time-based scheduling |
| `:checkbox` | `boolean?` | ❌ | Toggle properties |
| `:url` | `url-entity?` | ✅ | URL strings or macros |
| `:node` | `node-entity?` | ❌ | Block/page references |
| `:class` | `class-entity?` | ❌ | Class entities |

## Property Configuration Keys

```clojure
{:db/ident :user.property/my-property
 :logseq.property/type :default           ; Property type
 :logseq.property/cardinality :one        ; :one or :many
 :logseq.property/hide? false             ; Hide by default
 :logseq.property.ui/position :properties ; UI placement
 :logseq.property/closed-values [...]     ; Restricted choices
 :logseq.property/schema-classes [...]    ; Associated classes
 :block/title "My Property"}              ; Display name
```

## Property Namespaces

| Namespace | Purpose | Example |
|-----------|---------|---------|
| `logseq.property` | Core system properties | `:logseq.property/type` |
| `logseq.property.class` | Class-related | `:logseq.property.class/extends` |
| `logseq.property.table` | Table views | `:logseq.property.table/columns` |
| `user.property` | User-defined | `:user.property/author` |
| `plugin.property` | Plugin-defined | `:plugin.property/custom` |

## Schema Versioning

```clojure
;; Version format
{:major 65 :minor 12}

;; Stored in
:logseq.kv/schema-version  ; Graph's current version
db-schema/version          ; Expected version
```

Migrations handle schema upgrades between versions (65.0 → 65.12+).

## Malli Validation Flow

1. **Entity transformation**: Properties → `[property-map value]` tuples
2. **Schema dispatch**: Validation dispatches on `:logseq.property/type`
3. **Value validation**: Individual values checked against type schemas
4. **Cardinality handling**: Automatic `:many` vs `:one` handling
5. **Transaction validation**: `validate-tx-report` ensures integrity

## Node Model

### Unified Node Concept

In DB version, **nodes** represent both pages and blocks:

```
Node
├── Page (unique by tag combination)
│   ├── Journal pages (#Journal)
│   ├── Regular pages (#Page)
│   └── Class pages (#Tag)
└── Block (within pages)
    ├── Content blocks
    ├── Property blocks
    └── Convertible to page via #Page tag
```

### Page Uniqueness

Pages are unique by their tag combination:
- "Apple #Company" ≠ "Apple #Fruit"
- Both can coexist as separate entities

## Common Patterns

### Creating a Custom Class

```clojure
;; Define a class with properties
{:db/ident :user.class/Book
 :block/tags [:logseq.class/Tag]
 :block/title "Book"
 :logseq.property.class/extends :logseq.class/Root
 :logseq.property/schema-classes
   [:user.property/author
    :user.property/isbn
    :user.property/rating]}
```

### Creating a Typed Property

```clojure
;; Number property with choices
{:db/ident :user.property/rating
 :block/title "Rating"
 :logseq.property/type :number
 :logseq.property/cardinality :one
 :logseq.property/closed-values [1 2 3 4 5]}
```

## Resources

When users need more information, reference:
- [Logseq DB Documentation](https://github.com/logseq/docs/blob/master/db-version.md)
- [Database Schema DeepWiki](https://deepwiki.com/logseq/logseq/4.2-views-and-tables)
- [Logseq DB Unofficial FAQ](https://discuss.logseq.com/t/logseq-db-unofficial-faq/32508)
