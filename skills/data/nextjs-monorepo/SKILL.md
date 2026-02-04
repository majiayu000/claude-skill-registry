---
name: nextjs-monorepo
description: Next.js monorepo patterns with Turborepo and pnpm workspaces. Use this skill when working with multi-package Next.js projects, managing dependencies across packages, optimizing build pipelines, or configuring Turborepo.
metadata:
  author: alias
  version: "1.0.0"
  project: monorepo-next-prisma
---

# Next.js Monorepo Skill

Best practices for developing Next.js applications in a monorepo using Turborepo and pnpm workspaces.

## Architecture

```
monorepo/
├── apps/
│   ├── dashboard/     # Next.js app
│   ├── marketing/     # Next.js app
│   └── public-api/    # Next.js app
├── packages/
│   ├── ui/            # Shared UI components
│   ├── config/        # Shared configs (ESLint, TS, etc.)
│   └── database/      # Shared database layer
├── package.json       # Root package.json
├── pnpm-workspace.yaml
├── turbo.json         # Turborepo config
└── tsconfig.json      # Root TS config
```

## When to Use This Skill

Use when:
- Setting up a new monorepo
- Adding new apps or packages
- Managing cross-package dependencies
- Optimizing build performance
- Configuring Turborebo pipelines
- Setting up CI/CD for monorepo

## Key Principles

### 1. Workspace Organization

**Package Naming:**
- Internal packages must have unique names
- Use scope prefix: `@myorg/ui`, `@myorg/database`
- Reference in package.json: `"@myorg/ui": "workspace:*"`

**Dependency Management:**
```bash
# Add dependency to specific package
pnpm --filter dashboard add react

# Add to all apps
pnpm --filter ./apps/* add next

# Add shared dependency to all packages
pnpm -w add typescript
```

### 2. Turborebo Configuration

**Pipeline Setup:**
```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^lint"]
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"]
    }
  }
}
```

**Task Execution:**
```bash
# Run task in all packages
turbo run build

# Run task in specific package
turbo run build --filter=dashboard

# Run with affected detection
turbo run build --filter=[HEAD^1]
```

### 3. TypeScript Configuration

**Root tsconfig.json:**
```json
{
  "compilerOptions": {
    "composite": true,
    "paths": {
      "@myorg/ui": ["./packages/ui/src"],
      "@myorg/database": ["./packages/database/src"]
    }
  },
  "references": [
    { "path": "./apps/dashboard" },
    { "path": "./packages/ui" }
  ]
}
```

**Package tsconfig.json:**
```json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "composite": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "references": [
    { "path": "../../packages/ui" }
  ],
  "include": ["src"]
}
```

### 4. Import Paths

**Use workspace names for imports:**
```tsx
// apps/dashboard/page.tsx
import { Button } from '@myorg/ui'
import { db } from '@myorg/database'

// NOT: import { Button } from '../../../packages/ui/src'
```

## Common Tasks

### Add New App

```bash
# 1. Create app directory
mkdir -p apps/my-app
cd apps/my-app

# 2. Initialize Next.js
pnpm create next-app . --typescript --tailwind --app

# 3. Update package.json with workspace name
# "name": "@myorg/my-app"

# 4. Add to root tsconfig references
# 5. Add to turbo.json pipeline if needed
```

### Add New Package

```bash
# 1. Create package directory
mkdir -p packages/my-package
cd packages/my-package

# 2. Initialize
pnpm init

# 3. Update package.json
{
  "name": "@myorg/my-package",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": "./src/index.ts"
  }
}

# 4. Add to root tsconfig.json references
# 5. Add path mapping to root tsconfig
```

### Build Optimization

```bash
# Build only changed packages
turbo run build --filter=[HEAD^1]

# Build specific package and dependents
turbo run build --filter=my-package

# Parallel build with cache
turbo run build --force

# Clean all build artifacts
turbo run clean
```

## Troubleshooting

### "Cannot find module" errors

1. Check pnpm-workspace.yaml includes the package
2. Run `pnpm install` from root
3. Verify package name in package.json
4. Check tsconfig paths are correct

### "Module not found" in Turborepo

1. Ensure dependencies are listed in package.json
2. Run `pnpm install` before turbo commands
3. Check for circular dependencies

### Build cache issues

```bash
# Clear turbo cache
turbo run build --force

# Clear pnpm cache
pnpm store prune

# Reinstall everything
rm -rf node_modules packages/*/node_modules apps/*/node_modules
pnpm install
```

## Best Practices

1. **Keep packages focused** - Single responsibility per package
2. **Use strict dependencies** - Only depend on what you need
3. **Internal packages only** - Use `private: true` for workspace packages
4. **Version together** - Use shared versions for core packages
5. **CI/CD with affected** - Only test/deploy changed packages
6. **Lock files** - Commit pnpm-lock.yaml
7. **Explicit types** - Export types from packages

## CI/CD Configuration

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      - uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm turbo run build --filter=[HEAD^1]
      - run: pnpm turbo run test --filter=[HEAD^1]
      - run: pnpm turbo run lint --filter=[HEAD^1]
```

## Related Skills

- `vercel-react-best-practices` - React/Next.js performance
- `typescript-strict` - TypeScript configuration
- `vercel-deploy-claimable` - Deployment

## Resources

- [Turborepo Docs](https://turbo.build/repo/docs)
- [pnpm Workspaces](https://pnpm.io/workspaces)
- [Next.js Monorepo](https://nextjs.org/docs/advanced-features/multi-zones)
