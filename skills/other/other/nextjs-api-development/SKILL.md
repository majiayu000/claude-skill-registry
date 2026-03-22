---
name: nextjs-api-development
description: |
  REST API development with Next.js 15 App Router.
  Dual authentication (API Key + Session), dynamic entities, metadata system.
  Use this skill to create endpoints, validate APIs, or understand API patterns.
allowed-tools: Read, Glob, Grep, Bash(python:*)
version: 1.1.0
---

# Next.js API Development Skill

Patterns and tools for REST API development with Next.js 15 App Router.

## Architecture Overview

```
app/api/v1/
├── [entity]/              # Dynamic CRUD (auto-generated from registry)
│   ├── route.ts          # GET (list) / POST (create)
│   └── [id]/route.ts     # GET (read) / PATCH (update) / DELETE
├── (contents)/           # Custom overrides (parentheses = not in URL)
│   └── tasks/            # Example: custom implementation
├── users/                # Core endpoints (not dynamic)
├── api-keys/             # API key management
├── auth/                 # Authentication endpoints
├── billing/              # Billing & subscriptions
├── teams/                # Team management
└── theme/                # Theme-specific endpoints
```

> **📍 Context-Aware Paths:** Core API routes (`app/api/v1/`) are read-only in consumer projects.
> Create custom endpoints in `contents/themes/{theme}/app/api/` or override via `(contents)/` pattern.
> See `core-theme-responsibilities` skill for complete rules.

## When to Use This Skill

- Creating new API endpoints
- Implementing dual authentication
- Adding custom business logic to entities
- Debugging API issues
- Testing API endpoints
- Understanding API patterns

## Core Patterns

### Route Handler Pattern (MANDATORY)

All routes MUST use `withApiLogging` wrapper and `addCorsHeaders`:

```typescript
import { NextRequest, NextResponse } from 'next/server'
import { queryWithRLS, mutateWithRLS } from '@/core/lib/db'
import {
  createApiResponse,
  createApiError,
  createPaginationMeta,
  parsePaginationParams,
  withApiLogging,
  handleCorsPreflightRequest,
  addCorsHeaders,
} from '@/core/lib/api/helpers'
import { authenticateRequest } from '@/core/lib/api/auth/dual-auth'

// Handle CORS preflight
export async function OPTIONS() {
  return handleCorsPreflightRequest()
}

// GET /api/v1/[endpoint] - List resources
export const GET = withApiLogging(async (req: NextRequest): Promise<NextResponse> => {
  try {
    // 1. Authenticate (API Key OR Session)
    const authResult = await authenticateRequest(req)

    if (!authResult.success) {
      return NextResponse.json(
        { success: false, error: 'Authentication required', code: 'AUTHENTICATION_FAILED' },
        { status: 401 }
      )
    }

    if (authResult.rateLimitResponse) {
      return authResult.rateLimitResponse as NextResponse
    }

    // 2. Parse pagination
    const { page, limit, offset } = parsePaginationParams(req)

    // 3. Fetch data with RLS
    const data = await queryWithRLS(
      `SELECT * FROM "table" WHERE 1=1 ORDER BY "createdAt" DESC LIMIT $1 OFFSET $2`,
      [limit, offset],
      authResult.user!.id
    )

    // 4. Create response with pagination
    const paginationMeta = createPaginationMeta(page, limit, total)
    const response = createApiResponse(data, paginationMeta)
    return addCorsHeaders(response)
  } catch (error) {
    console.error('[ENDPOINT] Error:', error)
    const response = createApiError('Failed to fetch data', 500)
    return addCorsHeaders(response)
  }
})
```

### Response Helpers (MANDATORY)

```typescript
import { createApiResponse, createApiError } from '@/core/lib/api/helpers'

// Success responses - always wrap with addCorsHeaders
const response = createApiResponse(data)
return addCorsHeaders(response)

const response = createApiResponse(data, { created: true }, 201)
return addCorsHeaders(response)

const response = createApiResponse(data, paginationMeta)
return addCorsHeaders(response)

// Error responses - always wrap with addCorsHeaders
const response = createApiError('Not found', 404)
return addCorsHeaders(response)

const response = createApiError('Validation error', 400, zodError.issues, 'VALIDATION_ERROR')
return addCorsHeaders(response)
```

### Response Format

```typescript
// Success
{
  "success": true,
  "data": { /* entity data */ },
  "info": {
    "timestamp": "2024-01-17T10:30:00Z",
    "pagination": { /* if applicable */ }
  }
}

// Error
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": { /* optional */ },
  "info": {
    "timestamp": "2024-01-17T10:30:00Z"
  }
}
```

## Route Types

### 1. Dynamic Entity Routes

For standard CRUD operations. Automatically generated from EntityRegistry.

```
GET  /api/v1/products     → List products
POST /api/v1/products     → Create product
GET  /api/v1/products/123 → Read product
PATCH /api/v1/products/123 → Update product
DELETE /api/v1/products/123 → Delete product
```

**When to use:** Standard CRUD, basic validation, standard pagination.

### 2. Custom Override Routes

For special business logic. Use `(contents)/` folder.

```typescript
// app/api/v1/(contents)/tasks/route.ts
export const POST = withApiLogging(async (req: NextRequest): Promise<NextResponse> => {
  const authResult = await authenticateRequest(req)

  // Custom logic: Admin can create for other users
  if (authResult.user?.role === 'admin' && body.userId) {
    task.userId = body.userId
  } else {
    task.userId = authResult.user!.id
  }

  // ... rest of implementation
  const response = createApiResponse(data, { created: true }, 201)
  return addCorsHeaders(response)
})
```

**When to use:** Complex validation, admin-level operations, external integrations.

### 3. Core Endpoints

System endpoints that cannot be overridden.

- `/api/v1/users` - User management
- `/api/v1/api-keys` - API key management
- `/api/v1/auth` - Authentication

## Input Validation

```typescript
import { z } from 'zod'

const CreateProductSchema = z.object({
  title: z.string().min(1).max(255),
  price: z.number().positive(),
  status: z.enum(['active', 'inactive']).default('active'),
})

export const POST = withApiLogging(async (req: NextRequest): Promise<NextResponse> => {
  try {
    const body = CreateProductSchema.parse(await req.json())
    // Validated body ready to use
  } catch (error) {
    if (error instanceof z.ZodError) {
      const response = createApiError('Validation error', 400, error.issues, 'VALIDATION_ERROR')
      return addCorsHeaders(response)
    }
    throw error
  }
})
```

## Scripts

### Scaffold New Endpoint
```bash
# Basic endpoint
python .claude/skills/nextjs-api-development/scripts/scaffold-endpoint.py \
  --name products \
  --methods GET,POST \
  --auth required

# With [id] route for single resource operations
python .claude/skills/nextjs-api-development/scripts/scaffold-endpoint.py \
  --name products \
  --methods GET,POST \
  --auth required \
  --with-id

# Preview without creating files
python .claude/skills/nextjs-api-development/scripts/scaffold-endpoint.py \
  --name products \
  --dry-run
```

### Generate CRUD Tests
```bash
# Generate test file only
python .claude/skills/nextjs-api-development/scripts/generate-crud-tests.py \
  --entity products

# Also generate API Controller
python .claude/skills/nextjs-api-development/scripts/generate-crud-tests.py \
  --entity products \
  --with-controller

# Preview
python .claude/skills/nextjs-api-development/scripts/generate-crud-tests.py \
  --entity products \
  --dry-run
```

### Validate API Structure
```bash
python .claude/skills/nextjs-api-development/scripts/validate-api.py \
  --path app/api/v1/

# Strict mode (exit with error if violations found)
python .claude/skills/nextjs-api-development/scripts/validate-api.py \
  --path app/api/v1/ \
  --strict
```

## Testing Pattern

Tests use API Controllers that extend `BaseAPIController`:

```typescript
// In test file
const ProductsAPIController = require('../../../src/controllers/ProductsAPIController.js')

describe('Products API - CRUD Operations', {
  tags: ['@api', '@feat-products', '@crud', '@regression']
}, () => {
  let productsAPI: any

  const SUPERADMIN_API_KEY = Cypress.env('SUPERADMIN_API_KEY')
  const TEAM_ID = Cypress.env('TEAM_ID')

  before(() => {
    productsAPI = new ProductsAPIController(BASE_URL, SUPERADMIN_API_KEY, TEAM_ID)
  })

  it('should list products', () => {
    productsAPI.getProducts().then((response: any) => {
      productsAPI.validateSuccessResponse(response, 200)
      expect(response.body.data).to.be.an('array')
    })
  })
})
```

## Security Best Practices

### SQL Injection Prevention

```typescript
// ✅ CORRECT - Parameterized queries with queryWithRLS
const result = await queryWithRLS(
  `SELECT * FROM products WHERE "userId" = $1 AND status = $2 LIMIT $3`,
  [userId, status, limit],
  authResult.user!.id
)

// ❌ NEVER - String concatenation
const query = `SELECT * FROM products WHERE userId = '${userId}'`
```

## Anti-Patterns

```typescript
// ❌ NEVER: Use export async function instead of withApiLogging
export async function GET(request: NextRequest) { }

// ❌ NEVER: Return response without addCorsHeaders
return createApiResponse(data)

// ❌ NEVER: Use raw NextResponse.json
return NextResponse.json({ data })

// ❌ NEVER: Skip authentication
export async function GET(request: NextRequest) {
  const data = await db.query('SELECT * FROM products')
  return createApiResponse(data)
}

// ✅ CORRECT: Full pattern
export const GET = withApiLogging(async (req: NextRequest): Promise<NextResponse> => {
  const authResult = await authenticateRequest(req)
  // ...
  const response = createApiResponse(data)
  return addCorsHeaders(response)
})
```

## Checklist for New Endpoint

- [ ] Uses `withApiLogging` wrapper
- [ ] Has `OPTIONS` handler using `handleCorsPreflightRequest()`
- [ ] All responses wrapped with `addCorsHeaders()`
- [ ] Dual authentication implemented
- [ ] Input validation with Zod schema
- [ ] Response helpers used (`createApiResponse`, `createApiError`)
- [ ] Proper error handling with try/catch
- [ ] Pagination for list endpoints using `parsePaginationParams`
- [ ] API scopes added to `core/lib/api/keys.ts`
- [ ] Cypress tests created with API Controller pattern
