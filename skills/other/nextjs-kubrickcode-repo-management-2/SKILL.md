---
name: nextjs
description: |
  Provides Next.js project architecture expertise and implementation patterns. Enforces BFF (Backend for Frontend) pattern, Server Components strategy, and data fetching policies. Specializes in App Router architecture, Server Actions, streaming SSR, incremental static regeneration, and route handlers. Ensures optimal performance through proper component boundaries and caching strategies.
  Use when: developing Next.js applications, implementing App Router patterns, creating Server Components and Client Components, designing Server Actions for mutations, implementing data fetching with fetch API, configuring BFF architecture, optimizing page performance with streaming and suspense, handling routing and navigation, implementing middleware, or setting up API route handlers.
---

# Next.js Project Architecture Rules

**Scope**: Project-specific policies and architecture decisions only.

**Version**: Next.js 15.5+ with App Router

---

## 1. BFF Architecture (Mandatory)

### Absolute Rules

Next.js serves ONLY as a thin Backend for Frontend (BFF) layer:

```
Browser ↔ Next.js Server ↔ Backend API ↔ Database
```

**NEVER**:

- ❌ Direct database access from Next.js (no Prisma, no ORMs)
- ❌ Business logic implementation in Next.js
- ❌ Data validation beyond input sanitization

**ALWAYS**:

- ✅ All business logic in separate backend service
- ✅ All database operations via backend API
- ✅ Next.js for: SSR/SSG, API aggregation, session management, caching

---

## 2. Component Strategy (Enforced)

### Server Components First

**Rule**: Default to Server Components. `'use client'` only at leaf nodes.

**Client Component allowed for**:

- Event handlers (onClick, onChange)
- Browser APIs (localStorage, window)
- React hooks (useState, useEffect)

**Violation**: Client Component wrapping Server Components

---

## 3. Rendering Strategy (Explicit Declaration Required)

### Mandatory Export

Every page MUST explicitly declare rendering intent:

```typescript
// Required - choose one:
export const dynamic = "force-static"; // SSG
export const dynamic = "force-dynamic"; // SSR
export const revalidate = 3600; // ISR
```

**No implicit rendering**. Always be explicit about caching behavior.

---

## 4. Data Fetching (Server Actions vs API Routes)

### Server Actions (Default for Internal Operations)

**Use for**:

- Form submissions
- Data mutations
- Internal Next.js operations

**Location**: `app/actions/*.ts` or inline with `'use server'`

### API Routes (External Integration ONLY)

**Use for**:

- Webhooks (Stripe, GitHub, etc.)
- OAuth callbacks
- Mobile app endpoints
- Third-party service integrations

**Location**: `app/api/*/route.ts`

**NEVER**: API routes for internal Next.js-to-Next.js communication

---

## 5. Caching Policy (Explicit Intent Required)

### Mandatory Cache Declaration

All fetch calls MUST explicitly specify caching:

```typescript
// Required - choose one:
fetch(url, { next: { revalidate: 3600 } }); // Time-based
fetch(url, { cache: "no-store" }); // Dynamic
```

**Use React `cache()`** to prevent duplicate requests within render cycle.

**No implicit caching**. Always declare intent.

---

## Critical Violations

1. **Direct DB access from Next.js** → Architecture violation
2. **API Routes for internal mutations** → Use Server Actions
3. **Missing rendering strategy declaration** → Add explicit export
4. **Client Component not at leaf** → Move `'use client'` down
5. **Implicit caching** → Add explicit cache declaration
6. **Backend not separated** → Mandatory separate service
