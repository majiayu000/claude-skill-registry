---
name: yarn
description: Yarn package manager with workspaces. Use for JavaScript dependencies.
---

# Yarn

Yarn (Berry) is a modern package manager. It introduced Plug'n'Play (PnP) to eliminate `node_modules` and support **Zero Installs**.

## When to Use

- **Monorepos**: Yarn Workspaces are robust and feature-rich (Constraints, plugins).
- **Speed**: PnP is faster than node_modules linking.
- **Correctness**: Strict phantom dependency checks prevent requiring packages you didn't list.

## Quick Start

```bash
corepack enable
yarn set version stable
yarn init -2

# Install
yarn add react
```

## Core Concepts

### Plug'n'Play (PnP)

Instead of copying files to `node_modules`, Yarn generates a `.pnp.cjs` map. Node requires are intercepted and resolved directly from the cache.

### Zero Installs

Commit the `.yarn/cache` folder. Cloning the repo = Installation complete. No `yarn install` needed in CI.

### Constraints

Enforce rules across workspaces (e.g., "All packages must use React 18").

## Best Practices (2025)

**Do**:

- **Use Corepack**: Manage Yarn versions via Node's `corepack` tool.
- **Use `yarn dlx`**: Equivalent to `npx`.
- **Commit Cache**: If using Zero Installs, do commit the binary cache.

**Don't**:

- **Don't use Yarn 1**: Legacy Yarn (v1) is dead. Migrate to Berry (v4+).

## References

- [Yarn Documentation](https://yarnpkg.com/)
