---
name: webapp-building
description: Tools for building modern React webapps with TypeScript, Tailwind CSS and shadcn/ui. Best suited for applications with complex UI components and state management.
---

# WebApp Building

**Stack**: React + TypeScript + Vite + Tailwind CSS + shadcn/ui

## Workflow

1. `scripts/init-webapp.sh <website-title>` — Initialize project in /mnt/okcomputer/output/app, with website title
2. Edit source code in `src/`
3. Build the React app 
4. Deploy the build output in `/mnt/okcomputer/output/app/dist/`

## Quick Start

### 1. Initialize

```bash
# init project in /mnt/okcomputer/output/app with website title
bash scripts/init-webapp.sh <website-title>
cd /mnt/okcomputer/output/app
```

**AI Agent Notes**:
- The project path is /mnt/okcomputer/output/app
- Non-interactive execution with auto-confirm

This creates a fully configured project with:

- ✅ React + TypeScript (via Vite)
- ✅ Tailwind CSS 3.4.19 with shadcn/ui theming system
- ✅ Path aliases (`@/`) configured
- ✅ 40+ shadcn/ui components pre-installed
- ✅ All Radix UI dependencies included
- ✅ Production build optimization with Vite
- ✅ Node 20+ compatibility (auto-detects and pins Vite version)

### 2. Develop

Edit generated files in `src/`: page sections go in `src/sections/`, custom React hooks in `src/hooks/`, and TypeScript definitions in `src/types/`.

### 3. Build

```bash
# within project:
cd /mnt/okcomputer/output/app && npm run build 2>&1
```

**Output** (`dist/`):
- `index.html` — Entry point
- `assets/index-[hash].js` — Bundled JS
- `assets/index-[hash].css` — Bundled CSS
- Optimized images, fonts, other assets

**Optimizations**: Tree-shaking, code splitting, asset compression, minification, cache-busting hashes.

### 4. Deploy

Deploy the build output in `/mnt/okcomputer/output/app/dist/`

## Debugging

1. Fix source files
2. `npm run build`
3. Test `dist/`
4. Redeploy

## Reference

- [shadcn/ui Components](https://ui.shadcn.com/docs/components)
