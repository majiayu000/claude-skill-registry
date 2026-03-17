---
name: monorepo-tools
description: Decision framework for monorepo build tools (Turborepo, Nx, Bazel). Use when choosing a monorepo tool, configuring build pipelines, or optimizing caching strategies.
---

# Monorepo Tools

## Decision Framework

| Factor | Turborepo | Nx | Bazel |
|--------|-----------|-----|-------|
| **Best for** | JS/TS monorepos, simple needs | JS/TS with architecture enforcement | Polyglot, large-scale |
| **Learning curve** | Low | Medium | High |
| **Caching** | File hash | File hash + computation | Content-addressable |
| **Remote cache** | Vercel (built-in) | Nx Cloud / S3 | gRPC remote execution |
| **Code generation** | None | Generators/executors | Rules/macros |
| **Architecture rules** | None | Module boundaries | Visibility rules |
| **Package manager** | npm/pnpm/yarn | npm/pnpm/yarn | Own dependency model |

### When to Choose Each

**Turborepo** (default choice for JS/TS):
- <50 packages
- Team already uses Vercel
- Need fast setup with minimal config
- No need for architecture enforcement
- `turbo.json` pipeline config is all you need

**Nx** (when you need guardrails):
- Need module boundary enforcement (`@nx/enforce-module-boundaries`)
- Want code generators for consistent project scaffolding
- Plugin ecosystem matters (React, Angular, Node have first-class support)
- Team is growing and you need architectural constraints

**Bazel** (when scale demands it):
- Polyglot codebase (JS + Python + Go + Java)
- >100 packages / >500 engineers
- Need hermetic, reproducible builds
- Need remote execution (distribute builds across machines)
- Willing to invest in build infrastructure team

### Migration Path
Turborepo -> Nx (when you need boundaries) -> Bazel (when Nx can't scale)

## Core Concepts

**Task graph**: DAG of build tasks. `^build` = build dependencies first. Tools traverse this for parallelism and caching.

**Caching**: Hash inputs (source files, env vars, configs) -> cache key -> store outputs. Cache hit = skip execution. All tools support local + remote cache.

**Affected detection**: Compare current state to base branch. Run only tasks for changed packages and their dependents. Critical for CI speed.

## Turborepo Key Opinions

### Pipeline Configuration
- Always specify `inputs` -- default hashes everything, including test files for build tasks
- Set `outputs` precisely -- `["dist/**"]` not `["dist"]`
- `env` must list all env vars that affect output -- missing one = stale cache
- `"dev": { "cache": false, "persistent": true }` -- dev servers are never cacheable

### Filtering
```bash
turbo build --filter='...[origin/main]'  # Changed since main (CI)
turbo build --filter=@myorg/web...       # Package + its dependencies
turbo build --filter='./apps/*'          # By directory
```

### Cache Debugging
```bash
turbo build --dry-run          # What would run
turbo build --summarize        # Cache hit/miss stats
turbo build --force            # Skip cache entirely
```

## Nx Key Opinions

### Library Types (enforce via tags)
| Type | Purpose | Can Depend On |
|------|---------|---------------|
| `type:app` | Deployable applications | feature, ui, data-access, util |
| `type:feature` | Smart components, business logic | ui, data-access, util |
| `type:ui` | Presentational components | ui, util |
| `type:data-access` | API calls, state | data-access, util |
| `type:util` | Pure functions | util |

This hierarchy prevents circular dependencies and enforces separation of concerns.

### Scope Tags
Add `scope:web`, `scope:api`, `scope:shared` to prevent cross-platform leaks.

## Shared Patterns

### TypeScript Config
- Single `tsconfig.base.json` at root with shared `compilerOptions`
- Per-project `tsconfig.json` extends base, adds `rootDir`/`outDir`
- Use `"moduleResolution": "bundler"` for modern projects

### Package Exports
```json
{
  "exports": {
    ".": { "import": "./dist/index.js", "types": "./dist/index.d.ts" },
    "./button": { "import": "./dist/button.js", "types": "./dist/button.d.ts" }
  }
}
```
- Always include `types` condition
- Use granular exports, not barrel files with everything

### Dependency Management (pnpm preferred)
- pnpm workspaces for JS/TS monorepos -- strict, fast, disk-efficient
- `pnpm add react --filter @repo/ui` -- add to specific package
- Use `catalog:` in pnpm-workspace.yaml to pin shared dependency versions

### Changesets for Publishing
- `@changesets/cli` for version management and npm publishing
- Changeset per PR -- enforced via CI check
- Auto-merge minor/patch updates, manual review for major
