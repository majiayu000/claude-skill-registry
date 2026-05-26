---
name: react-best-practices
description: React and Next.js performance playbook distilled from Vercel Engineering guidance. Use when building, reviewing, or refactoring React/Next.js code for waterfalls, bundle size, rendering cost, and client/server data flow.
---

# React Best Practices

Practical React and Next.js guidance for performance-sensitive product work.

This skill is a self-contained distillation of the Vercel React performance guidance so it can be installed and used directly inside Claude Arsenal.

## When To Use

Use this skill when the user asks to:
- build or refactor React components
- improve Next.js performance
- reduce bundle size
- remove data-fetch waterfalls
- fix expensive rerenders
- review frontend code for performance issues

## Priority Order

Always check higher-priority categories first.

| Priority | Category | Focus |
|----------|----------|-------|
| 1 | Waterfalls | start async work early, await late, parallelize independent fetches |
| 2 | Bundle size | avoid barrel imports, defer heavy code, split by feature |
| 3 | Server-side performance | dedupe work, minimize serialization, prefer server execution |
| 4 | Client data fetching | dedupe requests, avoid redundant listeners and client churn |
| 5 | Rerenders | reduce subscriptions, stabilize dependencies, move expensive work |
| 6 | Rendering | avoid hydration flicker, reduce DOM/SVG cost, optimize long lists |
| 7 | JavaScript hot paths | cache repeated lookups, combine iterations, exit early |
| 8 | Advanced patterns | stable refs and callback patterns for edge cases |

## Hard Rules

### 1. Eliminate Waterfalls First

- Start independent requests in parallel.
- Do not serialize async work unless there is a real dependency.
- In API routes and server components, create promises early and await them as late as possible.
- Use Suspense boundaries when streaming content helps unblock rendering.

### 2. Protect Bundle Size

- Prefer direct imports over barrel files on hot paths.
- Use dynamic imports for heavy or infrequently used components.
- Defer analytics, logging, and other non-critical third-party code until after hydration.
- Load optional modules only when the related feature is activated.

### 3. Prefer Server Work Over Client Work

- Keep data fetching and heavy transformation on the server when possible.
- Minimize data serialized into client components.
- Cache server-side repeated work when the request model allows it.

### 4. Control Rerenders

- Subscribe only to the state needed for rendering.
- Use primitive effect dependencies where possible.
- Use functional `setState` when it removes unstable dependencies.
- Initialize expensive state lazily.
- Use `startTransition` for non-urgent UI updates.

### 5. Optimize Rendering Paths

- Use virtualization or `content-visibility` for long lists when appropriate.
- Avoid animating heavy SVG nodes directly when a wrapper works.
- Hoist static JSX outside render paths when it is truly constant.
- Prefer explicit ternaries over brittle `&&` branches when rendering conditions matter.

### 6. Clean Up JavaScript Hot Spots

- Build `Map` or `Set` for repeated membership checks.
- Cache repeated property access or derived results in tight loops.
- Combine adjacent `filter` / `map` passes when the path is performance-sensitive.
- Return early from branches instead of carrying unnecessary work forward.

## Review Checklist

When reviewing React or Next.js code, check for:

1. Any sequential async calls that could be parallelized
2. Barrel imports or large dependencies in hot components
3. Data fetched on the client that could move to the server
4. Effects or callbacks with unstable object/function dependencies
5. Repeated list scans where `Map` or `Set` would help
6. User-visible loading or hydration flicker

## Output Expectations

When using this skill, the output should:
- identify the highest-impact category first
- explain why the current pattern is costly
- propose the smallest effective change
- include concrete verification ideas such as bundle diff, profiler, or render-count checks

## References

- React docs: `react.dev`
- Next.js docs: `nextjs.org`
- SWR docs: `swr.vercel.app`
- Vercel engineering performance posts
