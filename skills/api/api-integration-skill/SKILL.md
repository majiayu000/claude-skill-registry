---
name: api-integration
slug: api-integration
version: 1.0.0
category: core
description: Generate Next.js App Router API routes with Zod validation and TypeScript types
triggers:
  - pattern: "api|endpoint|route|fetch|request|rest|graphql"
    confidence: 0.6
    examples:
      - "create an API endpoint"
      - "build a REST API"
      - "I need API routes for CRUD"
      - "generate endpoint for users"
      - "create a fetch request handler"
      - "create endpoints to fetch data"
mcp_dependencies:
  - server: context7
    required: false
    capabilities:
      - "search"
  - server: exa
    required: false
    capabilities:
      - "search"
---

# API Integration Skill

Automatically generate production-ready Next.js 15 App Router API routes with Zod validation, TypeScript types, and comprehensive error handling. This skill transforms natural language API requirements into fully functional RESTful endpoints following Next.js best practices.

## Overview

This skill generates:
- **Next.js App Router API routes** (TypeScript)
- **Zod validation schemas** for request/response
- **TypeScript type definitions** (auto-inferred from Zod)
- **Error handling utilities** (consistent error responses)
- **RESTful conventions** (proper HTTP methods and status codes)

## When to Use This Skill

Activate this skill when the user requests:
- API endpoint creation
- REST API development
- Route handlers
- CRUD operations
- HTTP request/response handling
- Data validation for APIs
- GraphQL resolvers (basic)

## Key Features

### 1. Automatic Route Generation

Generates Next.js 15 App Router route handlers:

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { postSchema } from '@/lib/validations/post'
import { handleAPIError } from '@/lib/api/errors'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const page = parseInt(searchParams.get('page') || '1')
    const limit = parseInt(searchParams.get('limit') || '10')

    // Fetch posts from database
    const posts = await db.query.posts.findMany({
      limit,
      offset: (page - 1) * limit,
    })

    return NextResponse.json({ posts, page, limit })
  } catch (error) {
    return handleAPIError(error)
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const validated = postSchema.parse(body)

    // Create post in database
    const post = await db.insert(posts).values(validated).returning()

    return NextResponse.json(post, { status: 201 })
  } catch (error) {
    return handleAPIError(error)
  }
}
```

### 2. CRUD Operations Mapping

Automatically maps CRUD operations to HTTP methods:

| Operation | HTTP Method | Route Pattern | Description |
|-----------|-------------|---------------|-------------|
| List | GET | `/api/posts` | Get all resources |
| Get | GET | `/api/posts/[id]` | Get single resource |
| Create | POST | `/api/posts` | Create new resource |
| Update | PUT/PATCH | `/api/posts/[id]` | Update existing resource |
| Delete | DELETE | `/api/posts/[id]` | Delete resource |

### 3. Zod Validation Schemas

Generates type-safe validation schemas:

```typescript
// lib/validations/post.ts
import { z } from 'zod'

export const postSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
  published: z.boolean().default(false),
  authorId: z.string().uuid(),
  tags: z.array(z.string()).optional(),
  publishedAt: z.date().optional(),
})

export const createPostSchema = postSchema.omit({ id: true })
export const updatePostSchema = postSchema.partial()

export type Post = z.infer<typeof postSchema>
export type CreatePost = z.infer<typeof createPostSchema>
export type UpdatePost = z.infer<typeof updatePostSchema>
```

### 4. Field Type Inference

Automatically infers Zod types from field names and context:

| Field Pattern | Zod Schema | Validation |
|---------------|------------|------------|
| `email` | `z.string().email()` | Email format |
| `url`, `website` | `z.string().url()` | URL format |
| `age`, `count` | `z.number().int().positive()` | Positive integer |
| `price`, `amount` | `z.number().positive()` | Positive number |
| `password` | `z.string().min(8)` | Minimum length |
| `isActive`, `hasPermission` | `z.boolean()` | Boolean |
| `tags`, `categories` | `z.array(z.string())` | String array |
| `createdAt`, `updatedAt` | `z.date()` | Date object |

### 5. Error Handling Utilities

Generates comprehensive error handling:

```typescript
// lib/api/errors.ts
import { NextResponse } from 'next/server'
import { ZodError } from 'zod'

export class APIError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500
  ) {
    super(message)
    this.name = 'APIError'
  }
}

export class NotFoundError extends APIError {
  constructor(resource: string) {
    super(`${resource} not found`, 404)
    this.name = 'NotFoundError'
  }
}

export class ValidationError extends APIError {
  constructor(message: string) {
    super(message, 400)
    this.name = 'ValidationError'
  }
}

export class UnauthorizedError extends APIError {
  constructor(message: string = 'Unauthorized') {
    super(message, 401)
    this.name = 'UnauthorizedError'
  }
}

export function handleAPIError(error: unknown) {
  console.error('API Error:', error)

  if (error instanceof ZodError) {
    return NextResponse.json(
      {
        error: 'Validation failed',
        issues: error.issues,
      },
      { status: 400 }
    )
  }

  if (error instanceof APIError) {
    return NextResponse.json(
      {
        error: error.message,
      },
      { status: error.statusCode }
    )
  }

  return NextResponse.json(
    {
      error: 'Internal server error',
    },
    { status: 500 }
  )
}
```

### 6. Request/Response Types

Generates consistent API response types:

```typescript
// lib/api/types.ts
export interface APIResponse<T = unknown> {
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  page: number
  limit: number
  total: number
  hasMore: boolean
}

export interface APIErrorResponse {
  error: string
  issues?: Array<{
    path: string[]
    message: string
  }>
}
```

## Execution Steps

When this skill is activated:

1. **Parse API Requirements**
   - Extract resource name from prompt
   - Identify CRUD operations needed
   - Detect field types and validation rules
   - Determine authentication requirements

2. **Generate Route Structure**
   - Create appropriate directory structure
   - Generate route.ts files for each endpoint
   - Add dynamic route segments for single resources
   - Include middleware for auth if needed

3. **Create Validation Schemas**
   - Generate Zod schemas for each resource
   - Add field-specific validations
   - Create create/update schema variants
   - Export TypeScript types

4. **Add Error Handling**
   - Generate error classes
   - Create handleAPIError utility
   - Add try-catch blocks in routes
   - Include proper status codes

5. **Generate Type Definitions**
   - Create TypeScript interfaces
   - Export request/response types
   - Generate pagination types if needed
   - Add JSDoc comments

6. **Write Output Files**
   - `app/api/{resource}/route.ts` - List and Create operations
   - `app/api/{resource}/[id]/route.ts` - Get, Update, Delete operations
   - `lib/validations/{resource}.ts` - Zod schemas
   - `lib/api/errors.ts` - Error handling utilities
   - `lib/api/types.ts` - Shared TypeScript types

## Usage Examples

### Example 1: Simple CRUD API

**User Prompt:**
"Create a REST API for managing blog posts with CRUD operations"

**Generated Output:**
- `app/api/posts/route.ts` - GET (list) and POST (create)
- `app/api/posts/[id]/route.ts` - GET (single), PUT (update), DELETE
- `lib/validations/post.ts` - Zod schemas
- All routes with error handling and validation

### Example 2: API with Custom Fields

**User Prompt:**
"Create an API endpoint for users with email, name, age, and avatar URL"

**Generated Output:**
```typescript
// Zod schema with field-specific validations
const userSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().positive().max(150),
  avatarUrl: z.string().url().optional(),
})
```

### Example 3: Authenticated API

**User Prompt:**
"Create protected API routes for managing user profiles with authentication"

**Generated Output:**
- Routes with auth middleware
- Session validation
- User-scoped queries
- Proper 401 error handling

## RESTful Conventions

### HTTP Status Codes

The skill uses proper status codes:

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server errors

### Response Formats

Consistent JSON responses:

```typescript
// Success response
{
  "data": { ... }
}

// Error response
{
  "error": "Error message",
  "issues": [ ... ] // For validation errors
}

// Paginated response
{
  "data": [ ... ],
  "page": 1,
  "limit": 10,
  "total": 50,
  "hasMore": true
}
```

## MCP Integration

### Context7 (Optional)

When Context7 MCP is available:
- Search Next.js documentation for latest patterns
- Find existing API route examples in codebase
- Reference authentication patterns

### Exa (Optional)

When Exa MCP is available:
- Search for Next.js 15 App Router best practices
- Find Zod validation examples
- Discover error handling patterns

## Best Practices

### Route Organization

```
app/api/
  ├── posts/
  │   ├── route.ts           # GET, POST
  │   └── [id]/
  │       └── route.ts       # GET, PUT, DELETE
  ├── users/
  │   ├── route.ts
  │   └── [id]/
  │       └── route.ts
  └── auth/
      └── callback/
          └── route.ts
```

### Validation Strategy

- Validate all input data with Zod
- Use `.parse()` for strict validation (throws on error)
- Use `.safeParse()` for custom error handling
- Create separate schemas for create/update operations
- Add custom refinements for complex validations

### Error Handling

- Always use try-catch in route handlers
- Use custom error classes for different error types
- Log errors server-side
- Never expose sensitive error details to client
- Return consistent error response format

### Type Safety

- Export types from Zod schemas using `z.infer`
- Use TypeScript strict mode
- Add JSDoc comments for better IDE support
- Create shared types for common patterns

## Limitations

- Next.js App Router only (not Pages Router)
- REST APIs (GraphQL requires additional setup)
- PostgreSQL assumed (can be adapted for other databases)
- Authentication requires additional configuration

## Future Enhancements

- GraphQL schema generation
- OpenAPI/Swagger documentation generation
- API rate limiting middleware
- Request caching strategies
- Webhook handlers
- Real-time API support (Server-Sent Events)
- API versioning support
- Automated API testing generation

---

**Skill Version:** 1.0.0
**Last Updated:** 2026-01-04
**Maintainer:** Turbocat Agent System
