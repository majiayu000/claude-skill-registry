---
name: infra-monorepo-turborepo
description: Turborepo, workspaces, package architecture, @repo/* naming, exports, tree-shaking
---

# Monorepo Orchestration with Turborepo

> **Quick Guide:** Turborepo 2.7 with Bun for monorepo orchestration. Task pipelines with dependency ordering. Local + remote caching for massive speed gains. Workspaces for package linking. Syncpack for dependency version consistency. Internal packages use `@repo/*` naming, explicit `exports` fields, and `workspace:*` protocol.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define task dependencies using `dependsOn: ["^build"]` in turbo.json to ensure topological ordering)**

**(You MUST declare all environment variables in the `env` array of turbo.json tasks for proper cache invalidation)**

**(You MUST set `cache: false` for tasks with side effects like dev servers and code generation)**

**(You MUST use Bun workspaces protocol `workspace:*` for internal package dependencies)**

**(You MUST use `@repo/*` naming convention for ALL internal packages)**

**(You MUST define explicit `exports` field in package.json - never allow importing internal paths)**

**(You MUST mark React as `peerDependencies` NOT `dependencies` in component packages)**

</critical_requirements>

---

**Auto-detection:** Turborepo configuration, turbo.json, monorepo setup, workspaces, Bun workspaces, syncpack, task pipelines, @repo/\* packages, package.json exports, workspace dependencies, shared configurations

**When to use:**

- Configuring Turborepo task pipeline and caching strategies
- Setting up workspaces for monorepo package linking
- Enabling remote caching for team/CI cache sharing
- Synchronizing dependency versions across workspace packages
- Creating new internal packages in `packages/`
- Configuring package.json exports for tree-shaking
- Setting up shared configuration packages (@repo/eslint-config, @repo/typescript-config)

**When NOT to use:**

- Single application projects (use standard build tools directly)
- Projects without shared packages (no monorepo benefits)
- Very small projects where setup overhead exceeds caching benefits
- Polyrepo architecture is preferred over monorepo
- Projects already using Nx or Lerna (don't mix monorepo tools)
- App-specific code that won't be shared (keep in app directory)

**Key patterns covered:**

- Turborepo 2.7 task pipeline (dependsOn, outputs, inputs, cache)
- Local and remote caching strategies
- Bun workspaces for package linking
- Syncpack for dependency version consistency
- Environment variable handling in turbo.json
- Package structure and @repo/\* naming conventions
- package.json exports for tree-shaking
- Named exports and barrel file patterns
- Internal dependencies with workspace protocol

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md) (always start here)
  - [examples/caching.md](examples/caching.md) - Remote caching, CI/CD integration
  - [examples/workspaces.md](examples/workspaces.md) - Workspace protocol, syncpack, dependency boundaries
  - [examples/packages.md](examples/packages.md) - Internal package conventions, exports, creating packages
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Turborepo is a high-performance build system designed for JavaScript/TypeScript monorepos. It provides intelligent task scheduling, caching, and remote cache sharing to dramatically reduce build times. Combined with Bun workspaces, it enables efficient package management with automatic dependency linking.

**When to use Turborepo:**

- Managing monorepos with multiple apps and shared packages
- Teams need to share build cache across developers and CI
- Build times are slow and need optimization through caching
- Projects with complex task dependencies requiring topological ordering

**When NOT to use Turborepo:**

- Single application projects (use standard build tools)
- Projects without shared packages (no monorepo needed)
- Very small projects where setup overhead exceeds benefits
- Polyrepo architecture is preferred over monorepo

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Turborepo Task Pipeline with Dependency Ordering

Define task dependencies and caching behavior in turbo.json to enable intelligent build orchestration and caching.

#### Key Concepts

- `dependsOn: ["^build"]` - Run dependency tasks first (topological order)
- `outputs` - Define what files to cache
- `inputs` - Specify which files trigger cache invalidation
- `cache: false` - Disable caching for tasks with side effects
- `persistent: true` - Keep dev servers running

#### Configuration

```json
// Good Example - Proper task configuration with dependencies
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "env": ["DATABASE_URL", "NODE_ENV"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "test": {
      "dependsOn": ["^build"],
      "inputs": [
        "$TURBO_DEFAULT$",
        "src/**/*.tsx",
        "src/**/*.ts",
        "test/**/*.ts",
        "test/**/*.tsx"
      ]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "generate": {
      "dependsOn": ["^generate"],
      "cache": false
    },
    "lint": {}
  }
}
```

**Why good:** `dependsOn: ["^build"]` ensures topological task execution (dependencies build first), `env` array includes all environment variables for proper cache invalidation, `cache: false` prevents caching tasks with side effects (dev servers, code generation), `outputs` specifies cacheable artifacts while excluding cache directories

See [examples/core.md](examples/core.md) for good/bad comparison examples.

---

### Pattern 2: Caching Strategies

Turborepo's caching system dramatically speeds up builds by reusing previous task outputs when inputs haven't changed.

#### What Gets Cached

- Build outputs (`dist/`, `.next/`)
- Test results (when `cache: true`)
- Lint results

#### What Doesn't Get Cached

- Dev servers (`cache: false`)
- Code generation (`cache: false` - generates files)
- Tasks with side effects

#### Cache Invalidation Triggers

- Source file changes
- Dependency changes
- Environment variable changes (when in `env` array)
- Global dependencies changes (`.env`, `tsconfig.json`)

**Setup:** Link Vercel account, set `TURBO_TOKEN` and `TURBO_TEAM` environment variables to enable remote cache sharing.

See [examples/caching.md](examples/caching.md) for remote caching configuration and CI integration examples.

---

### Pattern 3: Bun Workspaces for Package Management

Configure Bun workspaces to enable package linking and dependency sharing across monorepo packages.

#### Workspace Configuration

```json
// Good Example - Properly configured workspaces
{
  "workspaces": ["apps/*", "packages/*"],
  "dependencies": {
    "@repo/ui": "workspace:*",
    "@repo/types": "workspace:*"
  }
}
```

**Why good:** `workspace:*` protocol links local packages automatically, glob patterns `apps/*` and `packages/*` discover all packages dynamically, Bun hoists common dependencies to root reducing duplication

#### Directory Structure

```
my-monorepo/
├── apps/
│   ├── client-next/      # Next.js app
│   ├── client-react/     # Vite React app
│   └── server/           # Backend server
├── packages/
│   ├── ui/               # Shared UI components
│   ├── api/              # API client
│   ├── eslint-config/    # Shared ESLint config
│   ├── prettier-config/  # Shared Prettier config
│   └── typescript-config/ # Shared TypeScript config
├── turbo.json            # Turborepo configuration
└── package.json          # Root package.json with workspaces
```

See [examples/workspaces.md](examples/workspaces.md) for workspace protocol good/bad comparison examples.

</patterns>

---

<performance>

## Performance Optimization

**Cache Hit Metrics:**

- First build: ~45s (5 packages, no cache)
- Cached build: ~1s (97% faster with local cache)
- Affected build: ~12s (73% faster, only changed packages rebuild)
- Team savings: Hours per week with remote cache enabled

**Optimization Strategies:**

- **Set `globalDependencies`** for files affecting all packages (`.env`, `tsconfig.json`) to prevent unnecessary cache invalidation
- **Use `inputs` array** to fine-tune what triggers cache invalidation for specific tasks
- **Enable remote caching** to share artifacts across team and CI
- **Use `--filter` with affected detection** (`--filter=...[HEAD^]`) to only run tasks for changed packages
- **Set `outputs` carefully** to exclude cache directories (e.g., `!.next/cache/**`)

**Force Cache Bypass:**

```bash
# Ignore cache when needed
bun run build --force

# Only build affected packages
bun run build --filter=...[HEAD^1]
```

</performance>

---

<decision_framework>

## Decision Framework

### When to Create a New Package

```
New code to write?
├─ Is it a deployable application? → apps/
├─ Is it shared across 2+ apps? → packages/
├─ Is it app-specific? → Keep in app directory
└─ Is it a build tool? → tools/
```

### When to Use Turborepo

```
Is this a monorepo with multiple packages/apps?
├─ NO → Use standard build tools
└─ YES → Do builds take > 30s or is caching important?
    ├─ YES → Use Turborepo
    └─ NO → Standard tools may suffice
```

For comprehensive decision trees and package creation criteria, see [reference.md](reference.md).

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing `dependsOn: ["^build"]` for build tasks (breaks topological ordering)
- Missing `env` array in turbo.json (causes cache misses across environments)
- Caching dev servers or code generation (incorrect outputs reused)
- Default exports in library packages (breaks tree-shaking)
- Missing `exports` field in package.json (allows internal path imports)

**Common Mistakes:**

- Hardcoded versions instead of `workspace:*` for internal deps
- React in `dependencies` instead of `peerDependencies`
- Giant barrel files re-exporting everything (negates tree-shaking)
- Running full test suite without `--filter=...[HEAD^]` affected detection

**Gotchas:**

- `dependsOn: ["^task"]` runs dependencies' tasks; `dependsOn: ["task"]` runs same package's task
- `--filter=...[HEAD^]` requires `fetch-depth: 2` in GitHub Actions
- Exclude cache directories in outputs: `!.next/cache/**`

For detailed anti-patterns and checklists, see [reference.md](reference.md).

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST define task dependencies using `dependsOn: ["^build"]` in turbo.json to ensure topological ordering)**

**(You MUST declare all environment variables in the `env` array of turbo.json tasks for proper cache invalidation)**

**(You MUST set `cache: false` for tasks with side effects like dev servers and code generation)**

**(You MUST use Bun workspaces protocol `workspace:*` for internal package dependencies)**

**(You MUST use `@repo/*` naming convention for ALL internal packages)**

**(You MUST define explicit `exports` field in package.json - never allow importing internal paths)**

**(You MUST mark React as `peerDependencies` NOT `dependencies` in component packages)**

**Failure to follow these rules will cause incorrect builds, cache misses, broken dependency resolution, and tree-shaking failures.**

</critical_reminders>
