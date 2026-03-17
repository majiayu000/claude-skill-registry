---
name: aurora-criteria
description: >
  Aurora Criteria Pattern - Complete guide for QueryStatement usage in Aurora/NestJS.
  Trigger: When implementing queries, filters, searches, pagination, or complex data retrieval.
license: MIT
metadata:
  author: aurora
  version: "1.1"
  auto_invoke: "Building QueryStatement filters, implementing pagination, creating search queries"
---

## When to Use

Use this skill when:
- Implementing GET/FIND queries in services or handlers
- Building filters for REST or GraphQL endpoints
- Adding pagination to data retrieval
- Creating complex search functionality
- Working with QueryStatement parameters

## What is QueryStatement?

**QueryStatement** is Aurora's standardized interface for building complex database queries using the Criteria Pattern.

### Core Structure

```typescript
interface QueryStatement {
    where?: JSON;           // Filtering conditions
    attributes?: JSON;      // Field selection
    include?: string[];     // Relations to eager load
    order?: JSON;           // Sorting
    group?: JSON;           // Grouping
    limit?: number;         // Max results
    offset?: number;        // Skip results (pagination)
    distinct?: boolean;     // Unique results only
    col?: string;           // Column operations
}
```

## Critical Patterns

### ⚠️ OPERATOR SYNTAX (CRITICAL!)

**Operators MUST be quoted keys wrapped in square brackets:**

```typescript
// ✅ CORRECT
{ "where": { "age": { "[gte]": 18 } } }
{ "where": { "name": { "[startsWith]": "Carlos" } } }

// ❌ INCORRECT (will NOT work)
{ "where": { "age": { gte: 18 } } }
```

### Usage in Services/Queries

```typescript
// In services
async main(queryStatement?: QueryStatement, constraint?: QueryStatement, cQMetadata?: CQMetadata) {
    return await this.repository.get({ queryStatement, constraint, cQMetadata });
}

// In queries
export class TeslaGetModelsQuery {
    constructor(
        public readonly queryStatement?: QueryStatement,
        public readonly constraint?: QueryStatement,
        public readonly cQMetadata?: CQMetadata,
    ) {}
}
```

## Detailed References

- [WHERE Operators Reference](operators.md) — All operators: logical, equality, comparison, range, set, string, array
- [Complete Examples & Common Patterns](examples.md) — Real-world examples, pagination, search, security constraints

## Other QueryStatement Properties

### Field Selection (attributes)

```typescript
{ attributes: ['id', 'name', 'status'] }
{ attributes: { exclude: ['deletedAt', 'createdAt'] } }
```

### Eager Loading (include)

```typescript
{ include: [{ association: 'model' }, { association: 'units' }] }
```

### Sorting (order)

```typescript
{ order: [{ createdAt: 'desc' }, { name: 'asc' }] }
```

### Pagination

```typescript
{ offset: 0, limit: 25 }     // Page 1
{ offset: 25, limit: 25 }    // Page 2
```

### Grouping & Distinct

```typescript
{ group: ['status', 'year'] }
{ distinct: true }
```

## Decision Tree

```
Need to filter data?
├─ Single condition → Use simple where: { field: value }
├─ Multiple AND conditions → Use implicit AND or "[and]"
├─ Multiple OR conditions → Use "[or]": [...]
├─ Range (min/max) → Use "[gte]" and "[lte]"
├─ List of values → Use "[in]": [...]
└─ Pattern matching → Use "[like]", "[iLike]", or "[startsWith]"

Need to sort?
└─ Use order: [{ field: 'asc'|'desc' }]

Need pagination?
└─ Use offset + limit

Need specific fields?
└─ Use attributes: [...]

Need relations?
└─ Use include: [...]

Need to ensure security?
└─ Use constraint parameter (separate from queryStatement)
```

## Best Practices

### ✅ DO

- Always use quoted operators with brackets: `"[gte]"`, `"[startsWith]"`
- Use `constraint` for system-enforced filters (security, soft-deletes)
- Use `queryStatement` for user-provided filters
- Combine operators in same field: `{ year: { "[gte]": 2020, "[lte]": 2024 } }`
- Use `[iLike]` for case-insensitive searches
- Always filter soft-deleted records: `deletedAt: { "[is]": null }`

### ❌ DON'T

- Don't use unquoted operators: `gte:` ❌ Use `"[gte]":` ✅
- Don't use operators without brackets: `"gte"` ❌ Use `"[gte]"` ✅
- Don't trust user-provided `constraint` (always set server-side)
- Don't forget pagination for large datasets
- Don't use `[like]` with user input without validation

## Resources

- **Aurora Core Types**: `@aurorajs.dev/core` exports `QueryStatement`
- **GraphQL Schema**: See `src/@api/graphql.ts` for QueryStatement interface

## Related Skills

- `aurora-project-structure` - Understand where queries live
- `typescript` - Type-safe QueryStatement construction
- `aurora-cli` - Regenerate repositories after schema changes
