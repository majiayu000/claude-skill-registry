---
name: rate-limiting
description: |
  Rate limiting patterns for all API endpoints in this Next.js application.
  Covers distributed rate limiting with Redis, tier selection, HOC patterns, and security best practices.
  Use this skill when creating new API endpoints or reviewing rate limiting implementation.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Rate Limiting Skill

Rate limiting patterns and best practices for protecting API endpoints from abuse and DDoS attacks.

## Architecture Overview

```
core/lib/
├── api/
│   └── rate-limit.ts          # withRateLimitTier HOC, checkDistributedRateLimit
└── rate-limit-redis.ts        # Redis/Upstash distributed rate limiting

packages/core/templates/app/api/  # All template routes use rate limiting
plugins/*/api/                    # Plugin API routes
themes/*/api/                     # Theme API routes
```

## When to Use This Skill

- **ALWAYS** when creating new API endpoints
- Reviewing existing endpoints for rate limiting coverage
- Debugging rate limit responses (429 errors)
- Configuring Redis for distributed rate limiting
- Choosing appropriate rate limit tiers

## MANDATORY RULE: All Endpoints Must Have Rate Limiting

**CRITICAL:** Every `route.ts` file that exports HTTP handlers (GET, POST, PUT, PATCH, DELETE)
MUST use the `withRateLimitTier` HOC wrapper.

**Only exceptions:**
- `/api/auth/**` - Better Auth handles its own rate limiting
- `/api/cron/**` - Protected by Vercel cron signatures
- `/api/webhooks/**` - Protected by webhook signatures

## Rate Limit Tiers

| Tier | Limit | Window | Use Case |
|------|-------|--------|----------|
| `auth` | 5 | 15 min | Authentication endpoints (login, register, reset password) |
| `read` | 200 | 1 min | GET requests, read-only operations |
| `write` | 50 | 1 min | POST, PUT, PATCH, DELETE operations |
| `api` | 100 | 1 min | General API (default tier) |
| `strict` | 10 | 1 hr | Sensitive operations (bulk delete, admin actions) |

## How to Apply Rate Limiting

### Basic Usage

```typescript
// route.ts
import { NextRequest, NextResponse } from 'next/server';
import { withRateLimitTier } from '@nextsparkjs/core/lib/api/rate-limit';

// For GET (read operations)
export const GET = withRateLimitTier(async (request: NextRequest) => {
  // Your handler logic
  return NextResponse.json({ data: [] });
}, 'read');

// For POST (write operations)
export const POST = withRateLimitTier(async (request: NextRequest) => {
  // Your handler logic
  return NextResponse.json({ created: true }, { status: 201 });
}, 'write');

// For PUT/PATCH (update operations)
export const PUT = withRateLimitTier(async (request: NextRequest) => {
  // Your handler logic
  return NextResponse.json({ updated: true });
}, 'write');

// For DELETE
export const DELETE = withRateLimitTier(async (request: NextRequest) => {
  // Your handler logic
  return NextResponse.json({ deleted: true });
}, 'write');
```

### With Dynamic Routes

```typescript
// [id]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { withRateLimitTier } from '@nextsparkjs/core/lib/api/rate-limit';

// Handler receives route params as second argument
export const GET = withRateLimitTier(async (
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) => {
  const { id } = await params;
  return NextResponse.json({ id });
}, 'read');
```

### For Sensitive Operations

```typescript
// Use 'strict' tier for operations like bulk delete, admin actions
export const DELETE = withRateLimitTier(async (request: NextRequest) => {
  // Bulk delete or sensitive operation
  return NextResponse.json({ deleted: true });
}, 'strict');
```

## Tier Selection Guidelines

### Use 'read' tier for:
- All GET requests
- Search endpoints
- List/pagination endpoints
- Public data endpoints
- Status/health check endpoints

### Use 'write' tier for:
- POST (create) operations
- PUT/PATCH (update) operations
- DELETE (remove) operations
- Form submissions
- File uploads

### Use 'strict' tier for:
- Bulk operations (delete all, import, export)
- Admin-only operations
- Superadmin endpoints
- Operations with significant server load
- AI/LLM endpoints with high compute cost

### Use 'auth' tier for:
- Login attempts
- Registration
- Password reset requests
- Email verification resends
- Any authentication-related endpoint

### Use 'api' tier for:
- General-purpose API endpoints
- When unsure (default fallback)
- Mixed read/write operations

## Response Headers

All rate-limited responses include these headers:

```
X-RateLimit-Limit: 200        # Max requests in window
X-RateLimit-Remaining: 150    # Requests remaining
X-RateLimit-Reset: 1705432100 # Unix timestamp when window resets
```

When limit is exceeded (429 response):

```
Retry-After: 45              # Seconds until retry allowed
```

## 429 Response Format

```json
{
  "success": false,
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later.",
  "code": "RATE_LIMIT_EXCEEDED",
  "meta": {
    "limit": 200,
    "remaining": 0,
    "resetTime": "2024-01-16T12:00:00.000Z",
    "retryAfter": 45
  }
}
```

## Rate Limiting Strategy

The system uses a **per-tier global limit** strategy (NOT per-endpoint):

```
User makes requests:
  GET /api/v1/products      → counts against 'read' tier
  GET /api/v1/orders        → counts against 'read' tier
  GET /api/v1/customers     → counts against 'read' tier

All 3 requests count toward the SAME 200/min 'read' limit
```

**Why global per-tier?**
- Prevents attackers from hitting multiple endpoints to bypass limits
- Simpler mental model for users
- More effective DDoS protection

## Identifier Strategy

Rate limits are tracked by:

1. **API Key** (when present): `{tier}:apikey:{first16chars}`
2. **IP Address** (fallback): `{tier}:ip:{clientIp}`

This allows:
- Per-user limits for authenticated API requests
- IP-based limits for unauthenticated or session-based requests

## Redis Configuration (Production)

For distributed rate limiting across multiple instances, configure Redis:

```env
# Upstash Redis (recommended for Vercel)
UPSTASH_REDIS_REST_URL=https://xxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=xxx

# Or standard Redis
REDIS_URL=redis://localhost:6379
```

Without Redis, the system falls back to in-memory rate limiting (single-instance only).

## Disabling Rate Limiting (Development/Testing)

To disable rate limiting completely (useful for development, testing, or debugging):

```env
# .env.local or .env
DISABLE_RATE_LIMITING=true
```

When disabled:
- All rate limit checks are bypassed
- A warning is logged once: `[RateLimit] WARNING: Rate limiting is DISABLED...`
- Handlers execute without rate limit headers

**WARNING:** Never disable rate limiting in production environments!

**Use cases for disabling:**
- Local development when hitting limits during testing
- Running automated tests that make many requests
- Debugging API behavior without rate limit interference
- Load testing (measure true capacity without limits)

## Anti-Patterns

```typescript
// NEVER: Skip rate limiting on public endpoints
export const GET = async (request: NextRequest) => {
  // Missing withRateLimitTier - VULNERABLE TO DDOS!
  return NextResponse.json({ data: [] });
};

// NEVER: Use wrong tier (read tier for write operations)
export const POST = withRateLimitTier(async (request: NextRequest) => {
  await createEntity(data);  // Write operation
  return NextResponse.json({ created: true });
}, 'read');  // WRONG! Should be 'write'

// NEVER: Hardcode rate limits in handlers
export const GET = async (request: NextRequest) => {
  const ip = request.headers.get('x-forwarded-for');
  if (requestCount[ip] > 100) {  // Custom implementation - DON'T
    return NextResponse.json({ error: 'Too many' }, { status: 429 });
  }
  // ...
};

// CORRECT: Always use the HOC
export const GET = withRateLimitTier(async (request: NextRequest) => {
  return NextResponse.json({ data: [] });
}, 'read');
```

## Checklist for New Endpoints

Before finalizing any API endpoint:

- [ ] Handler is wrapped with `withRateLimitTier`
- [ ] Appropriate tier selected based on operation type
- [ ] GET operations use 'read' tier
- [ ] POST/PUT/PATCH/DELETE use 'write' tier
- [ ] Sensitive operations use 'strict' tier
- [ ] Auth operations use 'auth' tier
- [ ] Import statement added: `import { withRateLimitTier } from '@nextsparkjs/core/lib/api/rate-limit'`

## Verification Commands

```bash
# Check if a route has rate limiting
grep -l "withRateLimitTier" packages/core/templates/app/api/**/route.ts

# Find routes WITHOUT rate limiting (potential vulnerabilities)
grep -L "withRateLimitTier" packages/core/templates/app/api/**/route.ts

# Count rate-limited vs unprotected routes
echo "Protected:"; grep -l "withRateLimitTier" packages/core/templates/app/api/**/route.ts | wc -l
echo "Unprotected:"; grep -L "withRateLimitTier" packages/core/templates/app/api/**/route.ts | wc -l
```

## Testing Rate Limits

```typescript
// Cypress test example
describe('Rate Limiting', () => {
  it('should return 429 after exceeding limit', () => {
    // Make requests up to the limit
    for (let i = 0; i < 210; i++) {
      cy.request({
        method: 'GET',
        url: '/api/v1/products',
        headers: { 'x-api-key': Cypress.env('API_KEY') },
        failOnStatusCode: false
      });
    }

    // Next request should be rate limited
    cy.request({
      method: 'GET',
      url: '/api/v1/products',
      headers: { 'x-api-key': Cypress.env('API_KEY') },
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(429);
      expect(response.body.code).to.eq('RATE_LIMIT_EXCEEDED');
      expect(response.headers).to.have.property('retry-after');
    });
  });
});
```

## Related Skills

- `better-auth` - Authentication patterns (auth tier integration)
- `nextjs-api-development` - API route development patterns
- `cypress-api` - API testing with rate limit considerations
