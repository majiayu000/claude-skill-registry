---
name: Routing
description: Standards for Angular Router, Lazy Loading, and Guards.
metadata:
  labels: [angular, routing, guards, lazy-loading]
  triggers:
    files: ['*.routes.ts']
    keywords: [angular router, loadComponent, canActivate, resolver]
---

# Routing

## **Priority: P0 (CRITICAL)**

## Principles

- **Lazy Loading**: Use `loadComponent` for standalone components and `loadChildren` for route files.
- **Functional Guards**: Use function-based guards (`CanActivateFn`) instead of class-based guards (Deprecated).
- **Component Inputs**: Enable `withComponentInputBinding()` to map route params directly to component inputs.

## Guidelines

- **Title Strategy**: Use `TitleStrategy` service to auto-set page titles from route data.
- **Resolvers**: Use `resolve` to pre-fetch critical data before navigation completes, but avoid blocking UI for too long.

## Anti-Patterns

- **Logic in Routes**: Keep route definitions clean. Move logic to Guards or Resolvers.
- **Eager Loading features**: Never direct import feature components in root routes.

## References

- [Routing Patterns](references/routing-patterns.md)
