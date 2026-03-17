---
name: turborepo-monorepo
description: Provides comprehensive Turborepo monorepo management guidance for TypeScript/JavaScript projects. Use when creating Turborepo workspaces, configuring turbo.json tasks, setting up Next.js/NestJS apps, managing test pipelines (Vitest/Jest), configuring CI/CD, implementing remote caching, or optimizing build performance in monorepos
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Turborepo Monorepo

## Overview

Provides comprehensive guidance for working with Turborepo monorepos in TypeScript/JavaScript projects. Turborepo is a high-performance build system written in Rust that optimizes task execution through intelligent caching, parallelization, and dependency graph analysis. This skill covers workspace creation, task configuration, framework integration (Next.js, NestJS, Vite), testing setup, CI/CD pipelines, and performance optimization.

## When to Use

Use this skill when:
- Creating a new Turborepo workspace or initializing in an existing project
- Configuring `turbo.json` tasks with proper dependencies and outputs
- Setting up Next.js or NestJS applications in a monorepo
- Configuring Vitest or Jest testing pipelines
- Implementing CI/CD workflows (GitHub Actions, CircleCI, GitLab CI)
- Setting up remote caching or Vercel Remote Cache
- Optimizing build times and cache hit ratios
- Managing package configurations for specific apps/libs
- Debugging task dependency issues
- Migrating from other monorepo tools to Turborepo

**Trigger phrases:** "create Turborepo workspace", "Turborepo monorepo", "turbo.json config", "Turborepo Next.js", "Turborepo NestJS", "Turborepo CI/CD", "Vitest Turborepo"

## Instructions

### Workspace Creation

1. **Create a new workspace:**
   ```bash
   # Using pnpm (recommended)
   pnpm create turbo@latest my-workspace

   # Using npm
   npm create turbo@latest my-workspace

   # Using yarn
   yarn create turbo my-workspace
   ```

2. **Initialize in an existing project:**
   ```bash
   pnpm add -D -w turbo
   ```

3. **Create turbo.json in root:**
   ```json
   {
     "$schema": "https://turborepo.dev/schema.json",
     "pipeline": {
       "build": {
         "dependsOn": ["^build"],
         "outputs": ["dist/**", ".next/**"]
       },
       "lint": {
         "outputs": []
       },
       "test": {
         "dependsOn": ["build"],
         "outputs": ["coverage/**"]
       }
     }
   }
   ```

4. **Add scripts to root package.json:**
   ```json
   {
     "scripts": {
       "build": "turbo run build",
       "dev": "turbo run dev",
       "lint": "turbo run lint",
       "test": "turbo run test",
       "clean": "turbo run clean"
     }
   }
   ```

### Task Configuration

1. **Configure task dependencies:**
   ```json
   {
     "pipeline": {
       "build": {
         "dependsOn": ["^build"],
         "outputs": ["dist/**"]
       },
       "test": {
         "dependsOn": ["build"],
         "outputs": ["coverage/**"]
       },
       "lint": {
         "outputs": []
       }
     }
   }
   ```

2. **Run tasks across packages:**
   ```bash
   # Run task for all packages
   turbo run build

   # Run multiple tasks
   turbo run lint test build

   # Run for specific package
   turbo run build --filter=web
   ```

3. **Use transit nodes for parallel type checking:**
   ```json
   {
     "pipeline": {
       "transit": {
         "dependsOn": ["^transit"]
       },
       "typecheck": {
         "dependsOn": ["transit"],
         "outputs": []
       }
     }
   }
   ```

### Framework Integration

1. **Next.js app configuration:**
   ```json
   {
     "pipeline": {
       "build": {
         "dependsOn": ["^build"],
         "outputs": [".next/**", "!.next/cache/**"],
         "env": ["NEXT_PUBLIC_*"]
       }
     }
   }
   ```
   See [references/nextjs-config.md](references/nextjs-config.md) for complete Next.js setup.

2. **NestJS API configuration:**
   ```json
   {
     "pipeline": {
       "build": {
         "dependsOn": ["^build"],
         "outputs": ["dist/**"]
       },
       "start:dev": {
         "cache": false,
         "persistent": true
       }
     }
   }
   ```
   See [references/nestjs-config.md](references/nestjs-config.md) for complete NestJS setup.

### Testing Setup

1. **Vitest configuration:**
   ```json
   {
     "pipeline": {
       "test": {
         "outputs": [],
         "inputs": ["$TURBO_DEFAULT$", "vitest.config.ts"]
       },
       "test:watch": {
         "cache": false,
         "persistent": true
       }
     }
   }
   ```

2. **Run affected tests:**
   ```bash
   turbo run test --filter=[HEAD^]
   ```
   See [references/testing-config.md](references/testing-config.md) for complete testing setup.

### Package Configurations

1. **Create package-specific turbo.json:**
   ```json
   {
     "extends": ["//"],
     "tasks": {
       "build": {
         "outputs": ["$TURBO_EXTENDS$", ".next/**"]
       }
     }
   }
   ```
   See [references/package-configs.md](references/package-configs.md) for detailed package configuration patterns.

### CI/CD Setup

1. **GitHub Actions basic workflow:**
   ```yaml
   - name: Install dependencies
     run: pnpm install

   - name: Run tests
     run: pnpm run test --filter=[HEAD^]

   - name: Build
     run: pnpm run build --filter=[HEAD^]
   ```

2. **Remote cache setup:**
   ```bash
   # Login to Vercel
   npx turbo login

   # Link repository
   npx turbo link
   ```
   See [references/ci-cd.md](references/ci-cd.md) for complete CI/CD setup examples.

## Task Properties Reference

| Property | Description | Example |
|----------|-------------|---------|
| `dependsOn` | Tasks that must complete first | `["^build"]` - dependencies first |
| `outputs` | Files/folders to cache | `["dist/**"]` |
| `inputs` | Files for cache hash | `["src/**/*.ts"]` |
| `env` | Environment variables affecting hash | `["DATABASE_URL"]` |
| `cache` | Enable/disable caching | `true` or `false` |
| `persistent` | Long-running task | `true` for dev servers |
| `outputLogs` | Log verbosity | `"full"`, `"new-only"`, `"errors-only"` |

### Dependency Patterns

- `^task` - Run task in dependencies first (topological order)
- `task` - Run task in same package first
- `package#task` - Run specific package's task

### Filter Syntax

| Filter | Description |
|--------|-------------|
| `web` | Only web package |
| `web...` | web + all dependencies |
| `...web` | web + all dependents |
| `...web...` | web + deps + dependents |
| `[HEAD^]` | Packages changed since last commit |
| `./apps/*` | All packages in apps/ |

## Best Practices

### Performance Optimization

1. **Use specific outputs** - Only cache what's needed
2. **Fine-tune inputs** - Exclude files that don't affect output
3. **Transit nodes** - Enable parallel type checking
4. **Remote cache** - Share cache across team/CI
5. **Package configurations** - Customize per-package behavior

### Caching Strategy

```json
{
  "pipeline": {
    "build": {
      "outputs": ["dist/**"],
      "inputs": ["$TURBO_DEFAULT$", "!README.md", "!**/*.md"]
    }
  }
}
```

### Task Organization

- **Independent tasks** - No `dependsOn`: lint, format, spellcheck
- **Build tasks** - `dependsOn: ["^build"]`: build, compile
- **Test tasks** - `dependsOn: ["build"]`: test, e2e
- **Dev tasks** - `cache: false, persistent: true`: dev, watch

### Workspace Structure

```
my-workspace/
├── apps/
│   ├── web/           # Next.js app
│   └── api/           # NestJS backend
├── packages/
│   ├── ui/            # React component library
│   └── config/        # Shared configs
├── turbo.json
├── package.json
└── pnpm-workspace.yaml
```

## Common Issues

### Tasks not running in order

**Problem:** Tasks execute in wrong order

**Solution:** Check `dependsOn` configuration

```json
{
  "build": {
    "dependsOn": ["^build"]
  }
}
```

### Cache misses on unchanged files

**Problem:** Cache invalidating unexpectedly

**Solution:** Review `globalDependencies` and `inputs`

```json
{
  "globalDependencies": ["tsconfig.json"],
  "pipeline": {
    "build": {
      "inputs": ["$TURBO_DEFAULT$", "!*.md"]
    }
  }
}
```

### Type errors after cache hit

**Problem:** TypeScript errors not caught due to cache

**Solution:** Use transit nodes for type checking

```json
{
  "transit": { "dependsOn": ["^transit"] },
  "typecheck": { "dependsOn": ["transit"] }
}
```

## Examples

### Example 1: Create New Workspace

**Input:** "Create a Turborepo with Next.js and NestJS"

```bash
pnpm create turbo@latest my-workspace
cd my-workspace

# Add Next.js app
pnpm add next react react-dom -F apps/web

# Add NestJS API
pnpm add @nestjs/core @nestjs/common -F apps/api
```

### Example 2: Configure Testing Pipeline

**Input:** "Set up Vitest for all packages"

```json
{
  "pipeline": {
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "inputs": ["$TURBO_DEFAULT$", "vitest.config.ts"]
    },
    "test:watch": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Example 3: Run Affected Tests in CI

**Input:** "Only test changed packages in CI"

```bash
pnpm run test --filter=[HEAD^]
```

### Example 4: Debug Cache Issues

**Input:** "Why is my cache missing?"

```bash
# Dry run to see what would be executed
turbo run build --dry-run --filter=web

# Show hash inputs
turbo run build --force --filter=web
```

## Constraints and Warnings

- **Node.js 18+** is required for Turborepo
- **Package manager field** required in root `package.json`
- **Outputs must be specified** for caching to work
- **Persistent tasks** cannot have dependents
- **Windows**: WSL or Git Bash recommended
- **Remote cache** requires Vercel account or self-hosted solution
- **Large monorepos** may need increased `concurrency` settings

## Reference Files

For detailed guidance on specific topics, consult:

| Topic | Reference File |
|-------|----------------|
| turbo.json template | [references/turbo.json](references/turbo.json) |
| Next.js integration | [references/nextjs-config.md](references/nextjs-config.md) |
| NestJS integration | [references/nestjs-config.md](references/nestjs-config.md) |
| Vitest/Jest/Playwright | [references/testing-config.md](references/testing-config.md) |
| GitHub/CircleCI/GitLab CI | [references/ci-cd.md](references/ci-cd.md) |
| Package configurations | [references/package-configs.md](references/package-configs.md) |
