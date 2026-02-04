---
name: laravel-vite
description: Complete Vite bundling for Laravel - assets, HMR, SSR, frameworks, optimization. Use when configuring frontend build pipeline.
versions:
  laravel: "12.x"
  vite: "6.x"
  php: "8.4"
user-invocable: true
references: references/setup.md, references/entry-points.md, references/preprocessors.md, references/assets.md, references/environment.md, references/dev-server.md, references/build-optimization.md, references/ssr.md, references/inertia.md, references/frameworks.md, references/security.md, references/deployment.md, references/templates/ViteConfig.js.md, references/templates/ViteConfigAdvanced.js.md, references/templates/InertiaSetup.md, references/templates/SSRSetup.md
related-skills: laravel-blade, laravel-livewire, fusecore
---

# Laravel Vite

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Check existing vite.config.js, package.json
2. **fuse-ai-pilot:research-expert** - Verify latest Vite docs via Context7
3. **mcp__context7__query-docs** - Query specific patterns (SSR, Inertia)

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

Vite is Laravel's default frontend build tool. It provides fast HMR in development and optimized builds for production.

| Feature | Purpose |
|---------|---------|
| **HMR** | Instant updates during development |
| **Bundling** | Optimized production assets |
| **SSR** | Server-side rendering support |
| **Frameworks** | Vue, React, Svelte integration |

---

## Critical Rules

1. **Always use laravel-vite-plugin** - Never raw Vite config
2. **VITE_ prefix for env vars** - Only exposed to frontend
3. **Use @vite directive** - Not manual script tags
4. **Build before deploy** - `npm run build` in CI/CD
5. **Configure HMR for Docker** - Set `server.host: '0.0.0.0'`

---

## Decision Guide

### Stack Selection

```
Using Tailwind CSS?
├── YES → v4? @tailwindcss/vite plugin
│         v3? PostCSS config
└── NO → Just laravel-vite-plugin

Using JavaScript framework?
├── Vue → @vitejs/plugin-vue
├── React → @vitejs/plugin-react
├── Svelte → @sveltejs/vite-plugin-svelte
└── None → Plain JS/CSS only
```

### SSR Decision

```
Need SEO/fast first paint?
├── YES → Using Inertia?
│   ├── YES → Inertia SSR
│   └── NO → Consider Inertia or Livewire
└── NO → Client-side only
```

---

## Reference Guide

### Concepts (WHY & Architecture)

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Setup** | [setup.md](references/setup.md) | Initial configuration |
| **Entry Points** | [entry-points.md](references/entry-points.md) | Multiple bundles |
| **Preprocessors** | [preprocessors.md](references/preprocessors.md) | Sass, Less, PostCSS |
| **Assets** | [assets.md](references/assets.md) | Images, fonts, static |
| **Environment** | [environment.md](references/environment.md) | VITE_ variables |
| **Dev Server** | [dev-server.md](references/dev-server.md) | HMR, Docker, HTTPS |
| **Build** | [build-optimization.md](references/build-optimization.md) | Chunks, minification |
| **SSR** | [ssr.md](references/ssr.md) | Server-side rendering |
| **Inertia** | [inertia.md](references/inertia.md) | SPA without API |
| **Frameworks** | [frameworks.md](references/frameworks.md) | Vue, React, Svelte |
| **Security** | [security.md](references/security.md) | CSP nonce |
| **Deployment** | [deployment.md](references/deployment.md) | Production, CDN |

### Templates (Complete Code)

| Template | When to Use |
|----------|-------------|
| [ViteConfig.js.md](references/templates/ViteConfig.js.md) | Standard setup |
| [ViteConfigAdvanced.js.md](references/templates/ViteConfigAdvanced.js.md) | Full optimization |
| [InertiaSetup.md](references/templates/InertiaSetup.md) | Inertia + Vue/React |
| [SSRSetup.md](references/templates/SSRSetup.md) | SSR configuration |

---

## Quick Reference

### Basic Setup

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.js'],
            refresh: true,
        }),
    ],
});
```

### Blade Directive

```blade
<!DOCTYPE html>
<head>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

### Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm run preview` | Preview build |

---

## Best Practices

### DO
- Use `refresh: true` for Blade HMR
- Configure aliases for clean imports
- Split vendors into separate chunks
- Use `VITE_` prefix for frontend env vars
- Test Docker/Sail config locally

### DON'T
- Expose sensitive data via VITE_ vars
- Forget to build before deploying
- Use absolute paths for assets
- Skip source maps in staging
- Ignore chunk size warnings
