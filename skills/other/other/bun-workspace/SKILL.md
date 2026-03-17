---
name: bun-workspace
description: >-
  Manage Bun monorepo workspaces and dependencies in the FTC Metrics project.
  Use when adding dependencies, running package scripts, troubleshooting
  workspace resolution, or managing cross-package imports.
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: tools
---

# Bun Workspace Management

FTC Metrics uses Bun as the JavaScript runtime and package manager with a monorepo workspace structure.

## Project Structure

```
ftcmetrics-v2/
├── package.json              # Root workspace config
├── bun.lock                  # Lockfile (committed)
├── .nvmrc                    # Node version: 22
├── packages/
│   ├── web/                  # @ftcmetrics/web - Next.js frontend
│   │   └── package.json
│   ├── api/                  # @ftcmetrics/api - Hono API server
│   │   └── package.json
│   ├── db/                   # @ftcmetrics/db - Prisma database layer
│   │   └── package.json
│   └── shared/               # @ftcmetrics/shared - Shared types/utils
│       └── package.json
```

## Workspace Configuration

### Root package.json

```json
{
  "name": "ftcmetrics-v2",
  "private": true,
  "workspaces": ["packages/*"],
  "scripts": {
    "dev": "bun run --filter '*' dev",
    "dev:web": "bun run --filter @ftcmetrics/web dev",
    "dev:api": "bun run --filter @ftcmetrics/api dev",
    "build": "bun run --filter '*' build",
    "lint": "bun run --filter '*' lint",
    "typecheck": "bun run --filter '*' typecheck",
    "db:generate": "bun run --filter @ftcmetrics/db generate",
    "db:push": "bun run --filter @ftcmetrics/db push",
    "db:migrate": "bun run --filter @ftcmetrics/db migrate",
    "db:studio": "bun run --filter @ftcmetrics/db studio"
  },
  "engines": {
    "node": ">=22"
  }
}
```

### Package Names

| Package | Name | Purpose |
|---------|------|---------|
| web | @ftcmetrics/web | Next.js frontend (React 19) |
| api | @ftcmetrics/api | Hono REST API server |
| db | @ftcmetrics/db | Prisma client and database |
| shared | @ftcmetrics/shared | Shared TypeScript types |

## Common Commands

### Development

```bash
# Run all packages in dev mode
bun run dev

# Run specific package
bun run dev:web          # Next.js on http://localhost:3000
bun run dev:api          # Hono API with --watch

# Run script in specific package (alternative)
bun run --filter @ftcmetrics/web dev
bun run --filter @ftcmetrics/api dev
```

### Building

```bash
# Build all packages
bun run build

# Build specific package
bun run --filter @ftcmetrics/web build
bun run --filter @ftcmetrics/api build
```

### Type Checking

```bash
# Typecheck all packages
bun run typecheck

# Typecheck specific package
bun run --filter @ftcmetrics/web typecheck
```

### Database Commands

```bash
# Generate Prisma client
bun run db:generate

# Push schema to database
bun run db:push

# Create migration
bun run db:migrate

# Open Prisma Studio
bun run db:studio
```

## Adding Dependencies

### To a Specific Package

```bash
# Add to packages/web
bun add <package> --filter @ftcmetrics/web

# Add dev dependency to packages/api
bun add -d <package> --filter @ftcmetrics/api

# Example: Add zod to the api package
bun add zod --filter @ftcmetrics/api
```

### To Root (Shared Across All)

```bash
# Add shared dev dependency at root
bun add -d typescript

# Only use root for truly shared tooling
```

### Workspace Dependencies

Internal packages use `workspace:*` protocol for cross-package dependencies:

```json
{
  "dependencies": {
    "@ftcmetrics/db": "workspace:*",
    "@ftcmetrics/shared": "workspace:*"
  }
}
```

To add an internal dependency:

```bash
# Add @ftcmetrics/shared to a package
cd packages/api
bun add @ftcmetrics/shared@workspace:*

# Or edit package.json directly
```

## Cross-Package Imports

### Importing from @ftcmetrics/db

```typescript
import { prisma } from "@ftcmetrics/db";
import type { User, Team } from "@ftcmetrics/db";
```

### Importing from @ftcmetrics/shared

```typescript
import type { FTCEvent, FTCMatch, TeamRole } from "@ftcmetrics/shared";
```

### Next.js Configuration

For Next.js to transpile workspace packages, add to `next.config.ts`:

```typescript
const nextConfig = {
  transpilePackages: ["@ftcmetrics/shared"],
};
```

## Filter Syntax

Bun's `--filter` flag supports various patterns:

```bash
# Exact package name
bun run --filter @ftcmetrics/web dev

# Glob pattern - all packages
bun run --filter '*' build

# Glob pattern - packages starting with @ftcmetrics
bun run --filter '@ftcmetrics/*' typecheck

# Multiple packages
bun run --filter @ftcmetrics/web --filter @ftcmetrics/api dev
```

## Lockfile Management

### bun.lock

The `bun.lock` file is a binary lockfile that should be committed to git. It ensures consistent installs across environments.

```bash
# Install all dependencies (respects lockfile)
bun install

# Update lockfile after package.json changes
bun install

# Update all dependencies to latest
bun update

# Update specific package
bun update <package>
```

## Troubleshooting

### "Cannot find module @ftcmetrics/..."

1. Ensure the package has `workspace:*` in dependencies
2. Run `bun install` from root
3. Check the package exports its types via `main` and `types` in package.json

### "Workspace package not found"

Verify the package exists in `packages/` and has a valid `package.json` with a `name` field.

### Dependency Hoisting Issues

Bun hoists dependencies to the root `node_modules`. If a package needs a specific version:

```json
{
  "dependencies": {
    "some-package": "^1.0.0"
  }
}
```

The hoisted version will be in `/node_modules/some-package`.

### TypeScript Path Resolution

Each package should have its own `tsconfig.json`. For workspace imports to resolve:

```json
{
  "compilerOptions": {
    "moduleResolution": "bundler",
    "paths": {
      "@ftcmetrics/*": ["../*/src"]
    }
  }
}
```

### Scripts Not Running in Package

Ensure the script exists in the package's `package.json`:

```bash
# Check what scripts are available
cat packages/web/package.json | jq '.scripts'
```

## Package-Level Scripts

### @ftcmetrics/web

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "typecheck": "tsc --noEmit"
  }
}
```

### @ftcmetrics/api

```json
{
  "scripts": {
    "dev": "bun run --watch src/index.ts",
    "build": "bun build src/index.ts --outdir dist --target node",
    "start": "bun run dist/index.js",
    "typecheck": "tsc --noEmit"
  }
}
```

### @ftcmetrics/db

```json
{
  "scripts": {
    "generate": "prisma generate",
    "push": "prisma db push",
    "migrate": "prisma migrate dev",
    "studio": "prisma studio",
    "typecheck": "tsc --noEmit"
  }
}
```

### @ftcmetrics/shared

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit"
  }
}
```

## Environment Setup

### .nvmrc

The project requires Node.js 22+:

```bash
# Using nvm
nvm use

# Or install directly
nvm install 22
```

### Bun Installation

```bash
# macOS/Linux
curl -fsSL https://bun.sh/install | bash

# Or via npm
npm install -g bun

# Verify
bun --version
```

## Dependency Graph

```
@ftcmetrics/web
  └── @ftcmetrics/db
  └── @ftcmetrics/shared

@ftcmetrics/api
  └── @ftcmetrics/db
  └── @ftcmetrics/shared

@ftcmetrics/db
  └── (external deps only)

@ftcmetrics/shared
  └── (no dependencies)
```

## Best Practices

1. **Add dependencies to packages, not root** - Only add to root for shared tooling like TypeScript
2. **Use workspace protocol** - Always use `workspace:*` for internal dependencies
3. **Run from root** - Execute commands from the repository root using `--filter`
4. **Keep shared types in @ftcmetrics/shared** - Avoid duplicating types across packages
5. **Export via index.ts** - Each package should have `src/index.ts` that exports public API

## Quick Reference

| Task | Command |
|------|---------|
| Install all deps | `bun install` |
| Dev all packages | `bun run dev` |
| Dev web only | `bun run dev:web` |
| Dev API only | `bun run dev:api` |
| Build all | `bun run build` |
| Typecheck all | `bun run typecheck` |
| Add dep to web | `bun add <pkg> --filter @ftcmetrics/web` |
| Add dev dep to api | `bun add -d <pkg> --filter @ftcmetrics/api` |
| Generate Prisma | `bun run db:generate` |
| Push DB schema | `bun run db:push` |
| Open Prisma Studio | `bun run db:studio` |
