---
name: aurora-schema
description: >
  Aurora YAML schema analysis and editing. Validates field names, descriptions,
  types, and module semantics following DDD best practices. Trigger: When
  analyzing or editing *.aurora.yaml files, improving field naming, adding
  descriptions, or validating schema semantics.
license: MIT
metadata:
  author: aurora
  version: '1.1'
  auto_invoke:
    'Analyzing or editing *.aurora.yaml files, schema validation, field
    semantics'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Analyzing `*.aurora.yaml` files for quality and consistency
- Editing YAML schemas (creating, updating, or deleting fields)
- Validating field naming conventions and descriptions
- Ensuring module descriptions explain purpose and context
- Reviewing data type appropriateness

**Always combine with:**

- `aurora-cli` skill when regenerating after YAML changes
- `aurora-project-structure` skill for locating YAML files
- `conventional-commits` skill when committing schema changes

## Detailed References

- [Types & Varchar Standards](types-reference.md) — Type selection guide, byte-optimized varchar lengths
- [Patterns & Workflow](patterns-workflow.md) — Common patterns, analysis/editing workflows, change log template

---

## Critical Patterns

### Module Description (REQUIRED)

Every `*.aurora.yaml` must have a `description` property **before** `aggregateProperties:`.

```yaml
# ✅ CORRECT
version: 0.0.1
boundedContextName: iam
moduleName: permission
description: >
  Module containing the permissions associated with each bounded context, to be
  used to manage access to each API.
aggregateProperties:
  - name: id
```

**Description should explain:** What the module contains, what it's used for, how it relates to other modules.

---

### Mandatory Fields (REQUIRED in all modules)

**All modules MUST include these fields:**

1. `rowId` (after `id`) — `bigint`, autoIncrement, unique
2. `createdAt` (end) — `timestamp`, nullable
3. `updatedAt` (end) — `timestamp`, nullable
4. `deletedAt` (end) — `timestamp`, nullable

**Field order:** `id` → `rowId` → ... module fields ... → `createdAt` → `updatedAt` → `deletedAt`

---

### Field Naming Conventions

| Pattern               | Use For             | Examples                                |
| --------------------- | ------------------- | --------------------------------------- |
| `camelCase`           | All field names     | `firstName`, `orderDate`, `totalAmount` |
| `is*`, `has*`, `can*` | Boolean flags       | `isActive`, `hasChildren`, `canEdit`    |
| `*At`                 | Timestamps          | `createdAt`, `updatedAt`, `publishedAt` |
| `*Date`               | Date-only fields    | `birthDate`, `startDate`, `endDate`     |
| `*Id`                 | Foreign keys        | `authorId`, `categoryId`, `parentId`    |
| `sort`                | Display/UI ordering | `sort` (NOT `displayOrder`, `order`)    |

---

### Field Descriptions (MANDATORY)

**Every field MUST have a description that explains WHY, not WHAT:**

```yaml
# ❌ BAD
- name: price
  type: decimal
  description: The price of the book

# ✅ GOOD
- name: price
  type: decimal
  decimals: [10, 2]
  description: >
    Retail price in the store's base currency. Does not include taxes or
    discounts. Used as base for price calculations.
```

---

### ID Fields (CRITICAL RULE)

**Fields of type `id` MUST NOT have a `length` property.**

```yaml
# ✅ CORRECT
- name: id
  type: id
  primaryKey: true

# ❌ INCORRECT
- name: id
  type: id
  length: 36  # ← DELETE THIS
```

---

### Relationship Fields (CRITICAL RULE)

| Side                      | Has FK? | Use                                      |
| ------------------------- | ------- | ---------------------------------------- |
| Child/Many (invoice-line) | YES     | `type: id` + `relationship` block inside |
| Parent/One (invoice)      | NO      | `type: relationship` (navigation only)   |
| Many-to-many              | NO      | `type: relationship` + `pivot` config    |

**⚠️ NEVER define both `invoiceId` (type: id) AND `invoice` (type: relationship) in the SAME module.**

```yaml
# ✅ child.aurora.yaml - ONLY the FK field
- name: parentId
  type: id
  relationship:
    type: many-to-one
    field: parent
    aggregateName: MyParent
    modulePath: my-context/parent

# ✅ parent.aurora.yaml - ONLY the navigation property
- name: children
  type: relationship
  relationship:
    type: one-to-many
    aggregateName: MyChild
    modulePath: my-context/child
    key: parentId
```

---

### Cross-Module Consistency

Use the same field names across ALL modules:

```yaml
- name: id        # Not: ID, _id, uuid
- name: createdAt # Not: created, createdDate
- name: updatedAt # Not: updated, modifiedAt
- name: deletedAt # Not: deleted, removedAt
- name: isActive  # Not: active, enabled
```

---

### Index Names (63-char limit) — MANDATORY VALIDATION

PostgreSQL limits index names to **63 characters**. Aurora generates: `{boundedContext}_{module}_{fieldName}` (snake_case).

**Every time you add `index: index` or `index: unique`, calculate the generated index name length.**

```
index_name = snake_case(boundedContextName) + "_" + snake_case(moduleName) + "_" + snake_case(fieldName)
```

**If length > 63 → MUST add `indexName` property with abbreviated name.**

```yaml
- name: administrativeAreaLevel1Id
  type: id
  index: index
  indexName: bpp_partner_addr_admin_area_lvl1_id  # < 63 chars
```

**Abbreviation pattern:** `{BC_abbrev}_{short_module}_{short_field}`

| Bounded Context           | Abbrev |
| ------------------------- | ------ |
| `production-planning`     | `pp`   |
| `business-partner-portal` | `bpp`  |
| `common`                  | `cmn`  |

---

## Decision Trees

### What Type Should This Field Be?

```
Is it a UUID identifier? ────YES───> type: id (NO length!)
      │
      NO
      │
Is it true/false? ────YES───> type: boolean (use is*/has*/can* prefix)
      │
      NO
      │
Is it money? ────YES───> type: decimal with decimals: [12, 2]
      │
      NO
      │
Fixed set of options? ────YES───> type: enum with enumOptions
      │
      NO
      │
Date and time? ────YES───> type: timestamp
      │
      NO
      │
Short text (< 255 chars)? ────YES───> type: varchar with maxLength
      │
      NO
      │
Long text? ────YES───> type: text
```

### Should I Edit or Just Analyze?

```
User explicitly requested edit? ────YES───> Edit mode
      │
      NO → Analysis mode (generate report)
```

---

## Anti-Patterns to Avoid

| ❌ Don't                                  | ✅ Do                                             |
| ----------------------------------------- | ------------------------------------------------- |
| Skip module description                   | Always add description before aggregateProperties |
| Skip mandatory fields (rowId, timestamps) | Always include rowId, createdAt, updatedAt, deletedAt |
| Use abbreviations (dt, qty, amt)          | Use full words (createdAt, quantity, amount)       |
| Name booleans without prefix (active)     | Use semantic prefix (isActive, hasPermission)     |
| Add `length` to `id` type fields          | Never specify length for id type                  |
| Write "The price" as description          | Explain context: "Retail price in base currency..." |
| Use `float` for money                     | Always use `decimal` with proper scale            |
| Duplicate relationship definitions        | FK side uses `type: id`, inverse uses `type: relationship` |

---

## Resources

- **Aurora Docs**: Check `aurora-cli` skill for regeneration commands
- **Project Structure**: Use `aurora-project-structure` skill to locate YAMLs

## Related Skills

| Skill                      | When to Use Together                                          |
| -------------------------- | ------------------------------------------------------------- |
| `aurora-cli`               | After editing YAML, regenerate with `aurora load back module` |
| `aurora-project-structure` | To locate YAML files in correct directories                   |
| `conventional-commits`     | When committing schema changes                                |
| `aurora-cqrs`              | Understanding how YAML generates commands/queries             |
