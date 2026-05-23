---
name: core-principles
description: Core principles and project structure for React 19 SPA development. Covers stack overview, project organization, agent execution rules, and authoritative sources. Use when planning new projects, onboarding, or reviewing architectural decisions.
---

# Core Principles for React 19 SPA Development

Production-ready best practices for building modern React applications with TypeScript, Vite, and TanStack ecosystem.

## Stack Overview

- **React 19** with React Compiler (auto-memoization)
- **TypeScript** (strict mode)
- **Vite** (bundler)
- **Biome** (formatting + linting)
- **TanStack Query** (server state)
- **TanStack Router** (file-based routing)
- **Vitest** (testing with jsdom)
- **Apidog MCP** (API spec source of truth)

## Project Structure

```
/src
  /app/               # App shell, providers, global styles
  /routes/            # TanStack Router file-based routes
  /components/        # Reusable, pure UI components (no data-fetch)
  /features/          # Feature folders (UI + hooks local to a feature)
  /api/               # Generated API types & client (from OpenAPI)
  /lib/               # Utilities (zod schemas, date, formatting, etc.)
  /test/              # Test utilities
```

**Key Principles:**
- One responsibility per file
- UI components don't fetch server data
- Put queries/mutations in feature hooks
- Co-locate tests next to files

## Agent Execution Rules

**Always do this when you add or modify code:**

1. **API Spec:** Fetch latest via Apidog MCP and regenerate `/src/api` types if changed

2. **Data Access:** Wire only through feature hooks that wrap TanStack Query. Never fetch inside UI components.

3. **New Routes:**
   - Create file under `/src/routes/**` (file-based routing)
   - If needs data at navigation, add loader that prefetches with Query

4. **Server Mutations:**
   - Use React 19 Actions OR TanStack Query `useMutation` (choose one per feature)
   - Use optimistic UI via `useOptimistic` (Actions) or Query's optimistic updates
   - Invalidate/selectively update cache on success

5. **Compiler-Friendly:**
   - Keep code pure (pure components, minimal effects)
   - If compiler flags something, fix it or add `"use no memo"` temporarily

6. **Tests:**
   - Add Vitest tests for new logic
   - Component tests use RTL
   - Stub network with msw

7. **Before Committing:**
   - Run `biome check --write`
   - Ensure Vite build passes

## "Done" Checklist per PR

- [ ] Route file added/updated; loader prefetch (if needed) present
- [ ] Query keys are stable (`as const`), `staleTime`/`gcTime` tuned
- [ ] Component remains pure; no unnecessary effects; compiler ✨ visible
- [ ] API calls typed from `/src/api`; inputs/outputs validated at boundaries
- [ ] Tests cover new logic; Vitest jsdom setup passes
- [ ] `biome check --write` clean; Vite build ok

## Authoritative Sources

- **React 19 & Compiler:**
  - React v19 overview
  - React Compiler: overview + installation + verification
  - `<form action>` / Actions API; `useOptimistic`; `use`
  - CRA deprecation & guidance

- **Vite:**
  - Getting started; env & modes; TypeScript targets

- **TypeScript:**
  - `moduleResolution: "bundler"` (for bundlers like Vite)

- **Biome:**
  - Formatter/Linter configuration & CLI usage

- **TanStack Query:**
  - Caching & important defaults; v5 migration notes; devtools/persisting cache

- **TanStack Router:**
  - Install with Vite plugin; file-based routing; search params; devtools

- **Vitest:**
  - Getting started & config (jsdom)

- **Apidog + MCP:**
  - Apidog docs (import/export, OpenAPI); MCP server usage

## Final Notes

- Favor compile-friendly React patterns
- Let the compiler and Query/Router handle perf and data orchestration
- Treat Apidog's OpenAPI (via MCP) as the single source of truth for network shapes
- Keep this doc as your "contract"—don't add heavy frameworks or configs beyond what's here unless explicitly requested

## Related Skills

- **tooling-setup** - Vite, TypeScript, Biome configuration
- **react-patterns** - React 19 specific patterns (compiler, actions, forms)
- **tanstack-router** - Routing patterns
- **tanstack-query** - Server state management with Query v5
- **router-query-integration** - Integrating Router with Query
- **api-integration** - Apidog + MCP patterns
- **performance-security** - Performance, accessibility, security
