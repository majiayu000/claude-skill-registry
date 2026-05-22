---
name: api-integration
description: Integrate Apidog + OpenAPI specifications with your React app. Covers MCP server setup, type generation, and query layer integration. Use when setting up API clients, generating types from OpenAPI, or integrating with Apidog MCP.
---

# API Integration (Apidog + MCP)

Integrate OpenAPI specifications with your frontend using Apidog MCP for single source of truth.

## Goal

The AI agent always uses the latest API specification to generate types and implement features correctly.

## Architecture

```
Apidog (or Backend)
  → OpenAPI 3.0/3.1 Spec
    → MCP Server (apidog-mcp-server)
      → AI Agent reads spec
        → Generate TypeScript types
          → TanStack Query hooks
            → React Components
```

## Process

### 1. Expose OpenAPI from Apidog

**Option A: Remote URL**
- Export OpenAPI spec from Apidog
- Host at a URL (e.g., `https://api.example.com/openapi.json`)

**Option B: Local File**
- Export OpenAPI spec to file
- Place in project (e.g., `./api-spec/openapi.json`)

### 2. Wire MCP Server

```json
// .claude/mcp.json or settings
{
  "mcpServers": {
    "API specification": {
      "command": "npx",
      "args": [
        "-y",
        "apidog-mcp-server@latest",
        "--oas=https://api.example.com/openapi.json"
      ]
    }
  }
}
```

**With Local File:**
```json
{
  "mcpServers": {
    "API specification": {
      "command": "npx",
      "args": [
        "-y",
        "apidog-mcp-server@latest",
        "--oas=./api-spec/openapi.json"
      ]
    }
  }
}
```

**Multiple APIs:**
```json
{
  "mcpServers": {
    "Main API": {
      "command": "npx",
      "args": ["-y", "apidog-mcp-server@latest", "--oas=https://api.main.com/openapi.json"]
    },
    "Auth API": {
      "command": "npx",
      "args": ["-y", "apidog-mcp-server@latest", "--oas=https://api.auth.com/openapi.json"]
    }
  }
}
```

### 3. Generate Types & Client

Create `/src/api` directory for all API-related code:

```
/src/api/
  ├── types.ts          # Generated from OpenAPI
  ├── client.ts         # HTTP client (axios/fetch)
  ├── queries/          # TanStack Query hooks
  │   ├── users.ts
  │   ├── posts.ts
  │   └── ...
  └── mutations/        # TanStack Mutation hooks
      ├── users.ts
      ├── posts.ts
      └── ...
```

**Option A: Hand-Written Types (Lightweight)**
```typescript
// src/api/types.ts
import { z } from 'zod'

// Define schemas from OpenAPI
export const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  createdAt: z.string().datetime(),
})

export type User = z.infer<typeof UserSchema>

export const CreateUserSchema = UserSchema.omit({ id: true, createdAt: true })
export type CreateUserDTO = z.infer<typeof CreateUserSchema>
```

**Option B: Code Generation (Recommended for large APIs)**
```bash
# Using openapi-typescript
pnpm add -D openapi-typescript
npx openapi-typescript https://api.example.com/openapi.json -o src/api/types.ts

# Using orval
pnpm add -D orval
npx orval --input https://api.example.com/openapi.json --output src/api
```

### 4. Create HTTP Client

```typescript
// src/api/client.ts
import axios from 'axios'
import createAuthRefreshInterceptor from 'axios-auth-refresh'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor - handle token refresh
const refreshAuth = async (failedRequest: any) => {
  try {
    const refreshToken = localStorage.getItem('refreshToken')
    const response = await axios.post('/auth/refresh', { refreshToken })

    const { accessToken } = response.data
    localStorage.setItem('accessToken', accessToken)

    failedRequest.response.config.headers.Authorization = `Bearer ${accessToken}`
    return Promise.resolve()
  } catch (error) {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    window.location.href = '/login'
    return Promise.reject(error)
  }
}

createAuthRefreshInterceptor(apiClient, refreshAuth, {
  statusCodes: [401],
  pauseInstanceWhileRefreshing: true,
})
```

### 5. Build Query Layer

**Feature-based query organization:**

```typescript
// src/api/queries/users.ts
import { queryOptions } from '@tanstack/react-query'
import { apiClient } from '../client'
import { User, UserSchema } from '../types'

// Query key factory
export const usersKeys = {
  all: ['users'] as const,
  lists: () => [...usersKeys.all, 'list'] as const,
  list: (filters: string) => [...usersKeys.lists(), { filters }] as const,
  details: () => [...usersKeys.all, 'detail'] as const,
  detail: (id: string) => [...usersKeys.details(), id] as const,
}

// API functions
async function fetchUsers(): Promise<User[]> {
  const response = await apiClient.get('/users')
  return z.array(UserSchema).parse(response.data)
}

async function fetchUser(id: string): Promise<User> {
  const response = await apiClient.get(`/users/${id}`)
  return UserSchema.parse(response.data)
}

// Query options
export function usersListQueryOptions() {
  return queryOptions({
    queryKey: usersKeys.lists(),
    queryFn: fetchUsers,
    staleTime: 30_000,
  })
}

export function userQueryOptions(id: string) {
  return queryOptions({
    queryKey: usersKeys.detail(id),
    queryFn: () => fetchUser(id),
    staleTime: 60_000,
  })
}

// Hooks
export function useUsers() {
  return useQuery(usersListQueryOptions())
}

export function useUser(id: string) {
  return useQuery(userQueryOptions(id))
}
```

**Mutations:**

```typescript
// src/api/mutations/users.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '../client'
import { CreateUserDTO, User, UserSchema } from '../types'
import { usersKeys } from '../queries/users'

async function createUser(data: CreateUserDTO): Promise<User> {
  const response = await apiClient.post('/users', data)
  return UserSchema.parse(response.data)
}

export function useCreateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createUser,
    onSuccess: (newUser) => {
      // Add to cache
      queryClient.setQueryData(usersKeys.detail(newUser.id), newUser)

      // Invalidate list
      queryClient.invalidateQueries({ queryKey: usersKeys.lists() })
    },
  })
}
```

## Validation Strategy

**Always validate API responses:**

```typescript
import { z } from 'zod'

// Runtime validation
async function fetchUser(id: string): Promise<User> {
  const response = await apiClient.get(`/users/${id}`)

  try {
    return UserSchema.parse(response.data)
  } catch (error) {
    console.error('API response validation failed:', error)
    throw new Error('Invalid API response format')
  }
}
```

**Or use safe parse:**
```typescript
const result = UserSchema.safeParse(response.data)

if (!result.success) {
  console.error('Validation errors:', result.error.errors)
  throw new Error('Invalid user data')
}

return result.data
```

## Error Handling

**Global error handling:**
```typescript
import { QueryCache } from '@tanstack/react-query'

const queryCache = new QueryCache({
  onError: (error, query) => {
    if (axios.isAxiosError(error)) {
      if (error.response?.status === 404) {
        toast.error('Resource not found')
      } else if (error.response?.status === 500) {
        toast.error('Server error. Please try again.')
      }
    }
  },
})
```

## Best Practices

1. **Single Source of Truth** - OpenAPI spec via MCP is authoritative
2. **Validate Responses** - Use Zod schemas for runtime validation
3. **Encapsulation** - Keep all API details in `/src/api`
4. **Type Safety** - Export types from generated/hand-written schemas
5. **Error Handling** - Handle auth errors, network errors, validation errors
6. **Query Key Factories** - Hierarchical keys for flexible invalidation
7. **Feature-Based Organization** - Group queries/mutations by feature

## Workflow with AI Agent

1. **Agent reads latest OpenAPI spec** via Apidog MCP
2. **Agent generates or updates** types in `/src/api/types.ts`
3. **Agent implements queries** following established patterns
4. **Agent creates mutations** with proper invalidation
5. **Agent updates components** to use new API hooks

## Example: Full Feature Implementation

```typescript
// 1. Types (generated or hand-written)
// src/api/types.ts
export const TodoSchema = z.object({
  id: z.string(),
  text: z.string(),
  completed: z.boolean(),
})
export type Todo = z.infer<typeof TodoSchema>

// 2. Queries
// src/api/queries/todos.ts
export const todosKeys = {
  all: ['todos'] as const,
  lists: () => [...todosKeys.all, 'list'] as const,
}

export function todosQueryOptions() {
  return queryOptions({
    queryKey: todosKeys.lists(),
    queryFn: async () => {
      const response = await apiClient.get('/todos')
      return z.array(TodoSchema).parse(response.data)
    },
  })
}

// 3. Mutations
// src/api/mutations/todos.ts
export function useCreateTodo() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (text: string) => {
      const response = await apiClient.post('/todos', { text })
      return TodoSchema.parse(response.data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: todosKeys.lists() })
    },
  })
}

// 4. Component
// src/features/todos/TodoList.tsx
export function TodoList() {
  const { data: todos } = useQuery(todosQueryOptions())
  const createTodo = useCreateTodo()

  return (
    <div>
      {todos?.map(todo => <TodoItem key={todo.id} {...todo} />)}
      <AddTodoForm onSubmit={(text) => createTodo.mutate(text)} />
    </div>
  )
}
```

## Related Skills

- **tanstack-query** - Query and mutation patterns
- **tooling-setup** - TypeScript configuration for generated types
- **core-principles** - Project structure with `/src/api` directory
