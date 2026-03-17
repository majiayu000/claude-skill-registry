---
name: pnpm
description: pnpm fast package manager with content-addressable storage. Use for efficient installs.
---

# pnpm

pnpm is fast and disk-efficient. It uses a **Content Addressable Store** and hard links to avoid duplicating packages. v9 (2025) adds Catalogs.

## When to Use

- **Disk Space**: Saves GBs by storing one copy of `lodash` globally.
- **Speed**: Installation is instant if packages are already in the store.
- **Monorepos**: Excellent workspace support with strict isolation.

## Quick Start

```bash
# Enable via Corepack
corepack enable
corepack prepare pnpm@latest --activate

pnpm add next
```

## Core Concepts

### Content Addressable Store

`~/.local/share/pnpm/store`. All packages live here. Projects assume `node_modules` structure via symlinks.

### Strict Resolution

Unlike npm/yarn (classic), pnpm does not flatten node_modules. You cannot access `dependency-of-dependency` unless you declare it.

### Catalogs (v9)

Define version groups in `pnpm-workspace.yaml`. e.g. `catalog:react-18` ensures all packages use exact same versions.

## Best Practices (2025)

**Do**:

- **Use CI Caching**: pnpm is fast, but setup `pnpm-store` caching in GitHub Actions to make it instant.
- **Use `pnpm -r`**: Run commands recursively across the monorepo.
- **Use `only-allow`**: Add `preinstall` script to force team to use pnpm.

**Don't**:

- **Don't shame hoist**: If legacy tools break with symlinks, use `shamefully-hoist=true` in `.npmrc` as a temporary fix.

## References

- [pnpm Documentation](https://pnpm.io/)
