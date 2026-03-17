---
name: facade-layer
description: Enforces project facade layer coding conventions when creating or modifying business logic facades. This skill ensures consistent patterns for transaction handling, error management, cache integration, query coordination, and cross-service orchestration.
---

# Facade Layer Skill

## Purpose

This skill enforces the project facade layer coding conventions automatically during business logic development. It ensures consistent patterns for transaction handling, error management, cache integration, query coordination, and cross-service orchestration with Sentry monitoring.

## Activation

This skill activates when:

- Creating new facade files in `src/lib/facades/`
- Modifying existing facade files (`.facade.ts`)
- Implementing business logic that coordinates multiple queries
- Working with database transactions
- Coordinating between multiple services or facades

## Workflow

1. Detect facade work (file path contains `facades/` or class name ends with `Facade`)
2. Load `references/Facade-Layer-Conventions.md`
3. Generate/modify code following all conventions
4. Scan for violations of facade patterns
5. Auto-fix all violations (no permission needed)
6. Report fixes applied

## Key Patterns (REQUIRED)

### Naming Conventions (Strict)

- **ALL async methods MUST use `Async` suffix** (e.g., `createAsync`, `updateAsync`, `deleteAsync`, `getByIdAsync`)
- No exceptions - this ensures consistent API across all facades

### Structure Requirements

- Use static class methods (no instantiation needed)
- Define `const facadeName = '{Domain}Facade'` at file top for error context
- Accept optional `DatabaseExecutor` (`dbInstance?: DatabaseExecutor`) as last parameter
- Create appropriate query context (`createProtectedQueryContext`, `createUserQueryContext`, `createPublicQueryContext`, `createAdminQueryContext`)

### QueryContext and Automatic Filtering (IMPORTANT)

- **Context drives filtering**: Query methods automatically apply permission and soft-delete filters based on context flags
- **Trust query methods**: Don't manually add filters that queries handle via `buildBaseFilters()`
- **Context factories set flags**: `createPublicQueryContext()` sets `isPublic: true`, etc.
- **Override when needed**: Pass `shouldIncludeDeleted: true` for admin restore features

### Transaction Requirements (MANDATORY for mutations)

- **ALL multi-step mutations MUST use transactions**: `(dbInstance ?? db).transaction(async (tx) => { ... })`
- Pass transaction executor (`tx`) to all nested query calls
- Single-step reads do NOT need transactions

### Caching Requirements (MANDATORY)

- **ALL read operations MUST use domain-specific CacheService** (`CacheService.bobbleheads.byId()`, etc.)
- **ALL write operations MUST invalidate cache** via `CacheRevalidationService`
- Never use generic `CacheService.cached()` when domain helper exists

### Error Handling (MANDATORY)

- **ALL methods MUST wrap in try-catch** with `createFacadeError(errorContext, error)`
- Use consistent return patterns (see Return Type Decision Matrix in conventions)

### Sentry Monitoring (MANDATORY)

- **Use `withFacadeBreadcrumbs()` wrapper** to add automatic entry/success/error breadcrumbs (recommended)
- Alternatively, use `trackFacadeEntry()` and `trackFacadeSuccess()` for manual control
- Use `trackFacadeWarning()` for non-critical failures that shouldn't fail the operation
- Use `captureFacadeWarning()` to capture non-critical exceptions with proper tags and warning level
- Never fail main operations due to monitoring failures

### Documentation Requirements (MANDATORY)

- **ALL public methods MUST have JSDoc** with:
  - Description of what the method does
  - `@param` for each parameter
  - `@returns` describing the return value
  - Cache behavior notes (TTL, invalidation triggers)

### Method Complexity Limits

- Methods should not exceed 50-60 lines
- Extract helpers for complex transformations
- Use `Promise.all` for parallel independent data fetching

## Anti-Patterns to Detect and Fix

1. **Missing `Async` suffix** on async methods
2. **Missing transactions** on multi-step mutations
3. **Missing cache invalidation** after write operations
4. **Missing Sentry breadcrumbs** in facade methods
5. **Missing JSDoc documentation** on public methods
6. **Stub/incomplete methods** that return hardcoded values
7. **Duplicate methods** with different naming (e.g., `getX` and `getXAsync`)
8. **Silent failures** that log errors but don't handle them properly
9. **Raw SQL/Drizzle queries in facades** - delegate to query classes that handle soft-delete
10. **Wrong operation constants** - use semantically correct operations (add new ones if needed)
11. **Hardcoded cache keys** - use `CACHE_KEYS.*` constants
12. **Mixed executor/context usage** - use single shared context for parallel queries
13. **Breadcrumbs only inside cache callbacks** - add pre-operation breadcrumb outside for visibility

## References

- `references/Facade-Layer-Conventions.md` - Complete facade layer conventions
