---
name: api-designing
description: Design consistent RESTful API endpoints, request/response formats, and error handling patterns. Use when creating new API routes, designing API structure, planning request/response schemas, or establishing API conventions. Triggers on requests like "design an API for", "create API endpoints", "plan the API structure", "design the response format", or "API conventions".
---

# API Designing

Design consistent RESTful APIs for this Next.js application.

## Process

1. **Identify resources** - What entities does the API manage?
2. **Define operations** - CRUD and custom actions
3. **Design endpoints** - URL structure and methods
4. **Specify schemas** - Request/response formats
5. **Plan error handling** - Consistent error responses

## RESTful Conventions

### URL Structure

```
/api/[resource]              # Collection
/api/[resource]/[id]         # Individual resource
/api/[resource]/[id]/[sub]   # Nested resource
```

### HTTP Methods

| Method | Purpose | Idempotent |
|--------|---------|------------|
| GET | Retrieve resource(s) | Yes |
| POST | Create resource | No |
| PUT | Replace resource | Yes |
| PATCH | Partial update | Yes |
| DELETE | Remove resource | Yes |

### Existing Project Patterns

Admin routes follow this structure:
```
/admin/api/articles          GET (list), POST (create)
/admin/api/articles/[id]     GET, PUT, DELETE
/admin/api/tags              GET, POST
/admin/api/media             GET, POST
/admin/api/users             GET, POST
/admin/api/users/[id]/approve POST (action)
```

## Request Schemas

### List Endpoints (GET collection)

Query parameters:
```
?page=1              # Pagination
?limit=10            # Items per page
?sort=created_at     # Sort field
?order=desc          # Sort direction
?status=published    # Filtering
?search=query        # Text search
```

### Create/Update (POST/PUT)

```typescript
// Request body
{
  title: string;
  body: string;
  slug?: string;      // Optional, auto-generate if missing
  published?: boolean;
  media_id?: number;
}
```

## Response Schemas

### Success Responses

**Single resource:**
```typescript
{
  success: true,
  data: {
    id: number;
    title: string;
    // ... resource fields
  }
}
```

**Collection:**
```typescript
{
  success: true,
  data: Resource[],
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  }
}
```

**Action result:**
```typescript
{
  success: true,
  message: "Article published successfully"
}
```

### Error Responses

```typescript
// 400 Bad Request - Validation error
{
  success: false,
  error: "Validation failed",
  details: {
    title: "Title is required",
    slug: "Slug already exists"
  }
}

// 401 Unauthorized
{
  success: false,
  error: "Authentication required"
}

// 403 Forbidden
{
  success: false,
  error: "Admin access required"
}

// 404 Not Found
{
  success: false,
  error: "Article not found"
}

// 500 Internal Server Error
{
  success: false,
  error: "An unexpected error occurred"
}
```

## Implementation Pattern

```typescript
// src/app/admin/api/[resource]/route.ts
import { NextRequest, NextResponse } from "next/server";
import { requireEditor } from "@/lib/api-auth";
import { getDb } from "@/lib/db";

export async function GET(request: NextRequest) {
  const auth = await requireEditor();
  if (!auth.authorized) return auth.response;

  try {
    const db = await getDb();
    const { searchParams } = new URL(request.url);

    const page = parseInt(searchParams.get("page") || "1");
    const limit = parseInt(searchParams.get("limit") || "10");
    const offset = (page - 1) * limit;

    const items = await db.prepare(`
      SELECT * FROM resources
      ORDER BY created_at DESC
      LIMIT ? OFFSET ?
    `).bind(limit, offset).all();

    const { total } = await db.prepare(`
      SELECT COUNT(*) as total FROM resources
    `).first();

    return NextResponse.json({
      success: true,
      data: items.results,
      pagination: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    });
  } catch (error) {
    console.error("API error:", error);
    return NextResponse.json(
      { success: false, error: "Failed to fetch resources" },
      { status: 500 }
    );
  }
}
```

## Validation

Validate at API boundaries:

```typescript
function validateArticle(data: unknown): { valid: boolean; errors?: Record<string, string> } {
  const errors: Record<string, string> = {};

  if (!data || typeof data !== 'object') {
    return { valid: false, errors: { _: 'Invalid request body' } };
  }

  const { title, body, slug } = data as Record<string, unknown>;

  if (!title || typeof title !== 'string') {
    errors.title = 'Title is required';
  }
  if (!body || typeof body !== 'string') {
    errors.body = 'Body is required';
  }
  if (slug && typeof slug !== 'string') {
    errors.slug = 'Slug must be a string';
  }

  return Object.keys(errors).length ? { valid: false, errors } : { valid: true };
}
```

## Output

Provide API design deliverables:
1. Endpoint specifications (URL, method, auth)
2. Request schema (body, query params)
3. Response schema (success, error)
4. Example implementation code
