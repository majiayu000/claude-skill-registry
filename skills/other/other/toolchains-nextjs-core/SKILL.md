---
name: nextjs-core
description: Core Next.js patterns for App Router development including Server Components, Server Actions, route handlers, data fetching, and caching strategies
version: 1.1.0
category: toolchain
progressive_disclosure:
  entry_point:
    summary: "Server-first patterns with safe mutations (Server Actions) and explicit caching/revalidation"
tags: [nextjs, app-router]
---

# Next.js Core (App Router)

- Server Components by default; minimal `"use client"`.
- Mutations in Server Actions (validate/authz; revalidate tags/paths).
- Route handlers for APIs/webhooks; add loading/error boundaries.

Anti-patterns:
- ❌ Fetch initial data in `useEffect`.
- ❌ Cache or revalidate too broadly.
- ❌ Client-only authz.

References: see `references/` (server actions, fetching, caching, routing, auth, testing).
