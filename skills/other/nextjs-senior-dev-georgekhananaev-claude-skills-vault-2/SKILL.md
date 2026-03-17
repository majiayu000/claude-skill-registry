---
name: nextjs-senior-dev
description: Senior Next.js 15+/16 Engineer skill for App Router. Use when scaffolding production apps, enforcing RSC patterns, auditing codebases, or optimizing performance.
author: George Khananaev
version: 1.3.0
---

# Next.js Senior Developer

Transform into Senior Next.js 15+/16 Engineer for production-ready App Router applications.

## When to Use

- Scaffolding new Next.js App Router projects
- RSC vs Client Component decisions
- Server Actions and data fetching patterns
- Performance optimization (CWV, bundle, caching)
- Middleware and authentication setup
- Next.js 15/16 migration or audit

## Version Notes

| Version | Key Changes |
|---------|-------------|
| Next.js 16 | `middleware.ts` → `proxy.ts`, Node.js runtime only, Cache Components |
| Next.js 15 | fetch uncached by default, React 19, Turbopack stable |

## Triggers

| Command | Purpose |
|---------|---------|
| `/next-init` | Scaffold new App Router project |
| `/next-route` | Generate route folder (page, layout, loading, error) |
| `/next-audit` | Audit codebase for patterns, security, performance |
| `/next-opt` | Optimize bundle, images, fonts, caching |

## Reference Files (23 Total)

Load based on task context:

### Core References

| Category | Reference | When |
|----------|-----------|------|
| Routing | `references/app_router.md` | Route groups, parallel, intercepting |
| Components | `references/components.md` | RSC vs Client decision, patterns |
| Data | `references/data_fetching.md` | fetch, cache, revalidation, streaming |
| Security | `references/security.md` | Server Actions, auth, OWASP |
| Performance | `references/performance.md` | CWV, images, fonts, bundle, memory |
| Middleware | `references/middleware.md` | Auth, redirects, Edge vs Node |

### Architecture & Quality

| Category | Reference | When |
|----------|-----------|------|
| Architecture | `references/architecture.md` | File structure, feature-sliced design |
| Shared Components | `references/shared_components.md` | DRY patterns, composition, reusability |
| Code Quality | `references/code_quality.md` | Error handling, testing, accessibility |

### Features & Integrations

| Category | Reference | When |
|----------|-----------|------|
| SEO & Metadata | `references/seo_metadata.md` | generateMetadata, sitemap, OpenGraph |
| Database | `references/database.md` | Prisma, Drizzle, queries, migrations |
| Authentication | `references/authentication.md` | Auth.js, sessions, RBAC |
| Forms | `references/forms.md` | React Hook Form, Zod, file uploads |
| i18n | `references/i18n.md` | next-intl, routing, RTL support |
| Real-Time | `references/realtime.md` | SSE, WebSockets, polling, Pusher |
| API Design | `references/api_design.md` | REST, tRPC, webhooks, versioning |

### DevOps & Migration

| Category | Reference | When |
|----------|-----------|------|
| Deployment | `references/deployment.md` | Vercel, Docker, CI/CD, env management |
| Monorepo | `references/monorepo.md` | Turborepo, shared packages, workspaces |
| Migration | `references/migration.md` | Pages→App Router, version upgrades |
| Debugging | `references/debugging.md` | DevTools, profiling, error tracking |
| Scripts & 3rd-Party | `references/scripts.md` | next/script, loading strategies, Google Analytics |
| Self-Hosting | `references/self_hosting.md` | Docker standalone, cache handlers, multi-instance ISR |
| Debug Tricks | `references/debug_tricks.md` | MCP debugging, --debug-build-paths |

## Core Tenets

### 1. Server-First

Default to Server Components. Use Client only when required.

```
RSC when: data fetching, secrets, heavy deps, no interactivity
Client when: useState, useEffect, onClick, browser APIs
```

### 2. Component Archetypes

| Pattern | Runtime | Must Have |
|---------|---------|-----------|
| `page.tsx` | Server | async, data fetching |
| `*.action.ts` | Server | "use server", Zod, 7-step security |
| `*.interactive.tsx` | Client | "use client", event handlers |
| `*.ui.tsx` | Either | Pure presentation, stateless |

### 3. 7-Step Server Action Security

```typescript
"use server"
// 1. Rate limit (IP/user)
// 2. Auth verification
// 3. Zod validation (sanitize errors!)
// 4. Authorization check (IDOR prevention)
// 5. Mutation
// 6. Granular revalidateTag() (NOT revalidatePath)
// 7. Audit log (async)
```

### 4. Data Fetching Strategy

```
Static → generateStaticParams + fetch
ISR → fetch(url, { next: { revalidate: 60 }})
Dynamic → fetch(url, { cache: 'no-store' })
Real-time → Client fetch (SWR)
```

**Next.js 15 Change**: fetch is UNCACHED by default (opposite of 14).

### 5. Caching

| Type | Scope | Invalidation |
|------|-------|--------------|
| Request Memoization | Request | Automatic |
| Data Cache | Server | revalidateTag() |
| Full Route Cache | Server | Rebuild |
| Router Cache | Client | router.refresh() |

Prefer `revalidateTag()` over `revalidatePath()` to avoid cache storms.

### 6. Feature-Sliced Architecture

For large apps (50+ routes), use domain-driven structure:

```
src/
├── app/           # Routing only
├── components/    # Shared UI (ui/, shared/)
├── features/      # Business logic per domain
│   └── [feature]/
│       ├── components/
│       ├── actions/
│       ├── queries/
│       └── hooks/
├── lib/           # Global utilities
└── types/         # Global types
```

### 7. Component Sharing Rules

| Used 3+ places? | Contains business logic? | Action |
|-----------------|-------------------------|--------|
| Yes | No | Move to `components/ui/` or `shared/` |
| Yes | Yes | Keep in `features/` |
| No | Any | Keep local (`_components/`) |

### 8. State Management Hierarchy

| State Type | Tool | Example |
|------------|------|---------|
| URL State | searchParams | Filters, pagination |
| Server State | Server Components | User data, posts |
| Form State | useFormState | Form submissions |
| UI State | useState | Modals, dropdowns |
| Shared Client | Context/Zustand | Theme, cart |

**Rule**: Prefer URL state for shareable/bookmarkable state.

### 9. DRY with createSafeAction

```typescript
// lib/safe-action.ts - Reuse for all Server Actions
export const createPost = createSafeAction(schema, handler, {
  revalidateTags: ["posts"]
})
```

Eliminates duplicate auth/validation/error handling.

## Anti-Patterns

| Don't | Do |
|-------|-----|
| "use client" at tree root | Push boundary down to leaves |
| API routes for server data | Direct DB in Server Components |
| useEffect for fetching | Server Component async fetch |
| revalidatePath('/') | Granular revalidateTag() |
| Trust middleware alone | Validate at data layer too |
| Prop drill 5+ levels | Context or composition |
| `any` types | Proper types or `unknown` |
| Barrel exports in features | Direct imports |
| localStorage for auth | httpOnly cookies |
| Global caches (memory leak) | LRU cache or React cache() |

## Middleware: Deny by Default

```typescript
// middleware.ts - Public routes MUST be allowlisted
const publicRoutes = ['/login', '/register', '/api/health']
if (!publicRoutes.some(r => pathname.startsWith(r))) {
  // Require auth
}
```

**CRITICAL**: Upgrade to Next.js 15.2.3+ (CVE-2025-29927 fix).

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/scaffold_route.py` | Generate route folder w/ all files |

## Templates

| File | Purpose |
|------|---------|
| `templates/page.tsx` | Standard async page |
| `templates/layout.tsx` | Layout w/ metadata |
| `templates/action.ts` | 7-step secure Server Action |
| `templates/loading.tsx` | Loading UI skeleton |
| `templates/error.tsx` | Error boundary |

## Assets

| File | Purpose |
|------|---------|
| `assets/next.config.ts` | Production config w/ security headers |
| `assets/middleware.ts` | Deny-by-default auth (Next.js 15) |
| `assets/proxy.ts` | Deny-by-default auth (Next.js 16+) |

## Quick Reference: Senior Code Review

Before merging any PR, verify:

**Performance**
- [ ] No unnecessary "use client"
- [ ] Images use next/image with dimensions
- [ ] Heavy components dynamic imported
- [ ] Parallel fetching (Promise.all)

**Security**
- [ ] Server Actions validate with Zod
- [ ] Auth in actions (not just middleware)
- [ ] IDOR prevention (user owns resource)
- [ ] No secrets in client bundles

**Architecture**
- [ ] Components in correct layer
- [ ] No cross-feature imports
- [ ] DRY patterns used (createSafeAction)
- [ ] URL state for shareable state

**Quality**
- [ ] No `any` types
- [ ] Error boundaries present
- [ ] Loading states for async
- [ ] Accessibility (semantic HTML, alt text)