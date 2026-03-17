---
name: frontend-development
description: "Frontend implementation patterns, conventions, and tooling. Use this skill when creating components, building pages, implementing forms, fetching data, styling UI, organizing frontend code, or configuring frontend tooling (Biome, ESLint, Prettier, linting, formatting). Covers file structure, component patterns, state management, data fetching, and code quality tools."
---

# Frontend Development

Active workflow knowledge for building frontend applications with React, Next.js, TypeScript, Tailwind, and frontend tooling (Biome, ESLint, Prettier).

##  Core Principles (See detailed in references)

### 1. Server-First Architecture
Start with Server Components. Only add `'use client'` when you need interactivity, state, or browser APIs. Keep client boundaries as small as possible—extract only the interactive leaf, not the entire page.

### 2. Colocation Over Centralization
Keep code close to where it's used. Types, hooks, and utilities that serve one feature live in that feature's directory. Only truly shared code goes in global directories. This reduces cognitive load and makes features self-contained.

### 3. Searchable, Specific Naming
Every file should be findable with a single grep. Use `login-form.tsx` not `form.tsx`. Use `user-profile-types.ts` not `types.ts`. Generic names create needle-in-haystack problems at scale.

### 4. Composition Over Customization
Prefer composing existing components over adding props/variants. shadcn/ui components are meant to be copied and modified—don't fight against this. Build up from primitives rather than configuring monoliths.

### 5. Data Flows Down, Events Flow Up
Server fetches data and passes it as props. Client components handle interactions and call server actions or mutations. Never fetch in client components what could be fetched on the server.

## Quick Start

1. **Check file structure first** - Does the project use Next.js App Router or plain React?
2. **Identify the feature boundary** - What feature does this work belong to?
3. **Start with Server Component** - Only add `'use client'` when you hit a wall
4. **Name files specifically** - Would grep find this file uniquely?
5. **Match existing patterns** - Look at 2-3 similar files before creating new ones

## References

| Topic | Entry Point |
|-------|-------------|
| **Conventions** | [conventions.md](./references/conventions.md) |
| **Next.js** | [overview.md](./references/nextjs/overview.md) |
| **React** | [overview.md](./references/react/overview.md) |
| **TypeScript** | [typescript.md](./references/typescript.md) |
| **shadcn/ui + Dice UI** | [shadcn.md](./references/shadcn.md) |
| **Tailwind** | [tailwind.md](./references/tailwind.md) |
| **Data Fetching** | [overview.md](./references/data-fetching/overview.md) |
| **Biome** | [biome.md](./references/biome.md) |
| **Browser Testing** | Use browser skill to verify frontend work in a real browser |

## Official Resources

For framework knowledge beyond project-specific patterns, use `/docs-seeker` or consult:

| Framework | Documentation |
|-----------|--------------|
| Next.js | https://nextjs.org/docs |
| React | https://react.dev |
| TypeScript | https://www.typescriptlang.org/docs |
| Tailwind CSS | https://tailwindcss.com/docs |
| shadcn/ui | https://ui.shadcn.com/docs |
| Dice UI | https://www.diceui.com/docs |
| TanStack Query | https://tanstack.com/query/latest/docs |
| tRPC | https://trpc.io/docs |
| Zustand | https://zustand.docs.pmnd.rs |
| React Hook Form | https://react-hook-form.com |
| Zod | https://zod.dev |
| Biome | https://biomejs.dev |
| nuqs | https://nuqs.47ng.com |
