---
name: nx-monorepo
description: Provides comprehensive Nx monorepo management guidance for TypeScript/JavaScript projects. Use when creating Nx workspaces, generating apps/libraries/components, running affected commands, setting up CI/CD, configuring Module Federation, or implementing NestJS backends within Nx
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Nx Monorepo

## Overview

Provides comprehensive guidance for working with Nx monorepos in TypeScript/JavaScript projects. Nx is a smart build system with advanced caching, affected command execution, and powerful generators for React, Next.js, NestJS, and more. This skill covers workspace creation, project generation, task execution, caching strategies, Module Federation, and CI/CD integration.

## When to Use

Use this skill when:
- Creating a new Nx workspace or initializing Nx in an existing project
- Generating applications, libraries, or components with Nx generators
- Running affected commands or executing tasks across multiple projects
- Setting up CI/CD pipelines for Nx projects (GitHub Actions, CircleCI, etc.)
- Configuring Module Federation with React or Next.js
- Implementing NestJS backend applications within Nx
- Managing TypeScript package libraries with buildable and publishable libs
- Setting up remote caching or Nx Cloud
- Optimizing monorepo build times and caching strategies
- Debugging dependency graph issues or circular dependencies

**Trigger phrases:** "create Nx workspace", "Nx monorepo", "generate Nx app", "Nx affected", "Nx CI/CD", "Module Federation Nx", "Nx Cloud"

## Instructions

### Workspace Creation

1. **Create a new workspace with interactive setup:**
   ```bash
   npx create-nx-workspace@latest
   ```
   Follow prompts to select preset (Integrated, Standalone, Package-based) and framework stack.

2. **Initialize Nx in an existing project:**
   ```bash
   nx@latest init
   ```

3. **Create with specific preset (non-interactive):**
   ```bash
   npx create-nx-workspace@latest my-workspace --preset=react
   ```

### Project Generation

1. **Generate a React application:**
   ```bash
   nx g @nx/react:app my-app
   ```

2. **Generate a library:**
   ```bash
   # React library
   nx g @nx/react:lib my-lib

   # TypeScript library
   nx g @nx/js:lib my-util
   ```

3. **Generate a component in lib:**
   ```bash
   nx g @nx/react:component my-comp --project=my-lib
   ```

4. **Generate NestJS backend:**
   ```bash
   nx g @nx/nest:app my-api
   ```

### Task Execution

1. **Run tasks for affected projects only:**
   ```bash
   nx affected -t lint test build
   ```

2. **Run tasks across all projects:**
   ```bash
   # Build all projects
   nx run-many -t build

   # Test specific projects
   nx run-many -t test -p=my-app,my-lib

   # Test by pattern
   nx run-many -t test --projects=*-app
   ```

3. **Run specific target on single project:**
   ```bash
   nx run my-app:build
   ```

4. **Visualize dependency graph:**
   ```bash
   nx graph
   ```

### Project Configuration

Each project has a `project.json` defining targets, executor, and configurations:

```json
{
  "name": "my-app",
  "projectType": "application",
  "sourceRoot": "apps/my-app/src",
  "targets": {
    "build": {
      "executor": "@nx/react:webpack",
      "outputs": ["{workspaceRoot}/dist/apps/my-app"],
      "configurations": {
        "production": {
          "optimization": true
        }
      }
    },
    "test": {
      "executor": "@nx/vite:test"
    }
  },
  "tags": ["type:app", "scope:frontend"]
}
```

### Dependency Management

1. **Set up project dependencies:**
   ```json
   {
     "targets": {
       "build": {
         "dependsOn": [
           { "projects": ["shared-ui"], "target": "build" }
         ]
       }
     }
   }
   ```

2. **Use tags for organization:**
   ```json
   { "tags": ["type:ui", "scope:frontend", "platform:web"] }
   ```

### Module Federation (Nx 17+)

1. **Generate a remote (micro-frontend):**
   ```bash
   nx g @nx/react:remote checkout --host=dashboard
   ```

2. **Generate a host:**
   ```bash
   nx g @nx/react:host dashboard
   ```

### CI/CD Setup

Use affected commands in CI to only build/test changed projects:

```yaml
# .github/workflows/ci.yml
- run: npx nx affected -t lint --parallel
- run: npx nx affected -t test --parallel
- run: npx nx affected -t build --parallel
```

## Examples

### Example 1: Create New React Workspace

**Input:** "Create a new Nx workspace with React and TypeScript"

**Steps:**
```bash
npx create-nx-workspace@latest my-workspace
# Select: Integrated Monorepo → React → Integrated monorepo (Nx Cloud)
```

**Expected Result:** Workspace created with:
- `apps/` directory with React app
- `libs/` directory for shared libraries
- `nx.json` with cache configuration
- CI/CD workflow files ready

### Example 2: Run Tests for Changed Projects

**Input:** "Run tests only for projects affected by recent changes"

**Command:**
```bash
nx affected -t test --base=main~1 --head=main
```

**Expected Result:** Only tests for projects affected by changes between commits are executed, leveraging cached results from previous runs.

### Example 3: Generate and Build a Shared Library

**Input:** "Create a shared UI library and use it in the app"

**Steps:**
```bash
# Generate library
nx g @nx/react:lib shared-ui

# Generate component in library
nx g @nx/react:component button --project=shared-ui

# Import in app (tsconfig paths auto-configured)
import { Button } from '@my-workspace/shared-ui'
```

**Expected Result:** Buildable library at `libs/shared-ui` with proper TypeScript path mapping configured.

### Example 4: Set Up Module Federation

**Input:** "Configure Module Federation for micro-frontends"

**Steps:**
```bash
# Create host app
nx g @nx/react:host dashboard

# Add remote to host
nx g @nx/react:remote product-catalog --host=dashboard

# Start dev servers
nx run dashboard:serve
nx run product-catalog:serve
```

**Expected Result:** Two separate applications running where product-catalog loads dynamically into dashboard at runtime.

### Example 5: Debug Build Dependencies

**Input:** "Why is my app rebuilding when unrelated lib changes?"

**Diagnosis:**
```bash
# Show project graph
nx graph --focused=my-app

# Check implicit dependencies
nx show project my-app --json | grep implicitDependencies
```

**Solution:** Add explicit dependency configuration or use `namedInputs` in `nx.json` to exclude certain files from triggering builds.

## Best Practices

- **Always use `nx affected` in CI** to only test/build changed projects
- **Organize libs by domain/business capability**, not by technical layer
- **Use tags consistently** (`type:app|lib`, `scope:frontend|backend|shared`)
- **Prevent circular dependencies** by configuring `workspaceLayout` boundaries in `nx.json`
- **Enable remote caching** with Nx Cloud for team productivity
- **Keep project.json simple** - use defaults from `nx.json` when possible
- **Leverage generators** instead of manual file creation for consistency
- **Configure `namedInputs`** to exclude test files from production cache keys
- **Use Module Federation** for independent deployment of micro-frontends
- **Keep workspace generators** in `tools/` for project-specific scaffolding

## Constraints and Warnings

- **Node.js 18.10+** is required for Nx 17+
- **Windows users**: Use WSL or Git Bash for best experience
- **First-time setup** may take longer due to package installation
- **Large monorepos** (50+ projects) should use distributed task execution
- **Module Federation** requires webpack 5+ and specific Nx configuration
- **Some generators** require additional plugins to be installed first
- **Cache location**: Default `~/.nx/cache` can grow large; configure `cacheDirectory` in `nx.json` if needed
- **Circular dependencies** will cause build failures; use `nx graph` to visualize
- **Preset migration**: Converting between Integrated/Standalone/Package-based requires manual effort

## Reference Files

For detailed guidance on specific topics, consult:

| Topic | Reference File |
|-------|----------------|
| Workspace setup, basic commands | [references/basics.md](references/basics.md) |
| Generators (app, lib, component) | [references/generators.md](references/generators.md) |
| React, Next.js, Expo patterns | [references/react.md](references/react.md) |
| NestJS backend patterns | [references/nestjs.md](references/nestjs.md) |
| TypeScript packages | [references/typescript.md](references/typescript.md) |
| CI/CD (GitHub, CircleCI, etc.) | [references/ci-cd.md](references/ci-cd.md) |
| Caching, affected, advanced | [references/advanced.md](references/advanced.md) |
