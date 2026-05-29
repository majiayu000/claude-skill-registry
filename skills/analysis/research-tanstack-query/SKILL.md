---
name: research-tanstack-query
description: Research Tanstack Query (React Query) patterns for server state management using Exa code search and Ref documentation
---

# Research Tanstack Query Patterns

Use this skill when you need to:
- Learn client-side data fetching patterns
- Understand caching and invalidation strategies
- Research mutations and optimistic updates
- Find pagination and infinite scroll patterns
- Learn about prefetching and SSR integration

## Process

1. **Identify Data Fetching Need**
   - Queries (GET), mutations (POST/PUT/DELETE)?
   - Caching strategy needed?
   - Optimistic updates required?
   - Pagination or infinite scroll?

2. **Search Documentation (Ref)**
   ```
   Query patterns:
   - "Tanstack Query React Query [feature]"
   - "React Query useQuery caching"
   - "React Query useMutation optimistic updates"
   - "React Query Next.js integration"
   ```

3. **Find Real Implementations (Exa)**
   ```
   Query patterns:
   - "Tanstack Query useQuery TypeScript example"
   - "React Query useMutation optimistic update implementation"
   - "React Query pagination infinite scroll example"
   - "React Query Next.js SSR prefetch example"
   ```

4. **Consider Integration**
   - How does this work with Next.js Server Components?
   - Client Component boundaries?
   - Type safety with API responses?

## Common Research Topics

### Basic Queries
```typescript
// Documentation
Query: "Tanstack Query useQuery hook"

// Code examples
Query: "React Query useQuery TypeScript fetch API example"
```

### Mutations
```typescript
// Documentation
Query: "Tanstack Query useMutation"

// Code examples
Query: "React Query useMutation POST request invalidate cache example"
```

### Optimistic Updates
```typescript
// Documentation
Query: "Tanstack Query optimistic updates"

// Code examples
Query: "React Query optimistic update todo list rollback example"
```

### Pagination
```typescript
// Documentation
Query: "Tanstack Query pagination useQuery"

// Code examples
Query: "React Query pagination page state keepPreviousData example"
```

### Infinite Scroll
```typescript
// Documentation
Query: "Tanstack Query infinite queries"

// Code examples
Query: "React Query useInfiniteQuery infinite scroll implementation"
```

### Prefetching
```typescript
// Documentation
Query: "Tanstack Query prefetch queryClient"

// Code examples
Query: "React Query prefetchQuery Next.js server component example"
```

## Next.js Integration

### With Server Components
```typescript
// Research pattern
Query: "React Query Next.js 15 server components prefetch hydration"
```

### With Server Actions
```typescript
// Research pattern
Query: "React Query Next.js server actions mutation invalidation"
```

### SSR and Hydration
```typescript
// Research pattern
Query: "React Query Next.js SSR hydration dehydrate example"
```

## Advanced Patterns

### Dependent Queries
```
Query: "React Query dependent queries enabled option example"
```

### Parallel Queries
```
Query: "React Query parallel queries useQueries hook example"
```

### Query Invalidation
```
Query: "React Query invalidate queries specific pattern example"
```

### Background Refetching
```
Query: "React Query background refetch staleTime refetchInterval"
```

### Error Handling
```
Query: "React Query error handling retry onError example"
```

## Caching Strategies

Research topics:
- Cache time vs stale time
- Garbage collection
- Cache invalidation patterns
- Persistent caching
- Cache warming

```
Query: "React Query caching strategy staleTime cacheTime best practices"
Query: "React Query cache persistence localStorage example"
```

## Output Format

Provide:
1. **Pattern explanation** - How the pattern works
2. **Code examples** - Real implementations from Exa
3. **Type safety** - TypeScript patterns and generics
4. **Caching strategy** - When data refetches
5. **Best practices** - Error handling, loading states
6. **Integration guide** - How to use in this project

## Project Context

Your project uses:
- Tanstack Query 5.90.2
- Next.js 15 Server Components + Client Components
- TypeScript with strict mode
- API routes for backend

Consider:
- Query keys organization
- Global error handling
- Loading state management
- Integration with Server Components

## Common Use Cases

### List Views
```
Research: "React Query useQuery list pagination filtering"
```

### Detail Views
```
Research: "React Query useQuery detail view cache update"
```

### Forms
```
Research: "React Query useMutation form submission validation"
```

### Real-time Updates
```
Research: "React Query polling refetchInterval WebSocket integration"
```

## When to Use

- Fetching data in Client Components
- Managing server state cache
- Implementing mutations with optimistic updates
- Building paginated or infinite scroll lists
- Prefetching data for performance
- Debugging data fetching issues
- Optimizing API calls and caching

## Comparison with Server Components

Research when to use:
- Server Components (initial data load)
- Tanstack Query (client-side updates, interactivity)

```
Query: "React Query vs Next.js server components when to use"
```

## Related Skills

- research-nextjs (for integration patterns)
- research-react (for hooks and state)
- research-typescript (for type safety)
