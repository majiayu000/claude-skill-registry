---
name: research-drizzle
description: Research Drizzle ORM patterns, queries, and PostgreSQL integration using Exa code search and Ref documentation
---

# Research Drizzle ORM Patterns

Use this skill when you need to:
- Learn Drizzle ORM query patterns
- Understand schema definitions and migrations
- Research relations and joins
- Find transaction patterns
- Learn type-safe query building

## Process

1. **Identify Database Need**
   - Schema design, queries, or migrations?
   - Relations, joins, or transactions?
   - Performance optimization?

2. **Search Documentation (Ref)**
   ```
   Query patterns:
   - "Drizzle ORM [feature] PostgreSQL"
   - "Drizzle schema relations"
   - "Drizzle query builder"
   - "Drizzle migrations"
   ```

3. **Find Implementation Examples (Exa)**
   ```
   Query patterns:
   - "Drizzle ORM PostgreSQL schema definition example"
   - "Drizzle query relations join implementation"
   - "Drizzle transaction rollback example"
   - "Drizzle migration file structure"
   ```

4. **Verify Type Safety**
   - Check TypeScript integration
   - Review inferred types
   - Validate query safety

## Common Research Topics

### Schema Definition
```typescript
// Documentation
Query: "Drizzle ORM schema definition PostgreSQL types"

// Code examples
Query: "Drizzle pgTable schema relations foreign keys example"
```

### Queries
```typescript
// Documentation
Query: "Drizzle query builder select where join"

// Code examples
Query: "Drizzle ORM complex query multiple joins filtering example"
```

### Relations
```typescript
// Documentation
Query: "Drizzle ORM relations one-to-many many-to-many"

// Code examples
Query: "Drizzle relations query nested data user posts example"
```

### Migrations
```typescript
// Documentation
Query: "Drizzle kit migrations generate apply"

// Code examples
Query: "Drizzle migration alter table add column example"
```

### Transactions
```typescript
// Documentation
Query: "Drizzle transactions rollback commit"

// Code examples
Query: "Drizzle transaction atomic operations multiple tables example"
```

## Integration with Next.js

### Server Actions
```typescript
// Research pattern
Query: "Drizzle ORM Next.js server actions database mutations"
```

### API Routes
```typescript
// Research pattern
Query: "Drizzle ORM Next.js API route handler database query"
```

### Server Components
```typescript
// Research pattern
Query: "Drizzle ORM Next.js server component async query"
```

## Performance Patterns

Research topics:
- Query optimization
- Index usage
- Connection pooling
- Prepared statements
- Batch operations

```
Query: "Drizzle ORM performance optimization batch insert"
Query: "Drizzle PostgreSQL connection pooling Neon"
```

## Output Format

Provide:
1. **Schema examples** - Table definitions with relations
2. **Query patterns** - Common query structures
3. **Type safety** - How TypeScript types are inferred
4. **Best practices** - From docs and real implementations
5. **Performance tips** - Optimization strategies
6. **Migration guide** - How to handle schema changes

## When to Use

- Designing new database tables
- Writing complex queries
- Setting up relations
- Creating migrations
- Optimizing database performance
- Debugging query issues
- Learning Drizzle-specific features

## Example Queries

### User Authentication Schema
```
Documentation: "Drizzle schema user authentication sessions"
Code: "Drizzle PostgreSQL user table bcrypt password schema example"
```

### E-commerce Relations
```
Documentation: "Drizzle relations orders products users"
Code: "Drizzle ORM order items products join query example"
```

### Full-text Search
```
Documentation: "Drizzle PostgreSQL full text search"
Code: "Drizzle ts_vector search query implementation example"
```

## Project-Specific Context

Your project uses:
- PostgreSQL with Drizzle ORM 0.44.5
- Neon serverless database
- Better Auth for authentication
- Next.js Server Components and Actions

Always research with this context in mind.

## Related Skills

- research-typescript (for type patterns)
- research-nextjs (for Next.js integration)
- research-security (for secure queries)
