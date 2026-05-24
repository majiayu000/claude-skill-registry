---
name: npm-workspaces
# prettier-ignore
description: Use when managing npm workspaces monorepos - package dependencies, build ordering, cross-package development, and publishing workflows
---

# npm Workspaces

## Quick Start

```json
// Root package.json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["packages/*"],
  "scripts": {
    "build": "npm run build --workspaces",
    "test": "npm run test --workspaces"
  }
}
```

## Core Commands

| Command | Purpose |
|---------|---------|
| `npm install` | Install all workspace deps |
| `npm run build --workspaces` | Run in all workspaces |
| `npm run build -w pkg-name` | Run in specific workspace |
| `npm run build --if-present` | Skip if script missing |

## Cross-Package Dependencies

```json
// packages/compiler/package.json
{
  "name": "my-compiler",
  "dependencies": {
    "my-parser": "^1.0.0"  // Reference sibling package
  }
}
```

- Use semver (not `file:`) for publishable packages
- npm symlinks local packages automatically
- Build order matters: dependencies before dependents

## Build Ordering

```json
// Root package.json - explicit order
{
  "scripts": {
    "build": "npm run build -w my-parser && npm run build -w my-compiler && npm run build -w my-cli"
  }
}
```

Or use a tool like `wireit` or `turbo` for dependency-aware builds.

## Publishing

```bash
# Update versions (from root)
npm version patch -w my-parser
npm version patch -w my-compiler

# Publish all
npm publish --workspaces

# Publish specific
npm publish -w my-parser
```

## Tips

- Use `"private": true` in root to prevent accidental publish
- Run `npm ls` to verify dependency resolution
- Use `npm explain <pkg>` to debug why a package is installed
- Add `engines` field to enforce Node version
- Use `--include-workspace-root` to also run in root
