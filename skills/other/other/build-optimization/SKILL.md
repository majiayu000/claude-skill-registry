---
name: build-optimization
description: Build system optimization covering compilation, caching, incremental builds, and developer tooling. Use when improving build times, configuring CI pipelines, or designing developer tools.
---

# Build Optimization

Expert guidance for optimizing build systems, reducing compilation times, maximizing cache hit rates, and building developer tools that enhance productivity across the development lifecycle.

## When to Use This Skill

- Diagnosing slow build times and identifying bottlenecks
- Configuring caching strategies (local, remote, distributed)
- Setting up incremental builds and parallel execution
- Optimizing CI/CD pipeline performance and cost
- Designing or improving bundle splitting and tree shaking
- Building CLIs, plugins, code generators, or IDE extensions
- Configuring monorepo tooling (Nx, Turborepo, Bazel)
- Reducing developer feedback loop times (hot reload, watch mode)
- Managing build artifacts and reproducibility

## Quick Reference

| Task | Load reference |
| --- | --- |
| Compilation, caching, incremental builds, CI/CD optimization | `skills/build-optimization/references/build-systems.md` |
| Plugin systems, code generation, linting, IDE integration, monorepo tooling | `skills/build-optimization/references/developer-tooling.md` |

## Core Targets

- Build time under 30 seconds for development builds
- Rebuild time under 5 seconds with watch mode
- Cache hit rate above 90% in CI
- Zero flaky builds in production pipelines
- Reproducible builds across environments

## Workflow

### 1. Performance Analysis

Profile the current build before making changes.

- Measure cold build, incremental rebuild, and hot reload times
- Profile CPU, memory, and I/O during builds
- Map the dependency graph and identify bottlenecks
- Evaluate cache hit rates and invalidation patterns
- Review current tool configuration for missed optimizations

### 2. Optimization

Apply targeted improvements based on profiling data.

- Enable incremental compilation and caching
- Configure parallel execution across available cores
- Set up code splitting and tree shaking
- Optimize module resolution and source transformation
- Implement remote or distributed caching for CI

### 3. Tooling

Build or configure developer tools for fast feedback loops.

- Configure watch mode and hot module replacement
- Set up clear error messages and progress indicators
- Integrate build analytics and performance dashboards
- Add pre-commit hooks for format, lint, and validation

### 4. Monitoring

Track build health over time.

- Set up automated build time tracking and alerting
- Monitor cache hit rates and bundle size trends
- Detect performance regressions in CI
- Review and optimize periodically based on data

## Common Mistakes

- Optimizing without profiling first
- Disabling caching due to intermittent issues instead of fixing invalidation
- Running full builds when incremental builds would suffice
- Not parallelizing independent build tasks
- Ignoring I/O as a bottleneck (disk speed, network latency)
- Letting bundle sizes grow unchecked without analysis
- Using a single build configuration for development and production
