---
name: TanStack Types
description: This skill should be used when the user asks about "type-safe React Query", "queryOptions typing", "Zod validation", "TypeScript with TanStack Query", "generic useQuery", "DataTag", "infer query types", or needs guidance on type safety patterns, runtime validation, and TypeScript best practices for TanStack Query.
version: 1.0.0
---

# TanStack Query Type Safety Patterns

This skill provides guidance for achieving type safety in TanStack Query, covering queryOptions, runtime validation with Zod, and TypeScript best practices based on TKDodo's recommendations.

## Core Principle: Trust in Types

The foundation of type safety is **trust in type definitions**. Without trust, TypeScript becomes just a linter that can be silenced.

> "To truly leverage the power of TypeScript, there is one thing that you need above all: Trust."

## The Anti-Pattern: Manual Generics

Avoid passing type parameters directly to `useQuery`:

```typescript
// BAD: Manual generics
const { data } = useQuery<Todo>({
  queryKey: ['todos', id],
  queryFn: () => fetchTodo(id),
})
// data is Todo | undefined, but is it really?
// The generic is just a type assertion in disguise
```

This violates the "golden rule of generics": **For a generic to be useful, it must appear at least twice.**

## The Pattern: Type the Data Source

Instead of typing the consumer, type the source:

```typescript
// GOOD: Type the queryFn return
const fetchTodo = async (id: string): Promise<Todo> => {
  const response = await axios.get(`/todos/${id}`)
  return response.data
}

// Types flow through automatically
const { data } = useQuery({
  queryKey: ['todos', id],
  queryFn: () => fetchTodo(id),
})
// data is Todo | undefined, and we can trust it
```

## The queryOptions Helper

The `queryOptions()` helper provides compile-time type safety:

```typescript
import { queryOptions, useQuery } from '@tanstack/react-query'

const todoQueryOptions = (id: string) => queryOptions({
  queryKey: ['todos', id] as const,
  queryFn: async (): Promise<Todo> => {
    const response = await api.get(`/todos/${id}`)
    return response.data
  },
  staleTime: 5 * 60 * 1000,
})

// Usage - types are inferred correctly
const { data } = useQuery(todoQueryOptions(id))
// data: Todo | undefined

// TypeScript catches property typos
const bad = queryOptions({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  stallTime: 5000, // Error! Did you mean 'staleTime'?
})
```

### DataTag for getQueryData/setQueryData

queryOptions enables type-safe cache access:

```typescript
const options = todoQueryOptions(id)

// getQueryData knows the return type
const cachedTodo = queryClient.getQueryData(options.queryKey)
// cachedTodo: Todo | undefined

// setQueryData gets type checking
queryClient.setQueryData(options.queryKey, (old) => {
  // old: Todo | undefined
  return old ? { ...old, completed: true } : old
})
```

## Runtime Validation with Zod

The network boundary is inherently untrustworthy. Validate responses at runtime:

```typescript
import { z } from 'zod'

// Define schema
const todoSchema = z.object({
  id: z.string(),
  title: z.string(),
  completed: z.boolean(),
  createdAt: z.string().datetime(),
})

type Todo = z.infer<typeof todoSchema>

// Validate in queryFn
const fetchTodo = async (id: string): Promise<Todo> => {
  const response = await axios.get(`/todos/${id}`)
  return todoSchema.parse(response.data) // Throws if invalid
}
```

### Benefits of Runtime Validation

1. **Catches mismatches early**: API changes are caught immediately
2. **Descriptive errors**: Zod provides clear error messages
3. **Triggers error state**: Invalid data triggers React Query's error handling
4. **Self-documenting**: Schema serves as documentation

### List Validation

```typescript
const todosSchema = z.array(todoSchema)

const fetchTodos = async (): Promise<Todo[]> => {
  const response = await axios.get('/todos')
  return todosSchema.parse(response.data)
}
```

### Partial/Optional Fields

```typescript
const todoSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string().optional(),
  metadata: z.record(z.string()).nullable(),
})
```

## Query Factories with Full Type Safety

Combine queryOptions with factory pattern:

```typescript
// queries/todos.ts
import { queryOptions } from '@tanstack/react-query'
import { z } from 'zod'

const todoSchema = z.object({
  id: z.string(),
  title: z.string(),
  completed: z.boolean(),
})

const todosSchema = z.array(todoSchema)

export type Todo = z.infer<typeof todoSchema>

export const todoQueries = {
  all: () => queryOptions({
    queryKey: ['todos'] as const,
    queryFn: async () => {
      const res = await api.get('/todos')
      return todosSchema.parse(res.data)
    },
  }),

  detail: (id: string) => queryOptions({
    queryKey: ['todos', 'detail', id] as const,
    queryFn: async () => {
      const res = await api.get(`/todos/${id}`)
      return todoSchema.parse(res.data)
    },
    staleTime: 5 * 60 * 1000,
  }),

  byStatus: (status: 'active' | 'completed') => queryOptions({
    queryKey: ['todos', 'status', status] as const,
    queryFn: async () => {
      const res = await api.get(`/todos?status=${status}`)
      return todosSchema.parse(res.data)
    },
  }),
}
```

## Typing Selectors

When using `select`, type the output properly:

```typescript
// Basic select - output type inferred
const { data: title } = useQuery({
  ...todoQueryOptions(id),
  select: (data) => data.title, // data: Todo, returns string
})
// title: string | undefined

// With generic for reusable options
const productOptions = <TData = Product>(
  id: string,
  select?: (data: Product) => TData
) => queryOptions({
  queryKey: ['products', id] as const,
  queryFn: () => fetchProduct(id),
  select,
})

// Usage
const { data: product } = useQuery(productOptions(id))
// product: Product | undefined

const { data: title } = useQuery(productOptions(id, (p) => p.title))
// title: string | undefined
```

## Typing Mutations

Apply the same patterns to mutations:

```typescript
const createTodoSchema = z.object({
  title: z.string().min(1),
  description: z.string().optional(),
})

type CreateTodoInput = z.infer<typeof createTodoSchema>

const useCreateTodo = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (input: CreateTodoInput) => {
      // Validate input
      const validated = createTodoSchema.parse(input)
      const res = await api.post('/todos', validated)
      return todoSchema.parse(res.data)
    },
    onSuccess: (newTodo) => {
      // newTodo is typed as Todo
      queryClient.setQueryData(
        todoQueries.detail(newTodo.id).queryKey,
        newTodo
      )
    },
  })
}
```

## Error Types

Type your errors for better error handling:

```typescript
// Define error types
interface ApiError {
  code: string
  message: string
  details?: Record<string, string[]>
}

const apiErrorSchema = z.object({
  code: z.string(),
  message: z.string(),
  details: z.record(z.array(z.string())).optional(),
})

// Parse errors in fetch wrapper
const apiFetch = async <T>(
  url: string,
  schema: z.ZodType<T>
): Promise<T> => {
  const response = await fetch(url)

  if (!response.ok) {
    const error = await response.json()
    throw apiErrorSchema.parse(error)
  }

  return schema.parse(await response.json())
}

// Usage in query
const { data, error } = useQuery({
  queryKey: ['todos'],
  queryFn: () => apiFetch('/todos', todosSchema),
})
// error: ApiError | null
```

## Quick Reference

| Goal | Pattern |
|------|---------|
| Type query data | Type the queryFn return, not useQuery generic |
| Catch typos | Use queryOptions() helper |
| Type-safe cache access | Use queryOptions with getQueryData/setQueryData |
| Runtime validation | Parse with Zod in queryFn |
| Reusable queries | Query factories with queryOptions |
| Typed selectors | Generic parameter on factory function |

## Common Mistakes

### 1. Using Generics as Type Assertions

```typescript
// BAD: This is lying to TypeScript
const { data } = useQuery<Todo>({
  queryKey: ['todo'],
  queryFn: () => fetch('/todo').then(r => r.json()),
})
// data could be anything at runtime!

// GOOD: Validate at runtime
const { data } = useQuery({
  queryKey: ['todo'],
  queryFn: () => fetch('/todo').then(r => r.json()).then(todoSchema.parse),
})
```

### 2. Not Using `as const` for Query Keys

```typescript
// BAD: Types are too wide
queryKey: ['todos', id] // string[]

// GOOD: Exact types preserved
queryKey: ['todos', id] as const // readonly ['todos', string]
```

## Additional Resources

### Reference Files

For detailed patterns and advanced techniques, consult:
- **`references/advanced-typing.md`** - Complex type scenarios

### Related Skills

- **tanstack-query** - Core concepts, query factories
- **tanstack-mutations** - Type-safe mutations
- **tanstack-errors** - Typed error handling
