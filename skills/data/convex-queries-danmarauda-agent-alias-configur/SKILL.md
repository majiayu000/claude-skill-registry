---
name: convex-queries
description: This skill should be used when implementing Convex query functions. It provides comprehensive guidelines for defining, registering, calling, and optimizing queries, including pagination, full text search, and indexing patterns.
---

# Convex Queries Skill

This skill provides specialized guidance for implementing Convex query functions, including best practices for function definition, registration, calling patterns, pagination, indexing, and full text search.

## When to Use This Skill

Use this skill when:
- Defining new query functions to fetch data from the Convex database
- Implementing pagination for large result sets
- Setting up indexes for efficient querying
- Using full text search functionality
- Calling queries from other Convex functions
- Optimizing query performance

## Skill Resources

This skill includes comprehensive reference documentation in `references/query-guidelines.md` that covers:

### Core Query Development
- Function definition syntax using the new function syntax
- Query registration (`query` and `internalQuery`)
- Argument validators and their usage
- Function calling patterns (`ctx.runQuery`)
- Function references (`api` and `internal` objects)
- File-based routing for query paths

### Query Optimization
- Query guidelines (avoiding `filter`, using indexes with `withIndex`)
- Ordering results with `.order('asc')` and `.order('desc')`
- Using `.unique()` for single document retrieval
- Async iteration with `for await` syntax
- Query limits and performance considerations

### Advanced Query Features
- **Pagination**: Implementing paginated queries with `paginationOptsValidator`
  - Understanding `paginationOpts` (numItems and cursor)
  - Reading paginated results (page, isDone, continueCursor)
- **Full Text Search**: Setting up and querying search indexes
- **Indexing**: Creating and using indexes for efficient lookups
  - Built-in indexes (by_id, by_creation_time)
  - Custom index naming and field ordering
  - Nested queries with multiple indexes

### Database Queries
- Reading from the Convex database with `ctx.db.query()`
- Index usage with `.withIndex()`
- Result collection with `.collect()` and `.take(n)`

## How to Use This Skill

1. **Read the reference documentation** at `references/query-guidelines.md` to understand the complete query patterns
2. **Follow the syntax examples** for defining query functions with proper validators
3. **Use indexes** for efficient filtering instead of the `filter` method
4. **Implement pagination** when dealing with large datasets
5. **Leverage full text search** for text-based filtering needs
6. **Optimize ordering** by understanding how Convex orders results

## Key Query Guidelines

- ALWAYS include argument validators for all query functions
- Do NOT use `filter` in queries; use `withIndex` instead
- Use `ctx.runQuery` to call queries from mutations or actions
- Specify return type annotations when calling queries in the same file (TypeScript circularity workaround)
- Queries execute for at most 1 second and can read up to 16384 documents
- Return `null` implicitly if your query doesn't have an explicit return value

## Example: Basic Query with Index

```ts
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getMessagesByChannel = query({
  args: {
    channelId: v.id("channels"),
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .order("desc")
      .take(20);
  },
});
```

For more detailed information and additional patterns, refer to the complete reference documentation.
