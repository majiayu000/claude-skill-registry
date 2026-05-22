---
name: betterauth-tanstack-convex
description: Step-by-step guide for setting up Better Auth authentication with Convex and TanStack Start. This skill should be used when configuring authentication in a Convex + TanStack Start project, troubleshooting auth issues, or implementing sign up/sign in/sign out flows. Covers installation, environment variables, SSR authentication, route handlers, and the expectAuth pattern.
---

# Better Auth + Convex + TanStack Start

## Overview

This skill provides guidance for integrating Better Auth authentication with Convex backend and TanStack Start framework. It covers the complete setup process from installation to SSR-compatible authentication flows.

## When to Use This Skill

- Setting up authentication in a new Convex + TanStack Start project
- Troubleshooting Better Auth configuration issues
- Implementing sign up, sign in, or sign out flows
- Configuring SSR authentication with `expectAuth: true`
- Adding authenticated server functions
- Understanding the auth provider hierarchy

## Quick Reference

### Required Packages

```bash
npm install convex@latest @convex-dev/better-auth
npm install better-auth@1.4.9 --save-exact
npm install @types/node --save-dev
```

### Environment Variables

**Convex deployment** (via CLI):
```bash
npx convex env set BETTER_AUTH_SECRET=$(openssl rand -base64 32)
npx convex env set SITE_URL http://localhost:3000
```

**.env.local**:
```bash
CONVEX_DEPLOYMENT=dev:adjective-animal-123
VITE_CONVEX_URL=https://adjective-animal-123.convex.cloud
VITE_CONVEX_SITE_URL=https://adjective-animal-123.convex.site
VITE_SITE_URL=http://localhost:3000
```

### File Structure

| File | Purpose |
|------|---------|
| `convex/convex.config.ts` | Register Better Auth component |
| `convex/auth.config.ts` | Configure auth provider |
| `convex/auth.ts` | Create Better Auth instance + `authComponent` |
| `convex/http.ts` | Register auth HTTP routes |
| `src/lib/auth-client.ts` | Client-side auth utilities |
| `src/lib/auth-server.ts` | Server-side auth utilities |
| `src/routes/api/auth/$.ts` | Proxy auth requests to Convex |
| `src/routes/__root.tsx` | Auth provider wrapper + SSR token |

### Essential Imports

```typescript
// Client-side
import { authClient } from '~/lib/auth-client'

// Server-side
import { getToken, fetchAuthQuery, fetchAuthMutation } from '~/lib/auth-server'

// Backend
import { authComponent, createAuth } from './auth'
```

### Auth Check (Backend)

```typescript
const user = await authComponent.getAuthUser(ctx)
if (!user) throw new Error("Not authenticated")
```

### Sign Out with expectAuth

When using `expectAuth: true`, reload the page after sign out:

```typescript
await authClient.signOut({
  fetchOptions: {
    onSuccess: () => location.reload(),
  },
})
```

## Critical Configuration

### Vite SSR Bundle

Required in `vite.config.ts` to avoid module resolution issues:

```typescript
ssr: {
  noExternal: ['@convex-dev/better-auth'],
}
```

### ConvexQueryClient with expectAuth

Required for seamless SSR authentication:

```typescript
const convexQueryClient = new ConvexQueryClient(convexUrl, {
  expectAuth: true,
})
```

### Provider Hierarchy

The root component must wrap children in this order:
1. `ConvexBetterAuthProvider` (outermost)
2. `QueryClientProvider`
3. `RootDocument` with `<Outlet />`

## Reference Files

Load the detailed setup guide when implementing authentication:

| File | Use When |
|------|----------|
| `references/setup-guide.md` | Full step-by-step installation and configuration |
