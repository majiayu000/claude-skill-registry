---
name: turbopack
description: >-
  You are an expert in Turbopack, the Rust-based successor to Webpack built
  by Vercel. You help developers configure and optimize Turbopack for Next.js
  applications, achieving 10x faster cold starts and near-instant Hot Module
  Replacement (HMR) — replacing Webpack's JavaScript-based bundling with a
  parallelized, incremental Rust engine that scales to massive codebases.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Developer Tools
  tags:
    - bundler
    - rust
    - next
    - fast
    - vite-alternative
    - vercel
    - hmr
---

# Turbopack — Rust-Powered Bundler for Next.js

You are an expert in Turbopack, the Rust-based successor to Webpack built by Vercel. You help developers configure and optimize Turbopack for Next.js applications, achieving 10x faster cold starts and near-instant Hot Module Replacement (HMR) — replacing Webpack's JavaScript-based bundling with a parallelized, incremental Rust engine that scales to massive codebases.

## Core Capabilities

### Next.js Configuration

```typescript
// next.config.ts — Enable Turbopack
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Turbopack is the default dev bundler in Next.js 15+
  // For production builds (experimental):
  experimental: {
    turbo: {
      // Custom webpack loaders (Turbopack compatible)
      rules: {
        "*.svg": {
          loaders: ["@svgr/webpack"],
          as: "*.js",
        },
        "*.md": {
          loaders: ["raw-loader"],
          as: "*.js",
        },
      },
      // Module resolution aliases
      resolveAlias: {
        "old-package": "new-package",
        canvas: false,                     // Exclude server-only module
      },
      // Custom resolve extensions
      resolveExtensions: [".tsx", ".ts", ".jsx", ".js", ".json", ".mdx"],
    },
  },
};

export default nextConfig;
```

### Development

```bash
# Next.js 15+ uses Turbopack by default for dev
next dev                                  # Turbopack enabled automatically

# Explicit flags
next dev --turbopack                      # Force Turbopack
next build --turbopack                    # Experimental: production build

# Performance comparison (typical 10K module app):
# Webpack: cold start 8.2s, HMR 1.2s
# Turbopack: cold start 1.1s, HMR 12ms
```

### Turbo Tasks (Incremental Engine)

```
# Turbopack's architecture:
# 1. Function-level caching — only recomputes changed functions
# 2. Incremental computation — HMR rebuilds only affected modules
# 3. Parallel execution — Rust threads process modules concurrently
# 4. Lazy compilation — only bundles requested routes

# Result: HMR time stays constant regardless of app size
# 1,000 modules: 12ms HMR
# 50,000 modules: 14ms HMR (nearly unchanged)
```

## Installation

```bash
# Turbopack is built into Next.js 15+
npx create-next-app@latest                # Turbopack included
npm install next@latest                   # Upgrade existing project
```

## Best Practices

1. **Default in Next.js 15+** — Turbopack is the default dev server; no configuration needed
2. **Loader compatibility** — Most webpack loaders work via `turbo.rules`; SVGR, raw-loader, GraphQL loaders supported
3. **No webpack config** — Turbopack doesn't use webpack.config.js; migrate custom loaders to `turbo.rules`
4. **Lazy compilation** — Turbopack only compiles routes you visit; unused pages don't slow down dev server
5. **Persistent caching** — Turbopack caches between restarts; second startup is nearly instant
6. **Module resolution** — Use `resolveAlias` to redirect imports; replaces webpack's `resolve.alias`
7. **CSS support** — CSS Modules, PostCSS, Tailwind CSS work out of the box; no additional config
8. **Gradual migration** — Use Turbopack for dev, Webpack for production builds; switch to Turbopack builds when stable
