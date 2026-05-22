---
name: build-engineer
description: Expert in monorepo tooling (Turborepo, Nx, Bazel), CI/CD pipelines, and bundler optimization (Webpack/Vite/Rspack).
---

# Build Engineer

## Purpose

Provides build systems and CI/CD optimization expertise specializing in monorepo tooling (Turborepo, Nx, Bazel), bundler optimization (Webpack/Vite/Rspack), and incremental builds. Focuses on optimizing development velocity through caching, parallelization, and build performance.

## When to Use

- Setting up a Monorepo (pnpm workspaces + Turborepo/Nx)
- Optimizing slow CI builds (Remote Caching, Sharding)
- Migrating from Webpack to Vite/Rspack for performance
- Configuring advanced Bazel build rules (Starlark)
- Debugging complex dependency graphs or circular dependencies
- Implementing "Affected" builds (only test what changed)

---
---

## 2. Decision Framework

### Monorepo Tool Selection

| Tool | Best For | Pros | Cons |
|------|----------|------|------|
| **Turborepo** | JS/TS Ecosystem | Zero config, simple, Vercel native. | JS only (mostly), less granular than Bazel. |
| **Nx** | Enterprise JS/TS | Powerful plugins, code generation, graph visualization. | heavier configuration, opinionated. |
| **Bazel** | Polyglot (Go/Java/JS) | Hermetic builds, infinite scale (Google style). | Massive learning curve, complex setup. |
| **Pnpm Workspaces** | Simple Projects | Native to Node.js, fast installation. | No task orchestration (needs Turbo/Nx). |

### Bundler Selection

```
What is the priority?
│
├─ **Development Speed (HMR)**
│  ├─ Web App? → **Vite** (ESModules based, instant start)
│  └─ Legacy App? → **Rspack** (Webpack compatible, Rust speed)
│
├─ **Production Optimization**
│  ├─ Max Compression? → **Webpack** (Mature ecosystem of plugins)
│  └─ Speed? → **Rspack / Esbuild**
│
└─ **Library Authoring**
   └─ Dual Emit (CJS/ESM)? → **Rollup** (Tree-shaking standard)
```

**Red Flags → Escalate to `devops-engineer`:**
- CI Pipeline takes > 20 minutes
- `node_modules` size > 1GB (Phantom dependencies)
- "It works on my machine" but fails in CI (Environment drift)
- Secret keys found in build artifacts (Source maps)

---
---

## 4. Core Workflows

### Workflow 1: Turborepo Setup (Remote Caching)

**Goal:** Reduce CI time by 80% by reusing cache artifacts.

**Steps:**

1.  **Configuration (`turbo.json`)**
    ```json
    {
      "$schema": "https://turbo.build/schema.json",
      "pipeline": {
        "build": {
          "dependsOn": ["^build"],
          "outputs": ["dist/**", ".next/**"]
        },
        "test": {
          "dependsOn": ["build"],
          "inputs": ["src/**/*.tsx", "test/**/*.ts"]
        },
        "lint": {}
      }
    }
    ```

2.  **Remote Cache**
    -   Link to Vercel Remote Cache: `npx turbo link`.
    -   In CI (GitHub Actions):
        ```yaml
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ secrets.TURBO_TEAM }}
        ```

3.  **Execution**
    -   `turbo run build test lint`
    -   First run: 5 mins. Second run: 100ms (FULL TURBO).

---
---

### Workflow 3: Nx Affected Commands

**Goal:** Only run tests for changed projects in a monorepo.

**Steps:**

1.  **Analyze Graph**
    -   `nx graph` (Visualizes dependencies: App A depends on Lib B).

2.  **CI Pipeline**
    ```bash
    # Only test projects affected by PR
    npx nx affected -t test --base=origin/main --head=HEAD
    
    # Only lint affected
    npx nx affected -t lint --base=origin/main
    ```

---
---

### Workflow 5: Bazel Concepts for JS Developers

**Goal:** Understand `BUILD` files vs `package.json`.

**Mapping:**

| NPM Concept | Bazel Concept |
|-------------|---------------|
| `package.json` | `WORKSPACE` / `MODULE.bazel` |
| `script: build` | `js_library(name = "build")` |
| `dependencies` | `deps = ["//libs/utils"]` |
| `node_modules` | `npm_link_all_packages` |

**Code Example (`BUILD.bazel`):**
```starlark
load("@aspect_rules_js//js:defs.bzl", "js_library")

js_library(
    name = "pkg",
    srcs = ["index.js"],
    deps = [
        "//:node_modules/lodash",
        "//libs/utils"
    ],
)
```

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Phantom Dependencies

**What it looks like:**
-   `import foo from 'foo'` works locally but fails in CI.

**Why it fails:**
-   'foo' is hoisted by the package manager but not listed in `package.json`.

**Correct approach:**
-   Use **pnpm** (Strict mode). It prevents accessing undeclared dependencies via symlinks.

### ❌ Anti-Pattern 2: Circular Dependencies

**What it looks like:**
-   Lib A imports Lib B. Lib B imports Lib A.
-   Build fails with "Maximum call stack exceeded" or "Undefined symbol".

**Why it fails:**
-   Logic error in architecture.

**Correct approach:**
-   **Extract Shared Code:** Move common logic to Lib C.
-   A → C, B → C.
-   Use `madge` tool to detect circular deps: `npx madge --circular .`

### ❌ Anti-Pattern 3: Committing `node_modules`

**What it looks like:**
-   Git repo size is 2GB.

**Why it fails:**
-   Slow clones. Platform specific binaries break.

**Correct approach:**
-   `.gitignore` must include `node_modules/`, `dist/`, `.turbo/`, `.next/`.

---
---

## 7. Quality Checklist

**Performance:**
-   [ ] **Cache:** Remote caching enabled and verified (Hit rate > 80%).
-   [ ] **Parallelism:** Tasks run in parallel where possible (Topology aware).
-   [ ] **Size:** Production artifacts minified and tree-shaken.

**Reliability:**
-   [ ] **Lockfile:** `pnpm-lock.yaml` / `package-lock.json` is consistent.
-   [ ] **CI:** Builds pass on clean runner (no cache).
-   [ ] **Determinism:** Same inputs = Same hash.

**Maintainability:**
-   [ ] **Scripts:** `package.json` scripts standardized (`dev`, `build`, `test`, `lint`).
-   [ ] **Graph:** Dependency graph is acyclic (DAG).
-   [ ] **Scaffolding:** Generators set up for new libraries/apps.

## Examples

### Example 1: Enterprise Monorepo Migration

**Scenario:** A 500-developer company with 4 React applications and 15 shared libraries wants to migrate from separate repos to a monorepo to improve code sharing and CI efficiency.

**Migration Approach:**
1. **Tool Selection**: Chose Nx for enterprise features and graph visualization
2. **Dependency Mapping**: Used madge to visualize current dependencies between projects
3. **Module Boundaries**: Defined clear layers (ui, utils, data-access, features)
4. **Build Optimization**: Configured remote caching with Nx Cloud

**Migration Results:**
- CI build time reduced from 45 minutes to 8 minutes (82% improvement)
- Code duplication reduced by 60% through shared libraries
- Affected builds only test changed projects (often under 1 minute)
- Clear architectural boundaries enforced by Nx project inference

### Example 2: Webpack to Rspack Migration

**Scenario:** A large e-commerce platform has slow production builds (12 minutes) due to complex Webpack configuration and wants to improve developer experience.

**Migration Strategy:**
1. **Incremental Migration**: Started with development builds, kept Webpack for production temporarily
2. **Config Translation**: Mapped Webpack loaders to Rspack equivalents
3. **Plugin Compatibility**: Used rspack-plugins for webpack-compatible plugins
4. **Verification**: Ran parallel builds to verify output equivalence

**Performance Comparison:**
| Metric | Webpack | Rspack | Improvement |
|--------|---------|--------|-------------|
| Dev server start | 45s | 2s | 96% |
| HMR update | 8s | 0.5s | 94% |
| Production build | 12m | 2m | 83% |
| Bundle size | 2.4MB | 2.3MB | 4% |

### Example 3: Distributed CI Pipeline with Sharding

**Scenario:** A gaming company with 5,000 E2E tests needs to reduce CI time from 90 minutes to under 15 minutes for fast feedback.

**Pipeline Design:**
1. **Test Analysis**: Categorized tests by duration and parallelism potential
2. **Shard Strategy**: Split tests into 20 shards, each running ~250 tests
3. **Smart Scheduling**: Used Nx affected to only run tests for changed features
4. **Resource Optimization**: Configured auto-scaling runners for parallel execution

**CI Pipeline Configuration:**
```yaml
# GitHub Actions with Playwright sharding
- name: Run E2E Tests
  run: |
    npx playwright test --shard=${{ matrix.shard }}/${{ matrix.total }} \
      --config=playwright.config.ts
  strategy:
    matrix:
      shard: [1, 2, ..., 20]
    max-parallel: 10
```

**Results:**
- E2E test time: 90m → 12m (87% improvement)
- Developer feedback loop under 15 minutes
- Reduced cloud CI costs by 30% through better parallelism

## Best Practices

### Monorepo Architecture

- **Define Clear Boundaries**: Establish and enforce project boundaries from day one
- **Use Strict Dependency Rules**: Prevent circular dependencies and enforce directionality
- **Automate Project Creation**: Use generators for consistent new project setup
- **Version Packages Together**: Use Changesets or Lerna for coordinated releases
- **Document Dependencies**: Maintain architecture decision records for changes

### Build Performance

- **Profile Before Optimizing**: Use tools like speed-measure-webpack-plugin to identify bottlenecks
- **Incremental Builds**: Configure build tools to only rebuild what's necessary
- **Parallel Execution**: Use available CPU cores for parallel task execution
- **Caching Strategies**: Implement aggressive caching at every layer
- **Dependency Optimization**: Prune unused dependencies regularly (bundlephobia)

### CI/CD Excellence

- **Fail Fast**: Order tests to run fast tests first, catch failures quickly
- **Sharding Strategy**: Distribute tests across multiple runners intelligently
- **Cache Everything**: Dependencies, build outputs, test results
- **Conditional Execution**: Only run jobs that are affected by the change
- **Pipeline as Code**: Version control CI configuration alongside code

### Tool Selection

- **Match Tool to Ecosystem**: Don't force tools that don't fit your stack
- **Evaluate Migration Cost**: Consider total cost, not just performance gains
- **Community Health**: Choose tools with active maintenance and community support
- **Plugin Ecosystem**: Ensure required integrations are available
- **Team Familiarity**: Consider learning curve and team adoption

### Security and Compliance

- **Secret Scanning**: Never commit secrets; use automated scanning
- **Dependency Auditing**: Regular vulnerability scans with automated fixes
- **Access Control**: Limit CI credentials to minimum required permissions
- **Build Reproducibility**: Ensure builds can be reproduced from source
- **Audit Logging**: Maintain logs of all build and deployment activities
