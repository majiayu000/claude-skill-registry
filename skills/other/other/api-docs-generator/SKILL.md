---
name: api-docs-generator
description: Generate OpenAPI 3.1 specification from existing Next.js API routes. Use when asked to generate API docs, create OpenAPI spec, document endpoints, generate Swagger file, or create API documentation.
---

# API Docs Generator

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Process

1. Scan the `app/api/` directory for all `route.ts` files.
2. For each route file, extract: exported HTTP method handlers, URL path (from file path), request/response types, Zod schemas, middleware/auth patterns.
3. Generate a valid OpenAPI 3.1 specification.
4. Output as YAML (default) or JSON if requested.

## Route Scanning

### Path Extraction

Convert Next.js App Router file paths to OpenAPI paths:

| File path | OpenAPI path |
|---|---|
| `app/api/users/route.ts` | `/api/users` |
| `app/api/users/[id]/route.ts` | `/api/users/{id}` |
| `app/api/posts/[postId]/comments/route.ts` | `/api/posts/{postId}/comments` |
| `app/api/[...slug]/route.ts` | `/api/{slug}` (note: catch-all) |

### Method Extraction

Detect exported functions: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`. Each becomes an operation in the spec.

### Schema Extraction

#### From Zod Schemas

If the route uses Zod for validation, extract the schema structure directly:

```typescript
// Detect this pattern:
const createSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
});

// Convert to OpenAPI:
// type: object
// properties:
//   name: { type: string, minLength: 1, maxLength: 100 }
//   email: { type: string, format: email }
// required: [name, email]
```

#### From TypeScript Types

If no Zod schema exists, infer from TypeScript type annotations on the request/response.

### Auth Detection

Detect common auth patterns and add security schemes:

```typescript
// Pattern: session check → Bearer auth or cookie session
const session = await auth();
if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

// Pattern: API key header → API key auth
const apiKey = request.headers.get("x-api-key");
```

### Response Detection

Scan `NextResponse.json(...)` calls and their status codes to build response schemas:

```typescript
// 200 with data shape
return NextResponse.json({ data: items, pagination: {...} });

// 400 with error shape
return NextResponse.json({ error: "...", details: ... }, { status: 400 });
```

## Common Patterns

### Pagination Parameters

Detect `page`, `limit`, `offset`, `cursor` in query params and document as standard pagination:

```yaml
parameters:
  - name: page
    in: query
    schema: { type: integer, minimum: 1, default: 1 }
  - name: limit
    in: query
    schema: { type: integer, minimum: 1, maximum: 100, default: 20 }
```

### File Uploads

Detect `request.formData()` and document as `multipart/form-data`.

### Consistent Error Schema

Extract the error response format used across routes and define as a reusable component:

```yaml
components:
  schemas:
    ErrorResponse:
      type: object
      properties:
        error: { type: string }
        details: {}
      required: [error]
```

## Output Structure

```yaml
openapi: "3.1.0"
info:
  title: "{project name} API"
  version: "1.0.0"
paths:
  /api/users:
    get:
      summary: List users
      parameters: [...]
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema: { $ref: "#/components/schemas/UserListResponse" }
    post:
      summary: Create user
      requestBody:
        content:
          application/json:
            schema: { $ref: "#/components/schemas/CreateUserInput" }
      responses:
        "201": ...
        "400": ...
components:
  schemas:
    User: ...
    CreateUserInput: ...
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
```

## Output Format

```
## Generated API Documentation

**File**: `openapi.yaml` (or `openapi.json`)
**Endpoints discovered**: X
**Schemas extracted**: X

[Generated spec]

### Endpoints Summary
| Method | Path | Summary | Auth |
|--------|------|---------|------|
| GET | /api/users | List users | Yes |
| POST | /api/users | Create user | Yes |
```

## Reference

See [references/openapi-patterns.md](references/openapi-patterns.md) for OpenAPI 3.1 structure, Zod-to-OpenAPI mapping, and security scheme patterns.
