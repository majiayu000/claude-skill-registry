---
name: aurora-criteria
description: >
  Aurora Criteria Pattern - Complete guide for QueryStatement usage in Aurora/NestJS.
  Trigger: When implementing queries, filters, searches, pagination, or complex data retrieval.
license: MIT
metadata:
  author: aurora
  version: "1.0"
  auto_invoke: "Building QueryStatement filters, implementing pagination, creating search queries"
---

## When to Use

Use this skill when:
- Implementing GET/FIND queries in services or handlers
- Building filters for REST or GraphQL endpoints
- Adding pagination to data retrieval
- Creating complex search functionality
- Working with QueryStatement parameters
- Need to filter, sort, or limit results

## What is QueryStatement?

**QueryStatement** is Aurora's standardized interface for building complex database queries using the Criteria Pattern.

It provides a unified API for filtering, sorting, pagination, and data selection across all repositories.

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
{ "where": { "name": { startsWith: "Carlos" } } }
```

### Usage in Services

```typescript
@Injectable()
export class TeslaGetModelsService {
    constructor(private readonly repository: TeslaIModelRepository) {}

    async main(
        queryStatement?: QueryStatement,
        constraint?: QueryStatement,
        cQMetadata?: CQMetadata,
    ): Promise<TeslaModel[]> {
        return await this.repository.get({
            queryStatement,  // User-provided filters
            constraint,      // System/security constraints
            cQMetadata,
        });
    }
}
```

### Usage in Queries

```typescript
export class TeslaGetModelsQuery {
    constructor(
        public readonly queryStatement?: QueryStatement,
        public readonly constraint?: QueryStatement,
        public readonly cQMetadata?: CQMetadata,
    ) {}
}
```

## WHERE Operators Reference

### Logical Operators

```typescript
// AND - All conditions must match
{
    where: {
        "[and]": [
            { status: "PRODUCTION" },
            { year: { "[gte]": 2020 } }
        ]
    }
}

// OR - Any condition must match
{
    where: {
        "[or]": [
            { status: "PRODUCTION" },
            { status: "PREPRODUCTION" }
        ]
    }
}

// NOT - Negate condition
{
    where: {
        "[not]": {
            deletedAt: { "[is]": null }
        }
    }
}
```

### Equality & Nulls

```typescript
// Simple equality (implicit [eq])
{ where: { id: "uuid-here" } }

// Explicit equality
{ where: { id: { "[eq]": "uuid-here" } } }

// Not equal
{ where: { status: { "[ne]": "DISCLAIMER" } } }

// IS NULL / IS NOT NULL
{ where: { deletedAt: { "[is]": null } } }
{ where: { deletedAt: { "[is]": "[not]null" } } }
```

### Comparison Operators

```typescript
// Greater than
{ where: { year: { "[gt]": 2020 } } }

// Greater than or equal
{ where: { year: { "[gte]": 2020 } } }

// Less than
{ where: { year: { "[lt]": 2025 } } }

// Less than or equal
{ where: { year: { "[lte]": 2024 } } }

// Combined range
{
    where: {
        year: {
            "[gte]": 2020,
            "[lte]": 2024
        }
    }
}
```

### Range Operators

```typescript
// BETWEEN (inclusive)
{ where: { year: { "[between]": [2020, 2024] } } }

// NOT BETWEEN
{ where: { year: { "[notBetween]": [2000, 2010] } } }
```

### Set Operators

```typescript
// IN - Value in list
{
    where: {
        status: {
            "[in]": ["PRODUCTION", "PREPRODUCTION"]
        }
    }
}

// NOT IN - Value not in list
{
    where: {
        status: {
            "[notIn]": ["DISCLAIMER", "CONCEPTION"]
        }
    }
}
```

### String Pattern Matching

```typescript
// LIKE - Case-sensitive pattern (% = wildcard)
{ where: { name: { "[like]": "%Model%" } } }

// NOT LIKE
{ where: { name: { "[notLike]": "Admin%" } } }

// ILIKE - Case-insensitive pattern
{ where: { name: { "[iLike]": "%roadster%" } } }

// NOT ILIKE
{ where: { name: { "[notILike]": "test%" } } }

// STARTS WITH - Convenience for LIKE "value%"
{ where: { name: { "[startsWith]": "Model" } } }

// ENDS WITH - Convenience for LIKE "%value"
{ where: { name: { "[endsWith]": "S" } } }

// SUBSTRING - Convenience for LIKE "%value%"
{ where: { name: { "[substring]": "Air" } } }

// REGEXP - Regular expression
{ where: { sku: { "[regexp]": "^[A-Z]{3}-[0-9]+$" } } }

// NOT REGEXP
{ where: { sku: { "[notRegexp]": "test" } } }

// IREGEXP - Case-insensitive regex
{ where: { sku: { "[iRegexp]": "abc" } } }

// NOT IREGEXP
{ where: { sku: { "[notIRegexp]": "xyz" } } }
```

### Column Comparison

```typescript
// Compare with another column
{
    where: {
        updatedAt: { "[col]": "createdAt" }
    }
}
```

### Array Operators (PostgreSQL)

```typescript
// OVERLAP - Arrays have common elements
{
    where: {
        tags: { "[overlap]": ["react", "node"] }
    }
}

// CONTAINS - Array contains all specified elements
{
    where: {
        tags: { "[contains]": ["graphql"] }
    }
}

// ANY - Value matches any array element
{
    where: {
        roles: { "[any]": ["admin", "editor"] }
    }
}
```

## Other QueryStatement Properties

### Field Selection (attributes)

```typescript
// Select specific fields only
{
    attributes: ['id', 'name', 'status']
}

// Exclude fields
{
    attributes: {
        exclude: ['deletedAt', 'createdAt']
    }
}
```

### Eager Loading (include)

```typescript
// Load relations
{
    include: [{ association: 'model' }, { association: 'units' }]
}

// In repositories, typically:
{
    include: {
        model: true,
        units: true
    }
}
```

### Sorting (order)

```typescript
// Single field ascending
{
    order: [
        { createdAt: 'asc' }
    ]
}

// Single field descending
{
    order: [
        { createdAt: 'desc' }
    ]
}

// Multiple fields
{
    order: [
        { status: 'asc' },
        { year: 'desc' },
        { name: 'asc' }
    ]
}
```

### Pagination

```typescript
// Limit results
{
    limit: 25
}

// Skip results (for pagination)
{
    offset: 0
}

// Combined (page 1, 25 per page)
{
    offset: 0,
    limit: 25
}

// Page 2
{
    offset: 25,
    limit: 25
}
```

### Grouping

```typescript
{
    group: ['status', 'year']
}
```

### Distinct

```typescript
// Return only unique results
{
    distinct: true
}
```

## Complete Examples

### Example 1: Simple Filter

```typescript
// Find active Tesla models from 2020 onwards
const queryStatement: QueryStatement = {
    where: {
        isActive: true,
        year: { "[gte]": 2020 }
    }
};

await this.repository.get({ queryStatement });
```

### Example 2: Complex Search with Pagination

```typescript
// Search production models, sorted by year, paginated
const queryStatement: QueryStatement = {
    where: {
        "[and]": [
            { status: { "[in]": ["PRODUCTION", "PREPRODUCTION"] } },
            { name: { "[iLike]": "%model%" } },
            { deletedAt: { "[is]": null } }
        ]
    },
    order: [
        { year: 'desc' },
        { name: 'asc' }
    ],
    offset: 0,
    limit: 10
};

await this.repository.get({ queryStatement });
```

### Example 3: With Relations and Field Selection

```typescript
// Get models with units, specific fields only
const queryStatement: QueryStatement = {
    where: {
        status: "PRODUCTION"
    },
    attributes: ['id', 'name', 'year', 'status'],
    include: [{ association: 'units' }],
    order: [
        { year: 'desc' }
    ]
};

await this.repository.get({ queryStatement });
```

### Example 4: Constraint Pattern (Security)

```typescript
// User query + System constraint
const queryStatement: QueryStatement = {
    where: {
        name: { "[startsWith]": "Model" }
    }
};

const constraint: QueryStatement = {
    where: {
        isActive: true,  // Force only active records
        deletedAt: { "[is]": null }  // Force soft-delete check
    }
};

await this.repository.get({
    queryStatement,
    constraint  // System applies this regardless of user input
});
```

### Example 5: GraphQL/REST Usage

```graphql
# GraphQL Query
query GetModels($query: QueryStatement) {
  teslaGetModels(query: $query) {
    id
    name
    year
    status
  }
}

# Variables
{
  "query": {
    "where": {
      "year": { "[gte]": 2020 }
    },
    "order": [
      { "year": "desc" }
    ],
    "limit": 10
  }
}
```

```typescript
// REST POST /tesla/model/get
{
    "query": {
        "where": {
            "year": { "[gte]": 2020 }
        },
        "order": [
            { "year": "desc" }
        ],
        "limit": 10
    }
}
```

## Common Patterns

### Paginated List

```typescript
const queryStatement: QueryStatement = {
    where: {
        deletedAt: { "[is]": null }
    },
    order: [
        { createdAt: 'desc' }
    ],
    offset: (page - 1) * pageSize,
    limit: pageSize
};
```

### Search by Multiple Fields

```typescript
const queryStatement: QueryStatement = {
    where: {
        "[or]": [
            { name: { "[iLike]": `%${searchTerm}%` } },
            { sku: { "[iLike]": `%${searchTerm}%` } },
            { description: { "[iLike]": `%${searchTerm}%` } }
        ]
    }
};
```

### Date Range Filter

```typescript
const queryStatement: QueryStatement = {
    where: {
        createdAt: {
            "[gte]": startDate,
            "[lte]": endDate
        }
    }
};
```

### Active Records Only

```typescript
const queryStatement: QueryStatement = {
    where: {
        "[and]": [
            { isActive: true },
            { deletedAt: { "[is]": null } }
        ]
    }
};
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
- Validate user input before building QueryStatement

### ❌ DON'T

- Don't use unquoted operators: `gte:` ❌ Use `"[gte]":` ✅
- Don't use operators without brackets: `"gte"` ❌ Use `"[gte]"` ✅
- Don't trust user-provided `constraint` (always set server-side)
- Don't forget pagination for large datasets
- Don't expose sensitive fields in `attributes`
- Don't use `[like]` with user input without validation (SQL injection risk)

## Resources

- **Aurora Core Types**: `@aurorajs.dev/core` exports `QueryStatement`
- **MCP Server**: See `src/@api/mcp/mcp.server.ts` for full operator reference
- **GraphQL Schema**: See `src/@api/graphql.ts` for QueryStatement interface
- **Test Examples**: See `test/acceptance/tesla/*.e2e-spec.ts` for real usage

## Related Skills

- `aurora-project-structure` - Understand where queries live
- `typescript` - Type-safe QueryStatement construction
- `aurora-cli` - Regenerate repositories after schema changes
