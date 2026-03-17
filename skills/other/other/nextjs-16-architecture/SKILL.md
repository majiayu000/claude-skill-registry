---
name: nextjs-16-architecture
description: >
  Comprehensive Next.js v16 development with Cache Components, feature-based architecture, and best practices.
  Use for ANY Next.js 16 task to know - (1) Project structure with features folder pattern, 
  (2) Where to fetch data with use cache, (3) Server vs Client component decisions, 
  (4) One file per query/type/schema/hook pattern, (5) Cache invalidation with updateTag/revalidateTag, 
  (6) Proper component organization within features. Apply to all Next.js 16 development tasks.
---

# Next.js 16 Architecture

Architecture patterns for Next.js 16 with Cache Components and feature-based organization.

## Core Philosophy

1. **Dynamic by default, cache what you choose** - Use `"use cache"` explicitly
2. **Fetch in smallest possible component** - Don't prop-drill data
3. **Keep everything static, stream only dynamic** - Use Suspense for dynamic parts
4. **Suspense boundaries high** - Place in pages/layouts, not feature components

## Quick Reference

### Feature Folder Structure
```
features/{feature}/
├── components/
│   ├── server/       # Async data-fetching components
│   ├── client/       # 'use client' interactive components
│   └── skeletons/    # Loading states for Suspense
├── data/             # Database queries (SELECT, INSERT, UPDATE, DELETE)
├── actions/          # Server Actions ('use server' + cache invalidation)
├── types/            # TypeScript types (1 file = 1 type)
├── schemas/          # Zod schemas (1 file = 1 schema)
├── hooks/            # Client-side hooks
└── lib/              # Feature-specific utilities
```

### File Naming
| Type | Pattern | Example |
|------|---------|---------|
| Server component | `kebab-case.tsx` | `agent-header.tsx` |
| Client component | `kebab-case.tsx` | `login-form.tsx` |
| Skeleton | `{name}-skeleton.tsx` | `agent-header-skeleton.tsx` |
| GET query | `get-{entity}.ts` | `get-agent.ts` |
| GET multiple | `get-{entities}.ts` | `get-agents.ts` |
| CREATE | `create-{entity}.ts` | `create-agent.ts` |
| DELETE | `delete-{entity}.ts` | `delete-agent.ts` |
| Server Action | `{verb}-{entity}-action.ts` | `delete-agent-action.ts` |

### Cache Pattern
```typescript
// Data file (SELECT with cache)
export async function getEntity(id: number) {
  "use cache";
  cacheTag(`entity-${id}`);
  cacheLife("hours");
  return await db.select()...
}

// Server Action (mutation + invalidation)
"use server";
export async function deleteEntityAction(id: number) {
  await deleteEntity(id);
  updateTag(`entity-${id}`);
}
```

### Import Rules
- **Always absolute**: `@/features/...`
- **Never relative**: `../../../`
- **Direction**: `app/` → `features/` → `shared/`

## References

Load these based on what you need:

- **[Feature Structure](references/feature-structure.md)** - Complete feature organization, anatomy, rules
- **[Components](references/components.md)** - Server, Client, Skeletons, Compound UI patterns
- **[Data Layer](references/data-layer.md)** - Cacheable queries, mutations, session handling
- **[Server Actions](references/server-actions.md)** - Actions, cache invalidation, auth patterns
- **[Pages & Layouts](references/pages-layouts.md)** - App router structure, route groups
- **[Internationalization](references/i18n.md)** - next-intl setup, flat keys, translations
- **[Shared Feature](references/shared-feature.md)** - Cross-cutting concerns, UI components
- **[Checklists](references/checklists.md)** - Code review and new feature checklists
