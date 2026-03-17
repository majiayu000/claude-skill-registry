---
name: vite
description: Vite fast build tool with HMR. Use for modern frontend builds.
---

# Vite

Vite is the standard build tool for modern web development. v6.0 (2025) introduces the **Environment API** for runtimes like Bun/Deno and native **Sass** support.

## When to Use

- **New Projects**: The default for React, Vue, Svelte, etc.
- **SPA**: Optimized for Single Page Apps.
- **Speed**: Instant server start via native ESM.

## Core Concepts

### Dev Server (ESM)

Vite serves files as native ESM modules. The browser downloads files as needed. No bundling in dev.

### Rollup Build

Vite uses Rollup for production builds, ensuring highly optimized chunks.

### Plugins

Rollup-compatible plugin system.

## Best Practices (2025)

**Do**:

- **Use `vitest`**: The native test runner for Vite projects.
- **Use `vite.config.ts`**: TypeScript config is standard.
- **Environment API**: Use the new API to define custom environments (e.g. `ssr`, `worker`).

**Don't**:

- **Don't use `require`**: Vite is ESM-first. Use `import`.

## References

- [Vite Documentation](https://vitejs.dev/)
