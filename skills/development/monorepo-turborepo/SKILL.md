---
name: monorepo-turborepo
description: Manage monorepos with Turborepo for workspace configuration, task caching, and CI optimization. Use when building multi-package projects, shared libraries, or optimizing large codebases.
---

# Turborepo Monorepo Management

Expert guidance for building and managing monorepos with Turborepo. Covers workspace setup, pipeline configuration, caching strategies, and CI/CD optimization.

## Quick Start

```bash
# Create new Turborepo monorepo
npx create-turbo@latest my-monorepo

# Add Turborepo to existing monorepo
npm install turbo --save-dev

# Run all build tasks
turbo run build

# Run with cache bypass
turbo run build --force
```

## Workspace Configuration

### pnpm Workspaces (Recommended)

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
  - "tools/*"
```

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "clean": "turbo run clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "^2.0.0"
  },
  "packageManager": "pnpm@9.0.0"
}
```

### npm Workspaces

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev"
  }
}
```

### Yarn Workspaces

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": {
    "packages": ["apps/*", "packages/*"],
    "nohoist": ["**/react-native", "**/react-native/**"]
  }
}
```

## turbo.json Pipeline Configuration

### Basic Configuration

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env", "tsconfig.json"],
  "globalEnv": ["NODE_ENV", "CI"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "build/**"],
      "env": ["API_URL", "DATABASE_URL"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"],
      "outputs": []
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "env": ["CI", "TEST_DATABASE_URL"]
    },
    "clean": {
      "cache": false
    }
  }
}
```

### Advanced Pipeline with Inputs

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": [
        "src/**",
        "package.json",
        "tsconfig.json",
        "!src/**/*.test.ts"
      ],
      "outputs": ["dist/**"],
      "outputLogs": "new-only"
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "inputs": ["**/*.ts", "**/*.tsx", "tsconfig.json"],
      "outputs": []
    },
    "test:unit": {
      "inputs": ["src/**", "tests/**", "jest.config.*"],
      "outputs": ["coverage/**"],
      "env": ["CI"]
    },
    "test:e2e": {
      "dependsOn": ["build"],
      "inputs": ["e2e/**", "playwright.config.*"],
      "outputs": ["test-results/**"],
      "cache": false
    }
  }
}
```

## Task Dependencies

### Dependency Types

```json
{
  "tasks": {
    // Depends on own package's dependencies' build first
    "build": {
      "dependsOn": ["^build"]
    },

    // Depends on same package's other tasks
    "test": {
      "dependsOn": ["build", "lint"]
    },

    // Depends on specific package's task
    "deploy": {
      "dependsOn": ["@repo/api#build", "@repo/web#build"]
    },

    // No dependencies - runs in parallel
    "lint": {
      "dependsOn": []
    }
  }
}
```

### Task Graph Visualization

```bash
# Visualize task graph
turbo run build --graph

# Output to file
turbo run build --graph=graph.html

# Dry run to see what would execute
turbo run build --dry-run
```

## Caching Strategies

### Local Cache Configuration

```json
{
  "tasks": {
    "build": {
      "outputs": ["dist/**"],
      "cache": true
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Cache Inputs

```json
{
  "tasks": {
    "build": {
      "inputs": [
        "src/**/*.ts",
        "src/**/*.tsx",
        "package.json",
        "tsconfig.json",
        "$TURBO_DEFAULT$"
      ],
      "outputs": ["dist/**"]
    }
  },
  "globalDependencies": [".env.production", "turbo.json"]
}
```

### Environment Variables in Cache

```json
{
  "globalEnv": ["CI", "NODE_ENV"],
  "tasks": {
    "build": {
      "env": ["API_URL", "PUBLIC_*"],
      "passThroughEnv": ["AWS_SECRET_KEY"]
    }
  }
}
```

## Remote Caching

### Vercel Remote Cache

```bash
# Login to Vercel
npx turbo login

# Link to Vercel project
npx turbo link

# Enable remote cache
turbo run build --remote-cache-timeout=60
```

### Self-Hosted Remote Cache

```bash
# Using custom remote cache server
TURBO_API="https://cache.mycompany.com" \
TURBO_TOKEN="your-token" \
TURBO_TEAM="my-team" \
turbo run build
```

```json
// turbo.json - Remote cache config
{
  "remoteCache": {
    "signature": true,
    "enabled": true
  }
}
```

### CI Environment Variables

```yaml
# GitHub Actions
env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}
  TURBO_REMOTE_ONLY: true
```

## Filtering and Scopes

### Filter Syntax

```bash
# Run in specific package
turbo run build --filter=@repo/web

# Run in package and dependencies
turbo run build --filter=@repo/web...

# Run in package and dependents
turbo run build --filter=...@repo/ui

# Run in changed packages (since main)
turbo run build --filter=[main]

# Run in changed packages and dependents
turbo run build --filter=...[main]

# Exclude packages
turbo run build --filter=!@repo/docs

# Multiple filters
turbo run build --filter=@repo/web --filter=@repo/api

# Directory-based filter
turbo run build --filter="./apps/*"

# Scope with dependencies
turbo run build --filter=@repo/web^...
```

### Package-Specific Scripts

```json
// apps/web/package.json
{
  "name": "@repo/web",
  "scripts": {
    "build": "next build",
    "dev": "next dev --port 3000",
    "lint": "eslint .",
    "test": "vitest"
  }
}
```

## Internal Packages

### Package Structure

```
packages/
├── ui/
│   ├── package.json
│   ├── tsconfig.json
│   └── src/
│       ├── Button.tsx
│       ├── Card.tsx
│       └── index.ts
├── utils/
│   ├── package.json
│   └── src/
│       └── index.ts
└── config/
    ├── eslint/
    │   └── package.json
    └── typescript/
        └── package.json
```

### Internal Package Configuration

```json
// packages/ui/package.json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "private": true,
  "exports": {
    ".": "./src/index.ts",
    "./button": "./src/Button.tsx",
    "./card": "./src/Card.tsx"
  },
  "typesVersions": {
    "*": {
      "*": ["src/*"]
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "dev": "tsup src/index.ts --format cjs,esm --dts --watch",
    "lint": "eslint src/"
  },
  "devDependencies": {
    "@repo/typescript-config": "workspace:*",
    "tsup": "^8.0.0",
    "typescript": "^5.0.0"
  }
}
```

### Consuming Internal Packages

```json
// apps/web/package.json
{
  "name": "@repo/web",
  "dependencies": {
    "@repo/ui": "workspace:*",
    "@repo/utils": "workspace:*"
  }
}
```

```tsx
// apps/web/src/page.tsx
import { Button, Card } from "@repo/ui";
import { formatDate } from "@repo/utils";
```

## Shared Configurations

### Shared TypeScript Config

```json
// packages/typescript-config/base.json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

```json
// packages/typescript-config/nextjs.json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./base.json",
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "jsx": "preserve",
    "module": "esnext",
    "noEmit": true,
    "plugins": [{ "name": "next" }]
  }
}
```

```json
// apps/web/tsconfig.json
{
  "extends": "@repo/typescript-config/nextjs.json",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
```

### Shared ESLint Config

```js
// packages/eslint-config/base.js
module.exports = {
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier",
  ],
  parser: "@typescript-eslint/parser",
  plugins: ["@typescript-eslint"],
  rules: {
    "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
    "@typescript-eslint/no-explicit-any": "warn",
  },
};
```

```js
// packages/eslint-config/react.js
module.exports = {
  extends: [
    "./base.js",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
  ],
  plugins: ["react", "react-hooks"],
  settings: {
    react: {   },
  rules: {
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off",
  },
};
```

## CI/CD Optimization

### GitHub Actions with Turborepo

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - uses: pnpm/action-setup@v3
        with:
          
      - uses: actions/setup-node@v4
        with:
          node-          cache: "pnpm"

      - run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm turbo run build --filter="...[HEAD^1]"

      - name: Test
        run: pnpm turbo run test --filter="...[HEAD^1]"

      - name: Lint
        run: pnpm turbo run lint --filter="...[HEAD^1]"
```

### Affected Package Detection

```yaml
# Build only affected packages
- name: Build affected
  run: |
    pnpm turbo run build \
      --filter="...[origin/main]" \
      --concurrency=4

# Deploy specific apps if changed
- name: Deploy web if changed
  run: |
    if pnpm turbo run build --filter=@repo/web...[origin/main] --dry-run | grep -q "@repo/web"; then
      pnpm turbo run deploy --filter=@repo/web
    fi
```

### Parallel Jobs Matrix

```yaml
jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      packages: ${{ steps.filter.outputs.packages }}
    steps:
      - uses: actions/checkout@v4
      - id: filter
        run: |
          PACKAGES=$(pnpm turbo run build --dry-run=json --filter="[HEAD^1]" | jq -c '[.packages[]]')
          echo "packages=$PACKAGES" >> $GITHUB_OUTPUT

  build:
    needs: detect-changes
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package: ${{ fromJson(needs.detect-changes.outputs.packages) }}
    steps:
      - uses: actions/checkout@v4
      - run: pnpm turbo run build --filter=${{ matrix.package }}
```

## Nx Comparison Notes

| Feature              | Turborepo             | Nx                      |
| -------------------- | --------------------- | ----------------------- |
| Task Caching         | ✅ Built-in           | ✅ Built-in             |
| Remote Cache         | ✅ Vercel/Self-hosted | ✅ Nx Cloud             |
| Affected Detection   | ✅ Git-based          | ✅ Dependency graph     |
| Code Generation      | ❌ None               | ✅ Extensive generators |
| Plugin Ecosystem     | ❌ Limited            | ✅ Rich ecosystem       |
| Learning Curve       | ✅ Minimal            | ⚠️ Steeper              |
| Configuration        | ✅ Simple JSON        | ⚠️ More complex         |
| Incremental Adoption | ✅ Easy               | ⚠️ More involved        |

### When to Choose Turborepo

- Simpler monorepo needs
- Already using Vercel
- Minimal configuration preferred
- Incremental adoption from existing setup

### When to Choose Nx

- Need code generators
- Complex enterprise monorepos
- Want integrated tooling
- Need extensive plugin support

## Best Practices

### Repository Structure

```
my-monorepo/
├── apps/
│   ├── web/              # Next.js frontend
│   ├── api/              # Express/Fastify backend
│   └── docs/             # Documentation site
├── packages/
│   ├── ui/               # Shared React components
│   ├── utils/            # Shared utilities
│   ├── types/            # Shared TypeScript types
│   └── config/
│       ├── eslint/       # Shared ESLint config
│       └── typescript/   # Shared TS config
├── turbo.json
├── pnpm-workspace.yaml
└── package.json
```

### Performance Tips

```bash
# Limit concurrency on CI
turbo run build --concurrency=4

# Use remote cache in CI only
TURBO_REMOTE_ONLY=true turbo run build

# Skip cache for debugging
turbo run build --force

# Prune for Docker builds
turbo prune @repo/api --docker
```

### Docker Optimization

```dockerfile
# Dockerfile using turbo prune
FROM node:20-alpine AS builder
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install turbo globally
RUN npm install -g turbo

# Copy source and prune
COPY . .
RUN turbo prune @repo/api --docker

# Install dependencies
FROM node:20-alpine AS installer
WORKDIR /app
COPY --from=builder /app/out/json/ .
COPY --from=builder /app/out/pnpm-lock.yaml ./pnpm-lock.yaml
RUN corepack enable pnpm && pnpm install --frozen-lockfile

# Build
COPY --from=builder /app/out/full/ .
RUN pnpm turbo run build --filter=@repo/api

# Run
FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=installer /app/apps/api/dist ./dist
CMD ["node", "dist/index.js"]
```

### Versioning and Publishing

```json
// package.json
{
  "scripts": {
    "version-packages": "changeset version",
    "publish-packages": "turbo run build --filter='./packages/*' && changeset publish"
  }
}
```

## Troubleshooting

### Common Issues

```bash
# Clear all caches
turbo run clean
rm -rf node_modules .turbo

# Debug cache misses
turbo run build --summarize

# Check why task ran
turbo run build --dry-run=json | jq '.tasks[] | {name, cache}'

# Verbose logging
turbo run build --verbosity=2
```

### Cache Debugging

```bash
# Show cache status
turbo run build --summarize

# Output shows:
# - Tasks: 5 successful, 3 cached
# - Time saved: 45s
# - Cache hit rate: 60%
```

## Quick Reference

| Command                              | Description                   |
| ------------------------------------ | ----------------------------- |
| `turbo run build`                    | Run build in all packages     |
| `turbo run build --filter=web`       | Run in specific package       |
| `turbo run build --filter=...[main]` | Run in changed packages       |
| `turbo run build --force`            | Skip cache                    |
| `turbo run build --dry-run`          | Show what would run           |
| `turbo run build --graph`            | Visualize task graph          |
| `turbo prune --docker`               | Prune for Docker              |
| `turbo login`                        | Authenticate for remote cache |
| `turbo link`                         | Link to Vercel project        |
