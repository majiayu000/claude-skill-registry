---
name: monorepo
model: standard
description: Build and manage monorepos with Turborepo, Nx, and pnpm workspaces — covering workspace structure, dependency management, task orchestration, caching, CI/CD, and publishing. Use when setting up monorepos, optimizing builds, or managing shared packages.
---

# Monorepo Management

Build efficient, scalable monorepos that enable code sharing, consistent tooling, and atomic changes across multiple packages and applications.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install monorepo
```


## When to Use

- Setting up a new monorepo or migrating from multi-repo
- Optimizing build and test performance
- Managing shared dependencies across packages
- Configuring CI/CD for monorepos
- Versioning and publishing packages

## Why Monorepos?

**Advantages:** Shared code and dependencies, atomic commits across projects, consistent tooling, easier refactoring, better code visibility.

**Challenges:** Build performance at scale, CI/CD complexity, access control, large Git history.

## Tool Selection

### Package Managers

| Manager | Recommendation | Notes |
|---------|---------------|-------|
| **pnpm** | Recommended | Fast, strict, excellent workspace support |
| **npm** | Acceptable | Built-in workspaces, slower installs |
| **Yarn** | Acceptable | Mature, but pnpm surpasses in most areas |

### Build Systems

| Tool | Best For | Trade-off |
|------|----------|-----------|
| **Turborepo** | Most projects | Simple config, fast caching, Vercel integration |
| **Nx** | Large orgs, complex graphs | Feature-rich but steeper learning curve |
| **Lerna** | Legacy projects | Maintenance mode — migrate away |

**Guidance:** Start with Turborepo unless you need Nx's code generation, dependency graph visualization, or plugin ecosystem.

## Workspace Structure

```
my-monorepo/
├── apps/
│   ├── web/              # Next.js app
│   ├── api/              # Backend service
│   └── docs/             # Documentation site
├── packages/
│   ├── ui/               # Shared UI components
│   ├── utils/            # Shared utilities
│   ├── types/            # Shared TypeScript types
│   ├── config-eslint/    # Shared ESLint config
│   └── config-ts/        # Shared TypeScript configs
├── turbo.json            # Turborepo pipeline config
├── pnpm-workspace.yaml   # Workspace definition
└── package.json          # Root package.json
```

**Convention:** `apps/` for deployable applications, `packages/` for shared libraries.

## Turborepo Setup

### Root Configuration

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
```

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "type-check": "turbo run type-check",
    "clean": "turbo run clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "prettier": "^3.0.0"
  },
  "packageManager": "pnpm@9.0.0"
}
```

### Pipeline Configuration

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"],
      "inputs": ["src/**", "package.json", "tsconfig.json"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    },
    "type-check": {
      "dependsOn": ["^build"],
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

Key concepts:
- `dependsOn: ["^build"]` — build dependencies first (topological)
- `outputs` — what to cache (omit for side-effect-only tasks)
- `inputs` — what invalidates cache (default: all files)
- `persistent: true` — for long-running dev servers
- `cache: false` — disable caching for dev tasks

### Package Configuration

```json
// packages/ui/package.json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "private": true,
  "exports": {
    ".": { "import": "./dist/index.js", "types": "./dist/index.d.ts" },
    "./button": { "import": "./dist/button.js", "types": "./dist/button.d.ts" }
  },
  "scripts": {
    "build": "tsup src/index.ts --format esm,cjs --dts",
    "dev": "tsup src/index.ts --format esm,cjs --dts --watch"
  },
  "devDependencies": {
    "@repo/config-ts": "workspace:*",
    "tsup": "^8.0.0"
  }
}
```

## Nx Setup

```bash
npx create-nx-workspace@latest my-org

# Generate projects
nx generate @nx/react:app my-app
nx generate @nx/js:lib utils
```

```json
// nx.json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["production", "^production"],
      "cache": true
    },
    "test": {
      "inputs": ["default", "^production"],
      "cache": true
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*"],
    "production": ["default", "!{projectRoot}/**/*.spec.*"]
  }
}
```

```bash
# Nx-specific commands
nx build my-app
nx affected:build --base=main    # Only build what changed
nx graph                          # Visualize dependency graph
nx run-many --target=build --all --parallel=3
```

**Nx advantage:** `nx affected` computes exactly which projects changed, skipping unaffected ones entirely.

## Dependency Management (pnpm)

```bash
# Install in specific package
pnpm add react --filter @repo/ui
pnpm add -D typescript --filter @repo/ui

# Install workspace dependency
pnpm add @repo/ui --filter web

# Install in root (shared dev tools)
pnpm add -D eslint -w

# Run script in specific package
pnpm --filter web dev
pnpm --filter @repo/ui build

# Run in all packages
pnpm -r build

# Filter patterns
pnpm --filter "@repo/*" build
pnpm --filter "...web" build    # web + all its dependencies

# Update all dependencies
pnpm update -r
```

### .npmrc

```ini
# Hoist shared dependencies for compatibility
shamefully-hoist=true

# Strict peer dependency management
auto-install-peers=true
strict-peer-dependencies=true
```

## Shared Configurations

### TypeScript

```json
// packages/config-ts/base.json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "declaration": true
  }
}

// apps/web/tsconfig.json
{
  "extends": "@repo/config-ts/base.json",
  "compilerOptions": { "outDir": "dist", "rootDir": "src" },
  "include": ["src"]
}
```

## Build Optimization

### Remote Caching

```bash
# Turborepo + Vercel remote cache
npx turbo login
npx turbo link

# Now builds share cache across CI and all developers
# First build: 2 minutes. Cache hit: 0 seconds.
```

### Cache Configuration

```json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"],
      "inputs": ["src/**/*.tsx", "src/**/*.ts", "package.json"]
    }
  }
}
```

**Critical:** Define `inputs` precisely. If a build only depends on `src/`, don't let changes to `README.md` invalidate the cache.

## CI/CD

### GitHub Actions

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0    # Required for affected commands

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo run build test lint type-check
```

### Deploy Affected Only

```yaml
- name: Deploy affected apps
  run: |
    AFFECTED=$(pnpm turbo run build --dry-run=json --filter='[HEAD^1]' | jq -r '.packages[]')
    if echo "$AFFECTED" | grep -q "web"; then
      pnpm --filter web deploy
    fi
```

## Publishing Packages

```bash
# Setup Changesets
pnpm add -Dw @changesets/cli
pnpm changeset init

# Workflow
pnpm changeset          # Create changeset (describe what changed)
pnpm changeset version  # Bump versions based on changesets
pnpm changeset publish  # Publish to npm
```

```yaml
# .github/workflows/release.yml
- name: Create Release PR or Publish
  uses: changesets/action@v1
  with:
    publish: pnpm changeset publish
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Best Practices

1. **Lock dependency versions** — Use exact versions or lock files across the workspace
2. **Centralize configs** — ESLint, TypeScript, Prettier in shared packages
3. **Keep the graph acyclic** — No circular dependencies between packages
4. **Define cache inputs/outputs precisely** — Incorrect cache config wastes time or serves stale builds
5. **Share types between frontend/backend** — Single source of truth for contracts
6. **Unit tests in packages, E2E in apps** — Match test scope to package scope
7. **README in each package** — What it does, how to develop, how to use
8. **Use changesets for versioning** — Automated, reviewable release process

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Circular dependencies | Refactor shared code into a third package |
| Phantom dependencies (using deps not in package.json) | Use pnpm strict mode |
| Incorrect cache inputs | Add missing files to `inputs` array |
| Over-sharing code | Only share genuinely reusable code |
| Missing `fetch-depth: 0` in CI | Required for `affected` commands to compare history |
| Caching dev tasks | Set `cache: false` and `persistent: true` |

## NEVER Do

- **NEVER use `*` for workspace dependency versions** — Use `workspace:*` with pnpm
- **NEVER skip `--frozen-lockfile` in CI** — Ensures reproducible builds
- **NEVER cache dev server tasks** — They're long-running, not cacheable
- **NEVER create circular package dependencies** — Breaks build ordering
- **NEVER hoist without understanding** — `shamefully-hoist` is a compatibility escape hatch, not a default

## Related Skills

- **Related:** [service-layer-architecture](../service-layer-architecture/) — API patterns within monorepo apps
- **Related:** [postgres-job-queue](../postgres-job-queue/) — Background jobs for monorepo services
