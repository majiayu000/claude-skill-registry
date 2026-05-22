---
name: aurora-schema
description: >
  Aurora YAML schema analysis and editing. Validates field names, descriptions, types, and module semantics following DDD best practices.
  Trigger: When analyzing or editing *.aurora.yaml files, improving field naming, adding descriptions, or validating schema semantics.
license: MIT
metadata:
  author: aurora
  version: "1.0"
  auto_invoke: "Analyzing or editing *.aurora.yaml files, schema validation, field semantics"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:
- Analyzing `*.aurora.yaml` files for quality and consistency
- Editing YAML schemas (creating, updating, or deleting fields)
- Validating field naming conventions and descriptions
- Ensuring module descriptions explain purpose and context
- Reviewing data type appropriateness
- Checking cross-module consistency

**Always combine with:**
- `aurora-cli` skill when regenerating after YAML changes
- `aurora-project-structure` skill for locating YAML files
- `conventional-commits` skill when committing schema changes

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
    Module containing the permissions associated with each bounded context, to be used
    to manage access to each API.
aggregateProperties:
  - name: id
```

```yaml
# ❌ INCORRECT - Missing description
version: 0.0.1
boundedContextName: iam
moduleName: permission
aggregateProperties:
  - name: id
```

**Description should explain:**
1. What the module contains (main entity)
2. What it's used for (purpose)
3. How it relates to other modules in the bounded context

---

### Field Naming Conventions

| Pattern | Use For | Examples |
|---------|---------|----------|
| `camelCase` | All field names | `firstName`, `orderDate`, `totalAmount` |
| `is*`, `has*`, `can*` | Boolean flags | `isActive`, `hasChildren`, `canEdit` |
| `*At` | Timestamps | `createdAt`, `updatedAt`, `publishedAt` |
| `*Date` | Date-only fields | `birthDate`, `startDate`, `endDate` |
| `*Id` | Foreign keys | `authorId`, `categoryId`, `parentId` |

**Anti-patterns:**

```yaml
# ❌ BAD
- name: stat          # → status
- name: dt            # → createdAt
- name: qty           # → quantity
- name: active        # → isActive (boolean prefix)
- name: author        # → authorId (if it's a foreign key)
  type: id

# ✅ GOOD
- name: status
- name: createdAt
- name: quantity
- name: isActive
- name: authorId
  type: id
```

---

### Field Descriptions (MANDATORY)

**Every field MUST have a description that explains WHY, not WHAT:**

```yaml
# ❌ BAD - States the obvious
- name: price
  type: decimal
  description: The price of the book

# ✅ GOOD - Explains context and usage
- name: price
  type: decimal
  decimals: [10, 2]
  description: >
      Retail price in the store's base currency (configured in settings). Does
      not include taxes or discounts. Used as base for price calculations.
```

**Include:**
- Business context and constraints
- Default values and behavior
- Validation rules
- Examples for complex formats

```yaml
- name: isbn
  type: varchar
  maxLength: 17
  index: unique
  description: >
      International Standard Book Number in ISBN-13 format. Must be unique
      across all books. Validated against checksum algorithm. Example:
      978-3-16-148410-0
```

---

### Type Selection Guide

| Use Case | Type | Configuration | Notes |
|----------|------|---------------|-------|
| UUID identifiers | `id` | NO `length` property | **CRITICAL: Never add `length` to `id` type** |
| Short text | `varchar` | `maxLength: N` | Names, titles, codes |
| Long text | `text` | - | Descriptions, content |
| Fixed-length text | `char` | `length: N` | Country codes, currency |
| Passwords | `password` | - | Auto-hashed by Aurora |
| Integer counters | `int` | - | Standard integers |
| Large numbers | `bigint` | - | > 2 billion |
| Small numbers | `smallint` | - | 0-255 range |
| Money/decimals | `decimal` | `decimals: [precision, scale]` | Never use float for money |
| Approximate | `float` | - | Scientific only |
| Date + time | `timestamp` | - | Most common |
| Date only | `date` | - | Birthdays, deadlines |
| True/false | `boolean` | - | Use is*/has*/can* prefix |
| Fixed options | `enum` | `enumOptions: [...]` | Document each option |
| Structured data | `json`, `jsonb` | - | Use jsonb for PostgreSQL |

---

### Varchar Length Standards (Byte-Optimized)

**IMPORTANT: When defining varchar fields, ALWAYS use one of these standard lengths.**

These lengths are optimized for PostgreSQL byte storage efficiency:

| Length | Use Case Examples                                      | Notes                                    |
|--------|--------------------------------------------------------|------------------------------------------|
| 1      | Single character flags, gender (M/F)                   | Minimum length                           |
| 4      | Country codes (US, ES), file extensions                | ISO codes                                |
| 8      | Short codes, abbreviations                             | Currency codes with margin               |
| 16     | Short identifiers, codes                               | 2^4 bytes                                |
| 36     | UUIDs in string format                                 | Standard UUID length (8-4-4-4-12)        |
| 64     | Short names, usernames, slugs                          | 2^6 bytes                                |
| 128    | Names, titles, email addresses                         | 2^7 bytes                                |
| 255    | Standard text fields                                   | 2^8 - 1 (single byte length indicator)   |
| 382    | Medium text, short descriptions                        | 1.5 × 255 (optimized for UTF-8)          |
| 510    | Longer descriptions, addresses                         | 2 × 255                                  |
| 1022   | Long text that needs indexing                          | ~4 × 255 (max recommended for indexes)   |
| 2046   | URLs, very long text with length limit                 | Max practical URL length (~2048 limit)   |

**Why these specific lengths?**

1. **Byte alignment**: PostgreSQL stores varchar with a length prefix. These values optimize storage blocks.
2. **Index compatibility**: Lengths ≤ 2046 can be indexed efficiently in PostgreSQL.
3. **UTF-8 consideration**: Lengths account for multi-byte characters (up to 4 bytes per char).
4. **URL compatibility**: 2046 is just under the 2048 practical limit for URLs (IE/Edge limit, SEO sitemaps).

**Selection guide:**

```yaml
# ❌ Bad - arbitrary lengths
- name: username
  type: varchar
  maxLength: 50

- name: description
  type: varchar
  maxLength: 500

# ✅ Good - byte-optimized lengths
- name: username
  type: varchar
  maxLength: 64
  description: >
      User's display name. Max 64 characters.

- name: description
  type: varchar
  maxLength: 510
  description: >
      Brief description of the item. Max 510 characters.
```

**Quick reference for common fields:**

| Field Type           | Recommended Length |
|----------------------|--------------------|
| UUID as string       | 36                 |
| Username             | 64                 |
| Email                | 128                |
| Name/Title           | 128                |
| Phone                | 64                 |
| Short description    | 255                |
| Address line         | 255                |
| Medium description   | 510                |
| Long description     | 1022               |
| URL/Link             | 2046               |
| Slug                 | 2046               |

---

### ID Fields (CRITICAL RULE)

**Fields of type `id` MUST NOT have a `length` property.**

```yaml
# ✅ CORRECT
- name: id
  type: id
  primaryKey: true
  description: >
      Unique identifier for the record. UUID v4 format, generated automatically
      on creation.

# ❌ INCORRECT - Remove length property
- name: id
  type: id
  length: 36  # ← DELETE THIS
  primaryKey: true
```

---

### Cross-Module Consistency

Use the same field names across ALL modules for common concepts:

```yaml
# Standard across all modules:
- name: id             # Not: ID, _id, uuid, identifier
- name: createdAt      # Not: created, createdDate, createTime
- name: updatedAt      # Not: updated, modifiedAt, updateTime
- name: deletedAt      # Not: deleted, removedAt, deletionDate
- name: isActive       # Not: active, enabled, status
```

---

## Analysis Workflow

### 1. Locate YAML Files

```bash
# Find all Aurora YAMLs
fd -e yaml -e yml aurora

# Find specific module
fd "book.aurora.yaml"
```

### 2. Read and Analyze

Check for:
- [ ] Module has `description` before `aggregateProperties`
- [ ] All fields have meaningful descriptions
- [ ] Field names follow conventions (camelCase, boolean prefixes)
- [ ] No `id` type fields have `length` property
- [ ] Descriptions explain WHY, not WHAT
- [ ] Enum values are documented
- [ ] Types are appropriate for use case
- [ ] Consistency with similar modules

### 3. Generate Report

```markdown
## Analysis of [module].aurora.yaml

### Summary
- Total fields: X
- Fields without description: Y
- Naming improvements needed: Z
- Module has description: Yes/No

### Module Description ❌ (if missing)
**Suggested:**
```yaml
description: >
    [Purpose and role within bounded context]
```

### Fields Without Description ❌
| Field | Type | Suggested Description |
|-------|------|----------------------|
| ... | ... | ... |

### Naming Improvements ⚠️
| Current | Suggested | Reason |
|---------|-----------|--------|
| dt | createdAt | Ambiguous abbreviation |
| active | isActive | Boolean convention |

### Type Issues ⚠️
| Field | Issue | Fix |
|-------|-------|-----|
| id | Has `length: 36` | Remove `length` property |
```

---

## Editing Workflow

### Creating Fields

```yaml
- name: publishedAt
  type: timestamp
  nullable: true
  description: >
      Timestamp when the book was published. NULL indicates unpublished.
      Automatically set when status changes to PUBLISHED.
```

**Checklist:**
- [ ] Name follows camelCase convention
- [ ] Boolean names have is*/has*/can* prefix
- [ ] Type is appropriate for use case
- [ ] Description explains context and usage
- [ ] No `length` property on `id` type fields
- [ ] Consistent with similar fields in other modules

### Editing Fields

**Only modify requested attributes:**

```yaml
# Before
- name: status
  type: varchar

# After (changing to enum)
- name: status
  type: enum
  enumOptions: [DRAFT, PUBLISHED, ARCHIVED]
  description: >
      Current publication status. DRAFT: Not ready. PUBLISHED: Available to
      readers. ARCHIVED: Preserved but no longer available.
```

### Deleting Fields

**Always check dependencies first:**

```bash
# Search for field references
rg "fieldName" cliter/ -g "*.aurora.yaml"
```

If field is referenced in relationships:
1. Alert the user
2. Confirm deletion
3. Document affected modules

---

## Common Patterns

### Status Fields with Enum

```yaml
- name: status
  type: enum
  enumOptions: [PENDING, APPROVED, REJECTED, CANCELLED]
  defaultValue: PENDING
  description: >
      Workflow status. PENDING: Awaiting review. APPROVED: Accepted and active.
      REJECTED: Denied (see rejectionReason). CANCELLED: Withdrawn by user.
```

### Soft Delete Pattern

```yaml
- name: deletedAt
  type: timestamp
  nullable: true
  description: >
      Soft delete timestamp. NULL means active record. When set, record is
      excluded from normal queries. Enables audit trail and recovery.
```

### Money Fields

```yaml
- name: amount
  type: decimal
  decimals: [12, 2]
  description: >
      Monetary amount in smallest currency unit with 2 decimal places.
      Currency determined by currencyCode field.

- name: currencyCode
  type: char
  length: 3
  description: >
      ISO 4217 currency code (USD, EUR, GBP). Must be valid and supported.
```

### URL-Friendly Slugs

```yaml
- name: slug
  type: varchar
  maxLength: 2046
  index: unique
  description: >
      URL-friendly identifier. Lowercase, hyphenated. Auto-generated from name
      if not provided. Example: "my-awesome-product". Max 2046 chars for URL
      compatibility.
```

---

## Commands

```bash
# Find all Aurora YAMLs
fd -e yaml aurora

# Search for fields without descriptions
rg -A1 "^  - name:" cliter/ -g "*.aurora.yaml" | rg -v "description:"

# Find id fields with length (incorrect)
rg -A2 "type: id" cliter/ -g "*.aurora.yaml" | rg "length:"

# Check for missing module descriptions
rg -L "^description:" cliter/ -g "*.aurora.yaml"

# Search for field usage across modules
rg "fieldName" cliter/ -g "*.aurora.yaml"

# Validate YAML syntax
yamllint cliter/**/*.aurora.yaml
```

---

## Decision Trees

### Should I Edit or Just Analyze?

```
User explicitly requested edit? ────YES───> Edit mode
      │
      NO
      │
Is this an analysis request? ────YES───> Analysis mode
      │
      NO
      │
Ask user for clarification
```

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
      │
      NO
      │
Review use case and choose appropriate type
```

---

## Anti-Patterns to Avoid

| ❌ Don't | ✅ Do |
|----------|-------|
| Skip module description | Always add description before aggregateProperties |
| Use abbreviations (dt, qty, amt) | Use full words (createdAt, quantity, amount) |
| Name booleans without prefix (active) | Use semantic prefix (isActive, hasPermission) |
| Add `length` to `id` type fields | Never specify length for id type |
| Write "The price" as description | Explain context: "Retail price in base currency..." |
| Mix naming styles across modules | Use consistent names (createdAt everywhere) |
| Use `float` for money | Always use `decimal` with proper scale |
| Leave enum values undocumented | Explain what each enum option means |

---

## Change Log Template

When making modifications:

```markdown
## Schema Changes - 2026-01-17

### tesla/model.aurora.yaml

#### Created
- `isActive` (boolean) - Flag to indicate if model is currently available

#### Modified
- `status`: Changed type from `varchar` to `enum` with options [ACTIVE, INACTIVE, DISCONTINUED]
- Module: Added `description` property explaining module purpose

#### Deleted
- `legacyCode` (varchar) - Removed after confirming no dependencies

#### Fixed
- `id`: Removed `length: 36` property (not needed for id type)
```

---

## Resources

- **Aurora Docs**: Check `aurora-cli` skill for regeneration commands
- **Project Structure**: Use `aurora-project-structure` skill to locate YAMLs
- **YAML Syntax**: Run `yamllint` to validate syntax
- **Cross-References**: Search with `rg` to find field usage

---

## Related Skills

| Skill | When to Use Together |
|-------|---------------------|
| `aurora-cli` | After editing YAML, regenerate with `aurora load back module` |
| `aurora-project-structure` | To locate YAML files in correct directories |
| `conventional-commits` | When committing schema changes |
| `typescript` | When reviewing generated TypeScript from YAML |
| `aurora-cqrs` | Understanding how YAML generates commands/queries |
