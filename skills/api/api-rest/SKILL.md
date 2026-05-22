---
name: api-rest
description: REST API conventions for Next.js App Router with Zod validation and standardized error handling. This skill should be used when creating API routes, implementing CRUD operations, or establishing API patterns for a project.
---

# REST API Skill

Conventions and patterns for building REST APIs in Next.js App Router with type-safe validation and consistent error handling.

## When to Use This Skill

- Creating new API routes
- Implementing CRUD operations
- Setting up validation with Zod
- Establishing error handling patterns
- Designing resource endpoints

## Core Conventions

### Resource Naming

**Resources are always plural**:

| Resource | Endpoint |
|----------|----------|
| Project | `/api/projects` |
| User | `/api/users` |
| Task | `/api/tasks` |

### HTTP Methods

| Method | Purpose | Example |
|--------|---------|---------|
| GET | Read | `GET /api/projects` |
| POST | Create | `POST /api/projects` |
| PATCH | Partial update | `PATCH /api/projects/:id` |
| PUT | Full replace | `PUT /api/projects/:id` |
| DELETE | Remove | `DELETE /api/projects/:id` |

### URL Structure

```
/api/{resource}           # Collection
/api/{resource}/{id}      # Single item
/api/{resource}/{id}/{sub-resource}  # Nested resource
```

Examples:
```
GET    /api/projects              # List all projects
POST   /api/projects              # Create project
GET    /api/projects/123          # Get project 123
PATCH  /api/projects/123          # Update project 123
DELETE /api/projects/123          # Delete project 123
GET    /api/projects/123/tasks    # List tasks for project 123
```

## Directory Structure

```
src/app/api/
├── projects/
│   ├── route.ts              # GET (list), POST (create)
│   └── [id]/
│       ├── route.ts          # GET, PATCH, DELETE
│       └── tasks/
│           └── route.ts      # Nested resource
├── users/
│   ├── route.ts
│   └── [id]/
│       └── route.ts
└── _lib/
    ├── errors.ts             # Error utilities
    ├── validation.ts         # Zod helpers
    └── response.ts           # Response helpers
```

## Response Format

### Success Responses

```typescript
// Single resource
{
  "data": {
    "id": "123",
    "name": "Project Alpha",
    "createdAt": "2025-01-15T10:30:00Z"
  }
}

// Collection
{
  "data": [
    { "id": "123", "name": "Project Alpha" },
    { "id": "124", "name": "Project Beta" }
  ],
  "meta": {
    "total": 42,
    "page": 1,
    "pageSize": 20
  }
}

// Empty success (204 No Content for DELETE)
// No body
```

### Error Responses

```typescript
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request body",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

## Setup

### Error Utilities

Create `src/app/api/_lib/errors.ts`:

```typescript
import { NextResponse } from 'next/server';
import { ZodError } from 'zod';

export type ApiErrorCode =
  | 'VALIDATION_ERROR'
  | 'NOT_FOUND'
  | 'UNAUTHORIZED'
  | 'FORBIDDEN'
  | 'CONFLICT'
  | 'INTERNAL_ERROR';

interface ApiError {
  code: ApiErrorCode;
  message: string;
  details?: unknown;
}

export function errorResponse(
  code: ApiErrorCode,
  message: string,
  status: number,
  details?: unknown
) {
  const error: ApiError = { code, message };
  if (details) error.details = details;
  
  return NextResponse.json({ error }, { status });
}

export function validationError(error: ZodError) {
  const details = error.errors.map((err) => ({
    field: err.path.join('.'),
    message: err.message,
  }));
  
  return errorResponse('VALIDATION_ERROR', 'Invalid request', 400, details);
}

export function notFound(resource: string) {
  return errorResponse('NOT_FOUND', `${resource} not found`, 404);
}

export function unauthorized(message = 'Unauthorized') {
  return errorResponse('UNAUTHORIZED', message, 401);
}

export function forbidden(message = 'Forbidden') {
  return errorResponse('FORBIDDEN', message, 403);
}

export function conflict(message: string) {
  return errorResponse('CONFLICT', message, 409);
}

export function internalError(message = 'Internal server error') {
  return errorResponse('INTERNAL_ERROR', message, 500);
}
```

### Validation Helpers

Create `src/app/api/_lib/validation.ts`:

```typescript
import { z, ZodSchema, ZodError } from 'zod';
import { NextRequest } from 'next/server';

export async function parseBody<T>(
  request: NextRequest,
  schema: ZodSchema<T>
): Promise<{ data: T; error: null } | { data: null; error: ZodError }> {
  try {
    const body = await request.json();
    const data = schema.parse(body);
    return { data, error: null };
  } catch (error) {
    if (error instanceof ZodError) {
      return { data: null, error };
    }
    throw error;
  }
}

export function parseQuery<T>(
  request: NextRequest,
  schema: ZodSchema<T>
): { data: T; error: null } | { data: null; error: ZodError } {
  try {
    const params = Object.fromEntries(request.nextUrl.searchParams.entries());
    const data = schema.parse(params);
    return { data, error: null };
  } catch (error) {
    if (error instanceof ZodError) {
      return { data: null, error };
    }
    throw error;
  }
}

// Common schemas
export const paginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  pageSize: z.coerce.number().int().positive().max(100).default(20),
});

export const idParamSchema = z.object({
  id: z.string().min(1),
});
```

### Response Helpers

Create `src/app/api/_lib/response.ts`:

```typescript
import { NextResponse } from 'next/server';

export function json<T>(data: T, status = 200) {
  return NextResponse.json({ data }, { status });
}

export function jsonList<T>(
  data: T[],
  meta: { total: number; page: number; pageSize: number }
) {
  return NextResponse.json({ data, meta });
}

export function created<T>(data: T) {
  return NextResponse.json({ data }, { status: 201 });
}

export function noContent() {
  return new NextResponse(null, { status: 204 });
}
```

## Route Implementations

### Collection Route (List + Create)

Create `src/app/api/projects/route.ts`:

```typescript
import { NextRequest } from 'next/server';
import { z } from 'zod';
import { db, project } from '@/lib/db';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { eq, desc, sql } from 'drizzle-orm';
import { json, jsonList, created } from '../_lib/response';
import { parseBody, parseQuery, paginationSchema } from '../_lib/validation';
import { validationError, unauthorized, internalError } from '../_lib/errors';

// Query params schema
const listQuerySchema = paginationSchema.extend({
  status: z.enum(['active', 'archived']).optional(),
  search: z.string().optional(),
});

// Create body schema
const createSchema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().optional(),
});

// GET /api/projects
export async function GET(request: NextRequest) {
  try {
    const session = await auth.api.getSession({ headers: await headers() });
    if (!session) return unauthorized();
    
    const { data: query, error } = parseQuery(request, listQuerySchema);
    if (error) return validationError(error);
    
    const { page, pageSize, status, search } = query;
    const offset = (page - 1) * pageSize;
    
    // Build where conditions
    const conditions = [eq(project.userId, session.user.id)];
    if (status) conditions.push(eq(project.status, status));
    // Add search if needed
    
    const [items, countResult] = await Promise.all([
      db.query.project.findMany({
        where: and(...conditions),
        orderBy: desc(project.createdAt),
        limit: pageSize,
        offset,
      }),
      db.select({ count: sql<number>`count(*)` })
        .from(project)
        .where(and(...conditions)),
    ]);
    
    return jsonList(items, {
      total: Number(countResult[0]?.count ?? 0),
      page,
      pageSize,
    });
  } catch (error) {
    console.error('GET /api/projects error:', error);
    return internalError();
  }
}

// POST /api/projects
export async function POST(request: NextRequest) {
  try {
    const session = await auth.api.getSession({ headers: await headers() });
    if (!session) return unauthorized();
    
    const { data: body, error } = await parseBody(request, createSchema);
    if (error) return validationError(error);
    
    const [newProject] = await db.insert(project).values({
      ...body,
      userId: session.user.id,
    }).returning();
    
    return created(newProject);
  } catch (error) {
    console.error('POST /api/projects error:', error);
    return internalError();
  }
}
```

### Item Route (Get + Update + Delete)

Create `src/app/api/projects/[id]/route.ts`:

```typescript
import { NextRequest } from 'next/server';
import { z } from 'zod';
import { db, project } from '@/lib/db';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { eq, and } from 'drizzle-orm';
import { json, noContent } from '../../_lib/response';
import { parseBody } from '../../_lib/validation';
import { validationError, unauthorized, notFound, forbidden, internalError } from '../../_lib/errors';

interface RouteParams {
  params: Promise<{ id: string }>;
}

const updateSchema = z.object({
  name: z.string().min(1).max(255).optional(),
  description: z.string().optional(),
  status: z.enum(['active', 'archived']).optional(),
});

// GET /api/projects/:id
export async function GET(request: NextRequest, { params }: RouteParams) {
  try {
    const { id } = await params;
    const session = await auth.api.getSession({ headers: await headers() });
    if (!session) return unauthorized();
    
    const item = await db.query.project.findFirst({
      where: eq(project.id, id),
    });
    
    if (!item) return notFound('Project');
    if (item.userId !== session.user.id) return forbidden();
    
    return json(item);
  } catch (error) {
    console.error('GET /api/projects/:id error:', error);
    return internalError();
  }
}

// PATCH /api/projects/:id
export async function PATCH(request: NextRequest, { params }: RouteParams) {
  try {
    const { id } = await params;
    const session = await auth.api.getSession({ headers: await headers() });
    if (!session) return unauthorized();
    
    const { data: body, error } = await parseBody(request, updateSchema);
    if (error) return validationError(error);
    
    // Check ownership
    const existing = await db.query.project.findFirst({
      where: eq(project.id, id),
    });
    
    if (!existing) return notFound('Project');
    if (existing.userId !== session.user.id) return forbidden();
    
    const [updated] = await db.update(project)
      .set({ ...body, updatedAt: new Date() })
      .where(eq(project.id, id))
      .returning();
    
    return json(updated);
  } catch (error) {
    console.error('PATCH /api/projects/:id error:', error);
    return internalError();
  }
}

// DELETE /api/projects/:id
export async function DELETE(request: NextRequest, { params }: RouteParams) {
  try {
    const { id } = await params;
    const session = await auth.api.getSession({ headers: await headers() });
    if (!session) return unauthorized();
    
    // Check ownership
    const existing = await db.query.project.findFirst({
      where: eq(project.id, id),
    });
    
    if (!existing) return notFound('Project');
    if (existing.userId !== session.user.id) return forbidden();
    
    await db.delete(project).where(eq(project.id, id));
    
    return noContent();
  } catch (error) {
    console.error('DELETE /api/projects/:id error:', error);
    return internalError();
  }
}
```

## Query Parameters

### Filtering

```
GET /api/projects?status=active&priority=high
```

```typescript
const filterSchema = z.object({
  status: z.enum(['active', 'archived']).optional(),
  priority: z.enum(['low', 'medium', 'high']).optional(),
});
```

### Sorting

```
GET /api/projects?sort=createdAt&order=desc
```

```typescript
const sortSchema = z.object({
  sort: z.enum(['createdAt', 'name', 'updatedAt']).default('createdAt'),
  order: z.enum(['asc', 'desc']).default('desc'),
});
```

### Search

```
GET /api/projects?search=alpha
```

```typescript
// In query
if (search) {
  conditions.push(
    or(
      ilike(project.name, `%${search}%`),
      ilike(project.description, `%${search}%`)
    )
  );
}
```

### Pagination

```
GET /api/projects?page=2&pageSize=20
```

Response includes meta:
```json
{
  "data": [...],
  "meta": {
    "total": 42,
    "page": 2,
    "pageSize": 20
  }
}
```

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PATCH, PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | No/invalid auth |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate, constraint violation |
| 500 | Internal Error | Unexpected server error |

## Best Practices

### Do

- Use plural resource names (`/projects` not `/project`)
- Return consistent response shapes
- Validate all inputs with Zod
- Use appropriate HTTP methods and status codes
- Include pagination for list endpoints
- Log errors server-side

### Don't

- Don't use verbs in URLs (`/getProjects` ❌)
- Don't return different shapes for same endpoint
- Don't expose internal error details to clients
- Don't skip authentication checks
- Don't use GET for mutations

## Type Safety

Export types from your schemas:

```typescript
// In a shared types file
import { z } from 'zod';

export const createProjectSchema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().optional(),
});

export type CreateProjectInput = z.infer<typeof createProjectSchema>;
```

Use in frontend:

```typescript
import type { CreateProjectInput } from '@/lib/api-types';

async function createProject(data: CreateProjectInput) {
  const res = await fetch('/api/projects', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  // ...
}
```
