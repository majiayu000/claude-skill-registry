---
name: SSR (Server-Side Rendering)
description: Hydration, TransferState, and Prerendering standards.
metadata:
  labels: [angular, ssr, hydration, server-side]
  triggers:
    files: ['**/*.server.ts', 'server.ts']
    keywords: [hydration, transferState, afterNextRender, isPlatformServer]
---

# SSR (Server-Side Rendering)

## **Priority: P2 (MEDIUM)**

## Principles

- **Hydration**: Enable Client Hydration in `app.config.ts`.
- **Platform Checks**: Use `afterNextRender` or `afterRender` for browser-only code (e.g., accessing `window`).
- **TransferState**: Use `makeStateKey` and `TransferState` to prevent double-fetching data on client.

## Guidelines

- **Browser Objects**: Never access `window`, `document`, or `localStorage` directly in component logic. Implement abstractions or use `afterNextRender`.
- **Prerendering**: Use SSG for static pages (Marketing, Blogs).

## References

- [Hydration](references/hydration.md)
