---
name: nx-monorepo
description: |
  Nx monorepo management skill for AI-native development. This skill should be used when working with Nx workspaces, project graphs, affected detection, code generation, and caching. Use when: analyzing dependencies, running affected commands, generating code, configuring Nx Cloud, or optimizing build performance. Invoke nx-mcp tools for documentation queries.
version: "1.0.0"
---

# Nx Monorepo

## Overview

This skill provides expert-level capabilities for Nx monorepo management. Nx is the standard build orchestrator for this AI-native platform due to its official MCP server integration.

**Why Nx**: Official MCP server, TypeScript-native, 5-minute setup, auto-generates CLAUDE.md/AGENTS.md for AI assistants.

## MCP Tools Available

```
nx_docs          - Query Nx documentation
nx_available_plugins - List official Nx plugins (NOT installed by default)
```

**Key Insight**: MCP provides documentation lookup. Use **Nx CLI** for all operations.

## Core CLI Commands

### Project Graph Analysis

```bash
# View interactive project graph
nx graph

# JSON output for programmatic use
nx graph --file=output.json

# Show dependencies of specific project
nx graph --focus=my-app

# Show what depends on a project
nx graph --affected
```

### Affected Detection

```bash
# What's affected since main?
nx affected -t build
nx affected -t test
nx affected -t lint

# Compare against specific base
nx affected -t build --base=origin/main --head=HEAD

# Show affected projects only
nx show projects --affected
```

### Running Tasks

```bash
# Run task for all projects
nx run-many -t build
nx run-many -t test

# Run for specific projects
nx run-many -t build --projects=app-a,lib-b

# Run with parallelism control
nx run-many -t build --parallel=4

# Single project
nx build my-app
nx test my-lib
```

### Code Generation

```bash
# List available generators
nx list @nx/next
nx list @nx/react

# Generate new application
nx g @nx/next:app my-app
nx g @nx/react:app my-frontend

# Generate library
nx g @nx/js:lib shared-utils
nx g @nx/react:lib ui-components

# Dry run (preview)
nx g @nx/next:app my-app --dry-run
```

## Configuration Files

### nx.json (Workspace Config)

```json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "cache": true
    },
    "test": {
      "cache": true
    },
    "lint": {
      "cache": true
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*"],
    "production": ["default", "!{projectRoot}/**/*.spec.ts"]
  },
  "defaultBase": "main"
}
```

### project.json (Project Config)

```json
{
  "name": "my-app",
  "projectType": "application",
  "targets": {
    "build": {
      "executor": "@nx/next:build",
      "outputs": ["{options.outputPath}"],
      "options": {
        "outputPath": "dist/apps/my-app"
      }
    },
    "serve": {
      "executor": "@nx/next:server",
      "options": {
        "buildTarget": "my-app:build"
      }
    }
  }
}
```

## Caching

### Local Cache

```bash
# Cache is automatic for cacheable targets
nx build my-app  # First run: executes
nx build my-app  # Second run: cached (instant)

# Clear cache
nx reset
```

### Nx Cloud (Remote Cache)

```bash
# Connect to Nx Cloud
npx nx connect

# Or add manually
nx g @nx/workspace:ci-workflow

# Verify connection
nx run-many -t build
# Look for: "Remote cache hit"
```

### Cache Inputs

```json
// In project.json or nx.json
{
  "targets": {
    "build": {
      "inputs": [
        "default",
        "^production",
        { "externalDependencies": ["next"] }
      ]
    }
  }
}
```

## Common Patterns

### Adding a New JS/TS App

```bash
# 1. Add plugin (if not already installed)
pnpm nx add @nx/next    # For Next.js
pnpm nx add @nx/react   # For React
pnpm nx add @nx/node    # For Node/Express

# 2. Generate app
pnpm nx g @nx/next:app dashboard --directory=apps/dashboard

# 3. Verify in graph
pnpm nx graph --focus=dashboard

# 4. Build & Serve
pnpm nx build dashboard
pnpm nx serve dashboard
```

### Adding a Python App (uv Workspace)

Python projects use **uv workspaces** (similar to pnpm workspaces for JS) with manual `project.json` for Nx:

```bash
# 1. Create directory and initialize
mkdir -p apps/my-python-app
cd apps/my-python-app
uv init
uv add --group dev pytest ruff mypy
cd ../..

# 2. Add to uv workspace (root pyproject.toml)
```

Edit root `pyproject.toml`:
```toml
[tool.uv.workspace]
members = [
    "apps/panaversity-fs-py",
    "apps/my-python-app",  # Add new project here
]
```

```bash
# 3. Sync all Python deps from root
uv sync --extra dev
```

**apps/my-python-app/project.json** (for Nx):
```json
{
  "name": "my-python-app",
  "projectType": "application",
  "targets": {
    "build": {
      "command": "uv build",
      "options": { "cwd": "apps/my-python-app" }
    },
    "test": {
      "command": "uv run --extra dev pytest",
      "options": { "cwd": "apps/my-python-app" }
    },
    "lint": {
      "command": "uv run --extra dev ruff check .",
      "options": { "cwd": "apps/my-python-app" }
    }
  }
}
```

```bash
# 4. Verify Nx recognizes it
pnpm nx show projects
pnpm nx graph --focus=my-python-app

# 5. Run tasks via Nx
pnpm nx test my-python-app
```

### Shared Python Libraries

Create libraries that multiple Python apps can import:

```bash
mkdir -p libs/auth-common-py
cd libs/auth-common-py
uv init --lib
cd ../..
# Add to workspace members, then uv sync
```

Reference in dependent projects:
```toml
# apps/my-python-app/pyproject.toml
[project]
dependencies = ["auth-common-py"]

[tool.uv.sources]
auth-common-py = { workspace = true }
```

**Key Insight**: uv manages Python deps via workspace, Nx orchestrates tasks. Single `uv.lock` at root.

### Creating Shared Libraries

```bash
# JS/TS UI library
pnpm nx g @nx/react:lib ui --directory=libs/shared/ui

# JS/TS Utility library
pnpm nx g @nx/js:lib utils --directory=libs/shared/utils

# Domain library
pnpm nx g @nx/js:lib auth --directory=libs/domain/auth
```

### CI Pipeline (GitHub Actions)

```yaml
name: CI
on: [push, pull_request]

jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      # Affected-only builds
      - run: npx nx affected -t lint build test --base=origin/main
```

## Troubleshooting

### "Cannot find project"

```bash
# Regenerate project graph
nx reset
nx graph
```

### Cache Not Working

```bash
# Verify target is cacheable
cat nx.json | grep -A5 "targetDefaults"

# Check inputs are stable
nx build my-app --verbose
```

### Dependency Issues

```bash
# Show project dependencies
nx graph --focus=my-app

# Check for circular deps
nx graph --file=graph.json
# Review edges in JSON
```

## Quick Reference

| Task | Command |
|------|---------|
| Interactive graph | `pnpm nx graph` |
| Affected build | `pnpm nx affected -t build` |
| Run all tests | `pnpm nx run-many -t test` |
| Generate JS/TS app | `pnpm nx g @nx/next:app name` |
| Generate JS/TS lib | `pnpm nx g @nx/js:lib name` |
| Add plugin | `pnpm nx add @nx/next` |
| Clear cache | `pnpm nx reset` |
| Show projects | `pnpm nx show projects` |
| List generators | `pnpm nx list @nx/next` |

### Python-Specific (uv)

| Task | Command |
|------|---------|
| Init Python project | `cd apps/name && uv init` |
| Add runtime dep | `uv add <package>` |
| Add dev dep | `uv add --group dev <package>` |
| Sync deps | `uv sync --extra dev` |
| Run via Nx | `pnpm nx test my-python-app` |

## Related Skills

- **monorepo-workflow**: PR stacking, trunk-based development, code review
- **monorepo-team-lead**: CODEOWNERS, human-AI task routing, RFC process
