---
name: package-management
description: Package management using pnpm and corepack with packageManager field in package.json. This skill should be used when installing dependencies, upgrading packages, troubleshooting package manager issues, or working with pnpm commands. Explicit triggers include "upgrade pnpm", "update pnpm", "pnpm version", "pnpm install", "pnpm add", "corepack", "package installation", "dependency updates", or "packageManager field".
---

# Package Management

## Overview

This project uses **pnpm** as the package manager, with **corepack** to manage pnpm versions automatically.

## Corepack Integration

### How It Works

- **pnpm version** is specified in `package.json` under the `packageManager` field
- **corepack** automatically uses the exact version specified
- No need to manually install pnpm - corepack handles it

### Example from package.json

```json
{
  "packageManager": "pnpm@9.1.0"
}
```

When you run `pnpm` commands, corepack ensures version 9.1.0 is used.

## Common Commands

### Installing Dependencies

```bash
pnpm install
```

This installs all dependencies from `package.json` using the version specified in the `packageManager` field.

### Adding New Dependencies

```bash
# Production dependency
pnpm add <package-name>

# Development dependency
pnpm add -D <package-name>
```

### Upgrading pnpm

To upgrade pnpm to the latest version:

```bash
corepack use pnpm@latest
```

This command:

1. Updates to the latest pnpm version
2. Automatically updates `package.json`'s `packageManager` field
3. Ensures the team uses the same version

### Upgrading to Specific pnpm Version

```bash
corepack use pnpm@9.5.0
```

## Troubleshooting

### Signature Verification Errors

If you encounter signature verification errors when running pnpm commands:

```bash
npm install -g corepack@latest
```

This updates corepack itself, which can resolve verification issues.

### pnpm Command Not Found

If `pnpm` is not recognized:

1. Enable corepack (if not already enabled):

   ```bash
   corepack enable
   ```

2. Install the project's pnpm version:
   ```bash
   corepack install
   ```

### Wrong pnpm Version

If the wrong pnpm version is being used:

1. Check the version specified in `package.json`:

   ```json
   {
     "packageManager": "pnpm@X.Y.Z"
   }
   ```

2. Ensure corepack is enabled:

   ```bash
   corepack enable
   ```

3. Re-run your command - corepack should download the correct version

## Best Practices

1. **Never install pnpm globally** - Let corepack manage it
2. **Use `corepack use pnpm@latest`** to upgrade, not manual installation
3. **Commit `package.json` changes** when upgrading pnpm (the `packageManager` field)
4. **Don't mix package managers** - Always use pnpm, never npm or yarn

## Why Corepack?

### Benefits

- **Version consistency** - Everyone uses the same pnpm version
- **No manual installation** - Corepack handles pnpm installation
- **Automatic switching** - Different projects can use different pnpm versions
- **Lockfile compatibility** - Ensures `pnpm-lock.yaml` is compatible

### How It's Different from Manual Installation

**With corepack (this project):**

```bash
# Just run pnpm - corepack handles the rest
pnpm install
```

**Without corepack:**

```bash
# Manual installation needed
npm install -g pnpm@9.1.0
pnpm install
```

## Integration with CI/CD

In CI/CD environments, ensure corepack is enabled:

```bash
# Enable corepack first
corepack enable

# Then run pnpm commands
pnpm install
pnpm build
```

Most modern CI environments (GitHub Actions, etc.) have corepack pre-installed.

## Common Workflows

### First-time Setup

```bash
# 1. Enable corepack (if needed)
corepack enable

# 2. Install dependencies
pnpm install

# 3. Start development
pnpm dev
```

### Upgrading All Dependencies

```bash
# Update all dependencies to latest versions
pnpm update --latest

# Or use interactive mode
pnpm update --interactive --latest
```

### Checking Outdated Packages

```bash
pnpm outdated
```

### Deduplicate Dependencies

```bash
pnpm dedupe
```

This removes duplicate packages from `pnpm-lock.yaml`, reducing installation size.

## Key Reminders

- ✅ Use `corepack use pnpm@latest` to upgrade pnpm
- ✅ Commit `package.json` changes when pnpm version changes
- ✅ Enable corepack before using pnpm
- ❌ Don't install pnpm globally with npm
- ❌ Don't manually edit the `packageManager` field
