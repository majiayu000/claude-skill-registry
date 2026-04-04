---
name: cloudflare-zero-trust-access
description: Cloudflare Zero Trust Access authentication for Workers. Use for JWT validation, service tokens, CORS, or encountering preflight blocking, cache race conditions, missing JWT headers.

  Keywords: Cloudflare Access, Zero Trust, Cloudflare Zero Trust Access, Access authentication, JWT validation, access jwt, service tokens, hono cloudflare access, hono-cloudflare-access middleware, workers authentication, protect worker routes, admin authentication, access policy, identity providers, azure ad access, google workspace access, okta access, github access, rbac cloudflare, geographic restrictions, multi-tenant access, cors access, CORS preflight blocked, JWT header missing, access key cache, team mismatch, access claims
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
metadata:
  version: "1.0.0"
  category: authentication
  framework: hono
  platform: cloudflare-workers
  package_versions:
    "@hono/cloudflare-access": "0.3.1"
    "hono": "4.10.3"
    "@cloudflare/workers-types": "4.20251014.0"
  errors_prevented: 8
  token_savings: "58%"
  time_savings: "2.5 hours"
  production_tested: true
  last_verified: "2025-10-28"
---

# Cloudflare Zero Trust Access Skill

Integrate Cloudflare Zero Trust Access authentication with Cloudflare Workers applications using proven patterns and templates.

---

## Overview

This skill provides complete integration patterns for Cloudflare Access, enabling application-level authentication for Workers without managing your own auth infrastructure.

**What is Cloudflare Access?**
Cloudflare Access is Zero Trust authentication that sits in front of your application, validating users before they reach your Worker. After authentication, Access issues JWT tokens that your Worker validates.

**Key Benefits**:
- No auth infrastructure to maintain
- Integrates with identity providers (Azure AD, Google, Okta, GitHub)
- Service tokens for machine-to-machine auth
- Built-in MFA and session management
- Comprehensive audit logs

---

## When to Use This Skill

Trigger this skill when tasks involve:

- **Authentication**: Protecting Worker routes, securing admin dashboards, API authentication
- **Access Control**: Role-based access (RBAC), group-based permissions, geographic restrictions
- **Service Auth**: Backend services calling Worker APIs, CI/CD pipelines, cron jobs
- **Multi-Tenant**: SaaS apps with organization-level authentication
- **CORS + Auth**: Single-page applications calling protected APIs

**Keywords to Trigger**:
cloudflare access, zero trust, access authentication, JWT validation, service tokens, cloudflare auth, hono access, workers authentication, protect worker routes, admin authentication

---

## Integration Patterns

📖 **New to Cloudflare Access?** Load `references/quick-start.md` for step-by-step setup instructions (15-20 minutes).

### Pattern 1: Hono Middleware (Recommended)

Use `@hono/cloudflare-access` for one-line Access integration.

**When to Use**:
- Building with Hono framework
- Need quick, production-ready setup
- Want automatic JWT validation and key caching

**Template**: `templates/hono-basic-setup.ts`

**Setup**:
```typescript
import { Hono } from 'hono'
import { cloudflareAccess } from '@hono/cloudflare-access'

const app = new Hono<{ Bindings: Env }>()

// Public routes
app.get('/', (c) => c.text('Public page'))

// Protected routes
app.use(
  '/admin/*',
  cloudflareAccess({
    domain: (c) => c.env.ACCESS_TEAM_DOMAIN,
  })
)

app.get('/admin/dashboard', (c) => {
  const { email } = c.get('accessPayload')
  return c.text(`Welcome, ${email}!`)
})
```

**Configuration** (`wrangler.jsonc`):
```jsonc
{
  "vars": {
    "ACCESS_TEAM_DOMAIN": "your-team.cloudflareaccess.com",
    "ACCESS_AUD": "your-app-aud-tag"
  }
}
```

**Benefits**:
- ✅ Automatic JWT validation
- ✅ Public key caching (1-hour TTL)
- ✅ Type-safe with TypeScript
- ✅ Production-tested and maintained

---

### Pattern 2: Manual JWT Validation

**When to Use**: Not using Hono, need custom validation logic

**Template**: `templates/jwt-validation-manual.ts` (~100 lines, uses Web Crypto API)

---

### Pattern 3: Service Token Authentication

**When to Use**: CI/CD pipelines, backend services, cron jobs (no interactive login)

**Client**: Send `CF-Access-Client-Id` + `CF-Access-Client-Secret` headers

**Server**: Same middleware handles both - detect via `!payload.email && payload.common_name`

📄 **Full guide**: `references/service-tokens-guide.md`

---

### Pattern 4: CORS + Access

**When to Use**: SPA (React/Vue/Angular) calling protected API

**⚠️ CRITICAL**: CORS middleware MUST come BEFORE Access middleware!
```typescript
// ✅ CORRECT ORDER
app.use('*', cors({ origin: 'https://app.example.com', credentials: true }))
app.use('/api/*', cloudflareAccess({ domain: (c) => c.env.ACCESS_TEAM_DOMAIN }))
```
**Why**: OPTIONS preflight has no auth headers → Access blocks with 401

📄 **Full pattern**: `templates/cors-access.ts`

---

### Pattern 5: Multi-Tenant

**When to Use**: SaaS with per-org authentication, white-label apps

**Architecture**: Tenant config in D1/KV → Dynamic middleware per request

📄 **Full pattern**: `templates/multi-tenant.ts` and `references/use-cases.md`

---

## Common Errors Prevented

This skill prevents 8 documented errors. Full details: `references/common-errors.md`

### Error #1: CORS Preflight Blocked (45 min saved)

**Problem**: OPTIONS requests return 401, breaking CORS

**Solution**: CORS middleware BEFORE Access middleware
```typescript
// ✅ Correct
app.use('*', cors())
app.use('/api/*', cloudflareAccess({ domain: '...' }))
```

---

### Error #2: Missing JWT Header (30 min saved)

**Problem**: Request not going through Access, no JWT header

**Solution**: Access Worker through Access URL, not direct `*.workers.dev`
```
✅ https://team.cloudflareaccess.com/...
❌ https://worker.workers.dev
```

---

### Error #3: Invalid Team Name (15 min saved)

**Problem**: Hardcoded or wrong team name causes "Invalid issuer"

**Solution**: Use environment variables
```typescript
// ✅ Correct
cloudflareAccess({ domain: (c) => c.env.ACCESS_TEAM_DOMAIN })

// ❌ Wrong
cloudflareAccess({ domain: 'my-team.cloudflareaccess.com' })
```

---

### Errors #4-8 (Quick Reference)

| # | Error | Solution |
|---|-------|----------|
| 4 | Key cache race | Use `@hono/cloudflare-access` (auto-caches) |
| 5 | Wrong service token headers | Use `CF-Access-Client-Id/Secret` (not `Authorization`) |
| 6 | Token expiration (401 after 1 hr) | Handle gracefully, redirect to login |
| 7 | Overlapping policies | Use most specific paths |
| 8 | Dev/prod mismatch | Use environment-specific configs |

📄 **Full error details**: `references/common-errors.md` (~2.5 hours saved per implementation)

---

## Templates

| Template | Purpose |
|----------|---------|
| `hono-basic-setup.ts` | Standard Hono + Access integration |
| `jwt-validation-manual.ts` | Manual JWT verification with Web Crypto |
| `service-token-auth.ts` | Service token patterns |
| `cors-access.ts` | CORS + Access (correct ordering) |
| `multi-tenant.ts` | Multi-tenant architecture |
| `wrangler.jsonc` | Complete Wrangler configuration |
| `.env.example` | Environment variable template |
| `types.ts` | TypeScript definitions |

## Scripts

| Script | Usage |
|--------|-------|
| `test-access-jwt.sh` | `./test-access-jwt.sh <jwt-token>` - Decode and validate JWT |
| `create-service-token.sh` | `./create-service-token.sh [name]` - Service token setup guide |

---

## Use Cases

| Use Case | Template | Key Point |
|----------|----------|-----------|
| Admin Dashboard | `hono-basic-setup.ts` | Email domain policy |
| API Authentication | `hono-basic-setup.ts` | Mixed user/service policy |
| SPA + API | `cors-access.ts` | CORS before Access! |
| CI/CD Pipeline | `service-token-auth.ts` | Service token in secrets |
| Multi-Tenant SaaS | `multi-tenant.ts` | D1 tenant config |

📄 **Detailed use cases**: `references/use-cases.md`

---

## When to Load References

| Reference File | Load When... |
|----------------|--------------|
| `references/quick-start.md` | Step-by-step setup for new users, first-time integration |
| `references/common-errors.md` | Debugging auth issues, prevention patterns (includes all 8 errors) |
| `references/jwt-payload-structure.md` | Accessing JWT claims, user vs service token |
| `references/service-tokens-guide.md` | Setting up machine-to-machine auth |
| `references/access-policy-setup.md` | Dashboard configuration, policy creation |
| `references/use-cases.md` | Detailed implementation for specific scenarios |
| `references/value-proposition.md` | Token efficiency metrics, workflow guidance, production validation |

---

## Package Versions

| Package | Version |
|---------|---------|
| @hono/cloudflare-access | 0.3.1 |
| hono | 4.10.7 |
| @cloudflare/workers-types | 4.20251126.0 |

**Verified**: 2025-12-14 | **Token Savings**: ~58% | **Production Tested**: ✅

---

## When NOT to Use

This skill is for **Cloudflare Workers** with **Cloudflare Access**. Do not use for:

- ❌ Cloudflare Pages (use `@cloudflare/pages-plugin-cloudflare-access` instead)
- ❌ Non-Cloudflare platforms
- ❌ Custom JWT auth (not Access)
- ❌ Auth.js or other auth libraries
- ❌ Self-hosted authentication

For those, use appropriate skills or libraries.

---

## Additional Resources

**Cloudflare Documentation**:
- [Access Overview](https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/)
- [JWT Validation](https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/validating-json/)
- [Service Tokens](https://developers.cloudflare.com/cloudflare-one/identity/service-tokens/)

**Packages**:
- [@hono/cloudflare-access](https://github.com/honojs/middleware/tree/main/packages/cloudflare-access)
- [Hono Framework](https://hono.dev/)

**Dashboard**:
- [Zero Trust Dashboard](https://one.dash.cloudflare.com/)

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-10-28
**Errors Prevented**: 8
**Token Savings**: 58%
**Time Savings**: 2.5 hours
**Production Tested**: ✅
