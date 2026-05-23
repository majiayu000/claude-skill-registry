---
name: modern-web-performance
description: High-Performance Web Engineering.
category: performance
version: 4.1.0-fractal
layer: master-skill
---

# ⚡ High-Performance Web Engineering
> **Source**: Vercel Best Practices / Anthony Fu (Antfu) Engineering Standards

This skill focuses on "Elite-Level" web development: speed, zero-config DX, and scalable architecture.

## 🚀 1. The Vercel Way (Modern Stack)
- **Edge-First Thinking**: Prioritize logic that runs on the Edge (Middleware, Edge Functions) to reduce TTFB.
- **Incremental Static Regeneration (ISR)**: Update static content without a full rebuild.
- **Server Component Patterns**: Minimize client-side JS. Use `use server` sparingly and only where needed.

## 🛠️ 2. Antfu-Grade Developer Experience (DX)
- **Zero-Config Philosophy**: Use modern tools like `Vite`, `Vitest`, and `ESLint (flat config)` to minimize boilerplate.
- **Composable Logic**: Build small, single-responsibility functions (Vue Composables or React Hooks) that are highly unit-testable.
- **Type-Safety Everywhere**: No `any`. Use Zod for runtime validation and strict TS configs.

## 📦 3. Monorepo & Scalability
- **Turborepo Master**: Manage multi-package projects with intelligent caching and parallel execution.
- **Shared UI Libraries**: Split the UI into a separate package within the monorepo for reuse across Web/Mobile.
- **Package Modernization**: Migrate from CJS to ESM. Ensure `package.json` exports are correctly defined.

## 🧪 4. Performance Auditing
- **Core Web Vitals**: Monitor LCP, FID, and CLS. Chasing "100" on PageSpeed Insights is the goal.
- **Bundle Analysis**: Use tools to find and remove "heavy" dependencies.
- **Preload/Prefetch Strategies**: Optimize asset loading for critical paths.

---
*Created by Antigravity Orchestrator - Powered by Elite Web Ecosystem Wisdom.*
