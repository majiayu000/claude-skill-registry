---
name: server-components
description: Enforces project server component conventions for async data fetching, caching integration, streaming with Suspense, and SEO metadata generation. Extends react-coding-conventions with server-specific patterns.
---

# Server Components Skill

## Purpose

This skill provides server-specific React conventions that extend the base react-coding-conventions skill. It covers patterns unique to server components: async data fetching, caching, streaming, and metadata generation.

## When to Use This Skill

Use this skill in the following scenarios:

- Creating page.tsx, layout.tsx, loading.tsx, or error.tsx files
- Implementing async server components
- Adding Suspense streaming or skeleton components
- Generating page metadata
- Fetching data in server components through facades

**Important**: This skill should activate automatically when server component work is detected.

## Prerequisite Skills

This skill REQUIRES loading these skills FIRST:

1. **react-coding-conventions** - Base React patterns
2. **ui-components** - UI component patterns
3. **caching** - Cache service patterns (for data fetching)

## How to Use This Skill

### 1. Load Prerequisites and Reference

Before creating or modifying server components:

```
1. Read .claude/skills/react-coding-conventions/references/React-Coding-Conventions.md
2. Read .claude/skills/ui-components/references/UI-Components-Conventions.md
3. Read .claude/skills/caching/references/Caching-Conventions.md
4. Read .claude/skills/server-components/references/Server-Components-Conventions.md
```

### 2. Apply Server Component Patterns

**Async Component Structure**:

- Use async arrow functions or async function declarations
- Add `import 'server-only'` guard for server-only code
- Fetch data through facades with caching
- Use Promise.all for parallel data fetching

**Authentication**:

- Use `getUserIdAsync()` for optional user auth
- Use `getRequiredUserIdAsync()` for required user auth (redirect if unauthenticated or user not found)
- Use `checkIsOwnerAsync()` for ownership checks

**Streaming with Suspense**:

- Wrap async children in `<Suspense fallback={<Skeleton />}>`
- Create corresponding skeleton components
- Use error boundaries for resilience

**Metadata Generation**:

- Export `generateMetadata` for pages
- Use `generatePageMetadata()` utility
- Include JSON-LD structured data

**ISR Configuration**:

- Export `revalidate` constant when appropriate

### 3. Automatic Convention Enforcement

After generating code:

1. **Scan for violations** against server component patterns
2. **Fix automatically** without asking permission
3. **Verify completeness** before presenting to user

### 4. Reporting

Provide a brief summary of conventions applied:

```
Server component conventions enforced:
  - Added 'server-only' import guard
  - Used async arrow function pattern
  - Wrapped children in Suspense with skeleton
  - Added generateMetadata for SEO
  - Used CacheService for data fetching
```

## Component Naming Conventions

- `*Async` suffix for async data-fetching components
- `*Server` suffix for server-only orchestration
- `*Skeleton` suffix for loading states

## File Patterns

This skill handles:

- `src/app/**/page.tsx`
- `src/app/**/layout.tsx`
- `src/app/**/loading.tsx`
- `src/app/**/error.tsx`
- `src/app/**/components/async/*.tsx`
- `src/app/**/components/*-async.tsx`
- `src/app/**/components/*-server.tsx`
- `*-skeleton.tsx`

## Workflow Summary

```
1. Detect server component work (page.tsx, async component, data fetch)
2. Load prerequisites: react-coding-conventions, ui-components, caching
3. Load references/Server-Components-Conventions.md
4. Generate/modify code following ALL conventions
5. Scan for violations
6. Auto-fix violations
7. Report fixes applied
```
