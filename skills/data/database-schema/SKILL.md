---
name: database-schema
description: Enforces project database schema conventions when creating or modifying Drizzle ORM table definitions, including constraints, indexes, relations, and column patterns. This skill should be used proactively whenever working with schema files to ensure consistent schema design for PostgreSQL with Neon serverless.
---

# Database Schema Conventions Enforcer

## Purpose

This skill enforces the project database schema conventions automatically during schema development. It ensures consistent patterns for table definitions, constraints, indexes, foreign keys, and column naming in Drizzle ORM with PostgreSQL (Neon serverless).

## When to Use This Skill

Use this skill proactively in the following scenarios:

- Creating new schema files in `src/lib/db/schema/`
- Modifying existing table definitions
- Adding indexes or constraints
- Defining foreign key relationships
- Working with Drizzle ORM schema syntax (`drizzle-orm/pg-core`)
- Reviewing or fixing schema issues
- Any task involving database structure changes

**Important**: This skill should activate automatically without explicit user request whenever schema work is detected.

## How to Use This Skill

### 1. Load Conventions Reference

Before creating or modifying any schema, load the complete conventions document:

```
Read references/Database-Schema-Conventions.md
```

This reference contains the authoritative schema standards including:

- Table definition templates
- Column conventions and patterns
- Foreign key relationship rules
- Check constraint patterns
- Index strategy (single, composite, covering, GIN)
- Junction table patterns
- Column naming conventions
- Constants usage

### 2. Apply Conventions During Development

When writing schema code, ensure strict adherence to all conventions:

**Table Structure**:

- Use `pgTable` with constraints/indexes in the callback function
- Order columns alphabetically within the column definition object
- Always include standard columns: `id`, `createdAt`, `updatedAt`
- Include soft delete column when applicable: `deletedAt` (timestamp, null = not deleted)

**Column Patterns**:

- UUID primary keys with `defaultRandom()` (never auto-increment)
- Use `SCHEMA_LIMITS` constants for all varchar lengths
- Use `DEFAULTS` constants for default values
- Use `varchar` with explicit length (never `text`)
- Timestamps with `defaultNow().notNull()`

**Foreign Key Rules**:

- `cascade` - when parent owns child (delete children with parent)
- `set null` - for optional relationships
- `restrict` - to prevent orphans

**Index Strategy**:

- Single column indexes for frequently filtered columns
- Composite indexes for multi-column WHERE conditions
- Covering indexes for common queries (avoid table lookups)
- Descending indexes for ORDER BY ... DESC queries
- GIN indexes for text search and JSONB columns
- Always index foreign key columns

**Check Constraints**:

- Validate numeric ranges (year, positive values)
- Validate non-empty required strings
- Validate date logic (created <= updated)
- Validate non-negative counters

### 3. Automatic Convention Enforcement

After generating or modifying schema code, immediately perform automatic validation and correction:

1. **Scan for violations**: Review the generated code against all conventions from the reference document
2. **Identify issues**: Create a mental checklist of any violations found:
   - Missing standard columns (id, createdAt, updatedAt)
   - Hardcoded lengths instead of `SCHEMA_LIMITS`
   - Hardcoded defaults instead of `DEFAULTS`
   - Missing foreign key indexes
   - Incorrect cascade rules
   - Missing check constraints
   - Using `text` instead of `varchar`
   - Using auto-increment instead of UUID
   - Missing soft delete column (`deletedAt`) when needed
   - Incorrect column naming (snake_case in DB, camelCase in code)

3. **Fix automatically**: Apply corrections immediately without asking for permission:
   - Add missing standard columns
   - Replace hardcoded values with constants
   - Add missing indexes for foreign keys
   - Add appropriate check constraints
   - Fix column type issues
   - Reorder columns alphabetically
   - Add missing soft delete column (`deletedAt`)

4. **Verify completeness**: Ensure all conventions are satisfied before presenting code to user

### 4. Reporting

After automatically fixing violations, provide a brief summary:

```
✓ Database schema conventions enforced:
  - Added missing timestamp columns (createdAt, updatedAt)
  - Replaced hardcoded length with SCHEMA_LIMITS.ENTITY.NAME.MAX
  - Added soft delete column (deletedAt)
  - Added foreign key index: collection_user_id_idx
  - Added check constraint: collection_name_not_empty
```

**Do not ask for permission to apply fixes** - the skill's purpose is automatic enforcement.

## Convention Categories

The complete conventions are detailed in `references/Database-Schema-Conventions.md`. Key categories include:

1. **File Structure** - Schema file organization patterns
2. **Table Definition Template** - Standard pgTable structure
3. **Column Conventions** - Standard, soft delete, counter, visibility columns
4. **String Columns** - varchar with SCHEMA_LIMITS
5. **Numeric Columns** - Decimal precision, integer patterns
6. **Foreign Key Patterns** - Cascade, set null, restrict rules
7. **Check Constraints** - Numeric, string, date validation
8. **Index Strategy** - Single, composite, covering, descending, GIN
9. **Junction Tables** - Many-to-many relationship patterns
10. **Column Naming** - snake_case DB, camelCase code conventions

## Anti-Patterns to Avoid

1. **Never hardcode lengths** - Use `SCHEMA_LIMITS` constants
2. **Never hardcode defaults** - Use `DEFAULTS` constants
3. **Never skip timestamps** - Always include `createdAt`, `updatedAt`
4. **Never use auto-increment** - Use UUID primary keys
5. **Never skip indexes** - Index all foreign keys and filter columns
6. **Never cascade delete without consideration** - Choose appropriate delete behavior
7. **Never skip check constraints** - Validate data at database level
8. **Never use `text` type** - Use `varchar` with explicit length

## Important Notes

- **Automatic enforcement**: Apply fixes immediately without requesting permission
- **No compromises**: All conventions must be followed strictly
- **Reference first**: Always load the conventions reference before working with schema code
- **Complete validation**: Check all aspects of the conventions, not just obvious violations
- **Proactive application**: Use this skill automatically when schema work is detected, even if user doesn't mention conventions

## Workflow Summary

```
1. Detect schema work (create/modify files in db/schema/)
2. Load references/Database-Schema-Conventions.md
3. Generate or modify schema code following all conventions
4. Scan generated code for any violations
5. Automatically fix all violations found
6. Present corrected code to user with brief summary of fixes applied
```

This workflow ensures every database schema in the project project maintains consistent, high-quality definitions that follow all established conventions.
