---
name: typescript-react-patterns
description: >
  Production-grade TypeScript reference for React & Next.js frontend development.
  Covers type narrowing, component Props, generic hooks, discriminated unions,
  as const, satisfies, Zod validation, TanStack Query, server/client boundaries,
  forms, state management, performance, accessibility, debugging, and code review.
  Use when the user works with TypeScript in React or Next.js: type errors,
  Props design, generics, API typing, SSR/CSR boundaries, hydration issues,
  form validation, state management, performance, or code review.
  Also use for "how should I type this?", "why does this type error happen?",
  or any architectural decision involving TypeScript in a frontend context.
---

# TypeScript for React & Next.js — Agent Skill

A structured reference for AI coding agents assisting frontend engineers with TypeScript, React, and Next.js in production environments.

---

## Agent Behavior Rules

### Before answering, always verify:

1. **Server or client?** Server Components, Server Actions, and Route Handlers have different type constraints than `"use client"` components.
2. **Runtime validation needed?** Static types do NOT validate API responses, URL params, form data, or localStorage. Data crossing a trust boundary requires Zod or equivalent.
3. **App Router or Pages Router?** Patterns differ significantly. If unclear, ask.
4. **TypeScript version?** `satisfies` requires 5.0+. Check before suggesting version-dependent features.
5. **Next.js version?** `params` is a `Promise` in 15+. Caching model changed in 16+.

### Assumptions the agent must NOT make:

- That API responses match their TypeScript types at runtime
- That `searchParams` values are the expected type (they are always `string | string[] | undefined`)
- That `any` in existing code is intentional
- That a type assertion (`as`) is justified without checking context
- That server-only imports are safe in client components
- That `useEffect` dependencies in existing code are correct

### When uncertain:

- State tradeoffs explicitly rather than picking one approach silently
- Mark unstable or version-dependent patterns as such
- Distinguish: **[HARD RULE]** (violating causes bugs) / **[DEFAULT]** (override with reason) / **[SITUATIONAL]** (depends on context)

---

## Decision Guide

### Quick: What pattern should I use?

| Situation | Start here |
|-----------|-----------|
| Typing component Props, children, events, refs | → `react-typescript-patterns.md` |
| Narrowing unions, `unknown`, type guards, utility types | → `typescript-core.md` |
| Next.js params, searchParams, Server Actions, RSC boundary | → `nextjs-typescript.md` |
| Discriminated unions, conditional props, compound components | → `component-patterns.md` |
| API responses, fetch typing, TanStack Query, caching | → `data-fetching-and-api-types.md` |
| Form state, validation, controlled vs uncontrolled | → `forms-and-validation.md` |
| Local state vs context vs server state vs Zustand | → `state-management.md` |
| Re-renders, memoization, accessibility | → `performance-and-accessibility.md` |
| Type errors, hydration, stale state, effect bugs | → `debugging-checklists.md` (hub) + `playbooks/` |
| PR review, risk vs preference, architecture smells | → `code-review-rules.md` |
| Common mistakes, cargo-cult patterns | → `anti-patterns.md` |

### Flowchart: Is this data safe to use?

```
Data comes from...
├─ Inside the app (useState, useReducer, computed)
│  → Static typing is sufficient. No runtime validation needed.
│
├─ Outside the app (API, URL, FormData, localStorage, postMessage)
│  → [HARD RULE] Validate at runtime. Use Zod or equivalent.
│  │
│  ├─ API response    → schema.parse(await res.json())
│  ├─ URL params      → schema.parse(searchParams)
│  ├─ FormData        → schema.safeParse({ field: formData.get('field') })
│  ├─ localStorage    → schema.safeParse(JSON.parse(stored))
│  └─ postMessage     → schema.safeParse(event.data)
│
└─ Third-party library callback
   → Check library types. Add runtime guard if types seem wrong.
```

### Flowchart: Where should this state live?

```
Is this data from a server/API?
├─ Yes → TanStack Query (NOT useState). See data-fetching-and-api-types.md
│
└─ No → Is it shareable via URL? (filters, page, sort)
   ├─ Yes → searchParams or nuqs. See state-management.md
   │
   └─ No → How many components need it?
      ├─ 1 component → useState or useReducer
      ├─ 2-3 in same tree → Lift state up (props)
      └─ Many across trees → How often does it change?
         ├─ Rarely (theme, locale, auth) → Context
         └─ Often (cart, notifications) → Zustand with selectors
```

### Flowchart: Should I memoize this?

```
Is there a measured performance problem?
├─ No → Don't memoize. Stop here.
│
└─ Yes → Can you restructure instead?
   ├─ Yes → Move state down, extract components. See performance-and-accessibility.md
   │
   └─ No → What needs memoizing?
      ├─ Expensive computation → useMemo (verify it's truly expensive)
      ├─ Callback to memoized child → useCallback
      └─ Component in a long list → React.memo (verify props are stable)
```

### Quick: hard rule vs default vs situational

| Label | Meaning | Example |
|-------|---------|---------|
| **[HARD RULE]** | Violating causes bugs or security issues. No exceptions. | "Validate API responses at runtime" |
| **[DEFAULT]** | Recommended unless you have a documented reason to deviate. | "Use `interface` for Props" |
| **[SITUATIONAL]** | Depends on context. Both options are valid. Explain your choice. | "Polymorphic components — only for design-system foundations" |

---

## Code Generation Checklist

Before generating TypeScript/React/Next.js code:

**Context**
- [ ] Confirmed: server or client code?
- [ ] Confirmed: App Router or Pages Router?
- [ ] Confirmed: TypeScript strict mode enabled?

**Type Safety**
- [ ] No `any` — use `unknown` with validation or proper types
- [ ] No `as` without documented justification
- [ ] External data (API, URL, form, storage) validated at runtime
- [ ] Props use `interface`, only truly optional fields have `?`

**React**
- [ ] `children` typed as `React.ReactNode`
- [ ] Event handler Props expose values, not event objects
- [ ] Effects have stable dependencies and cleanup functions
- [ ] `"use client"` only where needed, as deep as possible
- [ ] No server data duplicated into `useState`

**Next.js (15+)**
- [ ] `params` and `searchParams` awaited
- [ ] Server Actions validate FormData with Zod
- [ ] Sensitive code protected with `import 'server-only'`
- [ ] Cross-boundary Props are JSON-serializable (no functions, Dates, Maps)

**Accessibility**
- [ ] Form inputs have associated labels
- [ ] Error messages use `role="alert"`
- [ ] Interactive elements are keyboard-accessible

---

## Code Review Checklist

### Flag as risk (likely bug or maintenance problem)

- `any` without documented reason
- `as` on external data without validation
- `!` non-null assertion without prior guard
- `useEffect` with object/array dependencies (likely unstable)
- Missing `useEffect` cleanup
- Server data copied into `useState`
- `"use client"` at page/layout level
- Functions passed across server/client boundary
- `params`/`searchParams` not awaited (Next.js 15+)
- Server Action without FormData validation

### Flag as preference (mention, don't block)

- `type` vs `interface` for object shapes
- Handler naming convention
- File/folder organization style
- Import ordering

---

## File Index

| File | Scope |
|------|-------|
| `typescript-core.md` | Narrowing, unions, generics, utility types, inference, `unknown` vs `any`, `as const`, `satisfies` |
| `react-typescript-patterns.md` | Props, children, events, hooks, context, forwardRef |
| `nextjs-typescript.md` | App Router types, params, searchParams, Server Actions, RSC boundaries, metadata |
| `component-patterns.md` | Discriminated union Props, compound components, controlled/uncontrolled, polymorphic |
| `data-fetching-and-api-types.md` | Fetch typing, Zod validation, TanStack Query, safe response handling |
| `forms-and-validation.md` | Form state, Zod, react-hook-form, Server Actions, progressive enhancement |
| `state-management.md` | Local state, Context, Zustand, TanStack Query, URL state, decision matrix |
| `performance-and-accessibility.md` | Memoization tradeoffs, effect stability, semantic HTML, ARIA patterns |
| `debugging-checklists.md` | Quick diagnosis router, serialization issues, null access, re-render errors |
| `code-review-rules.md` | Risk vs preference, architecture smells, review comment templates |
| `anti-patterns.md` | 12 common mistakes with root causes and fixes |

### `playbooks/` — Step-by-step debugging guides (consult when diagnosing specific bugs)

| File | Scope |
|------|-------|
| `type-error-debugging.md` | Systematic type error resolution with React/Next.js-specific errors |
| `hydration-issues.md` | SSR/CSR mismatch diagnosis flowchart and fix patterns |
| `effect-dependency-bugs.md` | Infinite loops, stale closures, missing cleanups, real-world debounce example |
