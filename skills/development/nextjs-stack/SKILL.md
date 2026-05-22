---
name: nextjs-stack
description: Next.js 16+ complete stack with App Router, Prisma 7, Better Auth, shadcn/ui, TanStack Form, Zustand. Use as the master reference combining all framework skills.
versions:
  nextjs: 16
  react: 19
  prisma: 7
  better-auth: 1.2
  shadcn-ui: 3.8.0
  tailwindcss: 4
user-invocable: true
related-skills: nextjs-16, prisma-7, better-auth, nextjs-shadcn, nextjs-tanstack-form, nextjs-zustand, nextjs-i18n, solid-nextjs
---

# Next.js Complete Stack

Master skill combining all framework documentation for modern Next.js development.

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze project structure and existing patterns
2. **fuse-ai-pilot:research-expert** - Verify latest docs for all stack technologies
3. **mcp__context7__query-docs** - Check integration compatibility

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Starting a new Next.js 16 project from scratch
- Need the complete recommended technology stack
- Building production applications with authentication
- Implementing forms, state management, and UI components
- Understanding how all parts fit together

### Technology Stack

| Layer | Technology | Skill Reference |
|-------|------------|-----------------|
| Framework | Next.js 16 (App Router) | `nextjs-16` |
| Database ORM | Prisma 7 | `prisma-7` |
| Authentication | Better Auth 1.2 | `better-auth` |
| UI Components | shadcn/ui 3.8.0 | `nextjs-shadcn` |
| Forms | TanStack Form | `nextjs-tanstack-form` |
| State | Zustand | `nextjs-zustand` |
| Styling | Tailwind CSS 4 | `tailwindcss` |
| i18n | next-intl 4.0 | `nextjs-i18n` |

---

## Stack Decisions

### Why These Technologies

| Choice | Reason |
|--------|--------|
| **Better Auth** over NextAuth.js | TypeScript-first, plugin system, self-hosted |
| **Prisma 7** over Drizzle | Mature ecosystem, migrations, studio |
| **TanStack Form** over React Hook Form | Modern API, server actions, type safety |
| **Zustand** over Redux/Context | Minimal boilerplate, SSR-friendly |
| **shadcn/ui** over MUI/Chakra | Copy/paste ownership, Radix primitives |

### Forbidden Patterns

- **NextAuth.js** - Use Better Auth instead
- **Pages Router** - Use App Router for new projects
- **React Hook Form** - Use TanStack Form
- **Client Components by default** - Server Components first

---

## SOLID Architecture

### Project Structure

```
src/
├── app/                    # Route handlers only
│   ├── [locale]/          # i18n routing
│   ├── api/               # API routes
│   └── layout.tsx         # Root layout
├── modules/
│   ├── cores/             # Shared infrastructure
│   │   ├── i18n/          # Internationalization
│   │   ├── shadcn/        # UI components
│   │   ├── lib/           # Utilities (cn, etc.)
│   │   └── db/            # Prisma client
│   ├── auth/              # Authentication module
│   └── [feature]/         # Feature modules
└── proxy.ts               # Route protection
```

### Module Pattern

Each feature module contains:

- **src/services/** - Business logic
- **src/hooks/** - React hooks
- **src/components/** - UI components
- **src/interfaces/** - TypeScript types

---

## Integration Points

### Authentication + Database

Better Auth integrates with Prisma adapter for user storage. Schema in `prisma/schema.prisma` includes User, Session, Account, Verification tables.

### Forms + UI + Validation

TanStack Form with Zod validation using shadcn/ui Field components. Server Actions for form submission.

### State + Server Components

Zustand stores for client state only. Server Components fetch data directly. No global state for server data.

### i18n + Routing

next-intl with `[locale]` segment. proxy.ts handles locale detection and redirects.

---

## Quick Reference

### Next.js 16

| Feature | Reference |
|---------|-----------|
| App Router | `nextjs-16/app-router.md` |
| Server Components | `nextjs-16/server-components.md` |
| Caching | `nextjs-16/caching.md`, `cache-components.md` |
| proxy.ts | `nextjs-16/proxy.md` |

### Prisma 7

| Feature | Reference |
|---------|-----------|
| Schema | `prisma-7/schema.md` |
| Client | `prisma-7/client.md` |
| Migrations | `prisma-7/migrations.md` |
| TypedSQL | `prisma-7/typed-sql.md` |

### Better Auth

| Feature | Reference |
|---------|-----------|
| Setup | `better-auth/installation.md` |
| OAuth | `better-auth/providers/` |
| Plugins | `better-auth/plugins/` |
| Prisma adapter | `better-auth/adapters/prisma.md` |

---

## Best Practices

1. **Server Components default** - Add `'use client'` only when needed
2. **Colocate code** - Keep related code in feature modules
3. **Type everything** - Full TypeScript, no any
4. **Fetch where used** - No prop drilling for data
5. **Validate at boundary** - Zod schemas for all inputs
6. **Cache explicitly** - Use `use cache` directive

---

## Getting Started

1. Review `nextjs-16` for App Router fundamentals
2. Set up `prisma-7` for database
3. Add `better-auth` for authentication
4. Install `nextjs-shadcn` components
5. Configure `nextjs-i18n` if multilingual
6. Add `nextjs-zustand` for client state
