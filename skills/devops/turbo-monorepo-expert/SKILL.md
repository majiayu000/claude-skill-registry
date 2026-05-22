---
name: Turbo Monorepo Expert
description: Expert guidance for Turborepo and pnpm workspace management, build optimization, caching strategies, and monorepo architecture patterns. Use when working with Turbo monorepos, pnpm workspaces, or multi-package projects.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Turbo Monorepo Expert

Expert system for Turborepo (Turbo) and pnpm workspace management, optimized for large-scale monorepo architectures.

## Core Capabilities

### 1. Turborepo Architecture & Setup

**Optimal turbo.json Configuration:**
```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env", "tsconfig.json"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "build/**"],
      "env": ["NODE_ENV"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "cache": false
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "type-check": {
      "dependsOn": ["^build"],
      "outputs": []
    }
  },
  "remoteCache": {
    "enabled": true
  }
}
```

**Root package.json Structure:**
```json
{
  "name": "monorepo-root",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*",
    "services/*"
  ],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev --parallel",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "type-check": "turbo run type-check",
    "clean": "turbo run clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "latest",
    "@turbo/gen": "latest"
  },
  "packageManager": "pnpm@8.15.0",
  "engines": {
    "node": ">=18.0.0",
    "pnpm": ">=8.0.0"
  }
}
```

### 2. pnpm Workspace Configuration

**Root pnpm-workspace.yaml:**
```yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'services/*'
  - 'tools/*'
```

**.npmrc Best Practices:**
```ini
# Hoist dependencies for faster installs
shamefully-hoist=true
# Strict peer dependencies
strict-peer-dependencies=false
# Use workspace protocol
link-workspace-packages=true
# Save exact versions
save-exact=true
# Faster installs
prefer-frozen-lockfile=true
# Store location
store-dir=~/.pnpm-store
```

### 3. Package Organization Patterns

**Recommended Structure:**
```
monorepo-root/
├── apps/                    # Deployable applications
│   ├── web/                # Next.js app
│   ├── api/                # Backend service
│   └── admin/              # Admin dashboard
├── packages/               # Shared libraries
│   ├── ui/                 # Component library
│   ├── config/             # Shared configs
│   ├── utils/              # Utilities
│   └── types/              # TypeScript types
├── services/               # Microservices
│   ├── auth/
│   ├── payments/
│   └── notifications/
├── tools/                  # Build tools & scripts
├── turbo.json
├── pnpm-workspace.yaml
└── package.json
```

**Package Naming Convention:**
```
@scope/package-name

Examples:
@company/ui
@company/utils
@company/config-eslint
@company/config-typescript
```

### 4. Internal Package Template

**packages/ui/package.json:**
```json
{
  "name": "@company/ui",
  "version": "0.0.0",
  "private": true,
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./styles.css": "./dist/styles.css"
  },
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "dev": "tsup src/index.ts --format cjs,esm --dts --watch",
    "lint": "eslint src/",
    "type-check": "tsc --noEmit"
  },
  "devDependencies": {
    "@company/config-typescript": "workspace:*",
    "@company/config-eslint": "workspace:*",
    "tsup": "^8.0.0",
    "typescript": "^5.3.0"
  },
  "dependencies": {
    "react": "^18.2.0"
  }
}
```

### 5. Build Optimization Strategies

**Parallel Execution:**
```bash
# Run tasks in parallel across all packages
turbo run build --parallel

# Run specific packages only
turbo run build --filter=@company/ui

# Run app and its dependencies
turbo run build --filter=web...
```

**Cache Management:**
```bash
# Clear all caches
turbo run clean

# Disable cache for specific run
turbo run build --force

# Check cache hit rate
turbo run build --summarize
```

**Remote Caching (Vercel):**
```bash
# Link to Vercel for remote caching
turbo login
turbo link

# Verify remote cache
turbo run build --remote-only
```

### 6. Dependency Management

**Adding Dependencies:**
```bash
# Add to root
pnpm add -w <package>

# Add to specific workspace
pnpm add <package> --filter @company/ui

# Add workspace dependency
pnpm add @company/utils --filter @company/ui --workspace
```

**Dependency Protocol:**
```json
{
  "dependencies": {
    "@company/utils": "workspace:*",  // Latest in workspace
    "@company/ui": "workspace:^",     // Compatible version
    "react": "^18.2.0"                // External dependency
  }
}
```

### 7. TypeScript Configuration

**Root tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "incremental": true,
    "noEmit": true
  },
  "exclude": ["node_modules"]
}
```

**Package-specific tsconfig.json:**
```json
{
  "extends": "@company/config-typescript/base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### 8. Code Generation with @turbo/gen

**Generate New Package:**
```bash
turbo gen workspace

# Follow prompts:
# - Name: @company/new-package
# - Type: package
# - Template: library
```

**Custom Generator:**
```typescript
// turbo/generators/config.ts
import type { PlopTypes } from "@turbo/gen";

export default function generator(plop: PlopTypes.NodePlopAPI): void {
  plop.setGenerator("package", {
    description: "Create new package",
    prompts: [
      {
        type: "input",
        name: "name",
        message: "Package name (without @company/):",
      },
      {
        type: "list",
        name: "type",
        message: "Package type:",
        choices: ["library", "config", "service"],
      },
    ],
    actions: [
      {
        type: "add",
        path: "packages/{{name}}/package.json",
        templateFile: "templates/package.json.hbs",
      },
      {
        type: "add",
        path: "packages/{{name}}/src/index.ts",
        templateFile: "templates/index.ts.hbs",
      },
    ],
  });
}
```

### 9. Common Patterns & Solutions

**Circular Dependency Detection:**
```bash
# Install dependency checker
pnpm add -Dw madge

# Check for cycles
madge --circular --extensions ts,tsx apps/web/src
```

**Shared Environment Variables:**
```typescript
// packages/env/src/index.ts
import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
});

export const env = envSchema.parse(process.env);
```

**Shared ESLint Configuration:**
```javascript
// packages/config-eslint/index.js
module.exports = {
  extends: [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended",
    "prettier",
  ],
  parser: "@typescript-eslint/parser",
  plugins: ["@typescript-eslint"],
  rules: {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "warn",
  },
};
```

### 10. Performance Optimization

**Task Dependency Optimization:**
```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],           // Wait for dependencies
      "outputs": ["dist/**"],
      "inputs": ["src/**", "package.json"]  // Track specific inputs
    }
  }
}
```

**Selective Task Running:**
```bash
# Only changed packages
turbo run build --filter=[HEAD^1]

# Specific scope
turbo run test --filter=@company/ui...

# Exclude packages
turbo run build --filter=!@company/deprecated
```

**Parallel Limits:**
```bash
# Limit concurrent tasks (for CI with limited resources)
turbo run build --concurrency=2

# Prevent OOM on large repos
export NODE_OPTIONS="--max-old-space-size=4096"
```

### 11. CI/CD Integration

**GitHub Actions Example:**
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Build
        run: turbo run build --filter=[HEAD^1]
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}

      - name: Test
        run: turbo run test --filter=[HEAD^1]

      - name: Lint
        run: turbo run lint --filter=[HEAD^1]
```

### 12. Migration Strategies

**From npm/yarn to pnpm + Turbo:**
```bash
# 1. Remove existing
rm -rf node_modules package-lock.json yarn.lock

# 2. Install pnpm
npm install -g pnpm

# 3. Import from package-lock.json
pnpm import

# 4. Install dependencies
pnpm install

# 5. Add Turbo
pnpm add -Dw turbo

# 6. Create turbo.json
turbo gen config
```

**Convert existing scripts:**
```json
{
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev --parallel",
    "test": "turbo run test --concurrency=1",
    "clean": "turbo run clean && rm -rf node_modules"
  }
}
```

### 13. Troubleshooting Guide

**Common Issues:**

1. **"Package not found" errors:**
   ```bash
   # Clear all node_modules and reinstall
   pnpm clean:all
   pnpm install
   ```

2. **Cache issues:**
   ```bash
   # Clear Turbo cache
   rm -rf .turbo

   # Clear pnpm cache
   pnpm store prune
   ```

3. **Build failures in CI:**
   ```bash
   # Use frozen lockfile
   pnpm install --frozen-lockfile

   # Disable remote cache if issues
   turbo run build --remote-only=false
   ```

4. **Slow installs:**
   ```ini
   # .npmrc
   auto-install-peers=true
   shamefully-hoist=true
   ```

### 14. Best Practices Checklist

- [ ] Use `workspace:*` protocol for internal dependencies
- [ ] Configure `globalDependencies` in turbo.json (.env, tsconfig)
- [ ] Set up remote caching (Vercel Turborepo or custom)
- [ ] Use `--filter` in CI to build only changed packages
- [ ] Configure `outputs` correctly for all tasks
- [ ] Use `dependsOn: ["^task"]` for proper build order
- [ ] Set `cache: false` for dev and test tasks
- [ ] Use consistent naming (@scope/package-name)
- [ ] Configure `engines` field for Node/pnpm versions
- [ ] Use `turbo gen` for new packages
- [ ] Set up path aliases in tsconfig
- [ ] Use shared ESLint/TypeScript configs
- [ ] Configure `.gitignore` for Turbo cache

### 15. Advanced Patterns

**Conditional Task Execution:**
```json
{
  "pipeline": {
    "deploy": {
      "dependsOn": ["build", "test"],
      "cache": false,
      "env": ["AWS_*", "VERCEL_*"]
    }
  }
}
```

**Task-Specific Environment Variables:**
```json
{
  "pipeline": {
    "build": {
      "env": ["NODE_ENV", "NEXT_PUBLIC_*"],
      "passThroughEnv": ["CI", "VERCEL"]
    }
  }
}
```

**Scoped Tasks:**
```bash
# Run only in apps
turbo run build --filter='./apps/*'

# Run in packages, not apps
turbo run test --filter='./packages/*'

# Complex filters
turbo run build --filter='@company/api...[origin/main]'
```

## Quick Commands Reference

```bash
# Installation
pnpm install                                    # Install all dependencies
pnpm add <pkg> --filter <workspace>            # Add to specific package
pnpm add <pkg> -w                              # Add to root

# Turbo Operations
turbo run build                                # Build all
turbo run build --filter=<package>             # Build specific package
turbo run dev --parallel                       # Run dev servers
turbo run test --concurrency=1                 # Run tests sequentially
turbo run lint --continue                      # Continue on errors

# Filters
turbo run build --filter=[HEAD^1]              # Changed since last commit
turbo run build --filter=<package>...          # Package + dependencies
turbo run build --filter=...<package>          # Package + dependents

# Cache
turbo run build --force                        # Skip cache
turbo run build --summarize                    # Show cache stats
turbo prune --scope=<package>                  # Create pruned subset

# Workspace Management
pnpm -r exec <command>                         # Run in all workspaces
pnpm --filter <package> <command>              # Run in specific workspace
turbo gen workspace                            # Generate new package

# Cleaning
turbo run clean                                # Run clean tasks
rm -rf .turbo                                  # Clear Turbo cache
pnpm store prune                               # Clear pnpm cache
```

## Integration with Existing Tools

**Vercel:**
```json
{
  "buildCommand": "turbo run build --filter={apps/web}...",
  "installCommand": "pnpm install"
}
```

**Docker:**
```dockerfile
FROM node:18-alpine AS base
RUN npm install -g pnpm turbo
WORKDIR /app

FROM base AS deps
COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./
COPY packages ./packages
RUN pnpm install --frozen-lockfile

FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN turbo run build --filter=api

FROM base AS runner
COPY --from=builder /app/apps/api/dist ./dist
CMD ["node", "dist/index.js"]
```

---

## When to Use This Skill

Invoke this skill when:
- Setting up new Turborepo monorepo
- Migrating to Turbo from Lerna/Nx/Rush
- Optimizing build times and caching
- Configuring pnpm workspaces
- Troubleshooting monorepo issues
- Setting up CI/CD for monorepo
- Creating new packages or apps
- Managing internal dependencies
- Scaling monorepo architecture
