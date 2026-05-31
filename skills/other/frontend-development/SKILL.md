---
name: frontend-development
description: "Use this skill for ANY work involving React, Next.js, TypeScript, or Tailwind in the browser layer. This includes building components and pages, but equally covers debugging and fixing frontend issues: CSS/Tailwind classes not applying, form validation behavior, hydration mismatches between server and client renders, styling bugs, layout shifts, and rendering problems. Also use for refactoring components (e.g., splitting Server vs Client Components), data fetching patterns, state management, bundle optimization, and frontend tooling. If the problem involves what users see or interact with in a web browser — whether building, fixing, or refactoring — use this skill. Not for backend APIs, databases, infrastructure, or DevOps."
---

# Frontend Development

Project-specific patterns for React/Next.js/TypeScript frontend work.

## Architecture Decisions

### Server-First Boundaries
Start with Server Components. Only add `'use client'` when you need interactivity, state, or browser APIs. Extract only the interactive leaf — not the entire page or section.

### Colocation Over Centralization
Types, hooks, and utilities that serve one feature live in that feature's directory. Only truly shared code goes in global directories.

### Composition Over Customization
Compose existing components rather than adding props/variants. shadcn/ui components are meant to be copied and modified. Build up from primitives.

### Data Flows Down, Events Flow Up
Server fetches data and passes it as props. Client components handle interactions and call server actions. Never fetch in client components what could be fetched on the server.

## Gotchas

- `'use client'` does NOT mean "runs only in the browser" — it runs on the server during SSR too. It means "include in the client bundle." Putting secrets or DB calls in a `'use client'` file will leak them.
- Importing a Server Component into a Client Component makes it a Client Component. The boundary propagates DOWN. Pass server content as `children` props instead.
- `useEffect` with empty deps fires AFTER paint — use `useLayoutEffect` for DOM measurements that affect layout, but never in Server Components.
- Next.js `fetch()` caches by default in App Router. Add `{ cache: 'no-store' }` or `revalidate: 0` for data that must be fresh. Forgetting this causes stale data bugs that only appear in production.
- Tailwind classes are purged at build time — dynamically constructed class names like `` bg-${color}-500 `` will be missing. Use complete class names or safelist them.
- `key` prop on mapped elements must be stable and unique. Using array index as key causes subtle bugs when list items are reordered, inserted, or deleted.
- `useSearchParams()` requires a `<Suspense>` boundary in Next.js App Router or the entire page becomes client-rendered.
- shadcn/ui components are source code, not a library. After `npx shadcn-ui add`, the component lives in YOUR codebase — modify it directly, don't wrap it.
- React Hook Form's `register()` returns a ref — don't also pass your own `ref` to the same input without merging them.
- `async` Server Components that throw `redirect()` or `notFound()` must NOT be wrapped in try/catch — these work by throwing special errors that Next.js catches upstream.

## Quick Start

1. **Check file structure** — App Router or plain React? Check references below.
2. **Identify the feature boundary** — What feature does this work belong to?
3. **Start with Server Component** — Only add `'use client'` when you hit a wall
4. **Name files specifically** — `login-form.tsx` not `form.tsx`. Must be grep-findable.
5. **Match existing patterns** — Read 2-3 similar files before creating new ones

## References

| When you need... | Read |
|------------------|------|
| File naming, imports, exports | [conventions.md](./references/conventions.md) |
| Next.js App Router patterns | [overview.md](./references/nextjs/overview.md) |
| React component patterns | [overview.md](./references/react/overview.md) |
| TypeScript project patterns | [typescript.md](./references/typescript.md) |
| shadcn/ui + Dice UI usage | [shadcn.md](./references/shadcn.md) |
| Tailwind configuration | [tailwind.md](./references/tailwind.md) |
| Data fetching (tRPC, TanStack, axios) | [overview.md](./references/data-fetching/overview.md) |
| Biome/linter config | [biome.md](./references/biome.md) |

## Official Resources

For general framework docs beyond project-specific patterns, consult:

| Framework | URL |
|-----------|-----|
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
