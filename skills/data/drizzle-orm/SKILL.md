---
name: drizzle-orm
description: Enforces project Drizzle ORM coding conventions when creating or modifying database queries, schemas, and migrations. This skill ensures consistent patterns for query structure, type safety, permission filtering, pagination, resilience, and database operations.
---

# Drizzle ORM Skill

## Purpose

This skill enforces the project Drizzle ORM coding conventions automatically during database query development. It ensures consistent patterns for query structure, type safety, permission filtering, pagination, circuit breaker resilience, and database operations.

## Activation

This skill activates when:

- Creating new query files in `src/lib/queries/`
- Modifying database schema in `src/lib/db/schema/`
- Writing database migrations
- Working with Drizzle query builders
- Implementing permission filtering or soft delete logic

## Workflow

1. Detect Drizzle ORM work (file imports from `drizzle-orm` or path contains `queries/` or `db/schema`)
2. Load `references/Drizzle-ORM-Conventions.md`
3. Generate/modify code following all conventions
4. Scan for violations of query patterns
5. Auto-fix all violations (no permission needed)
6. Report fixes applied

## Key Patterns

### Query Classes

- Extend `BaseQuery` class for all query classes
- Use `QueryContext` for database instance and user context
- Use `this.getDbInstance(context)` for database access
- Apply `this.applyPagination(options)` for list queries
- Use `this.combineFilters()` to combine multiple SQL conditions

### Context Types

- `createPublicQueryContext()` - public read operations (isPublic = true)
- `createUserQueryContext(userId)` - authenticated user operations
- `createProtectedQueryContext(requiredUserId)` - owner-only operations
- `createAdminQueryContext(adminUserId)` - admin access to all content

### Permission Filtering

- Use `this.buildBaseFilters(isPublicCol, userIdCol, deletedAtCol, context)` for permission + soft delete
- Import standalone filters from `@/lib/queries/base/permission-filters`:
  - `buildPermissionFilter()` - handles public/user/owner visibility
  - `buildSoftDeleteFilter()` - handles deletedAt filtering (returns `isNull(deletedAt)`)
  - `buildOwnershipFilter()` - handles owner-only access
  - `combineFilters()` - combines multiple SQL conditions with AND

### Resilience

- Use `this.executeWithRetry(operation, operationName)` for circuit breaker + retry logic
- Use `this.executeWithRetryDetails(operation, operationName)` when you need retry metadata

### Return Values

- Single item: `T | null` (return `null` for not found)
- List: `Array<T>` (return `[]` for empty)
- Count: `number` (return `0` for none)
- Boolean check: `boolean` (return `false` for not found)
- Map: `Map<K, V>` (return `new Map()` for empty)

## Anti-Patterns to Avoid

1. **Never access `db` directly** - Always use `this.getDbInstance(context)`
2. **Never skip permission filters** - Always use `buildBaseFilters` for user-visible data
3. **Never return undefined** - Return `null` for missing single items
4. **Never use raw strings in queries** - Use parameterized queries via Drizzle
5. **Never skip pagination limits** - Always apply `applyPagination`
6. **Never hard delete** - Use soft delete with `deletedAt` timestamp column
7. **Never ignore circuit breaker** - Use `executeWithRetry` for external calls

## References

- `references/Drizzle-ORM-Conventions.md` - Complete Drizzle ORM conventions
