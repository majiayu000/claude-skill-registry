---
name: prisma-query-optimizer
description: Analyze Prisma queries for performance issues and suggest optimizations. Use when asked to optimize, analyze, audit, or review Prisma queries, or when investigating slow database operations in a Prisma-based project.
---

# Prisma Query Optimizer

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Analysis Process

1. Locate all Prisma query calls in the specified files or project
2. For each query, check for the issues listed below
3. Output a structured report with findings and fixes

## Issues to Detect

### N+1 Queries
Look for loops that execute Prisma queries inside:
```typescript
// BAD: N+1 query
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { authorId: user.id } });
}

// FIX: Use include
const users = await prisma.user.findMany({
  include: { posts: true }
});
```

### Missing Eager Loading
Detect when related data is accessed after the initial query without being included:
```typescript
// BAD: Lazy loading triggers additional queries
const user = await prisma.user.findUnique({ where: { id } });
console.log(user.posts); // undefined or triggers additional query

// FIX: Include related data upfront
const user = await prisma.user.findUnique({
  where: { id },
  include: { posts: true }
});
```

### Missing Index Hints
Flag queries filtering on fields that likely need indexes:
- Foreign keys used in `where` clauses
- Fields used in `orderBy`
- Fields used in unique lookups without `@unique`

Suggest adding indexes in schema.prisma:
```prisma
model Post {
  authorId Int
  author   User @relation(fields: [authorId], references: [id])

  @@index([authorId]) // Add this
}
```

### Redundant Queries
Identify duplicate queries that fetch the same data multiple times in a request:
```typescript
// BAD: Same query twice
const user1 = await prisma.user.findUnique({ where: { id } });
// ... later in same function
const user2 = await prisma.user.findUnique({ where: { id } });

// FIX: Reuse the result
const user = await prisma.user.findUnique({ where: { id } });
// Use 'user' throughout
```

### Unnecessary Select/Include Combinations
Detect overly broad data fetching:
```typescript
// BAD: Fetching everything when only name is needed
const users = await prisma.user.findMany({
  include: { posts: true, comments: true, profile: true }
});
const names = users.map(u => u.name);

// FIX: Select only what's needed
const users = await prisma.user.findMany({
  select: { name: true }
});
```

### Missing Pagination
Flag `findMany` without `take`/`skip` on large tables:
```typescript
// BAD: Unbounded query
const allPosts = await prisma.post.findMany();

// FIX: Add pagination
const posts = await prisma.post.findMany({
  take: 20,
  skip: page * 20,
  orderBy: { createdAt: 'desc' }
});
```

### Inefficient Counting
Detect full fetches when only count is needed:
```typescript
// BAD: Fetching all records to count
const posts = await prisma.post.findMany({ where: { published: true } });
const count = posts.length;

// FIX: Use count
const count = await prisma.post.count({ where: { published: true } });
```

## Output Format

Present findings in this structure:

```
## Prisma Query Analysis

### Critical Issues
- **N+1 Query** in `src/services/user.ts:45`
  - Issue: Loop executes individual post queries for each user
  - Fix: [code block with corrected query]

### Warnings
- **Missing Index** in `schema.prisma`
  - Issue: `Post.authorId` used in queries but not indexed
  - Fix: Add `@@index([authorId])` to Post model

### Suggestions
- **Over-fetching** in `src/api/users.ts:23`
  - Issue: Including all relations when only user name is used
  - Fix: [code block with select]

### Summary
- Critical: X issues
- Warnings: X issues
- Suggestions: X issues
```

## Reference

See `references/patterns.md` for additional optimization patterns and advanced techniques.
