---
name: Bun Package Manager
description: Bun package manager commands (install, add, remove, update), workspaces, lockfiles, npm/yarn/pnpm migration. Use for dependency management with Bun.
---

# Bun Package Manager

Bun's package manager is a dramatically faster replacement for npm, yarn, and pnpm. Up to **25x faster** than npm install.

## Quick Start

```bash
# Install all dependencies
bun install

# Add packages
bun add react react-dom
bun add -D typescript @types/react

# Remove packages
bun remove lodash

# Update packages
bun update

# Run package binaries
bunx create-next-app
```

## Core Commands

| Command | Description |
|---------|-------------|
| `bun install` | Install all dependencies |
| `bun add <pkg>` | Add dependency |
| `bun add -D <pkg>` | Add dev dependency |
| `bun add -O <pkg>` | Add optional dependency |
| `bun add --peer <pkg>` | Add peer dependency |
| `bun remove <pkg>` | Remove dependency |
| `bun update [pkg]` | Update dependencies |
| `bunx <pkg>` | Run package binary |
| `bun pm cache rm` | Clear cache |

## Installation Flags

```bash
# Production mode (no devDependencies)
bun install --production

# Frozen lockfile (CI/CD)
bun install --frozen-lockfile
bun ci  # shorthand

# Dry run
bun install --dry-run

# Verbose/Silent
bun install --verbose
bun install --silent

# Force reinstall
bun install --force

# Global packages
bun install -g cowsay
```

## Lockfile

Bun uses `bun.lock` (text-based since v1.2):

```bash
# Generate text lockfile
bun install --save-text-lockfile

# Upgrade from binary bun.lockb
bun install --save-text-lockfile --frozen-lockfile --lockfile-only
rm bun.lockb
```

## Workspaces (Monorepos)

```json
{
  "name": "my-monorepo",
  "workspaces": ["packages/*", "apps/*"]
}
```

Run commands across workspaces:

```bash
# Run in matching packages
bun run --filter 'pkg-*' build

# Run in all workspaces
bun run --filter '*' test

# Install for specific packages
bun install --filter 'pkg-a'
```

## Lifecycle Scripts

Bun does **not** run lifecycle scripts from dependencies by default (security). Whitelist trusted packages:

```json
{
  "trustedDependencies": ["my-trusted-package"]
}
```

```bash
# Skip all lifecycle scripts
bun install --ignore-scripts

# Concurrent scripts
bun install --concurrent-scripts 5
```

## Overrides & Resolutions

Force specific versions for nested dependencies:

```json
{
  "overrides": {
    "lodash": "4.17.21"
  }
}
```

Yarn-style resolutions also supported:

```json
{
  "resolutions": {
    "lodash": "4.17.21"
  }
}
```

## Non-npm Dependencies

```json
{
  "dependencies": {
    "dayjs": "git+https://github.com/iamkun/dayjs.git",
    "lodash": "git+ssh://github.com/lodash/lodash.git#4.17.21",
    "zod": "github:colinhacks/zod",
    "react": "https://registry.npmjs.org/react/-/react-18.2.0.tgz",
    "bun-types": "npm:@types/bun"
  }
}
```

## Installation Strategies

### Hoisted (default for single packages)

Traditional flat node_modules:

```bash
bun install --linker hoisted
```

### Isolated (default for workspaces)

pnpm-like strict isolation:

```bash
bun install --linker isolated
```

Isolated prevents "phantom dependencies" - packages can only access declared dependencies.

## CI/CD

```yaml
# GitHub Actions
- uses: oven-sh/setup-bun@v2
- run: bun ci  # frozen lockfile
```

## Platform-Specific

```bash
# Install for different platform
bun install --cpu=x64 --os=linux
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find module` | Missing dependency | Run `bun install` |
| `Lockfile mismatch` | package.json changed | Run `bun install` |
| `Peer dependency` | Missing peer | `bun add` the peer |
| `Lifecycle script failed` | Untrusted package | Add to `trustedDependencies` |

## Migration from Other Package Managers

### From pnpm

Bun automatically migrates `pnpm-lock.yaml`:

```bash
bun install  # Auto-converts to bun.lock
```

Workspace config moves to package.json:

```json
{
  "workspaces": {
    "packages": ["apps/*", "packages/*"],
    "catalog": {
      "react": "^18.0.0"
    }
  }
}
```

### From npm/Yarn

Simply run `bun install` - Bun reads `package-lock.json` and `yarn.lock`.

## When to Load References

Load `references/cli-commands.md` when:
- Need complete CLI flag reference
- Working with advanced options

Load `references/workspaces.md` when:
- Setting up monorepos
- Configuring workspace filters

Load `references/migration.md` when:
- Migrating from npm/yarn/pnpm
- Converting lockfiles
