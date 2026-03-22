---
name: react-performance-audit
description: Audit React component rendering performance when the user asks to optimize React performance, fix re-renders, or improve UI speed
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep
argument-hint: "[component path or performance concern]"
read-only: true
destructive: false
idempotent: true
open-world: false
user-invocable: true
tags: react, performance, optimization
---

# React Performance Audit

## Overview

Audit React components for rendering performance issues. Provides a decision tree for when to apply memoization, virtualization, code splitting, and Suspense boundaries. Stack-specific Tier 3 reference skill.

## Workflow

1. **Read project setup** — Check `.chalk/docs/engineering/` for architecture docs, React version, state management library (Redux, Zustand, Jotai, Context), and rendering framework (CRA, Vite, Next.js, Remix). The framework determines which optimizations are available.

2. **Identify the scope** — Parse `$ARGUMENTS` for specific components or areas to audit. If none specified, scan `src/` for the largest component files and component tree entry points.

3. **Audit for unnecessary re-renders** — Check for:
   - Components re-rendering when their props have not changed (missing `React.memo`)
   - Inline object/array/function creation in JSX props (creates new references every render)
   - Context providers with frequently changing values that trigger wide re-render trees
   - State stored too high in the tree, causing children to re-render unnecessarily

4. **Audit memoization usage** — Apply this decision tree:
   - `React.memo`: Use when a component receives the same props frequently and is expensive to render. Do NOT use on components that almost always receive new props.
   - `useMemo`: Use for expensive computations (sorting/filtering large lists, complex transformations). Do NOT use for simple operations — the memoization overhead is worse.
   - `useCallback`: Use when passing callbacks to memoized children. Do NOT wrap every function — only those that are dependencies of memoized components or effects.

5. **Audit component tree structure** — Check for:
   - Large flat lists rendered without virtualization (>100 items should use `react-window` or `@tanstack/virtual`)
   - Deeply nested component trees without Suspense boundaries
   - Components that import large libraries without code splitting (`React.lazy`)
   - Missing error boundaries around async or third-party components

6. **Audit bundle impact** — Check for:
   - Large dependencies imported for small features (e.g., importing all of lodash for one function)
   - Missing tree-shaking (default imports from barrel files)
   - Images and assets not optimized or lazy-loaded

7. **Prioritize findings** — Rank issues by impact: (a) fixes that affect the critical rendering path, (b) fixes that reduce bundle size, (c) fixes that improve perceived performance, (d) micro-optimizations that rarely matter.

8. **Report findings** — Present the audit results with specific file references, the issue, the recommended fix, and the expected impact.

## Output

- **Format**: Audit report delivered in the conversation
- **Key sections**: Summary of findings ranked by impact, detailed findings with code references and suggested fixes, a decision tree summary for future reference

## Anti-patterns

- **Premature memoization** — Wrapping everything in `React.memo`, `useMemo`, and `useCallback` adds complexity and memory overhead. Only memoize when there is a measured or clearly predictable performance problem.
- **Fixing symptoms instead of structure** — Adding `useMemo` to work around a state management problem is a band-aid. If a component re-renders too often, first check whether state is in the right place.
- **Ignoring the profiler** — Guessing at performance problems is unreliable. Recommend using React DevTools Profiler to measure actual render times before and after optimizations.
- **Virtualizing short lists** — Lists under 50-100 items rarely benefit from virtualization. The added complexity of virtual scrolling is not worth it for small datasets.
- **Code splitting everything** — Splitting every route and component increases the number of network requests and can hurt performance. Split at meaningful boundaries: routes, heavy features, rarely-used modals.
